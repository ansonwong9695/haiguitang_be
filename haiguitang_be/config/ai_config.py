import os
from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark

# 加载环境变量
load_dotenv()


def get_ark_service():
    """
    初始化并返回 ArkService 实例
    """
    api_key = os.environ.get("ARK_API_KEY")  # 从环境变量中获取 API Key
    if not api_key:
        raise ValueError("ARK_API_KEY is not set in environment variables")

    base_url = "https://ark.cn-beijing.volces.com/api/v3"  # 默认路径
    return Ark(api_key=api_key, base_url=base_url)


# 初始化 service 实例
service = get_ark_service()
