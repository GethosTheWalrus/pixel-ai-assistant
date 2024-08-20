from VoiceHandler import VoiceHandler
from LanguageModelHandler import LanguageModelHandler
from TextToSpeechHandler import TextToSpeechHandler
from PluginsHandler import PluginsHandler
from InterceptorHandler import InterceptorHandler

import json


if __name__ == "__main__":
    config = {}
    with open("pixel.json") as json_data:
        config = json.load(json_data)
        json_data.close()

    interceptorsHandler = InterceptorHandler()
    pluginsHandler = PluginsHandler()
    ttsHandler = TextToSpeechHandler()
    llmHandler = LanguageModelHandler(
        config,
        ttsHandler.speak,
        None,
        pluginsHandler,
        interceptorsHandler
    )
    voiceHandler = VoiceHandler(
        llmHandler.get_response_to_prompt
    )

    # listen for voice input
    print("Listening...")
    voiceHandler.listen_for_speech_from_mic()
