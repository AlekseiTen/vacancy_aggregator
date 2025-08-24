from celery import shared_task
import asyncio
from sqlalchemy.future import select
from vacancy_aggregator.app.db.models import AsyncSessionLocal, HH, TelegramUser
from telegram.ext import ApplicationBuilder

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
