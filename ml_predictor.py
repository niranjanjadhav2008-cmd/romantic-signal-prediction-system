# ml_predictor.py
import numpy as np
import pandas as pd
import joblib
from feature_map import (
    feature_map,
    convert_quiz_answers,
    negative_key_inversions
)
# Load model and scaler once when file is imported
model  = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
FEATURE_COLUMNS = ["attr", "fun", "prob", "shar", "sinc", "int_corr"]
def quiz_to_feature_vector(quiz_answers):
    column_values = {"attr": [],"fun": [],"prob": [],"shar": [],"sinc": [],"int_corr": [],}
    for key, value in quiz_answers.items():
        if key in negative_key_inversions:
            converted = convert_quiz_answers(key, value)
            if key == "seen_ignore":
                column_values["prob"].append(converted)
            elif key == "dry_replies":
                column_values["fun"].append(converted)
        elif key in feature_map:
            dataset_col = feature_map[key]
            converted   = convert_quiz_answers(key, value)
            column_values[dataset_col].append(converted)
    feature_vector = []
    for col in FEATURE_COLUMNS:
        values = column_values[col]
        feature_vector.append(np.mean(values) if values else 5.0)
    return np.array(feature_vector).reshape(1, -1)
def predict_ml_compatibility(quiz_answers):
    feature_vector = quiz_to_feature_vector(quiz_answers)
    feature_df = pd.DataFrame(feature_vector,columns=FEATURE_COLUMNS)
    feature_scaled       = scaler.transform(feature_df)
    predicted_like_score = model.predict(feature_scaled)[0]
    predicted_like_score = np.clip(predicted_like_score, 1, 10)
    ml_percentage        = ((predicted_like_score - 1) / 9) * 100
    return round(ml_percentage, 2)