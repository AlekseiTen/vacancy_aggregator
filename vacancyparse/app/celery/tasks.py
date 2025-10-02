from datetime import datetime, timedelta, timezone

from celery import shared_task
import os
from dotenv import load_dotenv
import asyncio

from sqlalchemy import delete
from sqlalchemy.future import select
from telegram import Bot

from vacancyparse.app.db.database import AsyncSessionLocal
from vacancyparse.app.db.models import HH, TelegramUser, SJ, MTS
from vacancyparse.app.parsers.hh_vacancies import hh_get_vacancies
from vacancyparse.app.parsers.mts_parser import mts_get_vacancies
from vacancyparse.app.parsers.super_job_vacancies import sj_get_vacancies
from vacancyparse.app.repositories.vacancy_saver import save_vacancy
from vacancyparse.app.schemas.prepare_functions import (
    hh_prepare_vacancies,
    sj_prepare_vacancies,
    mts_prepare_vacancies,
)

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")


async def send_to_telegram(vacancy):
    bot = Bot(token=TG_TOKEN)

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(TelegramUser))
        users = result.scalars().all()

    text = f"Новая вакансия: {vacancy.name} - {vacancy.employer}\n{vacancy.url}"

    for user in users:
        try:
            await bot.send_message(chat_id=int(user.chat_id), text=text)
        except Exception as e:
            print(f"Ошибка при отправке пользователю {user.chat_id}: {e}")


@shared_task
def send_unsent_vacancies_task():
    """
    рассылка пользователям
    :return:
    """

    async def inner():
        async with AsyncSessionLocal() as session:
            # Получаем все вакансии с is_sent=False из трёх таблиц
            result_hh = await session.execute(select(HH).where(HH.is_sent == False))
            vacancies_hh = result_hh.scalars().all()

            result_sj = await session.execute(select(SJ).where(SJ.is_sent == False))
            vacancies_sj = result_sj.scalars().all()

            result_mts = await session.execute(select(MTS).where(MTS.is_sent == False))
            vacancies_mts = result_mts.scalars().all()

            # Объединяем все вакансии в один список
            all_vacancies = vacancies_hh + vacancies_sj + vacancies_mts

            # Отправляем всем пользователям каждую новую вакансию
            for vacancy in all_vacancies:
                await send_to_telegram(vacancy)
                vacancy.is_sent = True

            await session.commit()

    asyncio.run(inner())


@shared_task
def daily_parse_and_save_vacancies():
    """
    парсинг новых вакансий
    :return:
    """

    async def inner():
        raw_hh = hh_get_vacancies()
        raw_sj = sj_get_vacancies()
        raw_mts = mts_get_vacancies()

        prepared_hh = hh_prepare_vacancies(raw_hh)
        prepared_sj = sj_prepare_vacancies(raw_sj)
        prepared_mts = mts_prepare_vacancies(raw_mts)

        async with AsyncSessionLocal() as session:
            await save_vacancy(prepared_hh, HH, session)
            await save_vacancy(prepared_sj, SJ, session)
            await save_vacancy(prepared_mts, MTS, session)

    asyncio.run(inner())


@shared_task
def cleanup_old_vacancies():
    """
    удаление старых
    :return:
    """

    async def inner():
        async with AsyncSessionLocal() as session:
            cutoff_date = datetime.now(timezone.utc) - timedelta(weeks=2)

            # HH
            await session.execute(
                delete(HH).where(HH.is_sent == True, HH.created_at < cutoff_date)
            )
            # SJ
            await session.execute(
                delete(SJ).where(SJ.is_sent == True, SJ.created_at < cutoff_date)
            )
            # MTS
            await session.execute(
                delete(MTS).where(MTS.is_sent == True, MTS.created_at < cutoff_date)
            )

            await session.commit()

    asyncio.run(inner())
