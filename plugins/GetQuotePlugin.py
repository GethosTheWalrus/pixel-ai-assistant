from plugins.PixelPlugin import PixelPlugin
import requests
import random


class GetQuotePlugin(PixelPlugin):
    wake_phrase = "get me a random quote"

    def __init__(self, input={}):
        super().__init__(input)

    def process(self) -> str:
        super().process()
        quote_number = (
            self.input["quote_number"]
            if "quote_number" in self.input
            else None
        )
        quote_response = requests.get("https://www.miketoscano.com/quotes.txt")
        quotes = quote_response.text.split("----")
        quote_index = (
            quote_number
            if "quote_number" in self.input and quote_number >= 0
            else random.randint(0, len(quotes) - 1)
        )
        quote = quotes[quote_index]
        split_quote = list(filter(None, quote.split("\n")))
        quote_str = split_quote[0].strip() + \
            (". " + split_quote[1].strip()
             if len(split_quote) > 1
             else ". Unknown")

        return (
            quote_str
        )
