from plugins.GetQuotePlugin import GetQuotePlugin


def test_get_random_quote():
    getQuote = GetQuotePlugin({"quote_number": 0})
    quote = getQuote.response
    print(quote)
    assert len(quote) > 0
    assert quote == "Temper gets you into trouble. " \
                    "Pride keeps you there. - Unknown"
