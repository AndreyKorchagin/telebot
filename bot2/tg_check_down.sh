#!/bin/sh

count=$(ps | grep "python /root/telebot/bot2/bot2.py" | wc -l)

if [[ $count = 1 ]]
then
	echo "True $count"
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
		echo -e "bot restart \t`date`" >> /root/telebot/bot2/log_down
	fi

elif [[ $count -gt 2 ]]
then
	while [ $count -gt 2 ]
	do
		pid=$(ps | grep "python /root/telebot/bot2/bot2.py" | tail -2 | head -1 | awk '{print $1}')
		kill $pid
		count=$(ps | grep "python /root/telebot/bot2/bot2.py" | wc -l)
		echo -e "bot kill $pid \t`date`" >> /root/telebot/bot2/log_down
	done
fi
