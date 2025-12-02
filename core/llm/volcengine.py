from typing import Dict

from botpy import logging
from openai import OpenAI

logger = logging.get_logger()


class VolcengineChat:
    def __init__(self, conf: Dict):
        self.llm_conf = conf
        self.params = self.llm_conf["params"]

        api_key = self.params["api_key"]
        base_url = "https://ark.cn-beijing.volces.com/api/v3"
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        content = self.llm_conf["system_messages"]
        memory = self.llm_conf["memory_file"]
        if memory:
            content += f"这是你以往的认知：{memory}"
        self.message = [{"role": "system", "content": content}]

    def chat(self, message):
        """
        与AI聊天
        :param message: 传入信息
        :return: 返回信息
        """
        self.message.append({"role": "user", "content": message})
        response = self.client.chat.completions.create(
            model=self.params["model"],
            messages=self.message,
        )
        content = response.choices[0].message.content
        self.message.append({"role": "assistant", "content": content})
        return content


class VolcengineFunctionCall:
    def __init__(self, conf: Dict):
        self.llm_conf = conf
        self.params = self.llm_conf["params"]
        api_key = self.params["api_key"]
        base_url = "https://ark.cn-beijing.volces.com/api/v3"
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.message = [{"role": "system", "content": self.llm_conf["system_messages"]}]

    def function_call(self, message, tools):
        """
        调用函数
        :param message: 对话信息
        :param tools:
        :return: 函数结果
        """
        model = self.params.model
        response = self.client.chat.completions.create(
            model=model,
            messages=message,
            tools=tools,
            parallel_tool_calls=True,
        )
        return response

