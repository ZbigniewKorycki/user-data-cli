from argparse import Namespace, ArgumentParser
from actions import Actions

parser = ArgumentParser()

parser.add_argument("command", type=str, help="enter command")
parser.add_argument("--login", type=str, help="input user login")
parser.add_argument("--password", type=str, help="input user password")
args: Namespace = parser.parse_args()


if args.command == "print-all-accounts":
    action = Actions(login=args.login, password=args.password)
    result = action.count_all_users()
    print(result)

elif args.command == "print-oldest-account":
    action = Actions(login=args.login, password=args.password)
    oldest_account = action.get_oldest_account()
    if oldest_account is not None:
        print(
            f"name: {oldest_account['firstname']}\n"
            f"email_address: {oldest_account['email']}\n"
            f"created_at: {oldest_account['created_at']}")

elif args.command == "group-by-age":
    action = Actions(login=args.login, password=args.password)
    result = action.get_users_children_grouped_by_age()
    for child in result:
        print(f"age: {child['age']}, count: {child['count']}")

elif args.command == "print-children":
    action = Actions(login=args.login, password=args.password)
    action.get_user_children()


elif args.command == "find-similar-children-by-age":
    pass
elif args.command == "create-database":
    pass
else:
    print("Unrecognized command")
