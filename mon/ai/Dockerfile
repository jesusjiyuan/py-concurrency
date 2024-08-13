# 使用适合ARM的基础镜像
FROM arm64v8/ubuntu:latest

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN apt-get update && apt-get install -y \
    curl \
    openssl \
    python3-dev \
    python3-pip \
    build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHON_VERSION=3.9.19

RUN curl -O https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz \
    && tar -xf Python-${PYTHON_VERSION}.tar.xz \
    && rm Python-${PYTHON_VERSION}.tar.xz

WORKDIR Python-${PYTHON_VERSION}
RUN ./configure --enable-optimizations --prefix=/usr/local/python3 \
    && make -j$(nproc) \
    && make install

ENV PATH="/usr/local/python3/bin:${PATH}"
SHELL ["/bin/bash","-c"]

RUN pip3 install --upgrade pip -i http://pypi.tuna.tsinghua.edu.cn/simple/ \
    && pip3 install -U openai-whisper -i http://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn \
    && pip3 install moviepy -i http://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
#docker build -t arm64/ubuntu:jiyuan .
#docker buildx build --platform linux/arm64 -t arm64/ubuntu:jiyuan . --load