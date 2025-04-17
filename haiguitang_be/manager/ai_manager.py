from ..config import service
from volcenginesdkarkruntime import Ark


# AI 调用 工具类
class AiManager:

    def do_chat(self, system_prompt: str, user_prompt: str):
        """
        准备聊天消息并发送给AI模型处理。
        :param system_prompt: 系统预设提示内容。
        :param user_prompt: 用户预设输入内容。
        :return: AI的回复内容。
        """
        # 可以对chat_message 进行类的封装
        chat_message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.do_chat_message_list(chat_message)

    def do_chat_message_list(self, chat_message_list):
        """
        处理聊天消息列表并调用AI模型生成回复。
        :param chat_message_list: 聊天消息列表。
        :return: AI的回复内容。
        """

        completion = service.bot_chat.completions.create(
            model="bot-20250316173849-89vzg",  # bot-20250316173849-89vzg 为您当前的智能体的ID，注意此处与Chat API存在差异。差异对比详见 SDK使用指南
            messages=chat_message_list,
        )
        if not completion.choices:
            raise RuntimeError("AI 没有返回任何内容")

        content = completion.choices[0].message.content
        # print(f"AI 返回内容：{content}")
        return content
