import telebot
import random
from telebot import types
import game
import controller

bot = telebot.TeleBot("6004565538:AAGOxuc9VVSwLt3yJskgP8kU1BvYhqQlNcY")


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "/game")
    bot.send_message(message.chat.id, "/calculator")

bot.infinity_polling()
