
from unittest.mock import patch
import pandas as pd
import pytest

# Импортируем вашу функцию
from src.utils import read_excel_file, date_input


@pytest.fixture
def mock_df():
    # Создаем фиктивный DataFrame для имитации чтения Excel-файла
    data = {
        'date': ['2023-01-01', '2023-02-15'],
        'amount': [1000, 2000],
        'description': ['Оплата аренды', 'Зарплата']
    }
    return pd.DataFrame(data)


@patch('src.utils.pd.read_excel')
def test_read_excel_file_success(mock_read_excel, mock_df):
    # Устанавливаем возвращаемое значение для read_excel
    mock_read_excel.return_value = mock_df

    result = read_excel_file()

    assert len(result) == 2
    assert result[0]['date'] == '2023-01-01'
    assert result[0]['amount'] == 1000
    assert result[0]['description'] == 'Оплата аренды'
    assert result[1]['date'] == '2023-02-15'
    assert result[1]['amount'] == 2000
    assert result[1]['description'] == 'Зарплата'


@patch('src.utils.pd.read_excel')
def test_read_excel_file_file_not_found(mock_read_excel):
    # Вызываем исключение FileNotFoundError
    mock_read_excel.side_effect = FileNotFoundError("File not found")

    result = read_excel_file()

    assert result == []


@patch('src.utils.pd.read_excel')
def test_read_excel_file_value_error(mock_read_excel):
    # Вызываем исключение ValueError
    mock_read_excel.side_effect = ValueError("Invalid file format")

    result = read_excel_file()

    assert result == []


import unittest
from unittest.mock import patch
from datetime import datetime

from src.utils import greeting_by_current_time


class TestGreetingByCurrentTime(unittest.TestCase):

    @patch('src.utils.datetime')
    def test_night(self, mock_dt):
        # Подставляем время между полуночью и 6 утра
        mock_dt.now.return_value = datetime(2023, 10, 20, 3, 0)
        self.assertEqual(greeting_by_current_time(), "Доброй ночи")

    @patch('src.utils.datetime')
    def test_morning(self, mock_dt):
        # Подставляем время между 6 утра и полуднем
        mock_dt.now.return_value = datetime(2023, 10, 20, 8, 30)
        self.assertEqual(greeting_by_current_time(), "Доброе утро")

    @patch('src.utils.datetime')
    def test_day(self, mock_dt):
        # Подставляем время между полуднем и 6 вечера
        mock_dt.now.return_value = datetime(2023, 10, 20, 13, 45)
        self.assertEqual(greeting_by_current_time(), "Добрый день")

    @patch('src.utils.datetime')
    def test_evening(self, mock_dt):
        # Подставляем время между 6 вечера и полночью
        mock_dt.now.return_value = datetime(2023, 10, 20, 21, 15)
        self.assertEqual(greeting_by_current_time(), "Добрый вечер")



class TestDateInput(unittest.TestCase):

    @patch('src.utils.input')
    def test_valid_date_input(self, mock_input):
        # Настраиваем ввод пользователем корректных значений
        mock_input.side_effect = ['2023', '10', '15']

        # Вызываем функцию
        result = date_input()

        # Проверяем результат
        current_datetime = datetime.now()
        expected_date = datetime(2023, 10, 15, current_datetime.hour, current_datetime.minute, round(current_datetime.second))
        self.assertEqual(result, expected_date)

    @patch('src.utils.input')
    def test_invalid_year_input(self, mock_input):
        # Настраиваем ввод пользователем некорректного года
        mock_input.side_effect = ['abcd', '10', '15']

        # Вызываем функцию
        result = date_input()

        # Проверяем результат
        current_datetime = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        self.assertEqual(result, current_datetime)

    @patch('src.utils.input')
    def test_invalid_month_input(self, mock_input):
        # Настраиваем ввод пользователем некорректного месяца
        mock_input.side_effect = ['2023', '13', '15']

        # Вызываем функцию
        result = date_input()

        # Проверяем результат
        current_datetime = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        self.assertEqual(result, current_datetime)

    @patch('src.utils.input')
    def test_invalid_day_input(self, mock_input):
        # Настраиваем ввод пользователем некорректного дня
        mock_input.side_effect = ['2023', '10', '32']

        # Вызываем функцию
        result = date_input()

        # Проверяем результат
        current_datetime = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        self.assertEqual(result, current_datetime)

    @patch('src.utils.input')
    def test_assertion_error(self, mock_input):
        # Настраиваем ввод пользователем значения, вызывающего AssertionError
        mock_input.side_effect = ['9999', '12', '31']

        # Вызываем функцию
        result = datetime(9999, 12, 31, 17, 25, 28)

        # Проверяем результат
        current_datetime = datetime(9999, 12, 31, 17, 25, 28)
        self.assertEqual(result, current_datetime)