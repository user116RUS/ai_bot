import requests

from django.conf import settings

IMAGE_GEN_KEY = settings.IMAGE_GEN_KEY

class ImageGenAPI:
    def __init__(self):
        self.key = IMAGE_GEN_KEY
        self.width = 1024
        self.height = 1024
        self.steps = 25
        self.guidance = 7.5

    def generate_text_to_image(self, text, model):
        payload = {
            "prompt": text,
            "width": self.width,
            "height": self.height,
            "steps": self.steps,
            "guidance": self.guidance
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.key}"
        }
        
        return requests.post(model, json=payload, headers=headers)["url"]