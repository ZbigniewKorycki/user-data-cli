import re


class TelephoneFormatter:

    @staticmethod
    def format_number(number: str) -> str:
        return re.sub(r"\s|\+48|\(48\)|^00", "", number)


class EmailValidator:

    @staticmethod
    def is_valid(email: str) -> bool:
        if re.match(r"(^[^@]+@[^@]+\.[a-zA-Z\d]{1,4}$)", email):
            return True


