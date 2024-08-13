
import websockets
import asyncio
from datetime import datetime
import json
#
# # 连接WebSocket服务器并进行消息处理的异步函数
# async def websocket_handler(uri):
#     async with websockets.connect(uri) as websocket:
#         # 订阅消息
#         sub_message = {
#             "type": "subscribe",
#             "data": {
#                 "type": "whisper"
#             }
#         }
#         await websocket.send(json.dumps(sub_message))
#         print("Subscribed to whispers")
#
#         # 接收并处理消息
#         while True:
#             message = await websocket.recv()
#             message_data = json.loads(message)
#             if message_data.get('type') == 'whisper':
#                 print(f"Received whisper at {datetime.now()}: {message_data['data']['message']}")
#                 # 将语音转文字逻辑放在这里
#
# # 运行WebSocket客户端
# start_uri = "ws://localhost:8888/myws"
# asyncio.get_event_loop().run_until_complete(websocket_handler(start_uri))
#
#

import asyncio
import websockets

async def websocket_server(websocket, path):
    # 接收客户端消息
    message = await websocket.recv()
    print(f"Received message: {message}")

    # 向客户端发送消息
    response = "Hello from server!"
    await websocket.send(response)

start_server = websockets.serve(websocket_server, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()