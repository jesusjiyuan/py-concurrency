import websocket
import base64

def on_message(ws, message):
    print("收到消息:", message)

def on_error(ws, error):
    print("出现错误:", error)

def on_close(ws,ws1,ws2):
    print("WebSocket连接已关闭")

def on_open(ws):
    print("WebSocket连接已打开")
    # 读取音频流
    with open("test.wav","rb") as f:
        data = f.read()
        # encoded_string = base64.b64encode(f.read())
        print(f"读取到的文件长度是: {len(data)}")
        ws.send(data)
        print("================================")
        ws.send(data,opcode=websocket.ABNF.OPCODE_BINARY)
    # 发送数据
    # ws.send("Hello, WebSocket!")

if __name__ == "__main__":
    websocket.enableTrace(False)  # 启用调试信息
    ws = websocket.WebSocketApp("ws://127.0.0.1:7880/myws",  # WebSocket接口地址
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()  # 保持WebSocket连接