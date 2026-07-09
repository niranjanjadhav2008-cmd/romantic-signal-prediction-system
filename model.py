import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import joblib
from sklearn.metrics import accuracy_score
from feature_map import (feature_map,convert_quiz_answers,negative_key_inversions)

# STEP 1 — LOAD DATA

df = pd.read_csv("Speed Dating Data.csv", encoding="latin-1")
columns_needed = ["like","attr","fun","prob","shar","sinc","int_corr"]
df = df[columns_needed].copy()
print("=" * 40)
print("STEP 1 — DATA LOADED")
print("=" * 40)
print(f"Shape before cleaning : {df.shape}")

# STEP 2 — CLEAN DATA

df = df.dropna()
print(f"Shape after cleaning  : {df.shape}")
print("\nColumn ranges:")
for col in columns_needed:
    print(f"  {col:10s} → min: {df[col].min():.2f}  max: {df[col].max():.2f}  mean: {df[col].mean():.2f}")

# STEP 3 — FEATURES AND TARGET

FEATURE_COLUMNS = ["attr", "fun", "prob", "shar", "sinc", "int_corr"]
X = df[FEATURE_COLUMNS]
y = df["like"]
print("\n" + "=" * 40)
print("STEP 3 — FEATURES & TARGET")
print("=" * 40)
print(f"Features shape : {X.shape}")
print(f"Target shape   : {y.shape}")
print(f"Target range   : {y.min():.1f} to {y.max():.1f}")
print(f"Target mean    : {y.mean():.2f}")

# STEP 4 — SCALE FEATURES

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

print("\n" + "=" * 40)
print("STEP 4 — SCALING DONE")
print("=" * 40)
print("All features scaled to 0-1 range")
print(f"int_corr before: {X['int_corr'].min():.2f} to {X['int_corr'].max():.2f}")
print(f"int_corr after : {X_scaled[:, 5].min():.2f} to {X_scaled[:, 5].max():.2f}")

# STEP 5 — TRAIN TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y,test_size=0.2,random_state=42)
print("\n" + "=" * 40)
print("STEP 5 — DATA SPLIT")
print("=" * 40)
print(f"Training samples : {len(X_train)}")
print(f"Testing samples  : {len(X_test)}")

# STEP 6 — TRAIN MODEL

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=6,
    random_state=42
)

model.fit(X_train, y_train)

print("\n" + "=" * 40)
print("STEP 6 — MODEL TRAINED ✅")
print("=" * 40)

# ─────────────────────────────────────────
# STEP 7 — EVALUATE
# ─────────────────────────────────────────

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2  = r2_score(y_test, y_pred)
print("\n" + "=" * 40)
print("STEP 7 — EVALUATION")
print("=" * 40)
print(f"Mean Absolute Error : {mae:.2f} points (out of 10)")
print(f"R2 Score            : {r2:.2f}  (1.0 = perfect, 0.0 = random)")
if r2 >= 0.6:
    print("✅ Model quality : GOOD")
elif r2 >= 0.4:
    print("⚠️  Model quality : ACCEPTABLE")
else:
    print("❌ Model quality : WEAK — check feature mapping")

# STEP 8 — FEATURE IMPORTANCE CHART

importances    = model.feature_importances_
indices        = np.argsort(importances)[::-1]
sorted_features = [FEATURE_COLUMNS[i] for i in indices]
sorted_importances = [importances[i] for i in indices]
plt.figure(figsize=(8, 5))
bars = plt.bar(sorted_features, sorted_importances, color="#ff4b91")
plt.title("Feature Importance — What Predicts Compatibility?",fontsize=14, fontweight="bold")
plt.xlabel("Feature")
plt.ylabel("Importance Score")
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.show()
print("\n" + "=" * 40)
print("STEP 8 — FEATURE IMPORTANCE")
print("=" * 40)
print(f"🏆 Most important : {sorted_features[0]}")
print(f"📉 Least important: {sorted_features[-1]}")
for feat, imp in zip(sorted_features, sorted_importances):
    bar = "█" * int(imp * 50)
    print(f"  {feat:10s} {bar} {imp:.3f}")

# STEP 9 — SAVE MODEL & SCALER

joblib.dump(model,  "model.pkl")
joblib.dump(scaler, "scaler.pkl")
print("\n" + "=" * 40)
print("STEP 9 — SAVED ✅")
print("=" * 40)
print("model.pkl  saved")
print("scaler.pkl saved")
# STEP 10 — TEST WITH FAKE QUIZ ANSWERS

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
    for col in ["attr", "fun", "prob", "shar", "sinc", "int_corr"]:
        values = column_values[col]
        if values:
            feature_vector.append(np.mean(values))
        else:
            feature_vector.append(5.0) 
    return np.array(feature_vector).reshape(1, -1)
def predict_compatibility(quiz_answers):
    feature_vector        = quiz_to_feature_vector(quiz_answers)
    feature_vector_scaled = scaler.transform(pd.DataFrame(feature_vector, columns=["attr","fun","prob","shar","sinc","int_corr"]))
    predicted_like_score  = model.predict(feature_vector_scaled)[0]
    predicted_like_score  = np.clip(predicted_like_score, 1, 10)
    ml_percentage = ((predicted_like_score - 1) / 9) * 100
    return predicted_like_score, ml_percentage


# ── Test 1: All positive answers
positive_answers = {
    "eye_contact"        : "often",
    "compliments"        : "often",
    "personal_questions" : "often",
    "shares_personal"    : "often",
    "accepts_plan"       : "often",
    "initiates"          : "often",
    "chat_daily"         : 1,
    "close_friends"      : 1,
    "physical_closeness" : 5,
    "emoji_freq"         : "often",
    "message_length"     : 5,
    "fast_replies"       : "often",
    "insta_friends"      : 1,
    "likes_stories"      : "often",
    "seen_ignore"        : "never",
    "dry_replies"        : "never",
}

# ── Test 2: All negative answers
negative_answers = {
    "eye_contact"        : "never",
    "compliments"        : "never",
    "personal_questions" : "never",
    "shares_personal"    : "never",
    "accepts_plan"       : "never",
    "initiates"          : "never",
    "chat_daily"         : 0,
    "close_friends"      : 0,
    "physical_closeness" : 0,
    "emoji_freq"         : "never",
    "message_length"     : 0,
    "fast_replies"       : "never",
    "insta_friends"      : 0,
    "likes_stories"      : "never",
    "seen_ignore"        : "often",
    "dry_replies"        : "often",
}

# ── Test 3: Mixed answers
mixed_answers = {
    "eye_contact"        : "often",
    "compliments"        : "rarely",
    "personal_questions" : "often",
    "shares_personal"    : "never",
    "accepts_plan"       : "rarely",
    "initiates"          : "often",
    "chat_daily"         : 1,
    "close_friends"      : 0,
    "physical_closeness" : 2,
    "emoji_freq"         : "often",
    "message_length"     : 3,
    "fast_replies"       : "rarely",
    "insta_friends"      : 1,
    "likes_stories"      : "rarely",
    "seen_ignore"        : "rarely",
    "dry_replies"        : "often",
}

print("\n" + "=" * 40)
print("STEP 10 — PREDICTION TESTS")
print("=" * 40)
for label, answers in [("All Positive", positive_answers),("All Negative", negative_answers),("Mixed",mixed_answers)]:
    score, pct = predict_compatibility(answers)
    print(f"\n📊 {label}")
    print(f"   Like Score : {score:.2f} / 10")
    print(f"   ML Score   : {pct:.1f}%")
y_pred_rounded = np.round(y_pred)
y_test_rounded = np.round(y_test)

strict_accuracy = accuracy_score(y_test_rounded, y_pred_rounded)
within_1_point  = np.mean(np.abs(y_pred - y_test) <= 1.0) * 100

print(f"Strict Accuracy  : {strict_accuracy*100:.1f}%")
print(f"Within 1 point   : {within_1_point:.1f}%")
