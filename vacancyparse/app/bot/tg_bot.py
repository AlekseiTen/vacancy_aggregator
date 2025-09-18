import nest_asyncio
from sqlalchemy import select
import os
from dotenv import load_dotenv
from vacancyparse.app.db.database import AsyncSessionLocal
from vacancyparse.app.db.models import TelegramUser
from vacancyparse.app.service.vacancy_service import get_all_vacansies

nest_asyncio.apply()
load_dotenv()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
)

# Состояния для ConversationHandler
SHOW_VACANCIES = range(1)

TG_TOKEN = os.getenv("TG_TOKEN")


# сохранение пользователя в бд
async def save_user(update: Update):
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name or update.effective_user.username or "Неизвестный"

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(TelegramUser.chat_id == str(chat_id))
        )
        user = result.scalars().first()

        if not user:
            user = TelegramUser(chat_id=str(chat_id), user_name=user_name)
            session.add(user)
            await session.commit()


# Первое сообщение от пользователя
async def greet_user(update: Update, _):
    await save_user(update)

    keyboard = [[InlineKeyboardButton("Все вакансии", callback_data="show_vacancies")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Добро пожаловать! Нажми кнопку, чтобы посмотреть вакансии:",
        reply_markup=reply_markup,
    )
    return SHOW_VACANCIES


# Обработка кнопки "Все вакансии"
async def show_vacancies_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    await get_all_vacansies(update, context)
    return ConversationHandler.END


# Основной запуск бота
async def main():
    app = ApplicationBuilder().token(TG_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.ALL, greet_user)],  # реагируем на первое сообщение
        states={
            SHOW_VACANCIES: [
                CallbackQueryHandler(show_vacancies_handler, pattern="show_vacancies")
            ],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    print("Бот запущен...")
    await app.run_polling()
