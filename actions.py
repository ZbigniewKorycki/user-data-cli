from merger import data


class Actions:

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.authenticated_user = False
        self.role = None

    @staticmethod
    def admin_required(func):
        def wrapper(user):
            if user.role == "admin":
                return func(user)
            else:
                print("You do not have permission to perform this action.")
            return wrapper

    def authenticate_user(self):
        user = data[
            ((data["email"] == self.login) | (data["telephone_number"] == self.login)) & (
                    data["password"] == self.password)].to_dict(orient="records")[0]
        if user:
            self.authenticated_user = True
            self.role = user["role"]
        else:
            raise Exception("Invalid Login")

    def get_user_children(self):
        pass

    def find_similar_children_age(self):
        pass

    @admin_required
    def get_all_accounts(self):
        pass

    @admin_required
    def get_oldest_account(self):
        pass

    @admin_required
    def get_users_children_grouped_by_age(self):
        pass
