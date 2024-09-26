from django.conf import settings

import base64
import os

import dotenv
import openai
import telebot

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY") if settings.PROVIDER_NAME == "openai" else os.getenv("VSEGPT_API_KEY")
openai.base_url = settings.PROVIDER

ASSISTANT_PROMPT = ()
ANALYTIC_PROMPT = ()

ERROR = "Извините, что-то пошло не так"


def encode_image(image):
    with open(image, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class BaseAIAPI:
    def __init__(self, ) -> None:
        self._MAX_TOKENS: int = 1000
        self._ASSISTANT_PROMPT: str = ASSISTANT_PROMPT
        self._ANALYTIC_PROMPT: str = ANALYTIC_PROMPT
        self.chat_history: dict = {}
        self._TEMPERATURE = 0.7

    def clear_chat_history(self, chat_id: int) -> None:
        self.chat_history.pop(chat_id)


class OpenAIAPI(BaseAIAPI):
    def __init__(self, ) -> None:
        super().__init__()

    def _get_or_create_user_chat_history(self, chat_id: int, new_user_image: str = "",
                                         new_user_message: str = "") -> list:
        if not self.chat_history.get(chat_id, False):
            self.chat_history[chat_id] = []
            self.chat_history[chat_id].append(
                {"role": "system", "content": self._ASSISTANT_PROMPT})
            if new_user_image != "":
                self.chat_history[chat_id].append(
                    {"role": "user", "content": [
                        {"type": "text", "text": new_user_message},
                        {"type": "image_url", "image_url": new_user_image}
                    ]})
                return self.chat_history[chat_id]
            elif new_user_image == "":
                self.chat_history[chat_id].append(
                    {"role": "user", "content": {"type": "text", "text": new_user_message}})
                return self.chat_history[chat_id]

        self.chat_history[chat_id].append(
            {"role": "user", "content": [
                {"type": "text", "text": new_user_message},
                {"type": "image_url", "image_url": new_user_image}
            ]})
        chat_history = self.chat_history[chat_id]
        return chat_history

    def get_response(self, chat_id: int, text: str, model: str, image: str = "") -> str:
        try:
            if image != "":
                base64_image = encode_image(image)
                user_chat_history = self._get_or_create_user_chat_history_to_work_with_images(chat_id, text,
                                                                                              base64_image)
            else:
                user_chat_history = self._get_or_create_user_chat_history_to_work_with_images(chat_id, text)
            response = (
                openai.chat.completions.create(
                    model=model,
                    messages=user_chat_history,
                    temperature=self._TEMPERATURE,
                    max_tokens=self._MAX_TOKENS,
                    stream=False
                ).choices[0].message.content
            )

            self.chat_history[chat_id].append({"role": "assistant", "content": response})
            return response

        except Exception as e:
            return ERROR
