import telebot
from config import token
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])  # Функция обрабатывает текстовые сообщения
def in_text(message):
    bot.send_message(message.chat.id, 'Ведуться технические работы')

bot.polling()
