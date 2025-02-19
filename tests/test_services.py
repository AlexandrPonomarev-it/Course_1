import unittest
import json

from src.services import search_by_input_operation


class TestSearchByInputOperation(unittest.TestCase):
    def test_search_by_category(self):
        # Пример данных транзакций
        transactions = [
            {"Категория": "Еда", "Описание": "Покупка продуктов"},
            {"Категория": "Транспорт", "Описание": "Проезд на автобусе"},
            {"Категория": "Еда", "Описание": "Ужин в ресторане"}
        ]

        # Ожидаемый результат
        expected_result = json.dumps([
            {"Категория": "Еда", "Описание": "Покупка продуктов"},
            {"Категория": "Еда", "Описание": "Ужин в ресторане"}
        ], indent=4, ensure_ascii=False)

        # Вызов функции и проверка результата
        result = search_by_input_operation("еда", transactions)
        self.assertEqual(result, expected_result)

    def test_search_by_description(self):
        # Пример данных транзакций
        transactions = [
            {"Категория": "Еда", "Описание": "Покупка продуктов"},
            {"Категория": "Транспорт", "Описание": "Проезд на автобусе"},
            {"Категория": "Еда", "Описание": "Ужин в ресторане"}
        ]

        # Ожидаемый результат
        expected_result = json.dumps([
            {"Категория": "Транспорт", "Описание": "Проезд на автобусе"}
        ], indent=4, ensure_ascii=False)

        # Вызов функции и проверка результата
        result = search_by_input_operation("автобус", transactions)
        self.assertEqual(result, expected_result)

    def test_no_matches(self):
        # Пример данных транзакций
        transactions = [
            {"Категория": "Еда", "Описание": "Покупка продуктов"},
            {"Категория": "Транспорт", "Описание": "Проезд на автобусе"}
        ]

        # Ожидаемый результат
        expected_result = json.dumps([], indent=4, ensure_ascii=False)

        # Вызов функции и проверка результата
        result = search_by_input_operation("одежда", transactions)
        self.assertEqual(result, expected_result)