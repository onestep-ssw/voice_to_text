import os

import handler.ui_handler as ui_handel

os.environ["ffmpeg"] = os.getcwd() + "/ffmpeg/ffmpeg-master-latest-win64-gpl/bin/"
model_path = os.getcwd() + "\\vosk-model-cn-0.22"




if __name__ == '__main__':
     ui_handel.main(model_path)

