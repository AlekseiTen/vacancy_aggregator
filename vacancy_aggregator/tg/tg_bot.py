import nest_asyncio
from sqlalchemy import select

from vacancy_aggregator.app.db.models import TelegramUser, AsyncSessionLocal

nest_asyncio.apply()

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

# Состояния для ConversationHandler
ASK_NAME = 1


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Как тебя зовут?")
    return ASK_NAME


# Получаем имя пользователя
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.text
    chat_id = update.effective_chat.id

    # Здесь код сохранения пользователя в базу
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(TelegramUser).where(TelegramUser.chat_id == str(chat_id)))
        user = result.scalars().first()

        if not user:
            user = TelegramUser(chat_id=str(chat_id), user_name=user_name)
            session.add(user)
        else:
            user.user_name = user_name  # обновить имя, если нужно
        await session.commit()

    await update.message.reply_text(f"Приятно познакомиться, {user_name}! 🚀")
    return ConversationHandler.END


# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("обработчик отмены вызван", flush=True)  # Лог в консоль
    await update.message.reply_text("Диалог отменён.")
    return ConversationHandler.END


# Основной запуск бота
async def main():
    app = ApplicationBuilder().token("7733881445:AAGsKgDKO2utz3tPSMRxiG8AH0KqW-cKz9Q").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("Бот запущен...")
    await app.run_polling()


# Запуск
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
