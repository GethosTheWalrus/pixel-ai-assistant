class PixelPlugin:
    input = {}
    wake_phrase = "Run this plugin"

    def __init__(self, input={}):
        self.input = input
        pass

    def process(self):
        pass

    @property
    def response(self) -> str:
        try:
            return self.process()
        except Exception as e:
            return self.handle_plugin_error() + ": " + str(e)

    def handle_plugin_error(self) -> str:
        return "I encountered an error while processing your request." \
               " Please try again."
