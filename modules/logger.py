import pandas as pd
import os
from datetime import datetime

LOG_FILE = "logs/privacy_logs.csv"

os.makedirs("logs", exist_ok=True)

if not os.path.exists(LOG_FILE):
    pd.DataFrame(
        columns=["Time", "Command", "Status"]
    ).to_csv(LOG_FILE, index=False)


def save_log(command, status):

    try:
        data = pd.read_csv(LOG_FILE)
    except:
        data = pd.DataFrame(
            columns=["Time", "Command", "Status"]
        )

    new_row = pd.DataFrame({
        "Time": [datetime.now()],
        "Command": [command],
        "Status": [status]
    })

    data = pd.concat(
        [data, new_row],
        ignore_index=True
    )

    data.to_csv(LOG_FILE, index=False)