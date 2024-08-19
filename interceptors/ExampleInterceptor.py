from interceptors.PixelInterceptor import PixelInterceptor


class ExampleInterceptor(PixelInterceptor):
    keywords = ["what", "is", "an", "interceptor"]

    def __init__(self, voice_prompt=None):
        super().__init__(voice_prompt)

    def intercept(self) -> str:
        return "Interceptors listen to every voice prompt, " \
               "and run on relavent ones. If a particular " \
                "interceptor is matched, it will automatically " \
                "augment the prompt with relevant information " \
                "obtained from intercept method in its class."
