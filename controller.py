import main
import telebot
import random
from telebot import types
bot = telebot.TeleBot("6004565538:AAGOxuc9VVSwLt3yJskgP8kU1BvYhqQlNcY")

@bot.message_handler(commands=["calculator"])
def buttons(message):
    global typeNums
    a = types.ReplyKeyboardRemove()
    if message.text == 'Рациональные':
        bot.send_message(message.chat.id, f"Выбраны рациональные числа", reply_markup=a)
        bot.send_message(message.chat.id, f"Введите выражение разделяя пробелом")
        bot.register_next_step_handler(message, controller)
        typeNums = 0
    elif message.text == "Комплексные":
        bot.send_message(message.chat.id, f"Выбраны комплексные числа", reply_markup=a)
        bot.send_message(message.chat.id, f"Введите выражение разделяя пробелом")
        bot.register_next_step_handler(message, controller)
        typeNums = 1



def controller(message):
    res = ""
    line = message.txt.split()
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