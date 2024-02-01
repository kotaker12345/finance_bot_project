import time


from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telebot.async_telebot import AsyncTeleBot

from create_bot import bot


def panel_keyboard():
	keyboard = ReplyKeyboardMarkup(True, False)
	keyboard.row('Add expenses')
	keyboard.row('Show expenses')
	return keyboard


async def handler_start(message):
	await bot.send_message(message.from_user.id,"📖 Hello, choose an option 📖", reply_markup=panel_keyboard())
	str_time = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
	log_text = f"[{str_time}]:  {message.from_user.id}  --  {message.text}"
	
def register_handler_start(bot: AsyncTeleBot):
	bot.register_message_handler(handler_start, commands=['start'])
  
  
  
  
  
  
  
  
  
  
  
  
  