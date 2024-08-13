import os

import requests


def upfile(file_path):
    url = "http://127.0.0.1:18005/upload/"

    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f)}
            response = requests.post(url, files=files)
        if response.status_code == 200:
            print(response.json())
            return True
        else:
            print(f"Request failed with status code {response.status_code}")
            return False
    except Exception as e:
        print(e)
        return False


def download(fileName):
    url = "http://127.0.0.1:18005/download/{}".format(fileName)
    try:
        res = requests.get(url)
        if res.status_code == 200:
            with open(fileName, 'wb') as w:
                w.write(res.content)
            return True
        else:

            return False
    except Exception as e:
        print(e)
        return False


def main():
    file_path = r"d:\tmp\image.png"

    upfile(file_path)
    fileName = os.path.basename(file_path)
    print('待下载的文件名字：'.format(fileName))
    ret = download(fileName)
    if ret:
        print('下载成功：' + fileName)
    else:
        print('下载失败：' + fileName)


if __name__ == "__main__":
    main()
