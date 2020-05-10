file = "access.user"

def check_exist_user(content, user):
	for item in content:
		val = item.strip('\n')
		if val == user:
			status = True
			return status
		else:
			status = False
	return status


def get_content(file_loc):
	f = open(file_loc, "r")
	content = f.readlines()
	f.close()
	return content


def check_user(user_id):
	global file
	content = get_content(file)
	status = False
	for item in content:
		val = item.strip('\n')
		if val == user_id:
			status = True
	return status


def add_user(user_id):
	global file

	content = get_content(file)
	if not check_exist_user(content, user_id):
		content.append(user_id + '\n')
	content = "".join(content)
	f = open(file, "w")
	f.write(content)
	f.close()

def del_user(user_id):
	global file
	content = get_content(file)
	if check_exist_user(content, user_id.strip('\n')):
		content.remove(user_id + '\n')
		content = "".join(content)
		f = open(file, "w")
		f.write(content)
		f.close()


#if __name__ == '__main__':

