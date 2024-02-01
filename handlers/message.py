
import time

from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telebot.async_telebot import AsyncTeleBot
from datetime import datetime
from pprint import pprint

from create_bot import bot
from work_db import WorkDB


async def handler_message(message):

	str_time = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
	log_text = f"[{str_time}]:  {message.from_user.id}  --  {message.text}"

	db = WorkDB()

	match message.text:
		case 'Add expenses':
			keyboard = InlineKeyboardMarkup()
			food_btn = InlineKeyboardButton(text='Food', callback_data='aex t=Food')
			transport_btn = InlineKeyboardButton(text='Transportation', callback_data='aex t=Transport')
			clothing_cth = InlineKeyboardButton(text='Clothings', callback_data='aex t=Cloth')
			others_btn = InlineKeyboardButton(text='Others', callback_data='aex t=Others')
			keyboard.add(food_btn, transport_btn)
			keyboard.add(clothing_cth, others_btn)
			
			await bot.send_message(message.from_user.id,"Choose expense type", reply_markup=keyboard)
	
		case 'Show expenses':
			now = datetime.now()
			start_of_month = datetime(now.year, now.month, 1)
			timestamp_start_of_month = start_of_month.timestamp()
			sex = db.get_current_month_expenses(timestamp_start_of_month) 

			type_dict = {}
			for ex in sex:
				if ex['type'] not in type_dict.keys():
					type_dict[ex['type']] = 0
				type_dict[ex['type']] += ex['amount']
			text = "Overall expenses for current month:\n\n"
			total_expenses = 0
			for x in type_dict:
				total_expenses += type_dict[x]
				text += f"{x}: {type_dict[x]}\n"
			text += f"\nTotal expenses: {total_expenses}"
			
			keyboard = InlineKeyboardMarkup()
			sex_btn = InlineKeyboardButton(text='Details', callback_data='sex offset=0')
			keyboard.add(sex_btn)
			await bot.send_message(message.from_user.id, text, reply_markup=keyboard)


def register_handler_message(bot: AsyncTeleBot):
	bot.register_message_handler(handler_message, func=lambda message: True)
