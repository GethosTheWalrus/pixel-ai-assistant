class PixelInterceptor:
    voice_prompt = None
    keywords = []

    def __init__(self, voice_prompt=None):
        self.voice_prompt = voice_prompt

    def intercept(self):
        pass

    @property
    def response(self):
        try:
            return self.intercept()
        except Exception as e:
            return self.handle_interceptor_error() + ": " + str(e)
        
    def is_matched(self, voice_prompt) -> bool:
        self.voice_prompt = voice_prompt
        voice_prompt_words = self.voice_prompt.split(" ")
        intersections = set(voice_prompt_words) & set(self.keywords)
        return len(intersections) >= 4

    def handle_interceptor_error(self):
        return "I encountered an error while processing your request." \
               " Please try again"
