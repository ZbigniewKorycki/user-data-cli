from process_users_data import data
from scripts import logging_setup

logger = logging_setup.setup_logging(__name__)


class Actions:

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.authenticated_user = False
        self.role = None
        self.authenticate_user()

    def authenticate_user(self):
        try:
            user = data[
                ((data["email"] == self.login) | (data["telephone_number"] == self.login)) & (
                        data["password"] == self.password)].to_dict(orient="records")[0]
        except IndexError:
            logger.info("Invalid login - Not authenticate user")
        else:
            logger.info("Valid login - authenticate user")
            self.authenticated_user = True
            self.role = user["role"]
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
        pass

    @authentication_required
    def find_similar_children_age(self):
        pass

    @admin_required
    def count_all_accounts(self):
        return len(data)

    @admin_required
    def get_oldest_account(self):
        pass

    @admin_required
    def get_users_children_grouped_by_age(self):
        pass
