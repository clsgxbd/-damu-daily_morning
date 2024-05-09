from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

user_id_2 = os.environ["USER_ID_2"]
template_id_2 = os.environ["TEMPLATE_ID"]

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  print("\nurl"+url)
  res = requests.get(url).json()
  print("\nres"+res)
  weather = res['data']['list'][0]
  print("\nweather"+weather)
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
# wea, temperature = get_weather()
wea = "晴"
temperature = "520"
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
print("\n============================================\n============================================\n")
print("data: ",data)
print("user_id: ",user_id)
print("template_id: ",template_id)
print("user_id_2: ",user_id_2)
print("template_id_2: ",template_id_2)
print("\n============================================\n============================================\n")
res1 = wm.send_template(user_id, template_id, data)
print(res1)
res2 = wm.send_template(user_id_2, template_id_2, data)
print(res2)
