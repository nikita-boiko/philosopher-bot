# Основной код бота

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_TOKEN
from ml_gpt_api import get_philosophical_response

# настройка логирования 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO # уровень логирования - информационное сообщение
)

# обработчик команды /start - привественное сообщение
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
🏛️ Привет, искатель мудрости!
    
    Я - бот-философ. Задай мне вопрос о жизни, проблему или поделись размышлением, 
    и я дам тебе мудрый, философский ответ.
"""
    # Отправка пользователю
    await update.message.reply_text(welcome_text)

# обработчик текстовых сообщений от пользователя 
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # получение текста сообщения от пользователя
    user_message =  update.message.text

    # обработка сообщения о том, что бот "думает"
    thinking_message = await update.message.reply_text('🤔 Размышляю над твоим вопросом...') 
    # Вызов ML-функции для получения философского ответа на сообщения пользователя
    philosophical_response = get_philosophical_response(user_message)

    # Удаление сообщения "думаю"
    await thinking_message.delete()
    # Отправка финального ответа 
    await update.message.reply_text(f'💭 {philosophical_response}')

# обработка ошибок бота
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # логирование ошибки 
    logging.error(f'Ошибка: {context.error}')
    # отправка сообщения пользователяя об ошибке
    await update.message.reply_text('⚡ Мои мысли запутались... Попробуй еще раз.')

# основная функция запуска бота
def main():
    # создание приложения бота с использованием токена
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    # Регистрация обработчиков команд:
    # Обработчик команды /start - вызывает функцию start
    application.add_handler(CommandHandler('start', start))
    # обработчик тектовых сообщений (кроме команд) 
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # регистрация обработчика ошибок
    application.add_error_handler(error_handler)

    # запуск бота в режиме polling
    application.run_polling()

    # точка входа в программу 
if __name__ == '__main__':
    main()