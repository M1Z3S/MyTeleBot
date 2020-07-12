import telebot
import requests
import time
from bs4 import BeautifulSoup
from telebot import types

bot = telebot.TeleBot('1323095011:AAEn5_1rcStJ-k8AkKCudLkRSY3gzL8gY9s')
doll_url = 'https://www.google.ru/search?newwindow=1&source=hp&ei=ifUGX7qlFIjNrgSp8Z7YBw&q=курс+доллара+к+рублю&oq' \
           '=ку&gs_lcp' \
           '=CgZwc3ktYWIQARgAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIAFDDS1jhZGDFcGgDcAB4AIABqwGIAbQDkgE' \
           '=DMy4xmAEAoAEBqgEHZ3dzLXdperABAA&sclient=psy-ab '
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 '
                  'Safari/537.36 OPR/69.0.3686.49'}

n = int(time.localtime().tm_hour)

"""
Погода через парсинг синоптика, ссылка в конце содержит дату, можно дописать поиск на завтра
"""




# ___start____start____start____start____start____start
@bot.message_handler(commands=['start'])
def start(message):
    send = f"<b>Good evening {message.from_user.first_name} {message.from_user.last_name}</b>! \nЧего желаете? \n\n " \
           f"/menu для вызова кнопок "
    bot.send_message(message.chat.id, send, parse_mode='html')


# ______________________menu_________________________________
@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = types.KeyboardButton('Погода')
    button2 = types.KeyboardButton('Доллар')
    button3 = types.KeyboardButton('Активировать отправку')
    button4 = types.KeyboardButton('Выбор времени')
    markup.add(button1, button2, button3, button4)
    send_mess = "->"
    bot.send_message(message.chat.id, send_mess, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    get_message_bot = message.text.strip().lower()
    if get_message_bot == 'погода':
        final_mes = f"{message.from_user.first_name} , прогноз погоды на сегодня.\n\n " + f'<b>{weather_text}</b>' + "\n\nЯ могу ещё чем - нибудь помочь? "
        bot.send_message(message.chat.id, final_mes, parse_mode='html')
        return get_message_bot == 'активировать отправку'
    elif get_message_bot == 'доллар':
        final_mes = f'{message.from_user.first_name}, курс доллара по отношению к рублю на данный момент ' + f'<b>{compiled}</b>'+ "\nЯ могу ещё чем - нибудь помочь? "
        bot.send_message(message.chat.id, final_mes, parse_mode= 'html')
        return get_message_bot == 'активировать отправку'
    elif get_message_bot == 'активировать отправку':
        while True:
            if n == 7:
                lsit = f"<b>Доброе утро! Курс доллара сейчас:</b>\n\n" + compiled + f"\n\n<b>Погода:</b>\n\n" + weather_text
                bot.send_message(message.chat.id, lsit, parse_mode='html')
                time.sleep(3600)
            else:
                bot.send_message(message.chat.id, 'Прийдет в 7:00')
    elif get_message_bot != 'доллар' or 'погода' or 'отправка':
        final_mes = 'Воспользуйтесь кнопкой, нажмите <b>/menu</b>'
        bot.send_message(message.chat.id, final_mes, parse_mode='html')

weather_link = 'https://sinoptik.ua/погода-ялта/'
full_page_w = requests.get(weather_link, headers=headers)
soup_w = BeautifulSoup(full_page_w.content, 'html.parser')
convert_w = soup_w.findAll("div", {"class": "description"})
weather_text = str(convert_w[0].text) +" \n"+ str(convert_w[1].text)

full_page = requests.get(doll_url, headers=headers)
soup = BeautifulSoup(full_page.content, 'html.parser')
convert = soup.findAll("span", {"class": "DFlfde SwHCTb"})  # парсинг курса
compiled = str(convert[0].text)
print(convert[0].text)

print(n)
bot.polling(none_stop=True)
