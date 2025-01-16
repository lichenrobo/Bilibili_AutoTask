#!/bin/bash
#echo "$0"
#echo $1

csrf=$(cat ./user/csrf)                 # 因为在 btool.py 处调用，所以目录等级在根目录上
#echo "$csrf"
SESSDATA=$(cat ./user/SESSDATA)         # 因为在 btool.py 处调用，所以目录等级在根目录上
#echo "$SESSDATA"

curl 'https://api.bilibili.com/x/vip/privilege/receive' \
--data-urlencode "type=""$1" \
--data-urlencode "platform=web" \
--data-urlencode "csrf=""$csrf" \
-b "SESSDATA=""$SESSDATA"



