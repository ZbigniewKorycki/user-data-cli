from argparse import Namespace, ArgumentParser
from actions import Actions
import re
from users_data_utils import UsersDataFormatter

parser = ArgumentParser()
PHONE_VALIDATION_PATTERN = r"[\d]{9}"
EMAIL_VALIDATION_PATTERN = UsersDataFormatter.EMAIL_VALIDATION_PATTERN

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
        email_validation = re.match(EMAIL_VALIDATION_PATTERN, login, re.IGNORECASE)
    except TypeError:
        pass
    else:
        if email_validation:
            return login
    return "Invalid Login"


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
        action.print_user_children()

    elif args.command == "find-similar-children-by-age":
        action.find_users_with_similar_children_by_age()

    elif args.command == "create-database":
        action.create_database()
else:
    print("Unrecognized command")
