import requests
import json
# import schedule
# import time

def fetch_crypto_data(crypto_ids):
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'ids': ','.join(crypto_ids),
        'order': 'market_cap_desc',
        'per_page': len(crypto_ids),
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=params)
    return response.json()

def fetch_historical_data(crypto_id, days):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': days
    }
    response = requests.get(url, params=params)
    return response.json()

def update_crypto_data():
    crypto_ids = [
        'bitcoin', 'ethereum', 'ripple', 'litecoin', 'cardano', 'polkadot', 'bitcoin-cash',
        'binancecoin', 'chainlink', 'stellar', 'usd-coin', 'dogecoin', 'uniswap',
        'wrapped-bitcoin', 'terra-luna', 'aave', 'monero', 'theta-token', 'vechain',
        'solana', 'tron', 'tezos', 'dash', 'cosmos', 'filecoin', 'crypto-com-chain',
        'eos', 'algorand', 'maker', 'compound'
    ]

    # Fetch the current market data
    crypto_data = fetch_crypto_data(crypto_ids)

    # Fetch historical data for each cryptocurrency
    historical_data = {crypto_id: fetch_historical_data(crypto_id, '7') for crypto_id in crypto_ids}

    # Combine data for ease of access
    combined_data = {crypto['id']: {
        'current_price': crypto['current_price'],
        'market_cap': crypto['market_cap'],
        'circulating_supply': crypto['circulating_supply'],
        'total_supply': crypto['total_supply'],
        '24h_volume': crypto['total_volume'],
        'all_time_high': crypto['ath'],
        'all_time_low': crypto['atl'],
        'historical_data': historical_data[crypto['id']]
    } for crypto in crypto_data}

    # Save data to a JSON file
    with open('crypto_data.json', 'w') as f:
        json.dump(combined_data, f)

    print("Crypto data updated successfully.")

# Schedule the update_crypto_data function to run every 10 minutes
# schedule.every(10).minutes.do(update_crypto_data)

# Initial run
update_crypto_data()

# Keep the script running to execute the scheduled tasks
# while True:
    # schedule.run_pending()
    # time.sleep(1)