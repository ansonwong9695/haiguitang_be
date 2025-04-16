from ninja import NinjaAPI, Schema
from typing import List
from .service.chat_service_impl import ChatServiceImpl

api = NinjaAPI(title="Anson 海龟汤的 API", version="1.0.0")

# 实例化 ChatServiceImpl
chat_service = ChatServiceImpl()


# 定义请求和响应的 Schema
class MessageRequest(Schema):
    message: str


class ChatHistoryResponse(Schema):
    room_id: int
    chat_history: list


# 发送消息接口
@api.post("/chat/{room_id}/send", summary="发送消息")
def send_message(request, room_id: int, payload: MessageRequest):
    try:
        print(payload.message)
        response = chat_service.do_chat_service(room_id, payload.message)
        return {"response": response}
    except RuntimeError as e:
        return {"error": str(e)}


# 获取房间聊天记录接口
@api.get(
    "/chat/rooms", response=List[ChatHistoryResponse], summary="获取所有房间的聊天记录"
)
def get_chat_rooms(request):
    chat_list = chat_service.get_chat_room_list()
    print(chat_list)
    return chat_list
