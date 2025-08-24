from sqlalchemy import select, update as sqlalchemy_update
from vacancy_aggregator.app.db.models import AsyncSessionLocal, HH, SJ, MTS
from telegram import Update
from telegram.ext import ContextTypes

async def get_all_vacansies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with AsyncSessionLocal() as session:
        hh_result = await session.execute(select(HH).where(HH.is_sent == False))
        sj_result = await session.execute(select(SJ).where(SJ.is_sent == False))
        mts_result = await session.execute(select(MTS).where(MTS.is_sent == False))

        hh_vacancies = hh_result.scalars().all()
        sj_vacancies = sj_result.scalars().all()
        mts_vacancies = mts_result.scalars().all()

        all_vacancies = []
        hh_ids = []
        sj_ids = []
        mts_ids = []

        for v in hh_vacancies:
            all_vacancies.append(f"HH: {v.name} - {v.employer}\n{v.url}")
            hh_ids.append(v.id)
        for v in sj_vacancies:
            all_vacancies.append(f"SJ: {v.name} - {v.employer}\n{v.url}")
            sj_ids.append(v.id)
        for v in mts_vacancies:
            all_vacancies.append(f"MTS: {v.name} - {v.profession}\n{v.url}")
            mts_ids.append(v.id)

        if not all_vacancies:
            await update.callback_query.message.reply_text("Вакансий пока нет.")
            return

        # Разбиваем вакансии на сообщения по лимиту 4000 символов
        max_len = 4000
        messages = []
        current_text = ""
        for vac in all_vacancies:
            if len(current_text) + len(vac) + 2 > max_len:
                messages.append(current_text)
                current_text = ""
            current_text += vac + "\n\n"
        if current_text:
            messages.append(current_text)

        for msg in messages:
            await update.callback_query.message.reply_text(msg)

        # Обновляем флаги is_sent в базе
        if hh_ids:
            await session.execute(sqlalchemy_update(HH).where(HH.id.in_(hh_ids)).values(is_sent=True))
        if sj_ids:
            await session.execute(sqlalchemy_update(SJ).where(SJ.id.in_(sj_ids)).values(is_sent=True))
        if mts_ids:
            await session.execute(sqlalchemy_update(MTS).where(MTS.id.in_(mts_ids)).values(is_sent=True))

        await session.commit()
