#!/bin/bash
#echo "$0"
#echo $1

csrf=$(cat ./config/csrf)                 # 因为在 btool.py 处调用，所以目录等级在根目录上
#echo "$csrf"
SESSDATA=$(cat ./config/SESSDATA)         # 因为在 btool.py 处调用，所以目录等级在根目录上
#echo "$SESSDATA"

curl 'https://api.bilibili.com/x/vip/privilege/receive' \
--data-urlencode "type=""$1" \
--data-urlencode "platform=web" \
--data-urlencode "csrf=""$csrf" \
-b "SESSDATA=""$SESSDATA"



