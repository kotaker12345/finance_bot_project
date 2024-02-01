import os
import time
import asyncio	

from telebot.async_telebot import AsyncTeleBot


from create_bot import bot
from handlers import start, message, callbacks



start.register_handler_start(bot)
callbacks.register_callback_handler(bot)
message.register_handler_message(bot)







def debug_main():
	asyncio.run(bot.polling())

def unbmain():
	while True:
		try:
			asyncio.run(bot.polling())
		except:
			pass
			
if __name__ == "__main__":

	debug_main()






