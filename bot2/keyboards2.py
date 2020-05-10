#! /usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import types

button_1hour = types.InlineKeyboardButton(text = u'1 Час', callback_data = '1hour')
button_2hour = types.InlineKeyboardButton(text = u'2 Часа', callback_data = '2hour')
button_3hour = types.InlineKeyboardButton(text = u'3 Часа', callback_data = '3hour')
button_other = types.InlineKeyboardButton(text = u'Другое время', callback_data = 'other')

hours = types.InlineKeyboardMarkup()
hours.add(button_1hour)
hours.add(button_2hour)
hours.add(button_3hour)
hours.add(button_other)

button_minutes = types.InlineKeyboardButton(text = u'Минут(ы)', callback_data = 'minutes')
button_hours = types.InlineKeyboardButton(text = u'Час(ов)', callback_data = 'hours')

time_format = types.InlineKeyboardMarkup()
time_format.add(button_minutes)
time_format.add(button_hours)

YES = types.InlineKeyboardButton(text = u'Дать доступ', callback_data = 'user_approve')
NO = types.InlineKeyboardButton(text = u'Запретить', callback_data = 'user_decline')
access = types.InlineKeyboardMarkup()
access.add(YES)
access.add(NO)


def add_ssh(user_id, user_name):
	ssh_button_yes = types.InlineKeyboardButton(text = u'Добавить', callback_data = 'ssh_approve %s %s' % (user_id, user_name))
	ssh_button_no = types.InlineKeyboardButton(text = u'Не добавлять', callback_data = 'ssh_decline %s %s' % (user_id, user_name))
	ssh = types.InlineKeyboardMarkup()
	ssh.add(ssh_button_yes)
	ssh.add(ssh_button_no)
	return ssh

def add_new_user(user_id, user_name):
	YES = types.InlineKeyboardButton(text = u'Дать доступ', callback_data = 'add_approve %s %s' % (user_id, user_name))
	NO = types.InlineKeyboardButton(text = u'Запретить', callback_data = 'add_decline %s' % (user_id))
	access = types.InlineKeyboardMarkup()
	access.add(YES)
	access.add(NO)
	return access


def generate_buttons(count, user_list):
	del_buttons = types.InlineKeyboardMarkup()
	for item in range(0, count):
		del_buttons.add(types.InlineKeyboardButton(text = '%s (id:%s)' % (user_list[item][1], user_list[item][0]), callback_data = '%s %s %s' % ("del", user_list[item][0], user_list[item][1])))
	return del_buttons
