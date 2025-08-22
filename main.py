from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import *
from astrbot.api.event import filter, AstrMessageEvent
import os
import re
import aiohttp
import json
from typing import List

@register(
    name="zidingyi",
    author="溜溜球",
    desc="发送'资助'或'为爱发电'来获取图片",
    version="1.0.0"
)
class custommenu(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("资助", alias=['为爱发电'])
    async def custommenu(self, event: AstrMessageEvent):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        menu_dir = os.path.join(base_dir, "caidan")

        if not os.path.exists(menu_dir) or not os.path.isdir(menu_dir):
            logger.info(f"caidan文件夹不存在或不是一个有效的目录，尝试创建: {menu_dir}")
            try:
                os.makedirs(menu_dir, exist_ok=True)
                logger.info(f"caidan文件夹已成功创建: {menu_dir}")
            except Exception as e:
                logger.error(f"无法创建caidan文件夹: {menu_dir}, 错误信息: {e}")
                return

        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        image_paths = [
            os.path.join(menu_dir, f)
            for f in os.listdir(menu_dir)
            if os.path.isfile(os.path.join(menu_dir, f)) and os.path.splitext(f)[1].lower() in image_extensions
        ]

        if not image_paths:
            logger.warning(f"caidan文件夹中没有找到任何图片: {menu_dir}")
            return

        batch_size = 100

        for i in range(0, len(image_paths), batch_size):
            batch_paths = image_paths[i:i + batch_size]
            nodes_list = []

            for idx, path in enumerate(batch_paths):
                if not os.path.exists(path):
                    logger.info(f"图片不存在: {path}")
                    continue

                nickname = f"为爱发电"

                image = Image.fromFileSystem(path)
                logger.debug(f"成功加载图片: {path}")

                node = Node(
                    name=nickname,
                    content=[image]
                )
                nodes_list.append(node)

            if nodes_list:
                nodes = Nodes(nodes=nodes_list)
                yield event.chain_result([nodes])
            else:
                yield event.plain_result("发送失败，请检查caidan文件夹中的图片。")