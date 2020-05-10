#!/bin/sh
py=$(ps | grep "python /root/telebot/bot2/bot2.py" | head -n 1 | awk '{print $5}')
path=$(ps | grep "python /root/telebot/bot2/bot2.py" | head -n 1 | awk '{print $6}')

status=0

if [[ $py = "python" ]]
then
	if [[ $path = "/root/telebot/bot2/bot2.py" ]]
	then
		status=1
	fi
fi

if [[ $status = 0 ]]
then
	sh /root/telebot/bot2/start &
	echo "bot restart `date`" >> /root/telebot/bot2/log_bown
fi
