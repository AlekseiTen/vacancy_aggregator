import nest_asyncio
from sqlalchemy import select

from vacancy_aggregator.app.db.models import TelegramUser, AsyncSessionLocal
from vacancy_aggregator.app.schemas.get_vacansies import get_all_vacansies

nest_asyncio.apply()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
)

# Состояния для ConversationHandler

START, SHOW_VACANCIES = range(2)  # Стейты для ConversationHandler

# сохранение пользователя в бд
async def save_user(update: Update):
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name
    if not user_name:
        user_name = update.effective_user.username or "Неизвестный"

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(TelegramUser).where(TelegramUser.chat_id == str(chat_id)))
        user = result.scalars().first()

        if not user:
            user = TelegramUser(chat_id=str(chat_id), user_name=user_name)
            session.add(user)
        else:
            user.user_name = user_name
        await session.commit()


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Начать", callback_data='start')],
        [InlineKeyboardButton("Отмена", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Нажми кнопку, чтобы начать.", reply_markup=reply_markup)
    return START


# Обработка нажатий по кнопкам "Начать" и "Отмена"
async def start_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'start':
        await save_user(update)

        # Показываем кнопку "Все вакансии"
        keyboard = [
            [InlineKeyboardButton("Все вакансии", callback_data='show_vacancies')],
            [InlineKeyboardButton("Отмена", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Добро пожаловать! Выберите действие:", reply_markup=reply_markup)
        return SHOW_VACANCIES

    elif query.data == 'cancel':
        await query.edit_message_text(text="Диалог отменён.")
        return ConversationHandler.END


# Обработка кнопки "Все вакансии"
async def show_vacancies_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Ваша функция получения вакансий
    await get_all_vacansies(update, context)

    return ConversationHandler.END


# Отмена вне зависимости от состояния
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диалог отменён.")
    return ConversationHandler.END


# Основной запуск бота
async def main():
    app = ApplicationBuilder().token("7733881445:AAGsKgDKO2utz3tPSMRxiG8AH0KqW-cKz9Q").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [CallbackQueryHandler(start_button_handler)],
            SHOW_VACANCIES: [CallbackQueryHandler(show_vacancies_handler, pattern='show_vacancies')],
        },
        fallbacks=[CommandHandler("cancel", cancel), CallbackQueryHandler(cancel, pattern='cancel')],
    )

    app.add_handler(conv_handler)
    print("Бот запущен...")
    await app.run_polling()


if __name__ == "__main__":
    import nest_asyncio
    import asyncio

    nest_asyncio.apply()
    asyncio.run(main())
