from typing import Any

from src.reports import spending_by_category
from src.services import search_by_input_operation
from src.utils import read_excel_file, date_input
from src.views import banking_operations_analysis_func


def main_function() -> Any:
    banking_operations_analysis = banking_operations_analysis_func(read_excel_file())
    search_bar = input("Введите название категории или описание транзакции: ").lower()
    search_bar_func = search_by_input_operation(search_bar, read_excel_file())
    category_input = input("Введите название категории: ").title()
    spending_by_category_func = spending_by_category(read_excel_file(), category_input, date_input())

    return banking_operations_analysis,  search_bar_func, spending_by_category_func

for i in main_function():
    print(i)