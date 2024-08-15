from vosk import Model, KaldiRecognizer
import argparse
import queue
import sys
import sounddevice as sd
import json


class VoiceHandler:
    # general variables
    q = None
    parser = None
    args = None
    wake_word = "pixel"
    listening = True
    voice_input_callback = None
    default_reply = "I encountered an error while" + \
                    " processing your request. Please try again."
    speech_filters = [
        r'```(.+)?\n[\s\S]+?```'
    ]

    def __init__(self, voice_input_callback) -> None:
        self.q = queue.Queue()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.init_parser()
        self.voice_input_callback = voice_input_callback

    def init_parser(self):
        self.parser.add_argument(
            "-l", "--list-devices", action="store_true",
            help="show list of audio devices and exit")
        args, remaining = self.parser.parse_known_args()
        if args.list_devices:
            print(sd.query_devices())
            self.parser.exit(0)
        self.parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[self.parser])
        self.parser.add_argument(
            "-f", "--filename", type=str, metavar="FILENAME",
            help="audio file to store recording to")
        self.parser.add_argument(
            "-d", "--device", type=self.int_or_str,
            help="input device (numeric ID or substring)")
        self.parser.add_argument(
            "-r", "--samplerate", type=int, help="sampling rate")
        self.parser.add_argument(
            "-m", "--model", type=str,
            help="language model; e.g. en-us, fr, nl; default is en-us")
        self.args = self.parser.parse_args(remaining)

    def listen_for_speech_from_mic(self):
        try:
            if self.args.samplerate is None:
                device_info = sd.query_devices(self.args.device, "input")
                # soundfile expects an int, sounddevice provides a float:
                self.args.samplerate = int(device_info["default_samplerate"])

            if self.args.model is None:
                model = Model(lang="en-us")
            else:
                model = Model(lang=self.args.model)

            if self.args.filename:
                dump_fn = open(self.args.filename, "wb")
            else:
                dump_fn = None

            with sd.RawInputStream(
                samplerate=self.args.samplerate,
                blocksize=4000,
                device=self.args.device,
                dtype="int16",
                channels=1,
                callback=self.callback
            ):
                print("#" * 80)
                print("Press Ctrl+C to stop the recording")
                print("#" * 80)

                rec = KaldiRecognizer(model, self.args.samplerate)
                while True:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        # return json.loads(rec.Result())
                        self.listening = False
                        self.voice_input_callback(json.loads(
                                                  rec.Result())["text"],
                                                  self.wake_word
                                                  )
                        self.listening = True
                    else:
                        # print(rec.PartialResult())
                        pass
                    if dump_fn is not None:
                        dump_fn.write(data)

        except KeyboardInterrupt:
            print("\nDone")
            self.parser.exit(0)
        except Exception as e:
            self.parser.exit(type(e).__name__ + ": " + str(e))

    def int_or_str(self, text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    def callback(self, indata, frames, timestamp, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print("callback ->", status, file=sys.stderr)
        if self.listening:
            self.q.put(bytes(indata))
