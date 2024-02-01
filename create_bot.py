from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

import config

bot = AsyncTeleBot(config.API_TOKEN, state_storage = StateMemoryStorage())