from flask import Flask, render_template, request
from modules.privacy_detector import analyze_text
from modules.logger import save_log

import pandas as pd
import os

app = Flask(__name__)

LOG_FILE = "logs/privacy_logs.csv"


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    status = ""
    advice = ""

    if request.method == "POST":

        command = request.form["command"]
        status = analyze_text(command)

        save_log(command, status)

        if status == "Sensitive":
            advice = """
            This command may expose sensitive information.
            Avoid sharing passwords, bank details,
            OTP codes, or personal data.
            """
            result = "⚠️ Privacy Risk Detected"
        else:
            advice = """
            This command appears safe.
            No privacy risks were detected.
            """
            result = "✅ Safe Command"

    total = 0
    safe = 0
    sensitive = 0

    if os.path.exists(LOG_FILE):

        df = pd.read_csv(LOG_FILE)

        total = len(df)

        safe = len(
            df[df["Status"] == "Safe"]
        )

        sensitive = len(
            df[df["Status"] == "Sensitive"]
        )

        risk_percent = 0
        if total > 0:
            
            risk_percent = round(
                (sensitive / total) * 100
            )

    return render_template(
    "index.html",
    result=result,
    status=status,
    total=total,
    safe=safe,
    sensitive=sensitive,
    risk_percent=risk_percent,
    advice=advice
)


@app.route("/logs")
def logs():

    df = pd.read_csv(
        LOG_FILE
    )

    logs_data = df.to_dict(
        orient="records"
    )

    return render_template(
        "logs.html",
        logs=logs_data
    )


if __name__ == "__main__":
    app.run(debug=True)