import os
import subprocess
from django.conf import settings

import whisper
from bot import logger
model_name = settings.WHISPER_MODEL


class BaseVoiceRecognition:
    def recognize(self, audio):
        model = whisper.load_model(model_name)
        try:
            print("a")
            result = model.transcribe(audio)
            return result["text"]
        except Exception as e:
            return e


def convert_ogg_to_mp3(audio_path):
    from bot import logger

    mp3_path = os.path.splitext(audio_path)[0] + ".mp3"
    subprocess.run(["ffmpeg", "-i", audio_path, mp3_path])
    if os.path.exists(mp3_path):
        os.remove(audio_path)
        logger.info('audiofile converted to mp3')
        return mp3_path
    else:
        logger.error(f"Conversion of {audio_path} to mp3 failed.")
        return None
