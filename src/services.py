import json
import logging
import os
from typing import Any

import pandas as pd


current_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_dir, "..", "logs", "services.log")

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file_path)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def search_by_input_operation(search: str, transactions: dict | list) -> Any:
    """Функция принимает список транзакций и по введенному слову возвращает список
    всех транзакций из введенной категории или описания"""
    try:
        logger.info("Осуществлен поиск транзакций по категории")
        list_of_transactions_on_request = []
        for transaction in transactions:
            if not pd.isna(transaction["Категория"]):
                if (
                    search in transaction["Описание"].lower()
                    or search in transaction["Категория"].lower()
                ):
                    list_of_transactions_on_request.append(transaction)
            else:
                continue

        return json.dumps(list_of_transactions_on_request, indent=4, ensure_ascii=False)
    except TypeError as error:
        logger.error(f"Ошибка работы приложения {error}")
        return []

