from pydub import AudioSegment
from django.conf import settings

import whisper

class BaseVoiceRecognition:
    def __init__(self):
        self.model = whisper.load_model(settings.WHISPER_MODEL)

class WhisperVoiceRecognition(BaseVoiceRecognition):
    def __init__(self):
        super().__init__()

    def recognize(self, audio: AudioSegment) -> str:
        