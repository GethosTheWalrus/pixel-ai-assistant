from plugins.PixelPlugin import PixelPlugin
import requests
import random


class GetQuote(PixelPlugin):
    quote_number = None

    def __init__(self, quote_number=None):
        super().__init__()
        self.quote_number = quote_number
        self.process()

    def process(self) -> str:
        quote_response = requests.get("https://www.miketoscano.com/quotes.txt")
        quotes = quote_response.text.split("----")
        quote_index = (
            self.quote_number
            if self.quote_number >= 0
            else random.randint(0, len(quotes) - 1)
        )
        quote = quotes[quote_index]
        split_quote = quote.split("\n")
        split_quote = list(filter(None, split_quote))

        self.response = (
            split_quote[0].strip()
            + (" - " + split_quote[1].strip() if len(split_quote) > 1 else "")
        )
