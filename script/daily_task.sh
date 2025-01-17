#!/bin/bash
#echo "$0"
#echo $1

csrf=$(cat ./config/csrf)                 # 因为在 btool.py 处调用，所以目录等级在根目录上
#echo "$csrf"
SESSDATA=$(cat ./config/SESSDATA)         # 因为在 btool.py 处调用，所以目录等级在根目录上
#echo "$SESSDATA"

#大会员每日经验
curl 'https://api.bilibili.com/x/vip/experience/add' \
--data-urlencode "csrf=""$csrf" \
-b "SESSDATA=""$SESSDATA"


#curl 'https://api.bilibili.com/pgc/activity/score/task/sign' \
#--data-urlencode "csrf=""$csrf" \
#-b "SESSDATA=""$SESSDATA"\
#--referer 'https://www.bilibili.com'



