from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton

button_1hour = InlineKeyboardButton(text = '1 час', callback_data = '1hour')
button_2hour = InlineKeyboardButton(text = '2 часа', callback_data = '2hour')
button_3hour = InlineKeyboardButton(text = '3 часа', callback_data = '3hour')
button_other = InlineKeyboardButton(text = 'Другое', callback_data = 'other')

hours = InlineKeyboardMarkup()
hours.add(button_1hour)
hours.add(button_2hour)
hours.add(button_3hour)
hours.add(button_other)

button_minutes = InlineKeyboardButton(text = 'Минут(ы)', callback_data = 'minutes')
button_hours = InlineKeyboardButton(text = 'Час(а)', callback_data = 'hours')

time_formar = InlineKeyboardMarkup()
time_formar.add(button_minutes)
time_formar.add(button_hours)