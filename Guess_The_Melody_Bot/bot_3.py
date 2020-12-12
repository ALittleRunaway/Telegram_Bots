"""My third bot"""
import telebot
import os
import time
import configure


bot = telebot.TeleBot(configure.config["token"])

@bot.message_handler(commands=["test"])
def find_file_ids(message):
    for file in os.listdir("music/"):
        if file.split(".")[-1] == "ogg":
            f = open("music/"+file, "rb")
            msg = bot.send_voice(message.chat.id, f, None) #timeout=5/10...
            bot.send_message(message.chat.id, msg.voice.file_id, reply_to_message_id=msg.message_id)
        time.sleep(3)

bot.polling(none_stop=True, interval=0)
