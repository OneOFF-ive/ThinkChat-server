class ApiBuilder:

    @staticmethod
    def ChatCompletion(openai, msg, chatCompletionConfig):
        return openai.ChatCompletion.create(
            messages=msg,
            **vars(chatCompletionConfig)
        )

    @staticmethod
    def Image(openai, prompt, imageConfig):
        return openai.Image.create(
            prompt=prompt,
            **vars(imageConfig)
        )
