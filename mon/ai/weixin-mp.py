import requests
import os

def get_access_token(app_id, app_secret):
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    response = requests.get(url)
    return response.json().get('access_token')

def create_wxa_code(access_token, path='qrcode.png', width=430):
    url = f"https://api.weixin.qq.com/wxa/getwxacode?access_token={access_token}"
    data = {
        'path': path,
        'width': width
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        with open('qrcode.png', 'wb') as f:
            f.write(response.content)
        return 'qrcode.png'
    return None

# 替换成你的AppID和AppSecret
app_id = 'YOUR_APP_ID'
app_secret = 'YOUR_APP_SECRET'

access_token = get_access_token(app_id, app_secret)
qrcode_path = create_wxa_code(access_token)

print(f"小程序码已生成在 {qrcode_path}")