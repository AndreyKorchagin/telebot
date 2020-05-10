import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot
from aiogram import types
import keyboards as kb


from config import TOKEN

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

def function():
	pass

@dp.message_handler(commands=['start'])
async def process_start_command(message):
	print(message.from_user.id)
	await bot.send_message(message.from_user.id, text = 'HHHHH', reply_markup=kb.hours)



@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
	await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")

@dp.message_handler()
async def echo_message(msg: types.Message):
	await bot.send_message(msg.from_user.id, msg.text)

@dp.callback_query_handler(lambda call: call.data == '1hour')
async def process_callback_1hour(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')

@dp.callback_query_handler(lambda call: call.data == '2hour')
async def process_callback_2hour(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	await bot.send_message(callback_query.from_user.id, 'Нажата 2 кнопка!')

@dp.callback_query_handler(lambda call: call.data == '3hour')
async def process_callback_3hour(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	await bot.send_message(callback_query.from_user.id, 'Нажата 3 кнопка!')

@dp.callback_query_handler(lambda call: call.data == 'other')
async def process_callback_other(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	await bot.send_message(callback_query.from_user.id, 'Нажата other кнопка!')
	#await bot.register_next_step_handler(callback_query, select_time)
	#await bot.send_message(callback_query.message.chat.id, text = 'time', reply_markup=kb.time_formar)

@dp.callback_query_handler(lambda call: call.data == 'minutes')
async def process_callback_minutes(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	await bot.send_message(callback_query.from_user.id, 'minutes')

@dp.callback_query_handler(lambda call: call.data == 'hours')
async def process_callback_hours(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	await bot.send_message(callback_query.from_user.id, 'hours')

@dp.message_handler()
async def select_time(callback_query: types.CallbackQuery):
	print("select_time")

if __name__ == '__main__':
	executor.start_polling(dp)