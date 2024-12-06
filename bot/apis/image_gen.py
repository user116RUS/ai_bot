import json
import requests
import time

from django.conf import settings

GETIMG_AI_KEY = settings.GETIMG_AI_KEY
URL_FUSION = settings.URL_FUSION
FUSION_API_KEY = settings.FUSION_API_KEY
FUSION_SECRET_KEY = settings.FUSION_SECRET_KEY

class ImageGenAPI:
    def __init__(self):
        self.key = GETIMG_AI_KEY
        self.width = 1024
        self.height = 1024
        self.steps = 25
        self.guidance = 7.5
        self.num_of_images_fusion = 1
        self.delay = 5
        self.attempts = 6
        self.url = URL_FUSION
        self.auth_headers = {
            'X-Key': f'Key {FUSION_API_KEY}',
            'X-Secret': f'Secret {FUSION_SECRET_KEY}',
        }

    def generate_text_to_image(self, text, model) -> str:
        payload = {
            "prompt": text,
            "width": self.width,
            "height": self.height,
            "steps": self.steps,
            "guidance": self.guidance,
            "response_format": "url"
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.key}"
        }
        
        response = requests.post(model, json=payload, headers=headers)

        return response
    
    def generate_image_fusion(self, text) -> str:
        model_name = requests.get(self.url + 'key/api/v1/models', headers=self.auth_headers).json()[0]["id"]
        
        params = {
            "type": "GENERATE",
            "numImages": self.num_of_images_fusion,
            "width": self.width,
            "height": self.height,
            "generateParams": {
                "query": f"{text}"
            }
        }

        data = {
            'model_id': (None, model_name),
            'params': (None, json.dumps(params), 'application/json')
        }
        response_id = requests.post(self.url + 'key/api/v1/text2image/run', headers=self.auth_headers, files=data).json()['uuid']

        start_time = int(time.time() // 60)
        while self.attempts > 0:
            response = requests.get(self.url + 'key/api/v1/text2image/status/' + response_id, headers=self.auth_headers)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            if int(time.time() // 60) > start_time:
                return None
