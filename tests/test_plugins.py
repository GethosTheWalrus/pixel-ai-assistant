from plugins.GetQuote import GetQuote


def test_get_random_quote():
    getQuote = GetQuote({"quote_number": 0})
    quote = getQuote.response
    assert len(quote) > 0
    assert quote == "Temper gets you into trouble. " \
                    "Pride keeps you there. - Unknown"
