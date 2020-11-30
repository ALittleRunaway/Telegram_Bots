"""My first bot"""
import telebot
import time
from telebot import types
import requests
import xml.etree.ElementTree as ET
import configure

bot = telebot.TeleBot(configure.config["token"])
print("Bot is active!")


class Horoscope:

    @staticmethod
    def buttons_choose_sign():
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text="Овен", callback_data='zodiac_aries')
        keyboard.add(key_oven)
        key_telec = types.InlineKeyboardButton(text="Телец", callback_data='zodiac_taurus')
        keyboard.add(key_telec)
        key_bliznecy = types.InlineKeyboardButton(text="Близнецы", callback_data='zodiac_gemini')
        keyboard.add(key_bliznecy)
        key_rak = types.InlineKeyboardButton(text="Рак", callback_data='zodiac_cancer')
        keyboard.add(key_rak)
        key_lev = types.InlineKeyboardButton(text="Лев", callback_data='zodiac_leo')
        keyboard.add(key_lev)
        key_deva = types.InlineKeyboardButton(text="Дева", callback_data='zodiac_virgo')
        keyboard.add(key_deva)
        key_vesy = types.InlineKeyboardButton(text="Весы", callback_data='zodiac_libra')
        keyboard.add(key_vesy)
        key_scorpion = types.InlineKeyboardButton(text="Скорпион", callback_data='zodiac_scorpio')
        keyboard.add(key_scorpion)
        key_strelec = types.InlineKeyboardButton(text="Стрелец", callback_data='zodiac_sagittarius')
        keyboard.add(key_strelec)
        key_kozerog = types.InlineKeyboardButton(text="Козерог", callback_data='zodiac_capricorn')
        keyboard.add(key_kozerog)
        key_vodoley = types.InlineKeyboardButton(text="Водолей", callback_data='zodiac_aquarius')
        keyboard.add(key_vodoley)
        key_ryby = types.InlineKeyboardButton(text="Рыбы", callback_data='zodiac_pisces')
        keyboard.add(key_ryby)
        return keyboard

    @staticmethod
    def get_horoscope(sign_number):
        url = "https://ignio.com/r/export/utf/xml/daily/com.xml"
        r = requests.get(url)
        print(f"Status code: {r.status_code}")
        tree = ET.ElementTree(ET.fromstring(r.content))
        root = tree.getroot()
        return root[sign_number][1].text


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привет, сейчас я поведую, что уготовила тебе сегодня судьба! У-у-у!")
        keybord = Horoscope.buttons_choose_sign()
        bot.send_message(message.from_user.id, "Выбери знак, под покровительством "
                                               "которого ты был рождён.", reply_markup=keybord)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши: 'Привет'.")
    else:
        bot.send_message(message.from_user.id, "Странные вещи ты мне глаголишь. Напиши: '/help'.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "zodiac_aries":
        msg = Horoscope.get_horoscope(1)
    if call.data == "zodiac_taurus":
        msg = Horoscope.get_horoscope(2)
    if call.data == "zodiac_gemini":
        msg = Horoscope.get_horoscope(3)
    if call.data == "zodiac_cancer":
        msg = Horoscope.get_horoscope(4)
    if call.data == "zodiac_leo":
        msg = Horoscope.get_horoscope(5)
    if call.data == "zodiac_virgo":
        msg = Horoscope.get_horoscope(6)
    if call.data == "zodiac_libra":
        msg = Horoscope.get_horoscope(7)
    if call.data == "zodiac_scorpio":
        msg = Horoscope.get_horoscope(8)
    if call.data == "zodiac_sagittarius":
        msg = Horoscope.get_horoscope(9)
    if call.data == "zodiac_capricorn":
        msg = Horoscope.get_horoscope(10)
    if call.data == "zodiac_aquarius":
        msg = Horoscope.get_horoscope(11)
    if call.data == "zodiac_pisces":
        msg = Horoscope.get_horoscope(12)

    bot.send_message(call.message.chat.id, msg)
    time.sleep(5)
    bot.send_message(call.message.chat.id, "А вообще ты глупый, конечно, в такую ерунду-то верить. Завязывай.")


bot.polling(none_stop=True, interval=0)

