import json
import tempfile
import wave
import traceback
import os
import vosk
import main
import subprocess
model_path = main.model_path


def to_wav(widget, path):
    suffix = path.split(".")[-1].lower()
    if suffix == "wav":
        recognize_speech(path, model_path, widget)
    else:

        # # # 将音频保存为 WAV 格式
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp:
            output_file = temp.name
        try:
            # 检查输出文件是否存在，如果存在则删除
            if os.path.exists(output_file):
                os.remove(output_file)

            # audio = pydub.AudioSegment.from_file(path)
            # audio.export(temp, format="wav")
            # 在程序运行时添加环境和设置都招不到ffmpeg的环境 所以用下面的方式进行转换
            ffmpeg_exe = os.environ["ffmpeg"]
            print(ffmpeg_exe)
            subprocess.run([ffmpeg_exe, "-i", path, output_file])
            recognize_speech(output_file, model_path, widget)
        except Exception as e:
            widget.titleChange(widget.path_name + "（语音转换出错）")
            traceback.print_exc()
        finally:
            temp.close()
            # 如果关闭之后没有删除就手动删除
            if os.path.exists(output_file):
                os.remove(output_file)


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
    widget.titleChange(widget.path_name + "（完成）")
    # 关闭音频文件
    wf.close()
