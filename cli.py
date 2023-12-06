from argparse import Namespace, ArgumentParser
from actions import Actions
import re
from users_data_utils import UsersDataFormatter

PHONE_VALIDATION_PATTERN = r"[\d]{9}"
EMAIL_VALID_PATTERN = UsersDataFormatter.EMAIL_VALID_PATTERN

commands_list = [
    "print-all-accounts",
    "print-oldest-account",
    "group-by-age",
    "print-children",
    "find-similar-children-by-age",
    "create-database",
]


def validate_login(login):
    try:
        phone_validation = re.match(PHONE_VALIDATION_PATTERN, login)
    except TypeError:
        pass
    else:
        if phone_validation:
            return login
    try:
        email_validation = re.match(EMAIL_VALID_PATTERN, login, re.IGNORECASE)
    except TypeError:
        pass
    else:
        if email_validation:
            return login
    return "Invalid Login"


def main():
    parser = ArgumentParser()
    parser.add_argument("command", type=str, help="enter command")
    parser.add_argument("--login", type=validate_login, help="input user login")
    parser.add_argument("--password", type=str, help="input user password")
    args: Namespace = parser.parse_args()

    if args.command in commands_list:
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
        print("Unrecognized command")


if __name__ == "__main__":
    main()
