import joblib

model = joblib.load(
    "models/privacy_model.pkl"
)

def analyze_text(text):

    prediction = model.predict([text])[0]

    if prediction == 1:
        return "Sensitive"
    else:
        return "Safe"