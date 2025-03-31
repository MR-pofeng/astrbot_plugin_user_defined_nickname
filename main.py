from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.core import logger, LogManager, LogBroker
import os,json


@register("nickname", "MR_pofeng", "指令自定义nickname", "1.0.1")
class Plugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        cfg = context.get_config()
        dir = os.path.dirname(os.path.abspath(__file__))
        self.data = os.path.join(dir, "nickname.json")
        self.identifier = cfg["provider_settings"]["identifier"]
        self.id_Nickname = {}
        if not os.path.isfile(self.data):
            with open(self.data, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        with open(self.data, "r", encoding="utf-8") as f:
            self.id_Nickname = json.load(f)
    
    @filter.event_message_type(filter.EventMessageType.ALL)
    async def nickname_hook(self, event: AstrMessageEvent): 
        if self.identifier == False:
            return
        if event.message_obj.sender.user_id in self.id_Nickname:
            event.message_obj.sender.nickname = self.id_Nickname[event.message_obj.sender.user_id]
    
    @filter.command("nickname")
    async def nickname(self, event: AstrMessageEvent, message: str):
        uid= event.message_obj.sender.user_id
        yield event.plain_result(f"已将id为{uid}的用户昵称设置为: {message}")
        with open(self.data, "w", encoding="utf-8") as f:
            json.dump(self.id_Nickname, f, ensure_ascii=False, indent=4)
        self.id_Nickname[uid] = message

    @filter.command("nickname_list")
    async def nickname_list(self, event: AstrMessageEvent):
        yield event.plain_result(f"当前昵称列表为: {self.id_Nickname}")

    @filter.command("nickname_del")
    async def nickname_del(self, event: AstrMessageEvent):
        uid= event.message_obj.sender.user_id
        if uid in self.id_Nickname:
            del self.id_Nickname[uid]
            yield event.plain_result(f"已删除id为{uid}的用户昵称")
            with open(self.data, "w", encoding="utf-8") as f:
                json.dump(self.id_Nickname, f, ensure_ascii=False, indent=4)
        else:
            yield event.plain_result(f"未找到id为{uid}的用户昵称")

    async def terminate(self):
        with open(self.data, "w", encoding="utf-8") as f:
            json.dump(self.id_Nickname, f, ensure_ascii=False, indent=4)