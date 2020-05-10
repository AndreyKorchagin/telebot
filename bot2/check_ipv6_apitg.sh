#!/bin/bash
# check & define ipv6 address for api.telegram.org in /etc/hosts
# crontab example (not state-of-the-art)
# */10 * * * * ~/telebot/bot2/check_ipv6_apitg.sh& >/dev/null 2>&1 
# chpeckdev 5/9/2020 4:28am

target_file=/etc/hosts
url_apitg=api.telegram.org
ipv6_apitg=`nslookup $url_apitg | tail -n 1 | cut -c 12-46`
str_replace="${ipv6_apitg} ${url_apitg}"

ipv6_regex='^([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4}$'
if [[ $ipv6_apitg =~ $ipv6_regex ]]; then
    :
else
    exit 1
fi

if grep -q "$url_apitg" "$target_file"; then
    sed -i "/$url_apitg/c$str_replace" "$target_file"
else
    echo "" >> "$target_file"
    echo "$str_replace" >> "$target_file"
fi

exit 0
