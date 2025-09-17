from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# Асинхронная функция для сохранения списка вакансий в базу данных
async def save_vacancy(vacancy_list, model_class, session: AsyncSession, unique_field: str = "url"):
    # Открываем асинхронный контекст транзакции сессии
    async with session.begin():

        for vac in vacancy_list:
            unique_value = vac.get(unique_field)

            # Формируем SQL-запрос для поиска вакансии в базе по уникальному полю url
            # Выполняем запрос к базе данных
            # Получаем один объект вакансии или None, если такой записи нет
            stmt = select(model_class).where(getattr(model_class, unique_field) == unique_value)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                print(f"Пропущено (уже в БД): {vac['name']}")
                continue

            vacancy = model_class(**vac)
            session.add(vacancy)
