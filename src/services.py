import json

import pandas as pd

from src.utils import read_excel_file


def search_by_input_operation(search, transactions):
    list_of_transactions_on_request = []
    for transaction in transactions:
        if not pd.isna(transaction['Категория']):
            if search in transaction['Описание'].lower() or search in transaction['Категория'].lower():
                list_of_transactions_on_request.append(transaction)
        else:
            continue

    return json.dumps(list_of_transactions_on_request, indent=4, ensure_ascii=False)


search_bar = input("Введите название категории или описание транзакции: ").lower()
print(search_by_input_operation(search_bar, read_excel_file()))