from LanguageProcessor import LanguageProcessor


def ask_llm(voiceInputString, wake_word):
    print("callback: ", voiceInputString)
    # only process non-empty voice prompts
    if len(voiceInputString) == 0:
        return

    # only process requests following the wake word
    if voiceInputString.split(" ")[0] != wake_word:
        return

    # address the wake word
    if voiceInputString == "pixel":
        language_processor.speak("How can I help you? "
                                 "Please ask me a question "
                                 "after saying 'Pixel'.")
        return

    # process the contents of the voice prompt following the wake word
    full_response, filtered_response = language_processor.ask(
        " ".join(voiceInputString.split(" ")[1:])
    )

    # speak the response
    print(full_response)
    language_processor.speak(filtered_response)


if __name__ == "__main__":
    language_processor = LanguageProcessor(ask_llm)
    # listen for voice input
    print("Listening...")
    language_processor.listen_for_speech_from_mic()
