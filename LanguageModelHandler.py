import ollama
import time
import re


class LanguageModelHandler:
    # inject tts capabilities
    tts_handler_object_method = None

    # Set the model and temperature (optional)
    model = "phi3:mini"
    # model = "llama3"
    temperature = 1.0
    ollama_url = "http://localhost:3000"
    ollama_client = None

    # general variables
    retry_interval = 1
    default_reply = "I encountered an error while" + \
                    " processing your request. Please try again."
    speech_filters = [
        r'```(.+)?\n[\s\S]+?```'
    ]

    def __init__(
                    self,
                    tts_handler_object_method=None,
                    ollama_url="http://localhost:3000"
                ) -> None:
        # self.connect_to_ollama(ollama_url)
        self.init_ollama_connection(ollama_url)
        self.tts_handler_object_method = tts_handler_object_method

    def connect_to_ollama(self, ollama_url):
        self.ollama_client = ollama.Client(ollama_url)

    def init_ollama_connection(self, ollama_url):
        while self.ollama_client is None:
            time.sleep(self.retry_interval)
            try:
                print("connecting to OLLAMA...")
                self.connect_to_ollama(ollama_url)
                print("testing OLLAMA connection...")
                response = self.ask("hello, are you there?")
                print(response)
            except Exception as e:
                self.ollama_client = None
                print(
                    "init_ollama_connectio ->",
                    "error connecting to OLLAMA:",
                    e
                )

    def get_response_to_prompt(self, voiceInputString, wake_word):
        print("callback: ", voiceInputString)
        # only process non-empty voice prompts
        if len(voiceInputString) == 0:
            return

        # only process requests following the wake word
        if voiceInputString.split(" ")[0] != wake_word:
            return

        # address the wake word
        if voiceInputString == "pixel" and \
                self.tts_handler_object_method is not None:
            self.tts_handler_object_method("How can I help you? "
                                           "Please ask me a question "
                                           "after saying 'Pixel'.")
            return

        # process the contents of the voice prompt following the wake word
        full_response, filtered_response = self.ask(
            " ".join(voiceInputString.split(" ")[1:])
        )

        # speak the response
        print(full_response)
        self.tts_handler_object_method(filtered_response)

    def ask(self, prompt):
        llmResponse = ollama.chat(model=self.model, messages=[
            {
                'role': 'user',
                'content': prompt + ". reply as briefly as possible.",
            },
        ])

        response = llmResponse['message']['content']
        filtered_response = self.filter_response(response)
        return response, filtered_response

    def filter_response(self, llm_response):
        new_string = llm_response
        for filter in self.speech_filters:
            new_string = re.sub(filter, '', new_string)

        return new_string
