import ollama
import time
import re


class LanguageModelHandler:
    config = None
    # inject tts capabilities
    tts_handler_object_method = None

    # Set the model and temperature (optional)
    model = "llama3.1"
    temperature = 1.0
    ollama_url = "http://localhost:3000"
    ollama_client = None

    # general variables
    retry_interval = 1
    default_reply = "I encountered an error while" + \
                    " processing your request. Please try again."
    speech_filters = [
        r'```(.+)?\n[\s\S]+?```',
        r'\*'
    ]
    display_handler = None
    plugin_handler = None
    interceptor_handler = None

    def __init__(
                    self,
                    config,
                    tts_handler_object_method=None,
                    display_handler=None,
                    plugin_handler=None,
                    interceptor_handler=None,
                ) -> None:
        self.config = config
        self.init_ollama_connection(
            config["ollama_url"] or
            "http://localhost:3000"
        )
        self.tts_handler_object_method = tts_handler_object_method
        self.display_handler = display_handler
        self.plugin_handler = plugin_handler
        self.interceptor_handler = interceptor_handler

        self.set_display("Listening...")

    def set_display(self, message):
        if self.display_handler is not None:
            self.display_handler.set_message(message)

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
        print("Heard:", voiceInputString)
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

        self.set_display("Thinking...")
        prompt_without_wake_word = " ".join(voiceInputString.split(" ")[1:])

        full_response, filtered_response, prompt_augmentation = (
            None, None, None
        )

        if prompt_without_wake_word in self.plugin_handler.modules:
            # process the contents of the voice prompt
            # by invoking the proper plugin
            plugin = self.plugin_handler.modules[prompt_without_wake_word]
            full_response = filtered_response = plugin.response
        else:
            prompt_augmentation = self.interceptor_handler.evaluate_interceptors( # noqa
                prompt_without_wake_word
            )

            full_prompt = prompt_without_wake_word + " " + (
                prompt_augmentation if prompt_augmentation is not None else "" # noqa
            )

            print("Asking:", full_prompt)

            # process the contents of the voice prompt through the LLM
            full_response, filtered_response = self.ask(
                full_prompt
            )

        # speak the response
        print(full_response)
        self.set_display("Answering...")
        self.tts_handler_object_method(filtered_response)

        self.set_display("Listening...")

    def ask(self, prompt):
        llmResponse = ollama.chat(model=self.model, messages=[
            {
                'role': 'user',
                'content': prompt + ". reply as briefly as possible. Ideally in 4 sentences or less.", # noqa
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
