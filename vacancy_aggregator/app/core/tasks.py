from celery import shared_task
import asyncio
from sqlalchemy.future import select
from vacancy_aggregator.app.db.models import AsyncSessionLocal, HH


async def send_to_telegram(vacancy):
    print(f"Отправка вакансии: {vacancy.name} - {vacancy.url}")
    await asyncio.sleep(0.1)  # Эмуляция отправки


@shared_task
def send_unsent_hh_vacancies_task():
    async def inner():
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(HH).where(HH.is_sent == False))
            vacancies = result.scalars().all()

            for vacancy in vacancies:
                await send_to_telegram(vacancy)
                vacancy.is_sent = True

            await session.commit()

    asyncio.run(inner())
