from dataclasses import field
from pathlib import Path
from typing import ClassVar, List

from botpy import logging
from pydantic import BaseModel, RootModel

logger = logging.get_logger()


class Person(BaseModel):
    uid: str = ""
    name: str = "未知"
    aliases: List[str] = field(default_factory=list)
    relation: str = "陌生人"
    affection: int = 0

    FIELD_NAME_MAP: ClassVar[dict] = {
        "uid": "UID",
        "aliases": "别名",
        "name": "名字",
        "relation": "关系",
        "affection": "好感度",
    }

    @classmethod
    def get_field_chinese_name(cls, field_name: str) -> str:
        """根据英文字段名获取中文名称"""
        return cls.FIELD_NAME_MAP.get(field_name, field_name)

    def update(self, **kwargs):
        """更新实例属性"""
        for key, value in kwargs.items():
            if hasattr(self, key):  # 确保属性存在
                setattr(self, key, value)
            else:
                raise ValueError(f"不支持的字段：{key}")

    def __str__(self):
        return (f"UID：{self.uid}\n"
                f"别名：{self.aliases}\n"
                f"名字：{self.name}\n"
                f"关系：{self.relation}\n"
                f"好感度：{self.affection}")


class People(RootModel):
    root: List[Person]

    def get_person(self, uid: str) -> Person:
        """根据UID获取用户信息"""
        for person in self.root:
            if person.uid == uid:
                return person
        return None

    def update_person(self, uid: str, **kwargs) -> None:
        """更新指定用户的信息"""
        person = self.get_person(uid)
        if person:
            logger.info(f"更新用户信息：\n{person}")
            person.update(**kwargs)
        else:
            logger.warn(f"更新 {self.root} 信息：未找到")

    def add_person(self, **kwargs) -> None:
        if "uid" in kwargs:
            person = self.get_person(kwargs["uid"])
            if person:
                logger.warn(f"存在用户：{kwargs['uid']}")
                return
        person = Person(**kwargs)
        self.root.append(person)

    def save_to_json(self, output_path: str) -> None:
        json_str = self.model_dump_json(indent=2)
        Path(output_path).write_text(json_str, encoding="utf-8")

