"""
class validator
This module validate data for some regex pattern
"""

# Import match for matching strings to regex
from re import match

patterns = {
    "http_status": r"^[1-5]\d{2}\s[A-Za-z]",
    "email": r"^\w+@\w+(\.\w+)+$",
    "inn": R"^\d{12}$",
    "passport": r"^\d{2}\s\d{2}\s\d{6}$",
    "ipv4": (
        r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}"
        + r"([09]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    ),
    "latitude": r"^[-\d]\d*(\.\d+)?$",
    "rgb": r"^#[\dA-Fa-f]{6}$",
    "isbn": r"(^\d{3}-)?\d-\d{5}-\d{3}-\d$",
    "uuid": (
        r"^[\dafA-F]{8}-[\da-fA-F]{4}-" + r"[\da-fA-F]{4}-[\da-fA-F]{4}-[\da-fA-F]{12}$"
    ),
    "time": r"^([0-1][0-9]|[2][0-3]):[0-5][0-9]:[0-5][0-9]\.[0-9]{6}$",
    "telephone": r"^\+7-\(\d{3}\)-\d{3}(-\d{2}){2}$",  # телефончик
    "height": r"^[0-2]\.\d{2}$",  # рост
    "snils": r"^\d{11}$",  # снилс
    "identifier": r"^\d{2}-\d{2}\/\d{2}$",  # id
    "occupation": r"^[A-Za-zА-Яа-я- ]+$",  # профессия
    "longitude": r"^[(\-\d)\d]\d*\.\d*$",  # долгота
    "blood_type": r"^([ABO]|AB)[\−\+]$",  # кровушка
    "issn": r"^\d{4}\-\d{4}$",  # issn
    "locale_code": r"^[A-Za-z]+(\-[A-Za-z]+)*$",  # locale code
    "date": r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$",  # data
}

MAX_LONGITUDE = 180
MIN_LONGITUDE = -180

MIN_LATITUDE = -90
MAX_LATITUDE = 90


class Validator:
    """
    This class has methods for validating data.
    """

    def __init__(self):
        pass

    def validate_data(self, regex_pattern: str, input_data: str) -> bool:
        """This method validate data for pattern

        Args:
            regex_pattern (str): choosen pattern
            input_data (str): data for validation

        Returns:
            bool: True if data in right format, else false.
        """
        # check if pattern in patterns
        if regex_pattern not in patterns:
            return False

        # return is data in right format
        # match return class <'re.Match'> if format is true
        # and return <NoneType> else
        # thats wy we use (is not None)
        return match(patterns[regex_pattern], input_data) is not None
