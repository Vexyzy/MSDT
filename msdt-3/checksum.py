"""
В этом модуле обитают функции, необходимые
для автоматизированной проверки результатов ваших трудов.
"""

import json
import hashlib
from typing import List

# import csv package for work with csv file
from csv import DictReader

# import validator to checking input fields using regexes
from extensions import validator


CSV_PATH = "./20.csv"
JSON_PATH = "./result.json"
OPTION = 20


def get_numbers_with_mistakes(csv_path: str):
    """This method return numbers where format is wrong in some of fields

    Args:
        csv_path (str): path to csv file
    Returns:
        numbers_with_mistake (List[int]): numbers with format of data
    """
    numbers_with_mistakes = []

    with open(csv_path, newline="", encoding="utf-16") as csv_file:
        dict_reader = DictReader(csv_file, delimiter=";")
        for row_num, row in enumerate(dict_reader):
            for pattern, data in row.items():
                if not validator.validate_data(pattern, data):
                    numbers_with_mistakes.append(row_num - 1)

    return numbers_with_mistakes


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.

    ВНИМАНИЕ, ВАЖНО! Чтобы сумма получилась корректной, считать, что первая
    строка с данными csv-файла имеет номер 0
    Другими словами: В исходном csv 1я строка - заголовки столбцов,
    2я и остальные - данные.
    Соответственно, считаем что у 2 строки файла номер 0, у 3й - номер
    1 и так далее.

    :param row_numbers: список целочисленных номеров строк csv-файла,
    на которых были найдены ошибки валидации
    :return: md5 хеш для проверки через github action
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode("utf-8")).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Метод для сериализации результатов лабораторной пишите сами.
    Вам нужно заполнить данными - номером варианта и контрольной суммой - файл,
    лежащий в папке с лабораторной.
    Файл называется, очевидно, result.json.

    ВНИМАНИЕ, ВАЖНО! На json натравлен github action, который проверяет
    корректность выполнения лабораторной.
    Так что не перемещайте, не переименовывайте и не изменяйте его структуру,
    если планируете успешно сдать лабу.

    :param variant: номер вашего варианта
    :param checksum: контрольная сумма, вычисленная через calculate_checksum()
    """
    result = {"variant": variant, "checksum": checksum}
    with open(JSON_PATH, "w", encoding="utf-8") as json_file:
        json.dump(result, json_file)


def main():
    """Entry point"""
    numbers_with_mistakes = get_numbers_with_mistakes(CSV_PATH)
    check_sum = calculate_checksum(numbers_with_mistakes)
    serialize_result(OPTION, check_sum)


if __name__ == "__main__":
    main()
