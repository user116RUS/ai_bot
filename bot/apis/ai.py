import os

import telebot

import dotenv
import openai
import base64
import requests


dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


ASSISTANT_PROMPT = ()
ANALYTIC_PROMPT = ()

ERROR="Извините, что-то пошло не так"

def encode_image(image):
  with open(image, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

class BaseAIAPI:
    def __init__(self, ) -> None:
        self._CHAT_MODEL: str = "openai/gpt-4o-mini"  # "openai/gpt-4o-mini"
        self._ANALYTIC_MODEL: str = "openai/gpt-4o-mini"
        self._MAX_TOKENS: int = 1000
        self._ASSISTANT_PROMPT: str = ASSISTANT_PROMPT
        self._ANALYTIC_PROMPT: str = ANALYTIC_PROMPT
        self.chat_history: dict = {}
        self._TEMPERATURE = 0.7

    def clear_chat_history(self, chat_id: int) -> None:
        self.chat_history.pop(chat_id)

class OpenAIAPI(BaseAIAPI):
    def __init__(self,) -> None:
        super().__init__()
    
    def _get_or_create_user_chat_history(self, chat_id: int, new_user_message: str = "") -> list:
        """
        Retrieves or creates the chat history for a given user.

        Args:
            chat_id (int): The unique identifier for the user's chat.
            new_user_message (str): The new message from the user to be appended to the chat history. Defaults to an empty string.

        Returns:
            list: The updated chat history for the given user.
        """
        if not self.chat_history.get(chat_id, False):
            self.chat_history[chat_id] = []
            self.chat_history[chat_id].append(
                {"role": "system", "content": self._ASSISTANT_PROMPT})
            self.chat_history[chat_id].append(
                {"role": "user", "content": new_user_message})
            return self.chat_history[chat_id]

        self.chat_history[chat_id].append(
            {"role": "user", "content": new_user_message})
        chat_history = self.chat_history[chat_id]
        return chat_history
    def _get_or_create_user_chat_history_to_work_with_images(self, chat_id: int, new_user_message: str = "", new_user_image: str = "") -> list:
        if not self.chat_history.get(chat_id, False):
            self.chat_history[chat_id] = []
            self.chat_history[chat_id].append(
                {"role": "system", "content": self._ASSISTANT_PROMPT})
            self.chat_history[chat_id].append(
                {"role": "user", "content": [
                    {"type": "text", "text": new_user_message},
                    {"type": "image_url", "image_url": new_user_image}
                ]})
            return self.chat_history[chat_id]

        self.chat_history[chat_id].append(
            {"role": "user", content": [
                    {"type": "text", "text": new_user_message},
                    {"type": "image_url", "image_url": new_user_image}
                ]})
        chat_history = self.chat_history[chat_id]
        return chat_history
    
    def get_response_only_text(self, chat_id: int, text: str) -> str:
        user_chat_history = self._get_or_create_user_chat_history(
            chat_id, text)
        
        try:
            response = ( 
                openai.chat.completions.create(
                model=self._CHAT_MODEL,
                messages=user_chat_history,
                temperature=self._TEMPERATURE,
                max_tokens=self._MAX_TOKENS,
                stream=True
            ).choices[0].message.content
            )

            self.chat_history[chat_id].append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            return ERROR
    
    def get_response_image_plus_text(self, chat_id: int, image, text: str) -> str:
        try:
            user_chat_history = self._get_or_create_user_chat_history_to_work_with_images(chat_id, text, image)
            
            base64_image = encode_image(image)

            headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai.api_key}"
            }

            payload = {
            "model": "gpt-4o-mini",
            "messages": user_chat_history,
            "max_tokens": self._MAX_TOKENS
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()
            return response
        except Exception as e:
            return ERROR
