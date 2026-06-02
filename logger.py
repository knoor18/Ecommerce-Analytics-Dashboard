import pandas as pd
from datetime import datetime

def save_log(username, action):

    try:
        logs = pd.read_csv("logs.csv")
    except:
        logs = pd.DataFrame(columns=["username","action","time"])

    new_log = pd.DataFrame({
        "username":[username],
        "action":[action],
        "time":[datetime.now()]
    })

    logs = pd.concat([logs,new_log])

    logs.to_csv("logs.csv",index=False)