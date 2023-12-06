from argparse import Namespace, ArgumentParser
from actions import Actions
import re
from typing import Optional

PHONE_VALID_PATTERN = r"[\d]{9}"
EMAIL_VALID_PATTERN = r"(^[^@]+@[^@\.]+\.[a-z\d]{1,4}$)"
PASSWORD_VALID_PATTERN_LENGTH = r".{6,24}"

commands_list = [
    "print-all-accounts",
    "print-oldest-account",
    "group-by-age",
    "print-children",
    "find-similar-children-by-age",
    "create-database",
]


def validate_login(login: str) -> Optional[str]:
    try:
        re.match(PHONE_VALID_PATTERN, login)
    except TypeError:
        pass
    else:
        return login
    try:
        re.match(EMAIL_VALID_PATTERN, login, re.IGNORECASE)
    except TypeError:
        return None
    else:
        return login


def validate_password(password: str) -> Optional[str]:
    try:
        re.match(PASSWORD_VALID_PATTERN_LENGTH, password)
    except TypeError:
        return None
    else:
        return str(password)


def main():
    parser = ArgumentParser(description="Command-line interface for user actions")
    parser.add_argument(
        "command", type=str, help="enter command: " + ", ".join(commands_list)
    )
    parser.add_argument("--login", type=validate_login, help="input user login")
    parser.add_argument(
        "--password", type=validate_password, help="input user password"
    )
    args: Namespace = parser.parse_args()

    if args.command in commands_list:
        if (
            validate_login(args.login) is not None
            and validate_password(args.password) is not None
        ):
            action = Actions(login=args.login, password=args.password)

            if args.command == "print-all-accounts":
                action.print_all_accounts()

            elif args.command == "print-oldest-account":
                action.print_oldest_account()

            elif args.command == "group-by-age":
                action.group_children_by_age()

            elif args.command == "print-children":
                action.print_children()

            elif args.command == "find-similar-children-by-age":
                action.find_similar_children_by_age()

            elif args.command == "create-database":
                action.create_database()
        else:
            print("Invalid Login")
    else:
        print("Unrecognized Command")


if __name__ == "__main__":
    main()
