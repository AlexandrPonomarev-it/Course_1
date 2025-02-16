import os
import unittest
import datetime
from unittest.mock import patch, mock_open
import json
from src.views import currency_conversion_function_1, stock_conversion_function, banking_operations_analysis_func
import pytest


# Предположим, что функция time_interval_transactions находится в модуле src.views
from src.views import time_interval_transactions, number_card, top_5_transactions


class TestTimeIntervalTransactions(unittest.TestCase):
    @patch('src.views.date_input')
    def test_time_interval_transactions(self, mock_date_input):
        # Настраиваем заглушку для date_input
        mock_date_input.return_value = datetime.datetime(2023, 10, 15)

        # Пример списка транзакций
        transactions_list = [
            {'Дата операции': '10.10.2023 12:00:00'},
            {'Дата операции': '05.10.2023 15:30:00'},
            {'Дата операции': '20.09.2023 09:00:00'},
            {'Дата операции': '15.10.2023 18:45:00'},
        ]

        # Ожидаемый результат
        expected_result = [
            {'Дата операции': '10.10.2023 12:00:00'},
            {'Дата операции': '05.10.2023 15:30:00'},
            {'Дата операции': '15.10.2023 18:45:00'},
        ]

        # Проверяем, что функция возвращает правильный список транзакций
        result = time_interval_transactions(transactions_list)
        self.assertEqual(result, expected_result)


class TestNumberCard(unittest.TestCase):

    def setUp(self):
        self.transactions_list = [
            {'Номер карты': '*3456', 'Сумма операции с округлением': 100},
            {'Номер карты': '*7654', 'Сумма операции с округлением': 200},
            {'Номер карты': '*3456', 'Сумма операции с округлением': 150},
            {'Номер карты': '*7654', 'Сумма операции с округлением': 250},
            {'Номер карты': '*4444', 'Сумма операции с округлением': 500},
        ]

    def test_number_card(self):
        # Тестируем работу функции при передаче корректного списка транзакций
        result = number_card(self.transactions_list)
        expected_result = [
                {'cashback': 2.5, 'last_digits': '3456', 'total_spent': 250},
                {'cashback': 7.0, 'last_digits': '7654', 'total_spent': 700},
                {'cashback': 12.0, 'last_digits': '4444', 'total_spent': 1200}
        ]
        self.assertEqual(result, expected_result)

    def test_empty_transactions_list(self):
        # Проверяем поведение функции при пустом списке транзакций
        empty_transactions_list = []
        result = number_card(empty_transactions_list)
        self.assertEqual(result, [])

    def test_invalid_type_transactions_list(self):
        # Проверка поведения функции при передаче неверного типа данных
        invalid_transactions_list = None
        with self.assertRaises(TypeError):
            number_card(invalid_transactions_list)


import unittest


class TestTop5Transactions(unittest.TestCase):

    def setUp(self):
        self.operations_list_dict = [
            {
                'Дата операции': '2022-12-01',
                'Сумма операции с округлением': 1000,
                'Категория': 'Еда',
                'Описание': 'Покупка продуктов'
            },
            {
                'Дата операции': '2022-12-02',
                'Сумма операции с округлением': 2000,
                'Категория': 'Развлечения',
                'Описание': 'Посещение кинотеатра'
            },
            {
                'Дата операции': '2022-12-03',
                'Сумма операции с округлением': 3000,
                'Категория': 'Транспорт',
                'Описание': 'Оплата такси'
            },
            {
                'Дата операции': '2022-12-04',
                'Сумма операции с округлением': 4000,
                'Категория': 'Одежда',
                'Описание': 'Покупка одежды'
            },
            {
                'Дата операции': '2022-12-05',
                'Сумма операции с округлением': 5000,
                'Категория': 'Электроника',
                'Описание': 'Покупка смартфона'
            },
            {
                'Дата операции': '2022-12-06',
                'Сумма операции с округлением': 6000,
                'Категория': 'ЖКХ',
                'Описание': 'Оплата коммунальных услуг'
            }
        ]

    def test_top_5_transactions(self):
        # Тестируем работу функции при передаче корректного списка транзакций
        result = top_5_transactions(self.operations_list_dict)
        expected_result = [
            {
                "date": '2022-12-06',
                "amount": 6000,
                "category": 'ЖКХ',
                "description": 'Оплата коммунальных услуг'
            },
            {
                "date": '2022-12-05',
                "amount": 5000,
                "category": 'Электроника',
                "description": 'Покупка смартфона'
            },
            {
                "date": '2022-12-04',
                "amount": 4000,
                "category": 'Одежда',
                "description": 'Покупка одежды'
            },
            {
                "date": '2022-12-03',
                "amount": 3000,
                "category": 'Транспорт',
                "description": 'Оплата такси'
            },
            {
                "date": '2022-12-02',
                "amount": 2000,
                "category": 'Развлечения',
                "description": 'Посещение кинотеатра'
            }
        ]
        self.assertEqual(result, expected_result)

    def test_less_than_5_transactions(self):
        # Проверяем поведение функции, если количество транзакций меньше 5
        less_than_5_operations_list = self.operations_list_dict[:3]
        result = top_5_transactions(less_than_5_operations_list)
        expected_result = [
            {
                "date": '2022-12-03',
                "amount": 3000,
                "category": 'Транспорт',
                "description": 'Оплата такси'
            },
            {
                "date": '2022-12-02',
                "amount": 2000,
                "category": 'Развлечения',
                "description": 'Посещение кинотеатра'
            },
            {
                "date": '2022-12-01',
                "amount": 1000,
                "category": 'Еда',
                "description": 'Покупка продуктов'
            }
        ]
        self.assertEqual(result, expected_result)

    def test_empty_transactions_list(self):
        # Проверяем поведение функции при пустом списке транзакций
        empty_operations_list = []
        result = top_5_transactions(empty_operations_list)
        self.assertEqual(result, empty_operations_list)

import requests_mock

@pytest.fixture
def mock_user_settings_json():
    """Фикстура для создания файла user_settings.json с фиктивными данными."""
    with open('../user_settings.json', 'w') as file:
        json.dump({'user_currencies': ['USD']}, file)

@pytest.mark.usefixtures("mock_user_settings_json")
def test_currency_conversion_function_1(mock_user_settings_json):
    """Тестирование функции currency_conversion_function_1."""
    with requests_mock.Mocker() as m:
        # Фиктивный ответ API
        fake_response = {
            "result": 75.00,
            "info": {
                "quote": 75.00
            },
            "query": {
                "from": "USD",
                "to": "RUB",
                "amount": 1
            },
            "date": "2023-08-23T17:24:21Z",
            "timestamp": 1692887061
        }
        m.get('https://api.apilayer.com/currency_data/convert?to=RUB&from=USD&amount=1', json=fake_response)

        # Вызываем функцию
        result = currency_conversion_function_1()

        assert result == 75.00

def test_key_error_handling():
    """Проверка обработки исключения KeyError."""
    with pytest.raises(FileNotFoundError):
        # Убедимся, что файл user_settings.json отсутствует
        os.remove('../user_settings.json')
        currency_conversion_function_1()




@pytest.fixture
def mock_api_key_stock(monkeypatch):
    monkeypatch.setenv("API_KEY_STOCK", "fake_api_key")

@pytest.mark.usefixtures("mock_api_key_stock")
def test_stock_conversion_function(mock_api_key_stock):
    """Тестирование функции stock_conversion_function."""
    with requests_mock.Mocker() as m:
        # Фиктивный ответ API
        fake_response = [
            {"symbol": "AAPL", "price": "120.00"},
            {"symbol": "AMZN", "price": "2300.00"},
            {"symbol": "GOOGL", "price": "1400.00"},
            {"symbol": "MSFT", "price": "220.00"},
            {"symbol": "TSLA", "price": "700.00"}
        ]
        m.get(f' https://financialmodelingprep.com/api/v3/stock/list?apikey=uXUQXXcp70AqYJTiRpKUJV0HwAcAygzi', json=fake_response)

        # Вызываем функцию
        result = stock_conversion_function()

        assert result == [['AAPL', '120.00'], ['AMZN', '2300.00'], ['GOOGL', '1400.00'], ['MSFT', '220.00'], ['TSLA', '700.00']]

def test_key_error_handling_stock():
    """Проверка обработки исключения KeyError."""
    with pytest.raises(KeyError):
        # Убедимся, что переменная окружения отсутствует
        del os.environ["uXUQXXcp70AqYJTiRpKUJV0HwAcAygziK"]
        stock_conversion_function()




class TestBankingOperationsAnalysisFunc(unittest.TestCase):
    # Мокаем внешние функции
    @patch("src.views.greeting_by_current_time")
    @patch("src.views.time_interval_transactions")
    @patch("src.views.number_card")
    @patch("src.views.top_5_transactions")
    @patch("src.views.currency_conversion_function_1")
    @patch("src.views.currency_conversion_function_2")
    @patch("src.views.stock_conversion_function")
    @patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
    def test_banking_operations_analysis_func(self, mock_file, mock_stock_func, mock_currency_func_2, mock_currency_func_1, mock_top5, mock_number_card, mock_time_interval, mock_greeting):
        # Настройка моков
        mock_greeting.return_value = "Hello!"
        mock_time_interval.return_value = []
        mock_number_card.return_value = {}
        mock_top5.return_value = {}
        mock_currency_func_1.return_value = 1.0
        mock_currency_func_2.return_value = 1.0
        mock_stock_func.return_value = [("AAPL", 150), ("GOOGL", 1800), ("AMZN", 3000), ("MSFT", 280), ("FB", 200)]

        # Вызов тестируемой функции
        result = banking_operations_analysis_func([])

        # Проверка содержимого ответа
        expected_result = json.dumps({
            "greeting": "Hello!",
            "cards": {},
            "top_transactions": {},
            "currency_rates": [{"currency": "USD", "rate": 1.0},
                               {"currency": "EUR", "rate": 1.0}],
            "stock_prices": [{"stock": "AAPL", "price": 150},
                             {"stock": "GOOGL", "price": 1800},
                             {"stock": "AMZN", "price": 3000},
                             {"stock": "MSFT", "price": 280},
                             {"stock": "FB", "price": 200}]
        }, indent=4, ensure_ascii=False)

        self.assertEqual(result, expected_result)