from typing import Any
from datetime import datetime

import pandas as pd


def read_excel_file() -> Any:
    """Функция для считывания финансовых операций из excel, которая возвращает
    список транзакций"""
    try:
        df_excel = pd.read_excel('../operations.xlsx')
        list_transaction_excel = list(to_dict(df_excel, orient="records"))

        return list_transaction_excel
    except ValueError:
        return "Дынные в файле отсутствуют или не соответствуют формату"
    except FileNotFoundError:
        return "Файл не найден"


def greeting_by_current_time():
    """Функция возвращает приветствие в зависимости от времени суток"""
    current_date_time = datetime.now()
    if 00 <= current_date_time.hour < 6:
        return "Доброй ночи"
    elif 6 <= current_date_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_date_time.hour < 18:
        return "Добрый день"
    elif 18 <= current_date_time.hour <= 23:
        return "Добрый вечер"
    else:
        "Невозможно определить время суток"


def date_input():
    """Функция получает от пользователя дату в заданном формате"""
    year = int(input('Введите год: '))
    month = int(input('Введите месяц: '))
    day = int(input('Введите день: '))
    control_time = datetime.now()
    hour = control_time.hour
    minute = control_time.minute
    second = round(control_time.second)
    control_date = datetime(year, month, day, hour, minute, second)
    return control_date