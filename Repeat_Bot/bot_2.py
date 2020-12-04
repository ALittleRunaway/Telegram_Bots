"""My second bot"""
import telebot
import configure
from telebot import types

bot = telebot.TeleBot(configure.config["token"])
print("Bot is active!")


# @bot.message_handler(func=lambda message: True, content_types=['text'])
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    """This handler repeats all of the user's messages"""
    bot.send_message(message.chat.id, message.text)

#if __name__ == "main":
bot.polling(none_stop=True, interval=0)
