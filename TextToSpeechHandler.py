import pyttsx3 as tts


class TextToSpeechHandler:
    # init tts
    speaker = None

    def __init__(self) -> None:
        self.speaker = tts.init()

    def speak(self, content):
        self.speaker.say(content)
        self.speaker.runAndWait()
