
import wave

def truns_wav():
    input_file = r"D:\tmp\fm\FM985_202407221551.raw"
    with open(input_file, 'rb') as f:
        binary_data = f.read()

    # 创建音频对象
    audio = wave.open(r'D:\tmp\fm\FM985_202407221551.wav', 'wb')
    # 设置音频参数
    audio.setnchannels(1)  # 设置声道数为1
    audio.setsampwidth(2)  # 设置采样宽度为2字节（16位）
    audio.setframerate(44100)  # 设置采样率为44100Hz
    # 写入音频数据
    audio.writeframes(binary_data)
    # 关闭音频文件
    audio.close()

def truns_mp3():
    from pydub import AudioSegment

    # 读取WAV文件
    audio = AudioSegment.from_file(r'D:\tmp\fm\audio_file.wav', format='wav')
    # 将WAV文件转换为MP3格式
    audio.export(r'D:\tmp\fm\audio_file.mp3', format='mp3')



import wave
import struct
from pydub import AudioSegment

def binary_to_wav(binary_file, wav_file, channels=1, sample_width=2, frame_rate=44100):
    # 读取二进制数据
    with open(binary_file, 'rb') as f:
        binary_data = f.read()

    # 创建 WAV 文件
    wav = wave.open(wav_file, 'wb')
    wav.setnchannels(channels)
    wav.setsampwidth(sample_width)
    wav.setframerate(frame_rate)

    # 将二进制数据转换为音频样本并写入 WAV 文件
    for i in range(0, len(binary_data), sample_width):
        sample = struct.unpack('<h', binary_data[i:i + sample_width])[0]
        wav.writeframes(struct.pack('<h', sample))

    wav.close()

def wav_to_mp3(wav_file, mp3_file):
    audio = AudioSegment.from_file(wav_file, format='wav')
    audio.export(mp3_file, format='mp3')

# 示例用法
binary_file = r"D:\tmp\fm\FM985_202407200852.raw"
wav_file = r"D:\tmp\fm\audio_file1.wav"
mp3_file = 'output.mp3'


#truns_mp3()
truns_wav()
#binary_to_wav(binary_file, wav_file)
#wav_to_mp3(wav_file, mp3_file)