from VoiceHandler import VoiceHandler
from LanguageModelHandler import LanguageModelHandler
from TextToSpeechHandler import TextToSpeechHandler


if __name__ == "__main__":
    ttsHandler = TextToSpeechHandler()
    llmHandler = LanguageModelHandler(ttsHandler.speak)
    voiceHandler = VoiceHandler(llmHandler.get_response_to_prompt)

    # listen for voice input
    print("Listening...")
    voiceHandler.listen_for_speech_from_mic()
