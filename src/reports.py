import datetime
import logging
import os
from datetime import timedelta
from collections import defaultdict
from datetime import datetime
from functools import wraps
from typing import Any, Optional

current_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_dir, "..", "logs", "reports.log")

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file_path)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def writing_the_result_to_a_file(filename: Optional[str] = None) -> Any:
    """
    Декоратор позволяет записывать данные из функции в файл
    """
    def wrapper(func: Any) -> Any:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                with open(filename, 'a') as file:
                    file.write(f"{result}\n")
                return result
            except TypeError as error:
                with open(filename, 'a') as file:
                    file.write(f"{func.__name__} error: {error.__class__.__name__}.\n")
        return inner
    return wrapper




@writing_the_result_to_a_file("../result_of_the_reports.txt")
def spending_by_category(transactions: dict | list, category: str, control_date: Optional[Any] = None) -> Any:
    """Функция принимает файл с данными о транзакциях и осуществляет поиск по введенным пользователем данным
    и возвращает список транзакций по введенной категории за последние три месяца"""
    try:
        logger.info("Осуществлен поиск транзакций по категории")
        if control_date is None:
            control_date_check = datetime.now()
        else:
            control_date_check = control_date
        three_months_ago = control_date_check - timedelta(days=90)
        list_of_operations_of_the_3_month = []
        for transact in transactions:
            date_transactions = datetime.strptime(transact["Дата операции"], "%d.%m.%Y %H:%M:%S")
            if three_months_ago <= date_transactions <= control_date:
                list_of_operations_of_the_3_month.append(transact)

        list_category = []

        for transaction in list_of_operations_of_the_3_month:
            list_category.append(
                {transaction["Категория"]: transaction["Сумма операции с округлением"]}
            )

        category_list_len = defaultdict(list)
        for cat in list_category:
            for key, value in cat.items():
                category_list_len[key].append(value)

        sum_category = []
        for key, value in category_list_len.items():
            if key == category:
                sum_category.append({category: value})
        if sum_category:
            return sum_category
        else:
            return ["Операций по данной категории в указанный период не найдено"]

    except TypeError as error:
        logger.error(f"Ошибка работы приложения {error}")
        return ["Операций по данной категории в указанный период не найдено"]


