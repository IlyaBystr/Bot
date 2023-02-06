from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import telebot
import random
from telebot import types
from spy import log
bot = telebot.TeleBot("6004565538:AAGOxuc9VVSwLt3yJskgP8kU1BvYhqQlNcY")

sweets = 221
max_sweet = 28
user_turn = 0
bot_turn = 0
flag = ""

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("game")
    item2 = types.KeyboardButton("calculator")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Hello", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def button(message):
    if message.text == "game":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Узнать правила игры")
        but2 = types.KeyboardButton("Начать игру")
        markup.add(but1)
        markup.add(but2)
        bot.send_message(message.chat.id, "Выберите ниже", reply_markup=markup)
        bot.register_next_step_handler(message, sas)
    elif message.text == "calculator":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.KeyboardButton("Рациональные")
        key2 = types.KeyboardButton("Комплексные")
        markup.add(key1, key2)
        bot.send_message(message.chat.id, "Калькулятор", reply_markup=markup)
        bot.register_next_step_handler(message, sas)

def sas(message):
    a = 0 
    global typeNums 
    if message.text == "Узнать правила игры":
        bot.send_message(message.chat.id, "На столе лежит 221 конфета. Играют два игрока делая ход друг после друга.\n Первый ход определяется жеребьёвкой. За один ход можно забрать не более чем 28 конфет. \n Все конфеты оппонента достаются сделавшему последний ход.")
    elif message.text == "Начать игру":
        bot.send_message(message.chat.id, "Игра началась")
        bot.register_next_step_handler(message, paly)
    elif message.text == "Рациональные":
        bot.send_message(message.chat.id, f"Выбраны рациональные числа", reply_markup=a)
        bot.send_message(message.chat.id, f"Введите выражение разделяя пробелом")
        bot.register_next_step_handler(message, con)
        typeNums = 0
    elif message.text == "Комплексные":
        bot.send_message(message.chat.id, "Выбраны комплексные числа", reply_markup=a)
        bot.send_message(message.chat.id, "Введите выражение разделяя пробелом")
        bot.register_next_step_handler(message, con)
        typeNums = 1


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


def con(message):
    res = ""
    line = message.text.split()
    znak = line[1]
    if typeNums == 0:
        a = int(line[0])
        b = int(line[2])
    else:
        a = complex(line[0])
        b = complex(line[2])
    
    if znak == '+':
        res = summ_nums(a, b)
    elif znak == '-':
        res == sub_nums(a, b)
    elif znak == '*':
        res == mult_nums(a, b)        
    elif znak == "/":
        res == div_nums(a, b)
    elif typeNums == 1 and (znak == "//" or znak == "%"):
        bot.send_message(message.chat.id, "Неверный ввод выражения")
        bot.register_next_step_handler(message, controller)
        return
    elif znak == "//":
        res == div_int(a, b)     
    elif znak == "%":
        res == div_rem(a, b)
    bot.send_message(message.chat.id, str(res))

def summ_nums(a, b):
    return a + b

def sub_nums(a, b):
    return a - b

def mult_nums(a, b):
    return a * b

def div_nums(a, b):
    return a / b

def div_int(a, b):
    return a // b

def div_rem(a, b):
    return a % b 




bot.infinity_polling()