"""
Create data.json file with all the mutual fund details
"""
import json
import os.path

import requests
import requests_cache
from loguru import logger

session = requests_cache.CachedSession('mf_cn_kuvera_cache', expire_after=86400)

os.makedirs('data', exist_ok=True)


def mf_list():
    file = 'mf.json'
    if os.path.exists(file):
        with open(file, 'r') as f:
            data = json.load(f)
            print("Data loaded from mf.json")
            return data
    else:
        url = 'https://api.mfapi.in/mf'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            with open('mf.json', 'w') as file:
                json.dump(data, file, indent=4)
            print("Data saved to data.json")
    return data


def get_mf_info(isin):
    if not isin:
        return

    url = 'https://mf.captnemo.in/kuvera' + isin
    response = session.get(url)
    if not response.status_code == 200:
        print(f"Error fetching data for ISIN {isin}: {response.status_code}")
        return None

    data = response.json()
    if 'error' in data:
        print(f"Error in response for ISIN {isin}: {data['error']}")
        return None

    with open(f'data/{isin}.json', 'w') as file:
        json.dump(response.json(), file, indent=4)


if __name__ == "__main__":
    funds = mf_list()
    for index, fund in enumerate(funds):
        logger.info(f"Processing {index + 1}/{len(funds)}: {fund['schemeName']}")
        fund_info = get_mf_info(fund['isinGrowth'])
        fund_info = get_mf_info(fund['isinDivReinvestment'])