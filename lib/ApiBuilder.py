import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


class ApiBuilder:

    @staticmethod
    def ChatCompletion(msg: list[dict]):
        return openai.ChatCompletion.create(
            messages=msg,
            **vars(default_config.chatCompletionConfig)
        )

    @staticmethod
    def Image(prompt: str):
        res = openai.Image.create(
            prompt=prompt,
            **vars(default_config.imageConfig)
        )
        return res
