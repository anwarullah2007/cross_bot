import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

def fetch_market_data(coins, api_key):
    params = {
        "ids": ",".join(coins),
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "x_cg_demo_api_key": api_key
    }

    response = requests.get(COINGECKO_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
