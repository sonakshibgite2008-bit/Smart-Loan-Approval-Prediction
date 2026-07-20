import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# Dataset path
DATA_PATH = "dataset/load_dataset.csv"

# Load dataset
df = pd.read_csv(DATA_PATH)

print("Dataset Loaded Successfully")
print(df.head())
print("\nColumns:")
print(df.columns)


# Handle missing values
df = df.dropna()

# Encode categorical columns
encoder = LabelEncoder()

for column in df.select_dtypes(include="object").columns:
    df[column] = encoder.fit_transform(df[column])


print("\nAfter Encoding:")
print(df.head())


# Target column
TARGET = "Loan_Status"

if TARGET not in df.columns:
    print("Target column not found!")
    print("Available columns:", df.columns)
    exit()


# Features and target
X = df.drop(TARGET, axis=1)
y = df[TARGET]


# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Training
model.fit(X_train, y_train)


# Prediction
y_pred = model.predict(X_test)


# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)


# Save model
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/loan_model.pkl")

print("\nModel Saved Successfully ✅")