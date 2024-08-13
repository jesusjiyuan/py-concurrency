
python model_download.py --repo_id Qwen/Qwen-7B --mirror
python model_download.py --repo_id openai/whisper-tiny --mirror
---
# 新建chatglm环境
conda create -n whisper python==3.8
# 激活chatglm环境
conda activate chatglm
# 安装PyTorch环境
pip --trusted-host pypi.tuna.tsinghua.edu.cn install torch==1.10.1+cu102 torchvision==0.11.2+cu102 torchaudio==0.10.1 -f https://download.pytorch.org/whl/torch_stable.html
# 一键安装依赖包
pip install -U openai-whisper
# 执行tiny demo
whisper D:/11.mp4 --model tiny  --language Chinese

---

pip install git+https://github.com/m-bain/whisperx.git
pip install git+https://github.com/m-bain/whisperx.git --upgrade
torch>=2
torchaudio>=2
faster-whisper>=0.8
transformers
ffmpeg-python>=0.2
pandas
setuptools>=65
nltk

---

pip install faster-whisper -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
pip install -i https://mirrors.aliyun.com/pypi/simple moviepy



```
pip install --upgrade pip
pip install --upgrade transformers accelerate datasets[audio]
```