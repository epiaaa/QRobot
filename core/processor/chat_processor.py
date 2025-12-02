import datetime
import os

from botpy.message import GroupMessage

from core import People
from core.llm import VolcengineChat
from utils import get_root_path, additional_text, json_to_class

root_path = get_root_path()
person_data_path = os.path.join(root_path, "data/user_data/test.json")

"""
示例    
{
    "type": "function",
    "function": {
        "name": "update_favorability",
        "description": "获取指定城市天气",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "城市名称"}},
            "required": ["city"]
        }
    }
}
"""


tools = [
    {
        "type": "function",
        "function": {
            "name": "add_person",
            "description": "添加新朋友或者更改人物名字",
            "parameters": {
                "type": "object",
                "properties": {
                    "uid": {
                        "type": "string",
                        "description": "人物ID"
                    },
                    "name": {
                        "type": "str",
                        "description": "人物姓名"
                    }
                },
                "required": ["uid", "name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_favorability",
            "description": "更新与某人的好感度",
            "parameters": {
                "type": "object",
                "properties": {
                    "uid": {
                        "type": "string",
                        "description": "人物ID"
                    },
                    "change": {
                        "type": "int",
                        "description": "好感度改变值[-10 ~ 10]"
                    }
                },
                "required": ["uid", "change"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市天气",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "城市名称"}},
                "required": ["city"]
            }
        }
    }
]


class ChatProcessor:
    def __init__(self, config):
        self.people = json_to_class(person_data_path, People)  # 存储所有人物
        self.conversation_history = {}  # 存储与每个人的对话历史
        self.conversation = {}
        self.function_list = [
            "update_favorability",
            "add_person_name",
        ]

        # with open(person_data_path, "r", encoding="utf-8") as f:
        #     data = json.load(f)
        # for user_id, person in data.items():
        #     # -----------此段有大问题
        #     try:
        #         with open(f"history/{user_id}/{datetime.date.today()}.json", "r", encoding="utf-8") as f:
        #             chat_history = json.load(f)
        #             self.conversation_history[user_id] = chat_history
        #     except:
        #         self.conversation_history[user_id] = []
        #     # ----------------
        self.chat_ai = VolcengineChat(config)

    def chat(self, message: GroupMessage) -> dict:
        """
        聊天
        :param message:
        :return: 回复内容/错误信息
        """
        user_id = message.author.member_openid
        person = self.people.get_person(user_id)
        if person is None:
            self.people.add_person(uid=user_id)
            person = self.people.get_person(user_id)

        name = person.name
        time = message.timestamp
        chat_input = f"[{time}] {name}: {message.content}"

        try:
            content = self.chat_ai.chat(chat_input)
            # chat_history = self.get_conversation_history(user_id)
            # chat_history.append({"role": "user", "content": chat_input})
            # chat_history.append({"role": "assistant", "content": content})

            # self.analyzer_ai.chat_analysis(chat_history, self.function_list)

            path = f"data/chat_history/"
            current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
            additional_text(f"{path}/{user_id}/{datetime.date.today()}.txt",
                            f"{chat_input}\n[{current_time}] 阿狸: {content}"
                            )
            additional_text(f"{path}/{datetime.date.today()}.txt",
                            f"{chat_input}\n[{current_time}] 阿狸: {content}"
                            )
        except Exception as e:
            return {"success": "0", "content": "出错了！请at “Angel丶葬爱”", "error": str(e)}
        return {"success": "1", "content": content}

