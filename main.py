from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import ProviderRequest
import re


@register("helloworld", "Soulter", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        cfg = context.get_config()
        self.identifier = cfg["provider_settings"]["identifier"]
    
    @filter.on_llm_request()
    async def my_custom_hook_1(self, event: AstrMessageEvent, req: ProviderRequest): # 请注意有三个参数
        if self.identifier == False:
            return
        id_Nickname = {'09DD9BAB91E61DD58E26AEE1848B573A':'狂风'}
        pattern = r"\[User ID: ([0-9A-F]+), Nickname: .*?\]"
        match = re.search(pattern, req.prompt['contents'][-1]['parts'][0]['text'])
        if match:
            user_id = match.group(1)
        if user_id in id_Nickname:
            nickname = id_Nickname[user_id]
            req.prompt['contents'][-1]['parts'][0]['text'] = req.prompt['contents'][-1]['parts'][0]['text'].replace(match.group(0), f"[User ID: {user_id}, Nickname: {nickname}]")