import json
import os
import sys
import vosk
import wave
from pydub import AudioSegment

def recognize_speech(audio_file, model_path,content=None):
    # 打开音频文件
    wf = wave.open(audio_file, 'rb')

    # 创建Vosk识别器
    rec = vosk.KaldiRecognizer(vosk.Model(model_path), wf.getframerate())

    # 读取音频数据并进行识别
    while True:
        data = wf.readframes(4000)  # 每次读取一段音频数据
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):  # 使用AcceptWaveform方法传递音频数据
            result = rec.Result()
            #content.append(json.loads(rec.Result())['text'])
            print(result)  # 打印部分识别结果
        # else:
        #     print(rec.PartialResult())

    # 获取最终识别结果
    result = rec.FinalResult()
    print(result)
    #content.append(json.loads(rec.Result())['text']) # 打印最终识别结果

    # 关闭音频文件
    wf.close()


# 指定音频文件和语音模型路径
audio_file = 'path_to_audio_file.wav'
#model_path = 'C:\\tools\\model\\voice\\vosk\\vosk-model-small-cn-0.22'
model_path = 'C:\\tools\\model\\voice\\vosk\\vosk-model-cn-0.22'
#model_path = 'C:\\tools\\model\\voice\\vosk\\vosk-model-cn-kaldi-multicn-0.15'

# 调用识别函数



to_wav_file_path = "C:\\temp\\voice\\111.m4a"
#to_wav_file_path = "C:\\temp\\voice\\阿里云售后服务中心@95187_20230508154352.m4a"
wav_file = os.getcwd() + "\output.wav"

def to_wav(audio_file):

    # 加载音频文件
    audio = AudioSegment.from_file(audio_file)
    # 将音频保存为 WAV 格式
    audio.export(wav_file, format="wav")
    recognize_speech(wav_file, model_path)



def to_wav2(content):
    recognize_speech(wav_file, model_path,content)



if __name__ == '__main__':
    to_wav(to_wav_file_path)
    #recognize_speech(wav_file, model_path)
    #jiang_zao(wav_file)
    #bzh(wav_file)
