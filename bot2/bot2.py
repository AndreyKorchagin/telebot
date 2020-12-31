#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import keyboards2 as kb
from config import TOKEN
import telebot
from telebot import types
import on_off as on
import user_action as ua
import binascii
import re
from datetime import datetime
import edit_firewall as ef

time = 0;
admin_id = "139050906"

bot = telebot.TeleBot(TOKEN)

def access(message):
	if ua.check_user(str(message.from_user.id)) or message.from_user.id == int(admin_id):
		return True
	else:
		return False

def add_ssh_pub_to_tmp(key):
	f = open("/root/telebot/bot2/ssh.tmp", "w+")
	f.write(key)
	f.close

def check_add_ssh_pub():
	return os.popen("/root/telebot/bot2/check_add_ssh_pub.sh").read()

@bot.message_handler(commands=['start'])
def process_start_command(message):
	global new_user_id
	global new_user_first_name
	if access(message):
		bot.send_message(message.from_user.id, text = u'Вы авторизованы')
	else:
		bot.send_message(message.from_user.id, text = u'Вы не авторизованы.\nВаш запрос отправлен администратору!!!')
		bot.send_message(admin_id, text = u'Добавить пользователя "%s" (id:%d)?' % (message.from_user.first_name, message.from_user.id), reply_markup=kb.add_new_user(message.from_user.id, message.from_user.first_name))

help_str_auth = u'/help - Список функций\n\
/start - Авторизация\n\
/inet_on - Включить интернет\n\
/inet_off - Отключить интернет\n\
/ssh_add_pub_key - Добавить публичный ключ для ssh\n\
/status - Узнать статутс интернета\n\
/time_left - Узнать отсаток времени\n'

help_str = u'Вы не авторизованы!!!\n/start - Авторизация\n'
help_str_root = u'/help - Список функций\n\
/start - Авторизация\n\
/inet_on - Включить интернет\n\
/inet_off - Отключить интернет\n\
/list - Вывод списка пользователей\n\
/del_user - Удалить пользователй\n\
/ssh_add_pub_key - Добавить публичный ключ для ssh\n\
/status - Узнать статутс интернета\n\
/time_left - Узнать отсаток времени\n\
/clients_list - Список подключенных клиентов\n\
/black_list - Список наказанных пользователей\n\
/add_user_black_list - Добавляет засранца в список наказанных пользователей\n\
/delete_user_black_list - Удаляет засранца из списка наказанных пользователей\n'



@bot.message_handler(commands=['help'])
def process_help_command(message):
    if message.from_user.id == int(admin_id):
    	bot.send_message(message.from_user.id, text = help_str_root)
    elif access(message):
    	bot.send_message(message.from_user.id, text = help_str_auth)
    else:
    	bot.send_message(message.from_user.id, text = help_str)


@bot.message_handler(commands=['list'])
def process_help_command(message):
    if message.from_user.id == int(admin_id):
    	string = ""
    	for item in range(0, ua.get_count_user()):
    		string = u'%s%d.\t%s\t(id:%s)\n' % (string, item + 1, ua.get_user_list()[item][1], ua.get_user_list()[item][0])
    	bot.send_message(message.from_user.id, text = string)
    else:
    	bot.send_message(message.from_user.id, text = u'Вы не root!!!')


@bot.message_handler(commands=['status'])
def process_help_command(message):
    if access(message):
    	check = on.check(0)
    	if check == 0:
    		bot.send_message(message.from_user.id, 'Интернет включен')
    	else:
    		bot.send_message(message.from_user.id, 'Интернет выключен')
    else:
    	bot.send_message(message.from_user.id, text = u'Вы не авторизованы!!!')


@bot.message_handler(commands=['ssh_add_pub_key'])
def process_help_command(message):
	if access(message):
			bot.send_message(message.from_user.id, text = u'Скопируйте ваш публичный ключ, затем вставьте сюда и поставьте вначале "/"')
	else:
		bot.send_message(message.from_user.id, text = u'Вы не авторизованы!!!')


@bot.message_handler(commands=['ssh-rsa'])
def process_help_command(message):
	if access(message):
		key = re.split(r'\s{1,}', message.text)
		if len(key) == 3:
			bot.send_message(admin_id, text = u'Пользователь %s (id:%s) хочет добавить свой публичный ssh ключ!!!' % (message.from_user.first_name, message.from_user.id), reply_markup = kb.add_ssh(message.from_user.id, message.from_user.first_name))
			string = key[0]
			for i in range(1, 3):
				string = u'%s %s' % (string, key[i])
			string = u'%s\n' % (string[1:])
			print(string)
			add_ssh_pub_to_tmp(string)
	else:
		bot.send_message(message.from_user.id, text = u'Вы не авторизованы!!!')


@bot.message_handler(commands=['inet_on'])
def process_start_command(message):
	if access(message):
		bot.send_message(message.from_user.id, text = u'Выберите время работы интернета!', reply_markup = kb.hours)	
	else:
		bot.send_message(message.from_user.id, text = u'Вы не авторизованы.')

@bot.message_handler(commands=['inet_off'])
def process_help_command(message):
	if access(message):
		if on.check(0) == 0:
			bot.send_message(message.from_user.id, text = u'Интернет принудительно выключен')
			os.system("/bin/sh /root/telebot/managment/en_block")
			atq = "atq | awk '{print $1}'"
			answ = os.popen(atq).read()
			atrm  = "atrm " + str(answ)
			os.system(atrm)

			# badList = ef.getListMacsFromFirewall("option name 'Gera'\n");
			badList = ef.getListMacsFromFirewall("\toption name 'Gera'");
			UBUS = "ubus call hostapd.wlan1 del_client \"{\'addr\':'%s', \'reason\':5, \'deauth\':false, \'ban_time\':10000}\""

			for item in badList:
				print("UBUS" + item.lower())
				print(UBUS % item.lower())
				os.system(UBUS % item.lower())


		else:
			bot.send_message(message.from_user.id, text = u'Интернет уже выключен')
	else:
		bot.send_message(message.from_user.id, text = u'Вы не авторизованы.')


@bot.message_handler(commands=['del_user'])
def process_help_command(message):
	if message.from_user.id == int(admin_id):
		if not (ua.get_count_user()) == 0:
			bot.send_message(message.from_user.id, text = u'Вы в root!!!')
			bot.send_message(message.from_user.id, text = u'Выберите пользователя котогрого хотите удалить!!!', reply_markup = kb.generate_buttons(ua.get_count_user(), ua.get_user_list()))
		else:
			bot.send_message(message.from_user.id, text = u'Список пользователей пуст!!!')
	else:
		bot.send_message(message.from_user.id, text = u'Пшел отсюда!!!')


@bot.message_handler(commands=['time_left'])
def process_help_command(message):
	if access(message):
		if on.check(0) == 0:
			format = '%H:%M:%S'
			time = os.popen("atq | awk '{print $5}'").read()
			date = os.popen("date | awk '{print $4}'").read()
			stop = datetime.strptime(time.strip('\n'), format)
			start = datetime.strptime(date.strip('\n'), format)
			delta = stop - start
			bot.send_message(message.from_user.id, u'Интернет выключиться через %s' % (delta))
		else:
			bot.send_message(message.from_user.id, u'Интернет выключен')
	else:
		bot.send_message(message.from_user.id, text = u'Вы не авторизованы.')

@bot.message_handler(commands=['clients_list'])
def process_get_network_clients_list_commadn(message):
	if message.from_user.id == int(admin_id):

		bot.send_message(message.from_user.id, text = u'Вы в root!!!')

		string = u'Список подключенных пользователей:\n'

		connectionsList = ef.getConnections()
		for i in range(0, len(connectionsList)):
			item = connectionsList[i]
			string = u'%s%d. %s - %s - %s\n' % (string, i + 1, item[0].upper(), item[1], item[2])

		bot.send_message(message.from_user.id, text = string)

	else:
		bot.send_message(message.from_user.id, text = u'Пшел отсюда!!!')

@bot.message_handler(commands=['black_list'])
def process_get_network_clients_list_commadn(message):
	if message.from_user.id == int(admin_id):
		bot.send_message(message.from_user.id, text = u'Вы в root!!!')

		string = u'Список плохих пользователей:\n'

		# listMacsFromFirewall = ef.getListMacsFromFirewall("option name 'Gera'\n")
		listMacsFromFirewall = ef.getListMacsFromFirewall("\toption name 'Gera'")
		for i in range(0, len(listMacsFromFirewall)):
			item = listMacsFromFirewall[i]
			string = u'%s%d: %s\n' % (string, i + 1, item)
		bot.send_message(message.from_user.id, text = string)
	else:
		bot.send_message(message.from_user.id, text = u'Пшел отсюда!!!')

# @bot.message_handler(commands=['add_user_black_list'])
# def process_get_network_clients_list_commadn(message):
# 	if message.from_user.id == int(admin_id):
# 		bot.send_message(message.from_user.id, text = u'Вы в root!!!')



# 	else:
# 		bot.send_message(message.from_user.id, text = u'Пшел отсюда!!!')


@bot.message_handler(commands=['delete_user_black_list'])
def process_get_network_clients_list_commadn(message):
	if message.from_user.id == int(admin_id):
		bot.send_message(message.from_user.id, text = u'Вы в root!!!')


		list1 = ef.getConnections()
		list2 = ef.getListMacsFromFirewall("\toption name 'Gera'")
		# list2 = ef.getListMacsFromFirewall("option name 'Gera'\n")


		print("1:")
		print(list1)
		print("2")
		print(list2)


		newList = []

		for i in list1:
			for j in list2:
				if i[0].upper() == j:
					newList.append(i)

		print(newList)


		# if not (ua.get_count_user()) == 0:
		# listMacsFromFirewall = ef.getListMacsFromFirewall("option name 'Gera'\n")
		listMacsFromFirewall = ef.getConnections()
		bot.send_message(message.from_user.id, text = u'Вы в root!!!')
		bot.send_message(message.from_user.id, text = u'Выберите пользователя котогрого хотите удалить!!!', reply_markup = kb.generate_buttons(len(newList), newList))

		# else:
			# bot.send_message(message.from_user.id, text = u'Список пользователей пуст!!!')

	else:
		bot.send_message(message.from_user.id, text = u'Пшел отсюда!!!')


@bot.message_handler()
def process_digt_command(message):
	if access(message):
		if message.text.isdigit():
			global time
			time = int(message.text)
			bot.send_message(message.from_user.id, text = u'Выберите измерение времени!', reply_markup=kb.time_format)
		else:
			bot.send_message(message.from_user.id, text = u'Повторите ввод')
	else:
		bot.send_message(message.from_user.id, text = u'Вы не авторизованы.')


@bot.callback_query_handler(lambda call: True)
def callback_worker(call):
	global new_user_id
	if access(call):
		global time
		check = on.check(0)
		if call.data == '1hour':
			if check == 0:
				bot.send_message(call.from_user.id, u'Интернет уже включен!')
			else:
				bot.send_message(call.from_user.id, u'Интернет будет включен на 1 час')
				bot.send_message(admin_id, u'Пользователь %s включил интернет на 1 час' % (call.from_user.first_name))
				os.system("/bin/sh /root/telebot/managment/block 1 hours")
		elif call.data == '2hour':
			if check == 0:
				bot.send_message(call.from_user.id, u'Интернет уже включен!')
			else:
				bot.send_message(call.from_user.id, u'Интернет будет включен на 2 часа')
				bot.send_message(admin_id, u'Пользователь %s включил интернет на 2 часa' % (call.from_user.first_name))
				os.system("/bin/sh /root/telebot/managment/block 2 hours")
		elif call.data == '3hour':
			if check == 0:
				bot.send_message(call.from_user.id, u'Интернет уже включен!')
			else:
				bot.send_message(call.from_user.id, u'Интернет будет включен на 3 часа')
				bot.send_message(admin_id, u'Пользователь %s включил интернет на 3 час' % (call.from_user.first_name))
				os.system("/bin/sh /root/telebot/managment/block 3 hours")
		elif call.data == 'other':
			if check == 0:
				bot.send_message(call.from_user.id, u'Интернет уже включен!')
			else:
				bot.send_message(call.from_user.id, u'Введите число')
		elif call.data == 'minutes':
			if check == 0:
				bot.send_message(call.from_user.id, u'Интернет уже включен!')
			else:
				bot.send_message(call.from_user.id, u'Интернет будет включен на ' + str(time) + u' минут(ы)')
				bot.send_message(admin_id, u'Пользователь %s включил интернет на %d минут(ы)' % (call.from_user.first_name, time))
				os.system("/bin/sh /root/telebot/managment/block " + str(time) + "minutes")

		elif call.data == 'hours':
			if check == 0:
				bot.send_message(call.from_user.id, u'Интернет уже включен!')
			else:
				if time >= 24:
					bot.send_message(call.from_user.id, u'Интернет нельзя включить больше чем на 24 часа')
				else:
					bot.send_message(call.from_user.id, u'Интернет будет включен на ' + str(time) + u' часа(ов)')
					bot.send_message(admin_id, u'Пользователь %s включил интернет на %d часа(ов)' % (call.from_user.first_name, time))
					os.system("/bin/sh /root/telebot/managment/block " + str(time) + "hours")
		elif call.data.split(' ')[0] == 'add_approve':
			ua.add_user(str(call.data.split(' ')[1]), call.data.split(' ')[2])
			bot.send_message(call.data.split(' ')[1], u'Доступ предоставлен!!!')
			bot.send_message(call.from_user.id, u'Доступ предоставлен пользователю %s (id:%s)!!!' % (str(call.data.split(' ')[1]), call.data.split(' ')[2]))
			new_user_id = 0
			new_user_first_name = ""
		elif call.data.split(' ')[0] == 'add_decline':
			bot.send_message(call.data.split(' ')[1], u'Отказано в доступе!!!')
		elif call.data.split(' ')[0] == 'del':
			id_del = call.data.split(' ')[1]
			user_del = call.data.split(' ')[2]
			ua.del_user(id_del)
			bot.send_message(admin_id, u'Пользователь %s (id:%s) - УДАЛЕН' % (user_del, id_del))
			bot.send_message(id_del, u'Пользователь %s (id:%s) - УДАЛЕН' % (user_del, id_del))
		elif call.data.split(' ')[0] == 'ssh_approve':
			if check_add_ssh_pub() == 'True\n':
				bot.send_message(admin_id, u'SSH ключ пользователя %s (id:%s) добавлен' % (call.data.split(' ')[2], call.data.split(' ')[1]))
				bot.send_message(call.data.split(' ')[1], u'Ваш ключ добавлен и Вам предоставлен доступ')
			else:
				bot.send_message(admin_id, u'Ключ не верный')
				bot.send_message(call.data.split(' ')[1], u'Ключ не верный')
		elif call.data.split(' ')[0] == 'ssh_decline':
			bot.send_message(admin_id, u'Пользователь %s (id:%s) отказано в добавлении SSH Ключа' % (call.data.split(' ')[2], call.data.split(' ')[1]))
			bot.send_message(call.data.split(' ')[1], u'Вам отказано в добавлении SSH Ключа')
	else:
		bot.send_message(message.from_user.id, text = u'Вы не авторизованы.')


if __name__ == '__main__':
	bot.polling(none_stop = True, interval = 0)	


