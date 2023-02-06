import main
import telebot
import random
from telebot import types
bot = telebot.TeleBot("6004565538:AAGOxuc9VVSwLt3yJskgP8kU1BvYhqQlNcY")

sweets = 221
max_sweet = 28
user_turn = 0
bot_turn = 0
flag = ""

@bot.message_handler(commands=["game"])
def button(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Узнать правила игры")
    but2 = types.KeyboardButton("Начать игру")
    markup.add(but1)
    markup.add(but2)
    bot.send_message(message.chat.id, "Выберите ниже", reply_markup=markup)

@bot.message_handler(content_types="text")
def controller(message):
    print(message.text)
    if message.text == "Узнать правила игры":
        bot.send_message(message.chat.id, "На столе лежит 221 конфета. Играют два игрока делая ход друг после друга.\n Первый ход определяется жеребьёвкой. За один ход можно забрать не более чем 28 конфет. \n Все конфеты оппонента достаются сделавшему последний ход.")
    elif message.text == "Начать игру":
        bot.send_message(message.chat.id, "Игра началась")
        bot.register_next_step_handler(message, paly)


def paly(message):
    global flag
    bot.send_message(message.chat.id,f"Приветствую вас в игре!")
    bot.send_message(message.chat.id, f"Всего в игре {sweets} конфет")
    flag = random.choice(["user", "bot"])
    if flag == "user":
        bot.send_message(message.chat.id,f"Первым ходите вы")
        controller(message)
    else:
        bot.send_message(message.chat.id, f"Первым ходит бот")
        controller(message)
        
def controller(message):
    global flag
    if sweets>0:
        if flag == "user":
            bot.send_message(message.chat.id, f"Ваш ход введите кол-во конфет от 0 до {max_sweet}")
            bot.register_next_step_handler(message,user_input)
        else:
            bot_input(message)
    else:
        flag = "user" if flag == "bot" else "bot"
        bot.send_message(message.chat.id, f"Победил {flag}!")

def bot_input(message):
    global sweets,bot_turn,flag
    if sweets <= max_sweet:
        bot_turn = sweets
    elif sweets % max_sweet == 0:
        bot_turn = max_sweet - 1
    else:
        bot_turn = sweets % max_sweet - 1
        if bot_turn == 0:
            bot_turn = 1
    sweets -= bot_turn
    bot.send_message(message.chat.id, f"бот взял {bot_turn} конфет")
    bot.send_message(message.chat.id, f"осталось {sweets}")
    flag = "user" if flag == "bot" else "bot"
    controller(message)

def user_input(message):
    global flag,user_turn,sweets
    user_turn = int(message.text)
    sweets -= user_turn
    bot.send_message(message.chat.id, f"осталось {sweets}")
    flag = "user" if flag == "bot" else "bot"
    controller(message)
