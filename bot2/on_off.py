import sys
import os
from array import array
import edit_firewall as ef

# mode = 0 - check status
# mode = 1 - reverse status

def get_day():
	date = os.popen("date").read()
	day = date.split(' ')
	return day[0]

def check(mode):

	file = "/etc/config/firewall"
	#file = "firewall"
	
	block = 0
	str1 = get_day()
	str2 = ['\toption enabled \'0\'\n']

	f = open(file, "r")
	content = f.readlines()
	f.close()

	for i in range(len(content)):
		val = "".join(content[i])
		s = val.find(str1)
		if s > 0:
			if content[i + 1] == str2[0]:
				block = i + 1
				status = 1
			else:
				block = i + 1
				status = 0

	if mode == 1:
		if status:
			content.pop(block)

			f = open("/root/test", "a")
			for item in ef.getListMacsFromFirewall("\toption name 'Gera'"):
				print("ubus call hostapd.wlan1 del_client \"{\'addr\':'%s', \'reason\':5, \'deauth\':false, \'ban_time\':10000}\"" % item.lower())
				
				firewall = f.write("ubus call hostapd.wlan1 del_client \"{\'addr\':'%s', \'reason\':5, \'deauth\':false, \'ban_time\':10000}\"\n" % item.lower())
				os.system("ubus call hostapd.wlan1 del_client \"{\'addr\':'%s', \'reason\':5, \'deauth\':false, \'ban_time\':10000}\"" % item.lower())
			f.close()
		else:
			content.insert(block, str2[0])

			# f = open("/root/test", "a")
			# for item in ef.getListMacsFromFirewall("option name 'Gera'\n"):
			# 	print("ubus call hostapd.wlan1 del_client \"{\'addr\':'%s', \'reason\':5, \'deauth\':false, \'ban_time\':100000}\"" % item.lower())
				
			# 	firewall = f.write("ubus call hostapd.wlan1 del_client \"{\'addr\':'%s', \'reason\':5, \'deauth\':false, \'ban_time\':100000}\"\n" % item.lower())
			# 	os.system("ubus call hostapd.wlan1 del_client \"{\'addr\':'%s', \'reason\':5, \'deauth\':false, \'ban_time\':100000}\"" % item.lower())
			# f.close()



		f = open(file, "w")
		content = "".join(content)
		f.write(content)
		f.close()
	elif mode == 0:
		if status:
			#print("BLOCK 0FF")
			return 0
		else:
			#print("BLOCK ON")
			return 1

if __name__ == '__main__':
	check(1)