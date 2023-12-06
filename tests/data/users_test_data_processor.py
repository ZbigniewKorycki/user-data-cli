from users_data_processor import process_users_data
import os

paths = [
    os.path.join(os.path.dirname(__file__), *path.split("/"))
    for path in ["final_test_data.csv"]
]
test_final_users_data = process_users_data(paths)
