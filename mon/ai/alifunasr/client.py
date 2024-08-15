import base64
import requests

url = "http://10.18.32.170:2002/"

def asr_damo_api(wav_path):
    headers = {'Content-Type': 'application/json'}
    with open(wav_path, "rb") as f:
        wav = base64.b64encode(f.read()).decode()
    data = {"wav": wav}
    response = requests.post(url+"asr", headers=headers, json=data)
    response = response.json()
    if response['code'] == 0:
        res = response['res']
        return res
    else:
        return response['msg']

if __name__ == '__main__':
    res = asr_damo_api("xxx/.cache/modelscope/hub/iic/SenseVoiceSmall/example/en.mp3")
    print(res)