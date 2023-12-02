from argparse import Namespace, ArgumentParser
from actions import Actions

parser = ArgumentParser()

parser.add_argument("command", type=str, help="enter command")
parser.add_argument("--login", type=str, help="input user login")
parser.add_argument("--password", type=str, help="input user password")
args: Namespace = parser.parse_args()

if args.command == "print-all-accounts":
    action = Actions(login=args.login, password=args.password)
    result = action.count_all_accounts()
    print(result)
elif args.command == "print-oldest-account":
    pass
elif args.command == "group-by-age":
    pass
elif args.command == "print-children":
    pass
elif args.command == "find-similar-children-by-age":
    pass
elif args.command == "create-database":
    pass
else:
    print("Unrecognized command")
