import json
import tempfile
import wave

import vosk
from pydub import AudioSegment
import main

model_path = main.model_path


def to_wav(widget, path):
    suffix = path.split(".")[-1].lower()
    if suffix == "wav":
        recognize_speech(path, model_path, widget)
    else:
        temp = tempfile.TemporaryFile()
        # # # 将音频保存为 WAV 格式
        try:
            audio = AudioSegment.from_file(path)
            audio.export(temp, format="wav")
            recognize_speech(temp, model_path, widget)
        finally:
            temp.close()


def recognize_speech(audio_file, model_path, widget=None):
    # 打开音频文件
    wf = wave.open(audio_file, 'rb')
    # 创建Vosk识别器
    rec = vosk.KaldiRecognizer(vosk.Model(model_path), wf.getframerate())
    # 读取音频数据并进行识别
    while True:
        frames = wf.readframes(4000)  # 每次读取一段音频数据
        if len(frames) == 0:
            break

        if rec.AcceptWaveform(frames):  # 使用AcceptWaveform方法传递音频数据
            str1 = json.loads(rec.Result())['text'].replace(" ", "")
            widget.ui.content_text.append(str1)
            widget.ui.content_text.append("\n")
            # print(result)  # 打印部分识别结果
        else:
            pass
    # 获取最终识别结果
    widget.ui.content_text.append(json.loads(rec.Result())['text'].replace(" ", ""))  # 打印最终识别结果
    widget.titleChange(widget.path_name+"（完成）")
    # 关闭音频文件
    wf.close()
