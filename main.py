# -*- coding: utf-8 -*-
import base64
import os
import pilk

import botpy
from botpy import logging
from botpy.ext.command_util import Commands
from botpy.message import GroupMessage
from botpy.ext.cog_yaml import read
from botpy.types.message import MarkdownPayload

from command import handlers

logger = logging.get_logger()
config = read(os.path.join(os.path.dirname(__file__), "config/api/api.yaml"))
appid = config["appid"]
secret = config["secret"]


@Commands("test")
async def test(message: GroupMessage, params=None):
    try:
        output = "test/output.silk"

        pilk.encode("test/test.wav", output, pcm_rate=32000, tencent=True)
        with open(output, "rb") as f:
            file_content = f.read()
            file_base64 = base64.b64encode(file_content).decode("utf-8")

        uploadMedia = await message._api.post_group_file(
            group_openid=message.group_openid,
            file_type=3,  # 文件类型要对应上，具体支持的类型见方法说明
            file_data=file_base64
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

handlers.append(test)

class MyClient(botpy.Client):
    # async def handle_send_markdown(self, group_id, msg_id):
    #     markdown = MarkdownPayload(content="# 测试 \n## test")
    #     await self.api.post_group_message(group_openid=group_id, markdown=markdown, msg_id=msg_id)

    async def on_group_at_message_create(self, message: GroupMessage):
        # username = message.author
        # print(f"获取到群内用户名：{username}")
        for handler in handlers:
            if await handler(message=message):
                logger.info(f"回复{message.author.member_openid}信息：{handler.__name__}")
                return
        await message.reply(content="\n【⭐菜单】"
                                    "\n├💳每日打卡"
                                    "\n├💬每日一言"
                                    "\n├📰每日新闻"
                                    "\n├🌥天气查询"
                                    "\n├🎮免费游戏"
                                    "\n└🖼壁纸"
                            )
        # await self.handle_send_markdown(group_id=message.group_openid, msg_id=message.id)
        logger.info(f"回复{message.author.member_openid}：菜单")


if __name__ == "__main__":

    intents = botpy.Intents(public_messages=True, direct_message=True)
    client = MyClient(intents=intents)
    client.run(appid=appid, secret=secret)

