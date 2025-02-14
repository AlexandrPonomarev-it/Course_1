import json
import os
from typing import Any

import requests
from dotenv import load_dotenv
load_dotenv()
api_key_cur = os.getenv('API_KEY_CUR')
api_key_stock = os.getenv('API_KEY_STOCK')

def currency_conversion_function_1() -> Any:
    """
    Функция запрашивает и возвращает данные о курсе валюты USD по отношению к RUB
    """
    user_settings_list = []
    with open("../user_settings.json", 'r') as us:
        settings = json.load(us)
        for key, values in settings.items():
            if key == "user_currencies":
                user_settings_list += values

    api_url = f"https://api.apilayer.com/currency_data/convert?to=RUB&from={user_settings_list[0]}&amount=1"
    headers = {"apikey": api_key_cur}

    response = requests.get(api_url, headers=headers)
    result = response.text
    dict_result = json.loads(result)

    return dict_result


def currency_conversion_function_2() -> Any:
    """
    Функция запрашивает и возвращает данные о курсе валюты 1 по отношению к RUB
    """
    user_settings_list = []
    with open("../user_settings.json", 'r') as us:
        settings = json.load(us)
        for key, values in settings.items():
            if key == "user_currencies":
                user_settings_list += values


    api_url = f"https://api.apilayer.com/currency_data/convert?to=RUB&from={user_settings_list[1]}&amount=1"
    headers = {"apikey": "FpwbizlDvfgufh2sNNCKdpR43MhgHGlD"}

    response = requests.get(api_url, headers=headers)
    result = response.text
    dict_result = json.loads(result)

    return dict_result

print(currency_conversion_function_2())