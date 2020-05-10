#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

file = "/root/telebot/bot2/access.user"
#file = "access.user"


def get_id(item):
	id = item.split(' ')[0]
	return id


def check_exist_user(content, user_id):
	status = False
	for item in content:
		val = get_id(item)
		if val == user_id:
			status = True
			return status
	return status


def get_content(file_loc):
	f = codecs.open(file_loc, "r", "utf-8")
	content = f.readlines()
	f.close()
	return content


def check_user(user_id):
	global file
	content = get_content(file)
	status = False
	for item in content:
		val = get_id(item)
		if val == user_id:
			status = True
	return status


def add_user(user_id, first_name):
	global file

	content = get_content(file)
	if not check_exist_user(content, user_id):
		content.append('%s %s\n' % (user_id, first_name))
	content = "".join(content)
	f = codecs.open(file, "w", "utf-8")
	f.write(content)
	f.close()


def del_user(user_id):
	global file
	content = get_content(file)
	if check_exist_user(content, user_id):
		i = 0
		for item in content:
			item = item.split(' ')[0]
			if not item == user_id:
				i += 1
			else:
				content.pop(i)
				break;
		content = "".join(content)
		f = codecs.open(file, "w", "utf-8")
		f.write(content)
		f.close()

def get_count_user():
	return len(get_content(file))

def get_user_list():
	users = []
	for item in get_content(file):
		item = item.strip('\n').split(' ') 
		users.append(item)
	return users



#if __name__ == '__main__':
