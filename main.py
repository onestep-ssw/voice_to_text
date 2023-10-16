import os

import handler.ui_handler as ui_handel


# 这里配置 就可以傻瓜式使用了
os.environ["ffmpeg"] = os.getcwd() + r"\ffmpeg-n6.0-latest-win64-lgpl-6.0\bin\ffmpeg.exe"
model_path = os.getcwd() + r"\vosk-model-cn-0.22"


if __name__ == '__main__':
    # set_en()
    ui_handel.main()
