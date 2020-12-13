"""My fourth bot"""
import telebot
from telebot import types
import configure
import requests
import random
from datetime import datetime
import re

stickers = ['🎉', '🔥', '👻', '🎲', '🎳', '🎰', '🔮', '🌠', '🌌', '🌈']
DAY, MONTH, YEAR = 1, 1, 1

def get_info():
    url = "https://www.molomo.ru/test/numerology/numerology_number.php"
    res = requests.get(url)
    pattern = r'С точки зрения (.+) - "5".'
    text = re.search(pattern, res.text).group().replace("<br>", "\n").replace("</p>", "\n").replace("<span>", "<b>")
    return text.replace("</span>", "</b>").replace("<p>", "\n")


def get_the_number(day, month, year):
    today = datetime.today()
    month, year = 9, 2001
    day2, month2, year2 = int(today.strftime("%d")), int(today.strftime("%m")), int(today.strftime("%Y"))

    params = {
        "a": "d",
        "day": day,
        "month": month,
        "year": year,
        "day2": day2,
        "month2": month2,
        "year2": year2,
    }

    url = "https://www.molomo.ru/test/numerology/numerology_number.php"
    res = requests.get(url, params)

    if 'Неверно указана дата' in res.text:
        return 0, "Неверно указана дата. Пожалуйста, укажите новые данные."

    pattern = r'Число Дня: (\d+)'
    number_of_the_day_string = re.search(pattern, res.text).group()
    number_of_the_day = re.search(r'(\d+)', number_of_the_day_string).group()
    # print(f"И ваше персональное число дня: {number_of_the_day}!")
    pattern = r"Число Дня: (\d+)</h2><p>(.+)</p><div class"
    text = re.search(pattern, res.text).group()[20:-14:].replace("</p>", "\n").replace("<p>", "\n").replace("<br>",
                                                                                                            "\n")
    return number_of_the_day, text


def calculate(year, message):
    global YEAR
    YEAR = year
    number_of_the_day, text = get_the_number(DAY, MONTH, YEAR)

    if number_of_the_day == 0:
        bot.send_message(message.chat.id, text, parse_mode="html")
    else:
        bot.send_message(message.chat.id, f"И ваше персональное число дня: <b>{number_of_the_day}</b>!",
                         parse_mode="html")
        bot.send_message(message.chat.id, text, parse_mode="html")
        bot.send_message(message.chat.id, random.choice(stickers))


def calculate_day(message):
    markup = types.InlineKeyboardMarkup(row_width=7)
    for i in range(1, 28, 7):
        markup.add(types.InlineKeyboardButton(str(i), callback_data="day_" + str(i)),
                   types.InlineKeyboardButton(str(i + 1), callback_data="day_" + str(i + 1)),
                   types.InlineKeyboardButton(str(i + 2), callback_data="day_" + str(i + 2)),
                   types.InlineKeyboardButton(str(i + 3), callback_data="day_" + str(i + 3)),
                   types.InlineKeyboardButton(str(i + 4), callback_data="day_" + str(i + 4)),
                   types.InlineKeyboardButton(str(i + 5), callback_data="day_" + str(i + 5)),
                   types.InlineKeyboardButton(str(i + 6), callback_data="day_" + str(i + 6)))
    markup.add(types.InlineKeyboardButton(str(29), callback_data="day_" + str(29)),
               types.InlineKeyboardButton(str(30), callback_data="day_" + str(23)),
               types.InlineKeyboardButton(str(31), callback_data="day_" + str(31)))

    bot.send_message(message.chat.id, "Выберите дату рождения: ", reply_markup=markup)


def calculate_month(day, call):
    global DAY
    DAY = day
    bot.send_message(call.message.chat.id, f"Вы выбрали {day} число.")
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(types.InlineKeyboardButton("Январь ❄️", callback_data="month_1"),
               types.InlineKeyboardButton("Февраль 🌨", callback_data="month_2"),
               types.InlineKeyboardButton("Март 🌱", callback_data="month_3"),
               types.InlineKeyboardButton("Апрель 💐", callback_data="month_4"),
               types.InlineKeyboardButton("Май 🌺", callback_data="month_5"),
               types.InlineKeyboardButton("Июнь ☀️", callback_data="month_6"),
               types.InlineKeyboardButton("Июль 🌴", callback_data="month_7"),
               types.InlineKeyboardButton("Август 🌾", callback_data="month_8"),
               types.InlineKeyboardButton("Сентябрь 🍂", callback_data="month_9"),
               types.InlineKeyboardButton("Октябрь 🍁", callback_data="month_10"),
               types.InlineKeyboardButton("Ноябрь ☔️", callback_data="month_11"),
               types.InlineKeyboardButton("Декабрь 🎄", callback_data="month_12"))

    bot.send_message(call.message.chat.id, "Выберите месяц рождения: ", reply_markup=markup)

def calculate_year(month, call):
    global MONTH
    MONTH = month
    if month == 1:
        month_words = "Январь"
    if month == 2:
        month_words = "Февраль"
    if month == 3:
        month_words = "Март"
    if month == 4:
        month_words = "Апрель"
    if month == 5:
        month_words = "Май"
    if month == 6:
        month_words = "Июнь"
    if month == 7:
        month_words = "Июль"
    if month == 8:
        month_words = "Август"
    if month == 9:
        month_words = "Сентябрь"
    if month == 10:
        month_words = "Октябрь"
    if month == 11:
        month_words = "Ноябрь"
    if month == 12:
        month_words = "Декабрь"
    bot.send_message(call.message.chat.id, f"Вы выбрали {month_words} ({month}-й месяц) .")
    bot.send_message(call.message.chat.id, "Введите год рождения: ")


#
#
#
### BOT STARTS HERE ###

bot = telebot.TeleBot(configure.config["token"])
print("Bot is active!")


@bot.message_handler(commands=["start"])
def command_start(message):

    bot.send_message(message.chat.id, "✨")
    bot.send_message(message.chat.id, "Привет! Я помогу вам вычислить ваше персональное число дня.")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_help = types.KeyboardButton("❔ Справка")
    button_calculate = types.KeyboardButton("🎲 Вычислить")
    markup.add(button_help, button_calculate)

    bot.send_message(message.chat.id, "Выберете 'Справка', если хотите почитать про персональное чилсло дня подробнее. "
                                      "Или 'Вычислить', если вам не терпиться его узнать!", reply_markup=markup)


@bot.message_handler(commands=["info"])
def command_info(message):
    bot.send_message(message.chat.id, get_info(), parse_mode="html")


@bot.message_handler(commands=["calculate"])
def command_calculate(message):
    calculate_day(message)


@bot.message_handler(content_types=['text'])
def reply(message):
    year_data = re.search(r"\b\d\d\d\d\b", message.text)

    if message.text == "❔ Справка":
        bot.send_message(message.chat.id, get_info(), parse_mode="html")

    elif message.text == "🎲 Вычислить":
        print(f"Human: {not (message.from_user.is_bot)} || Name: {message.from_user.first_name} "
              f"{message.from_user.last_name} || Id: {message.from_user.id};")
        calculate_day(message)

    elif year_data:
        if message.text == year_data.group():
            if int(year_data.group()) <= 1900 or int(year_data.group()) >= 2021:
                bot.send_message(message.chat.id, "Врятли вам столько лет. Пожалуйста, "
                                                  "введите настоящий год рождения.")
            else:
                calculate(int(message.text), message)
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю ☹️")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """l"""
    try:
        # Day
        if call.data == "day_1":
            calculate_month(1, call)
        if call.data == "day_2":
            calculate_month(2, call)
        if call.data == "day_3":
            calculate_month(3, call)
        if call.data == "day_4":
            calculate_month(4, call)
        if call.data == "day_5":
            calculate_month(5, call)
        if call.data == "day_6":
            calculate_month(6, call)
        if call.data == "day_7":
            calculate_month(7, call)
        if call.data == "day_8":
            calculate_month(8, call)
        if call.data == "day_9":
            calculate_month(9, call)
        if call.data == "day_10":
            calculate_month(10, call)
        if call.data == "day_11":
            calculate_month(11, call)
        if call.data == "day_12":
            calculate_month(12, call)
        if call.data == "day_13":
            calculate_month(13, call)
        if call.data == "day_14":
            calculate_month(14, call)
        if call.data == "day_15":
            calculate_month(15, call)
        if call.data == "day_16":
            calculate_month(16, call)
        if call.data == "day_17":
            calculate_month(17, call)
        if call.data == "day_18":
            calculate_month(18, call)
        if call.data == "day_19":
            calculate_month(19, call)
        if call.data == "day_20":
            calculate_month(20, call)
        if call.data == "day_21":
            calculate_month(21, call)
        if call.data == "day_22":
            calculate_month(22, call)
        if call.data == "day_23":
            calculate_month(23, call)
        if call.data == "day_24":
            calculate_month(24, call)
        if call.data == "day_25":
            calculate_month(25, call)
        if call.data == "day_26":
            calculate_month(26, call)
        if call.data == "day_27":
            calculate_month(27, call)
        if call.data == "day_28":
            calculate_month(28, call)
        if call.data == "day_29":
            calculate_month(29, call)
        if call.data == "day_30":
            calculate_month(30, call)
        if call.data == "day_31":
            calculate_month(31, call)

        # Month
        if call.data == "month_1":
            calculate_year(1, call)
        if call.data == "month_2":
            calculate_year(2, call)
        if call.data == "month_3":
            calculate_year(3, call)
        if call.data == "month_4":
            calculate_year(4, call)
        if call.data == "month_5":
            calculate_year(5, call)
        if call.data == "month_6":
            calculate_year(6, call)
        if call.data == "month_7":
            calculate_year(7, call)
        if call.data == "month_8":
            calculate_year(8, call)
        if call.data == "month_9":
            calculate_year(9, call)
        if call.data == "month_10":
            calculate_year(10, call)
        if call.data == "month_11":
            calculate_year(11, call)
        if call.data == "month_12":
            calculate_year(12, call)

    except Exception as e:
        print(repr(e))
        bot.send_message(call.chat.id, "Ой, произошла ошибочка! Ну ничего страшного, просто попробуйте ещё раз 😌")


bot.polling(none_stop=True, interval=0)
# globals()["day_" + str(i)] = types.InlineKeyboardButton(str(i), callback_data="day_" + str(i))
# markup.add(globals()["day_" + str(i)])
