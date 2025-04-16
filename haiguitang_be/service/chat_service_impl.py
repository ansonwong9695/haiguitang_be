from ..manager.ai_manager import AiManager
from typing import Dict, List


class ChatServiceImpl:
    ai_manager = AiManager()
    # 全局消息映射
    global_message_dict: Dict[int, list] = {}

    def do_chat_service(self, room_id: int, message: str) -> str:

        # 系统预设
        system_prompt = """
        1. 提供一道海龟汤谜题的“汤面”（故事表面描述）。
        2. 根据玩家的提问，仅回答“是”、“否”或“与此无关”。
        3. 在特定情况下结束游戏并揭示“汤底”（故事真相）。

        游戏流程
        1. 当玩家输入“开始”时，你需立即提供一道海龟汤谜题的“汤面”。
        2. 玩家会依次提问，你只能回答以下三种之一：
        ○ 是：玩家的猜测与真相相符。
        ○ 否：玩家的猜测与真相不符。
        ○ 与此无关：玩家的猜测与真相无直接关联。
        3. 在以下情况下，你需要主动结束游戏并揭示“汤底”：
        ○ 玩家明确表示“不想玩了”、“想要答案”或类似表达。
        ○ 玩家几乎已经还原故事真相，或所有关键问题都已询问完毕。
        ○ 玩家输入“退出”。
        ○ 玩家连续提问 10 次仍未触及关键信息，或表现出完全无头绪的状态。

        注意事项
        1. 汤面设计：谜题应简短、有趣且逻辑严密，答案需出人意料但合理。
        2. 回答限制：严格遵守“是”、“否”或“与此无关”的回答规则，不得提供额外提示。
        3. 结束时机：在符合结束条件时，及时揭示“汤底”，避免玩家陷入无效推理。
        4. 当你决定结束时，必须在结束的消息中包含【游戏已结束】

        示例
        ● 玩家输入：“开始”
        ● AI 回复（汤面）：
        “一个人走进餐厅，点了一碗海龟汤，喝了一口后突然冲出餐厅自杀了。为什么？”
        ● 玩家提问：“他是因为汤太难喝了吗？”
        ● AI 回复：“否。”
        ● 玩家提问：“他认识餐厅里的人吗？”
        ● AI 回复：“与此无关。”
        ● 玩家输入：“退出。”
        ● AI 回复（汤底）：
        “这个人曾和同伴在海上遇难，同伴死后，他靠吃同伴的尸体活了下来。餐厅的海龟汤让他意识到自己吃的其实是人肉，因此崩溃自杀。”
        """

        # 1.准备消息列表
        system_message = {"role": "system", "content": system_prompt}
        user_message = {"role": "user", "content": message}
        chat_messasges = [system_message, user_message]

        # 首次开始时，需要初始化消息列表，并且额外添加系统消息到记录中
        # 优化空间，应该再写个函数，遍历 当前 chat_messages 里面有没有 开始游戏，如果 开始了游戏，用户再次开始是不被允许的
        # 防止用户在游戏没开始时候，乱输入
        if message != "开始" and room_id not in self.global_message_dict:
            raise RuntimeError("请开始游戏")
        # 游戏开始，创建房间
        elif message == "开始" and room_id not in self.global_message_dict:
            self.global_message_dict[room_id] = chat_messasges
        else:
            self.global_message_dict[room_id].append(user_message)

        # 2.调用api
        answer = self.ai_manager.do_chat_message_list(chat_messasges)
        assistant_message = {"role": "assistant", "content": answer}
        self.global_message_dict[room_id].append(assistant_message)

        # 3.返回结果
        if "【游戏已结束】" in answer:
            # 清理当前房间的消息记录
            del self.global_message_dict[room_id]

        return answer

    def get_chat_room_list(self):
        chat_list = []
        for room_id, chat_messages in self.global_message_dict.items():
            chat_list.append({"room_id": room_id, "chat_history": chat_messages})
        return chat_list
