import threading

import openai

lock = threading.Lock


class ApiBuilder:

    @staticmethod
    def ChatCompletion(openai_key, msg, chatCompletionConfig):
        openai.api_key = openai_key
        return openai.ChatCompletion.create(
            messages=msg,
            **vars(chatCompletionConfig)
        )

    @staticmethod
    def Image(openai_key, prompt, imageConfig):
        with lock:
            openai.api_key = openai_key
            return openai.Image.create(
                prompt=prompt,
                **vars(imageConfig)
            )
