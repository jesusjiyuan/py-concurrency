import os
import tempfile
import threading
import wave
from datetime import time

import pyaudio
import websocket
from faster_whisper import WhisperModel

# 定义音频缓冲时间
audio_buffer = 5

# 录制音频并保存为临时文件的函数
def record_audio(p, device):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        filename = f.name
        wave_file = wave.open(filename, "wb")
        wave_file.setnchannels(device["maxInputChannels"])
        wave_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(int(device["defaultSampleRate"]))

        def callback(in_data, frame_count, time_info, status):
            """写入音频数据并返回 pa 标志"""
            wave_file.writeframes(in_data)
            return (in_data, pyaudio.paContinue)

        stream = p.open(
            format=pyaudio.paInt16,
            channels=device["maxInputChannels"],
            rate=int(device["defaultSampleRate"]),
            frames_per_buffer=pyaudio.get_sample_size(pyaudio.paInt16),
            input=True,
            input_device_index=device["index"],
            stream_callback=callback,
        )
        try:
            time.sleep(audio_buffer)  # 阻塞执行，确保录制足够的音频时间
        finally:
            stream.stop_stream()
            stream.close()
            wave_file.close()
    return filename

# 使用 whisper 模型对音频进行转录的函数
def whisper_audio(filename, model):
    segments, info = model.transcribe(filename, beam_size=5, language="zh", vad_filter=True, vad_parameters=dict(min_silence_duration_ms=1000))
    for segment in segments:
        print("(%.2fs->%.2fs) %s" % (segment.start, segment.end, segment.text))

# 示例用法
model_size = "large-v3"
path = r"d:\project\python_project\fasterwhisper\large-v3"  # 替换为你的模型路径
model = WhisperModel(model_size_or_path=path, device="cuda", local_files_only=True)

p = pyaudio.PyAudio()
device = p.get_default_output_device_info()  # 获取默认输出设备信息

# 启动音频录制线程
thread = threading.Thread(target=record_audio, args=(p, device))
thread.start()

# 等待音频录制完成
thread.join()

# 获取录制的文件名并进行语音转文字
filename = record_audio(p, device)
whisper_audio(filename, model)

p.terminate()  # 关闭 PyAudio