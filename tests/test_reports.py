import unittest
from datetime import datetime, timedelta

from src.reports import spending_by_category


class TestSpendingByCategory(unittest.TestCase):
    def test_spending_by_category(self):
        # Пример данных транзакций
        transactions = [
            {"Дата операции": "01.01.2023 12:00:00", "Категория": "Еда", "Сумма операции с округлением": 100},
            {"Дата операции": "15.02.2023 12:00:00", "Категория": "Еда", "Сумма операции с округлением": 200},
            {"Дата операции": "10.03.2023 12:00:00", "Категория": "Транспорт", "Сумма операции с округлением": 50}
        ]

        # Устанавливаем контрольную дату
        control_date = datetime(2023, 3, 31)

        # Ожидаемый результат
        expected_result = [{'Еда': [100, 200]}]

        # Вызов функции и проверка результата
        result = spending_by_category(transactions, "Еда", control_date)
        self.assertEqual(result, expected_result)

    def test_no_transactions_in_category(self):
        # Пример данных транзакций
        transactions = [
            {"Дата операции": "01.01.2023 12:00:00", "Категория": "Еда", "Сумма операции с округлением": 100},
            {"Дата операции": "15.02.2023 12:00:00", "Категория": "Еда", "Сумма операции с округлением": 200}
        ]

        # Устанавливаем контрольную дату
        control_date = datetime(2023, 3, 31)

        # Ожидаемый результат
        expected_result = ["Операций по данной категории в указанный период не найдено"]

        # Вызов функции и проверка результата
        result = spending_by_category(transactions, "Транспорт", control_date)
        self.assertEqual(result, expected_result)