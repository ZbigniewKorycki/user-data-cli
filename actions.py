from process_users_data import data
from scripts import logging_setup
import itertools

logger = logging_setup.setup_logging(__name__)


class Actions:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.authenticated_user = False
        self.role = None
        self.user_data = None
        self.authenticate_user()

    def authenticate_user(self):
        try:
            user = data[
                (
                        (data["email"] == self.login)
                        | (data["telephone_number"] == self.login)
                )
                & (data["password"] == self.password)
                ].to_dict(orient="records")[0]
        except IndexError:
            logger.info("Invalid login - Not authenticate user")
        else:
            logger.info("Valid login - authenticate user")
            self.authenticated_user = True
            self.role = user["role"]
            self.user_data = user
            logger.info(f"role: {self.role}")

    @staticmethod
    def admin_required(func):
        def wrapper(self, *args, **kwargs):
            logger.info("Inside admin required")
            logger.info(f"{func}")
            logger.info(f"self.role: {self.role}")
            if self.role == "admin" and self.authenticated_user:
                return func(self, *args, **kwargs)
            else:
                print("Invalid Login")
                logger.info("Invalid login - admin required")

        return wrapper

    @staticmethod
    def authentication_required(func):
        def wrapper(self, *args, **kwargs):
            logger.info("Inside authentication_required")
            if self.authenticated_user:
                return func(self, *args, **kwargs)
            else:
                logger.info("Invalid login - authentication required")

        return wrapper

    @authentication_required
    def get_user_children(self):
        children_info = self.user_data["children"]
        if isinstance(children_info, list):
            children_info.sort(key=lambda x: x["name"])
            for child in children_info:
                print(f"{child['name']}, {child['age']}")
        else:
            print(f"{children_info['name']}, {children_info['age']}")

    @authentication_required
    def find_users_with_similar_children_by_age(self):
        user_children_age = [int(child["age"]) for child in self.user_data["children"]]
        users_with_children = data[data["children"].notna()]
        users_with_similar_children_age = users_with_children[
            users_with_children["children"].apply(
                lambda x: (any(child["age"] in user_children_age for child in x if isinstance(child, dict))))]
        users_similar = users_with_similar_children_age.to_dict(orient="records")
        for user in users_similar:
            children_sorted = sorted(user["children"], key=lambda x: x["name"])
            print(f"{user['firstname']}, {user['telephone_number']}: {children_sorted}")

    @admin_required
    def print_all_accounts(self):
        print(len(data))

    @admin_required
    def print_oldest_account(self):
        oldest_account = data.sort_values(by="created_at").to_dict(orient="records")[0]
        if oldest_account is not None:
            print(
                f"name: {oldest_account['firstname']}\n"
                f"email_address: {oldest_account['email']}\n"
                f"created_at: {oldest_account['created_at']}"
            )

    @admin_required
    def group_children_by_age(self):
        # implement data[data["children"].notna()]
        children_data = data["children"].to_list()
        filtered_children_without_none = [
            child for child in children_data if child is not None
        ]
        children = []
        for user_children in filtered_children_without_none:
            if isinstance(user_children, list):
                for child in user_children:
                    children.append(int(child["age"]))
            else:
                children.append(int(user_children["age"]))
        sorted_data = sorted(children)
        grouped_data = sorted(
            [
                {"age": key, "count": len(list(group))}
                for key, group in itertools.groupby(sorted_data)
            ],
            key=lambda x: x["count"],
        )
        for child in grouped_data:
            print(f"age: {child['age']}, count: {child['count']}")
