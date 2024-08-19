import requests
from pyquery import PyQuery as pq
from interceptors.PixelInterceptor import PixelInterceptor


class GetCurrentTimeInterceptor(PixelInterceptor):
    key_phrases = ["what", "time", "current", "now", "is", "it"]

    def __init__(self, voice_prompt=None):
        super().__init__(voice_prompt)

    def intercept(self) -> str:
        time_dot_gov_response = requests.get(
            "https://www.timeanddate.com/worldclock/"
        )
        html = pq(time_dot_gov_response.content)
        time = " ".join(html("td#p100").html().split(" ")[1:])
        return f"The current time in New York City is {time}"
