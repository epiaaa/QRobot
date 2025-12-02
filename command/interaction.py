import json
import os

from botpy import logging

from utils.path_utils import get_project_root

project_root = get_project_root()
with open(os.path.join(project_root, "user_data/person.json"), "r", encoding="utf-8") as f:
    user_data = json.load(f)
with open(os.path.join(project_root, "user_data/pet.json"), "r", encoding="utf-8") as f:
    pet_data = json.load(f)
_log = logging.get_logger()

def feeding(change: int):
    print("开始吃东西")
    changes_satiety(change)


as_time_passes()
while True:
    message = input("请输入信息：")
    if message == "q":
        break
    else:
        print(f"输入：{message}")
        print(f"回复：{pet_data}")
        continue
