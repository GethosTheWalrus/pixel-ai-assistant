from VoiceHandler import VoiceHandler
from LanguageModelHandler import LanguageModelHandler
from TextToSpeechHandler import TextToSpeechHandler

import json


if __name__ == "__main__":
    config = {}
    with open("pixel.json") as json_data:
        config = json.load(json_data)
        json_data.close()

    ttsHandler = TextToSpeechHandler()
    llmHandler = LanguageModelHandler(ttsHandler.speak)
    voiceHandler = VoiceHandler(llmHandler.get_response_to_prompt)

    # listen for voice input
    print("Listening...")
    voiceHandler.listen_for_speech_from_mic()
