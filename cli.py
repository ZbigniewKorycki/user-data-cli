from argparse import Namespace, ArgumentParser
import main


functions = {
    "print-all-accounts": "print all accounts",
    "print-oldest-account": "print oldest account",
    "group-by-age": "group by age",
    "print-children": "print children",
    "find-similar-children-by-age": "find similar children by age",
    "create-database": "create database"
}

parser = ArgumentParser()

parser.add_argument("command", type=str, help="enter command")
parser.add_argument("--login", type=str, help="input user login")
parser.add_argument("--password", type=str, help="input user password")
args: Namespace = parser.parse_args()
# print("command:", args.command)
# print("login:", args.login)
# print("password:", args.password)


if args.command in functions:
    result_user = main.find_user(args.login, args.password).to_dict(orient="records")
    for user in result_user:
        print(f"name: {user['firstname']}")
        print(f"email_address: {user['email']}")
        print(f"created_at: {user['created_at']}")


