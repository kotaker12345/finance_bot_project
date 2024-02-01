import time

from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.async_telebot import AsyncTeleBot
from telebot import asyncio_filters
from datetime import datetime
from decimal import Decimal
from pprint import pprint

from work_db import WorkDB
from create_bot import bot


class ExpensesStates(StatesGroup):
	cost_input = State() 
	
	
def nav_buttons_keyboard(offset, page_element_amount, elements_amount):
	next_button = InlineKeyboardButton(text='➡️', callback_data=f'sex offset={offset + page_element_amount if offset + page_element_amount >= 0 else 0}')
	back_button = InlineKeyboardButton(text='⬅️', callback_data=f'sex offset={offset - page_element_amount if offset - page_element_amount >= 0 else 0}')
	back_to_main = InlineKeyboardButton(text='🔙 ', callback_data='ssex')
	
	max_elements_amount = page_element_amount + 2
	
	if offset == 0 and elements_amount <= page_element_amount:

		navigation_buttons = [back_to_main]
	elif offset == 0 and elements_amount > page_element_amount:

		navigation_buttons = [back_to_main, next_button]
	elif offset >= page_element_amount - 2 and elements_amount > page_element_amount:

		navigation_buttons = [back_to_main, back_button, next_button]
	elif offset >= page_element_amount - 2 and elements_amount <= page_element_amount and elements_amount < max_elements_amount:

		navigation_buttons = [back_to_main, back_button]

	keyboard = InlineKeyboardMarkup()
	
	keyboard.add(*navigation_buttons)

	return keyboard


async def callback_handler(call):	
	print(f"{call.from_user.id}: {call.data}")


async def callback_cancel_handler(call):	
	await bot.delete_state(call.from_user.id, call.message.chat.id)
	await bot.delete_message(call.from_user.id, call.message.id)
	await bot.send_message(call.from_user.id, '✔️ Cancelled')
	
	
async def callback_details_handler(call):
	
	db = WorkDB()
	records_amount = 10
	params = call.data.split(' ')
	param_list = {}

	for param in params:				
		key_value = param.split('=')  	
		if len(key_value) > 1: 			
			key, value = key_value		
			param_list[key] = value	
	expenses = db.get_expenses( records_amount+2, int(param_list['offset']))

	keyboard = nav_buttons_keyboard(int(param_list['offset']), records_amount, len(expenses))
	text = 'Total expenses:\n\n'
	
	for x in expenses:
		text += f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x['timestamp']))} <b>{x['type']}</b> <code>{x['amount']}</code>\n"
	await bot.edit_message_text(text, call.from_user.id, call.message.id, reply_markup=keyboard, parse_mode="HTML")
	
	
async def callback_show_expenses_handler(call):
	db = WorkDB()
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
	await bot.edit_message_text(text, call.from_user.id, call.message.id, reply_markup=keyboard, parse_mode="HTML")

async def callback_expenses_handler(call):


	params = call.data.split(' ')		
	param_list = {}

	for param in params:				
		key_value = param.split('=')  	
		if len(key_value) > 1: 			
			key, value = key_value		
			param_list[key] = value		

	aexpense = params[0]				
	aexpense_type = param_list['t']

	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton(text='✖️ cancel', callback_data='cancel'))
	text = 'Enter cost spent'

	await bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=keyboard , parse_mode="HTML")
	await bot.set_state(call.from_user.id, ExpensesStates.cost_input, call.message.chat.id)
	async with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:  
		data['aexpense_type'] = aexpense_type										
		data['message_id'] = call.message.id
	


async def cost_input_handler(message):
	db = WorkDB()
	amount = message.text.replace(',', '.')
	async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
		expenses_type = data['aexpense_type']
		timestamp = time.time()
		message_id = data['message_id']
	try:
		amount = Decimal(amount)
	except:
		await bot.delete_state(message.from_user.id, message.chat.id)
		await bot.send_message(message.from_user.id, 'Error! Please, use numeric values')
		await bot.delete_message(message.from_user.id, message_id)
		return

	db.add_expenses(expenses_type=expenses_type, amount=amount, timestamp=timestamp)
	await bot.delete_state(message.from_user.id, message.chat.id)
	text = '✅ Done'
	await bot.edit_message_text(text, message.chat.id, message_id, parse_mode="HTML")



def register_callback_handler(bot: AsyncTeleBot):
	bot.add_custom_filter(asyncio_filters.StateFilter(bot))
	bot.register_message_handler(cost_input_handler, func=lambda message: True, state=ExpensesStates.cost_input)
	bot.register_callback_query_handler(callback_expenses_handler, func=lambda call: call.data.split(' ')[0] == 'aex') # попадает в обработчик при условии (' ')[0] == 'aex'
	bot.register_callback_query_handler(callback_details_handler, func=lambda call: call.data.split(' ')[0] == 'sex') # попадает в обработчик при условии (' ')[0] == 'aex'
	bot.register_callback_query_handler(callback_show_expenses_handler, func=lambda call: call.data.split(' ')[0] == 'ssex') # попадает в обработчик при условии (' ')[0] == 'aex'
	bot.register_callback_query_handler(callback_cancel_handler, func=lambda call: call.data == 'cancel')
	bot.register_callback_query_handler(callback_handler, func=lambda call: True)























