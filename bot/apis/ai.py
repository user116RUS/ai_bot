import os

import dotenv
import openai

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

ASSISTANT_PROMPT = ("Ты ассистент помощник.")
ANALYTIC_PROMPT = ()

openai.base_url = "https://api.vsegpt.ru:6070/v1/"


class BaseAIAPI:
    def __init__(self, ) -> None:
        self._MAX_TOKENS: int = 1000
        self._ASSISTANT_PROMPT: str = ASSISTANT_PROMPT
        self.chat_history: dict = {}
        self._TEMPERATURE = 0.7

    def clear_chat_history(self, chat_id: int) -> None:
        self.chat_history.pop(chat_id)


class OpenAIAPI(BaseAIAPI):
    """API for working with https://vsegpt.ru/Docs/API"""

    def __init__(self, ) -> None:
        super().__init__()

    def _get_or_create_user_chat_history(self, chat_id: int, new_user_message: str = "") -> list:
        if not self.chat_history.get(chat_id, False):
            self.chat_history[chat_id] = []
            self.chat_history[chat_id].append({"role": "system", "content": self._ASSISTANT_PROMPT})
            self.chat_history[chat_id].append({"role": "user", "content": new_user_message})
            return self.chat_history[chat_id]

        self.chat_history[chat_id].append({"role": "user", "content": new_user_message})
        chat_history = self.chat_history[chat_id]
        return chat_history

    def get_response(self, chat_id: int, text: str, model: str) -> str:
        """
        Make request to AI and write answer to message_history.
        Usually working in chats with AI.
        """
        user_chat_history = self._get_or_create_user_chat_history(chat_id, text)

        try:
            response = (
                openai.chat.completions.create(
                    model=model,
                    messages=user_chat_history,
                    temperature=self._TEMPERATURE,
                    n=1,
                    max_tokens=self._MAX_TOKENS, ).choices[0].message.content
            )

            self.chat_history[chat_id].append({"role": "assistant", "content": response})
            return response

        except Exception as e:
            self.clear_chat_history(chat_id)
            return e

    def get_single_response(self, text: str, model: str, meta_prompt: str = ANALYTIC_PROMPT) -> str:
        """
        Get response from AI without message_history.
        Working with parsing payments.
        """
        try:
            response = (
                openai.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "assistant", "content": meta_prompt},
                        {"role": "user", "content": f'{text}'}, ],
                    temperature=self._TEMPERATURE,
                    n=1,
                    max_tokens=self._MAX_TOKENS + 1000,
                ).choices[0].message.content
            )
            return response

        except Exception as e:
            return e

'''
ai = OpenAIAPI()
print(ai.get_response(134, 'hi', 'cohere/command-r-08-2024'))'''
