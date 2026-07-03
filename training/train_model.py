import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

df = pd.read_csv("data/privacy_dataset.csv")

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])

model.fit(df["text"], df["label"])

os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/privacy_model.pkl"
)

print("Model trained successfully!")