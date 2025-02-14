import datetime
from datetime import timedelta
import json
from collections import defaultdict
from datetime import datetime
from functools import wraps
from typing import Any, Optional, Callable

import pandas as pd

from src.utils import date_input, read_excel_file

def writing_the_result_to_a_file(filename: Optional[str] = None) -> Callable:
    """
    Декоратор позволяет записывать данные из функции в файл
    """
    def wrapper(func: Any) -> Any:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
                result = func(*args, **kwargs)
                with open(filename, 'w') as file:
                    file.write(result)
                return result
        return inner
    return wrapper


@writing_the_result_to_a_file("../result_of_the_reports.json")
def spending_by_category(transactions: pd.DataFrame, category: str, control_date: Optional[str] = None) -> Any:
    if control_date is None:
        control_date = datetime.now()
    three_months_ago = control_date - timedelta(days=90)
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

    return json.dumps(sum_category, ensure_ascii=False)


category_input = input("Введите название категории: ").title()
print(spending_by_category(read_excel_file(), category_input, date_input()))

