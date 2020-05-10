import keyboards as kb
import telebot
from telebot import types

bot = telebot.TeleBot('1178877902:AAFuyvhcRvNuNgsd0VoY-bxMPczFp3p_7jA');

@bot.message_handler(commands = ['start'])
#def process_start_command(message: types.Message):
async def process_start_command(message):
    #message.reply("Привет!", reply_markup = kb.times)
    #question = 'На сколько включить интернет?'
    #bot.send_message(message.from_user.id, text = question, reply_markup=kb.times)
    question = 'Hello'
    print("ANSWER = ", message.from_user.id)
    #bot.send_message(message.from_user.id, text = 'hhhhhhh', reply_markup = kb.times)
    await message.reply("Первое - изменяем размер клавиатуры", reply_markup=kb.times)
    #message.reply("ANSWERRRRRR")
    ##bot.send_message(message.from_user.id, text = question, reply_markup = keyboard)
    #keyboard(message)
    print("Hello")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if message.text == "Привет":
		bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
		#keyboard(message)
		#kb.times
	elif message.text == "/help":
		bot.send_message(message.from_user.id, "Напиши привет");
	else:
		bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.");

def keyboard(message):
	question = 'На сколько включить интернет?'
	keyboard = types.InlineKeyboardMarkup();
	key_1hour = types.InlineKeyboardButton(text = '1 час', callback_data = '1hour')
	key_2hour = types.InlineKeyboardButton(text = '2 часа', callback_data = '2hour')
	key_3hour = types.InlineKeyboardButton(text = '3 часа', callback_data = '3hour')
	key_other = types.InlineKeyboardButton(text = 'Другое', callback_data = 'other')
	keyboard.add(key_1hour)
	keyboard.add(key_2hour)
	keyboard.add(key_3hour)
	keyboard.add(key_other)
	bot.send_message(message.from_user.id, text = question, reply_markup = keyboard)

def keyboard_times():
	question = 'Выберите измерение времени!'
	keyboard = types.InlineKeyboardMarkup();
	key_hours = types.InlineKeyboardButton(text = 'Час(а)', callback_data = 'hours')
	key_minutes = types.InlineKeyboardButton(text = 'Минут(ы)', callback_data = 'minutes')
	keyboard.add(key_minutes)
	keyboard.add(key_hours)
	bot.send_message(message.from_user.id, text = question, reply_markup = keyboard)

@bot.callback_query_handler(func = lambda call: True)
def callback_worker(call):
	if call.data == "1hour":
		print("1H")
		#bot.send_message(call.message.chat.id, 'Запомню : )');
	elif call.data == "2hour":
		print("2M")
	elif call.data == "3hour":
		print("3M")
	elif call.data == "other":
		keyboard_times()
		print("OTHER")
	elif call.data == "minutes":
		print("M")
	elif call.data == "hours":
		print("H")

bot.polling(none_stop = True, interval = 0)
