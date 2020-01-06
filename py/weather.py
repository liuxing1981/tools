#!/usr/bin/python3
import json
from pprint import pprint
import requests
import sys


def parse(obj):
    low = obj['low'].replace('低温 ', '')
    high = obj['high'].replace('高温 ', '')
    temp = low + '~' + high
    type = obj['type']
    return type + ' ' + temp


url = 'http://wthrcdn.etouch.cn/weather_mini?city=青岛'
result = requests.get(url).content.decode('utf-8')
result = json.loads(result)
size = len(sys.argv)
# no param
if size == 1:
    day = result['data']['forecast'][0]
# one param
elif size > 1:
    index = int(sys.argv[1])
    if index > 0:
        day = result['data']['forecast'][index]
    elif index == -1:
        day = result['data']['yesterday']
weather = parse(day)
print(weather)
