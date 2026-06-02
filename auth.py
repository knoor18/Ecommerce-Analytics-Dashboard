import pandas as pd

def authenticate(username, password):

    users = pd.read_csv("users.csv")

    users["username"] = users["username"].astype(str)
    users["password"] = users["password"].astype(str)

    user = users[
        (users["username"] == str(username)) &
        (users["password"] == str(password))
    ]

    if not user.empty:
        return True, user.iloc[0]["role"]

    return False, None