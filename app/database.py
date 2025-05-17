# Simulated in-memory database using a list
users_db = []

def add_user(user_data: dict):
    users_db.append(user_data)

def find_user_by_username(username: str):
    return next((user for user in users_db if user["username"] == username), None)

def find_user_by_email(email: str):
    return next((user for user in users_db if user["email"] == email), None)
