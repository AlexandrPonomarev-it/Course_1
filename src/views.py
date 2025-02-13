import datetime
import json
import os
from typing import Any

import requests
from dotenv import load_dotenv

import pandas as pd

from src.utils import read_excel_file, date_input
from src.utils import greeting_by_current_time

load_dotenv()
api_key_cur = os.getenv('API_KEY_CUR')
api_key_stock = os.getenv('API_KEY_STOCK')

def time_interval_transactions(transactions_list):
    """Получает список транзакции за месяц от 1 числа до указанной даты"""

    control_date = date_input()
    list_of_operations_of_the_month = []
    control_year = control_date.year
    control_month = control_date.month
    control_day = control_date.day
    for transactions in transactions_list:
        date_transactions_month = datetime.datetime.strptime(transactions['Дата операции'], "%d.%m.%Y %H:%M:%S").month
        date_transactions_day = datetime.datetime.strptime(transactions['Дата операции'], "%d.%m.%Y %H:%M:%S").day
        date_transactions_year = datetime.datetime.strptime(transactions['Дата операции'], "%d.%m.%Y %H:%M:%S").year
        if control_month == date_transactions_month and control_day >= date_transactions_day and control_year == date_transactions_year:
            list_of_operations_of_the_month.append(transactions)

    return list_of_operations_of_the_month


def number_card(transactions_list):
    """Получает список транзакций с определенной карты за указанный период и
    возвращает список словарей, где ключ - номер карты,
    а значение - сумма всех операции за прошедший период"""

    card_numbers = []
    list_transactions_for_card_number = []
    list_dict_card_num_sum = []
    index_counter = 0
    for transactions in transactions_list:
        if transactions['Номер карты'] not in card_numbers and pd.isna(transactions['Номер карты']) != True:
            card_numbers.append(transactions['Номер карты'])
    for number in card_numbers:
        for transaction in transactions_list:
            if transaction['Номер карты'] == number:
                list_transactions_for_card_number.append(transaction['Сумма операции с округлением'])
        dict_transactions_for_card_number = {number: sum(x for x in list_transactions_for_card_number)}
        list_dict_card_num_sum.append(dict_transactions_for_card_number)
        index_counter += 1
    info_list = []
    for act in list_dict_card_num_sum:
        for key, value in act.items():
            info_list.append({"last_digits": key[1:], "total_spent": value, "cashback": round(float(value) / 100, 2)})



    return info_list


def top_5_transactions(operations_list_dict):
    """Функция выводит топ-5 транзакций по сумме платежа"""
    sorted_operation_list = sorted(operations_list_dict, key=lambda x: x['Сумма операции с округлением'], reverse=True)
    top_5_operations_list = sorted_operation_list[0:5]
    top_5_operations_list_clear = []
    for operation in top_5_operations_list:
        top_5_operations_list_clear.append({
            "date": operation['Дата операции'][:10],
            "amount": operation['Сумма операции с округлением'],
            "category": operation['Категория'],
            "description": operation['Описание']
        })



    return top_5_operations_list_clear


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

    api_url = f"https://api.currencylayer.com/live?access_key=037e8e04d040733632e1169c45c8ddc1&source={user_settings_list[0]}&currencies=RUB"
    headers = {"apikey": api_key_cur}

    response = requests.get(api_url, headers=headers)
    result = response.text
    dict_result = json.loads(result)

    return round(dict_result["quotes"]["USDRUB"], 2)


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


    api_url = f"https://api.currencylayer.com/live?access_key=037e8e04d040733632e1169c45c8ddc1&source={user_settings_list[1]}&currencies=RUB"
    headers = {"apikey": api_key_cur}

    response = requests.get(api_url, headers=headers)
    result = response.text
    dict_result = json.loads(result)

    return round(dict_result["quotes"]["EURRUB"], 2)


def stock_conversion_function() -> Any:
    """
    Функция запрашивает и возвращает данные о курсе валюты 2 по отношению к RUB
    """
    api_url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key_stock}"
    headers = {"apikey": api_key_stock}

    response = requests.get(api_url, headers=headers)
    result = response.text
    dict_result = json.loads(result)

    list_stock =  [x for x in dict_result if x["symbol"] == "AAPL" or x["symbol"] == "AMZN"
            or  x["symbol"] == "GOOGL" or x["symbol"] == "MSFT" or x["symbol"] == "TSLA"]

    return [[x['symbol'], x['price']] for x in list_stock]





def banking_operations_analysis_func(transactions):
    """Функция для обработки банковских операций, которая принимает дату
    и возвращает набор данных по найденным транзакциям"""

    greeting = greeting_by_current_time()
    transactions_list_for_month = time_interval_transactions(transactions)
    list_of_transactions_from_each_card = number_card(transactions_list_for_month)
    top_five_transactions = top_5_transactions(transactions_list_for_month)

    user_settings_list_val = []
    with open("../user_settings.json", 'r') as us:
        settings = json.load(us)
        for key, values in settings.items():
            if key == "user_currencies":
                user_settings_list_val += values

    json_answer = {
        "greeting": greeting,
        "cards": list_of_transactions_from_each_card,
        "top_transactions": top_five_transactions,
        "currency_rates": [{"currency": user_settings_list_val[0],"rate": currency_conversion_function_1()},
                           {"currency": user_settings_list_val[0],"rate": currency_conversion_function_1()}],
        "stock_prices": [{"stock": stock_conversion_function()[0][0], "price": stock_conversion_function()[0][1]},
                         {"stock": stock_conversion_function()[1][0], "price": stock_conversion_function()[1][1]},
                         {"stock": stock_conversion_function()[2][0], "price": stock_conversion_function()[2][1]},
                         {"stock": stock_conversion_function()[3][0], "price": stock_conversion_function()[3][1]},
                         {"stock": stock_conversion_function()[4][0], "price": stock_conversion_function()[4][1]}]
    }


    return json.dumps(json_answer, indent=4, ensure_ascii=False)

print(banking_operations_analysis_func(read_excel_file()))