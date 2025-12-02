import datetime
import os

import cn2an
import requests
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.ext.command_util import Commands
from botpy.message import GroupMessage

from utils import get_root_path

project_root = get_root_path()
config = read(os.path.join(project_root, "config/api/api.yaml"))
logger = logging.get_logger()
enter_group_date = datetime.date(2025, 9, 14)

weather_apikey = config["weather_apikey"]
weather_sign = config["weather_sign"]


@Commands("每日打卡")
async def daily_attendance(message: GroupMessage, params=None):
    if message.author.member_openid == "BB120C4A9FAB08E61D5602BE76AB1FB1  ":
        num = (datetime.date.today() - enter_group_date).days + 1
        chinese_num = cn2an.an2cn(num)
        await message.reply(content=f"\n想念超哥第{chinese_num}天")
        logger.info(f"回复信息：想念超哥第{chinese_num}天")
    else:
        await message.reply(content="\n打卡成功！\n（没什么用）")
    return True


@Commands("每日一言")
async def daily_say(message: GroupMessage, params=None):
    response = requests.get(config["daily_say_api_key"], timeout=5)
    if response.status_code == 200:
        content = response.json()["text"]
        await message.reply(content=content)
    else:
        await message.reply(content="\n出错了！请at开发者查询")
        logger.info(f"[error]：{response.status_code}")
    return True


@Commands("每日新闻")
async def daily_news(message: GroupMessage, params=None):
    response = requests.get(config["daily_news_api_key"], timeout=5)
    if response.status_code == 200:
        await post_group_file(message, response.url)
    else:
        await message.reply(content="\n出错了！请at开发者查询")
        logger.info(f"[error]：{response.status_code}")
    return True


def get_weather(city_name: str):
    weather_api_url = ("https://sapi.k780.com/?app=weather.today&cityNm=" + city_name +
                       f"&appkey={weather_apikey}&sign={weather_sign}&format=json")
    response = requests.get(url=weather_api_url, timeout=5)
    content_json_obj = response.json()
    return content_json_obj


@Commands("天气查询")
async def weather(message: GroupMessage, params):
    if params == "":
        await message.reply(content="\n请输入城市名称\n例如：/天气查询 北京")
        return True
    weather_json_obj = get_weather(params)
    if weather_json_obj["success"] == "1":
        weather_info = weather_json_obj["result"]
        send_info = f"\n{weather_info['days']} {weather_info['week']}" \
                    f"\n{weather_info['citynm']} {weather_info['api.yaml']}" \
                    f"\n当前温度：{weather_info['temperature_curr']}" \
                    f"\n湿度：{weather_info['humidity']}" \
                    f"\n风：{weather_info['wind'] + weather_info['winp']}" \
                    f"\npm2.5：{weather_info['aqi']}"

        await message.reply(content=send_info)
    else:
        await message.reply(content="\n出错了！请at开发者查询")
        logger.info(f"[error]：{weather_json_obj}")
    return True


@Commands("免费游戏")
async def free_game(message: GroupMessage, params=None):
    response = requests.get(config["epic_free_game_api_key"], timeout=5)
    if response.status_code == 200:
        data = response.json()["data"]
        send_info = ""
        for game in data:
            # f"\n{game['cover']}" \
            send_info += "\nEPIC免费游戏："\
                         f"\n游戏名：{game['title']}" \
                         f"\n原价：{game['original_price_desc']}" \
                         f"\n免费时间：{game['free_start']} - {game['free_end']}" \
                         f"\n当前是否免费：{game['is_free_now']}" \
                # f"\n链接：{game['link']}\n"
        await message.reply(content=send_info)
    return True


async def post_group_file(message: GroupMessage, file_url: str):
    try:
        uploadMedia = await message._api.post_group_file(
            group_openid=message.group_openid,
            file_type=1,  # 文件类型要对应上，具体支持的类型见方法说明
            url=file_url  # 文件Url
        )
        # 资源上传后，会得到Media，用于发送消息
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=7,  # 7表示富媒体类型
            msg_id=message.id,
            media=uploadMedia
        )
    except Exception as e:
        logger.info(f"[error]：{e}")
        await message.reply(content="\n出错了！请at “Angel丶葬爱”查询")
    return True


@Commands("壁纸")
async def wallpaper(message: GroupMessage, params):
    if params == "":
        response = requests.get(config["random_image_api_key"], timeout=5)
        if response.status_code == 200:
            await post_group_file(message, response.url)
    elif params == "福瑞":
        response = requests.get(config["furry_image_api_key"], timeout=5)
        if response.status_code == 200:
            await post_group_file(message, response.url)
    elif params == "表情包":
        response = requests.get(config["bq_image_api_key"], timeout=5)
        if response.status_code == 200:
            await post_group_file(message, response.url)
    elif params == "二次元":
        response = requests.get(config["acg_image_api_key"], timeout=5)
        if response.status_code == 200:
            await post_group_file(message, response.url)
    else:
        await message.reply(content="\n请输入指定壁纸类型："
                                    "\n壁纸 福瑞"
                                    "\n壁纸 表情包"
                                    "\n壁纸 二次元"
                            )
    return True


@Commands("华夏千秋")
async def huaxia(message: GroupMessage, params):
    if params == "种植":
        await message.reply(content="\n待开发")
    elif params == "养殖":
        await message.reply(content="\n待开发")
    elif params == "炼药":
        await message.reply(content="\n待开发")
    elif params == "挑战":
        await message.reply(content="\n待开发")
    elif params == "好感":
        await message.reply(content="\n待开发")
    else:
        await message.reply(content="\n请输入指定功能："
                                    "\n华夏千秋 种植"
                                    "\n华夏千秋 养殖"
                                    "\n华夏千秋 炼药"
                                    "\n华夏千秋 挑战"
                                    "\n华夏千秋 好感"
                            )
    return True
