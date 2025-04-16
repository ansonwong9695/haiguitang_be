import pytest

# from haiguitang_be.manager.ai_manager import AiManager
from manager.ai_manager import AiManager


def test_do_chat_with_real_service():
    # 初始化 AiManager 实例
    ai_manager = AiManager()

    # 调用 do_chat 方法
    system_prompt = "你是一个程序员大佬。"
    user_prompt = "帮我写一个hello world ,python程序"
    response = ai_manager.do_chat(system_prompt, user_prompt)

    # 验证返回值是否为非空字符串
    assert isinstance(response, str)
    assert len(response) > 0
    print(response)
