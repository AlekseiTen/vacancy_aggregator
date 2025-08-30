from celery import shared_task
import asyncio
from sqlalchemy.future import select
from vacancy_aggregator.app.db.models import AsyncSessionLocal, HH, TelegramUser, SJ, MTS
from telegram.ext import ApplicationBuilder

from vacancy_aggregator.app.parsers.hh_vacancies import hh_get_vacancies
from vacancy_aggregator.app.parsers.mts_parser import mts_get_vacancies
from vacancy_aggregator.app.parsers.super_job_vacancies import sj_get_vacancies
from vacancy_aggregator.app.schemas.prepare_functions import hh_prepare_vacancies, sj_prepare_vacancies, \
    mts_prepare_vacancies
from vacancy_aggregator.app.schemas.vacancy_saver import save_vacancy

BOT_TOKEN = "7733881445:AAGsKgDKO2utz3tPSMRxiG8AH0KqW-cKz9Q"


async def send_to_telegram(vacancy, application):
    # Этот метод должен совместим с вашим кодом бота
    # Пример отправки вакансии всем пользователям
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(TelegramUser))
        users = result.scalars().all()

    text = f"Новая вакансия: {vacancy.name} - {vacancy.employer}\n{vacancy.url}"

    for user in users:
        try:
            await application.bot.send_message(chat_id=int(user.chat_id), text=text)
        except Exception as e:
            print(f"Ошибка при отправке пользователю {user.chat_id}: {e}")


@shared_task
def send_unsent_hh_vacancies_task():
    async def inner():
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        await app.initialize()  # Инициализация app без polling

        async with AsyncSessionLocal() as session:
            result = await session.execute(select(HH).where(HH.is_sent == False))
            vacancies = result.scalars().all()

            for vacancy in vacancies:
                await send_to_telegram(vacancy, app)
                vacancy.is_sent = True
            await session.commit()

        await app.shutdown()

    asyncio.run(inner())


@shared_task
def daily_parse_and_save_vacancies():
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
