from django.conf import settings
from pydub import AudioSegment

import whisper

model_name = settings.WHISPER_MODEL

class BaseVoiceRecognition:
    def recognize(self, audio):
        model = whisper.load_model(model_name)
        try:
            result = model.transcribe(audio)
            return result["text"]
        except Exception as e:
            return e
    
    def convert_ogg_to_mp3(audio_path):
        audio = AudioSegment.from_file(audio_path)
        audio.export("converted_audio.mp3", format="mp3")
        return "converted_audio.mp3"