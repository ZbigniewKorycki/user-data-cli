from argparse import Namespace, ArgumentParser

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
print("command:", args.command)
print("login:", args.login)
print("password:", args.password)


if args.command in functions:
    print(functions[args.command])

