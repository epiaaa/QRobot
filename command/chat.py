import base64
import os
import re

import pilk
import requests
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.ext.command_util import Commands
from botpy.message import GroupMessage

from core.processor.chat_processor import ChatProcessor
from utils import get_root_path


project_root = get_root_path()
ai_conf = read(os.path.join(project_root, "config/llm/volcengine_chat.yaml"))
logger = logging.get_logger()
chat_manager = ChatProcessor(ai_conf)


@Commands("chat")
async def chat(message: GroupMessage, params):
    response = chat_manager.chat(message)
    if response["success"] == "1":
        content = response["content"]
        await message.reply(content=content)
        logger.info(f"回复{message.author.member_openid}信息：{content}")
    else:
        content = "出错了！请at “Angel丶葬爱”"
        await message.reply(content=content)
        logger.info(f"[error]：{response}")
    return True


@Commands("语音聊天")
async def voice_chat(message: GroupMessage, params):
    response = chat_manager.chat(message)
    if response["success"] == "1":
        content = response["content"]
        logger.info(f"回复{message.author.member_openid}信息：{content}")

        result = re.sub(r'（.*?）', '', content)
        url = "http://localhost:9880/"
        params = {
            "text": result,  # 目标文本
            "text_language": "zh"  # 目标文本语种（zh/en/ja/ko等）
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            with open("test/output.wav", "wb") as f:
                f.write(response.content)
            output = "test/output.silk"
            pilk.encode("test/output.wav", output, pcm_rate=32000, tencent=True)
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
            return True
    content = "出错了！请at “Angel丶葬爱”"
    await message.reply(content=content)
    logger.info(f"[error]：{response}")
    return True
