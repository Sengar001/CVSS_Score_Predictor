import numpy as np
from tensorflow.keras.models import load_model
import pickle
import pandas as pd
from scripts.preprocess import preprocess_data

MODEL_PATH = "models/model.keras"
TOKENIZER_PATH = "models/tokenizer.pkl"
SCALER_PATH = "models/scaler.pkl"
TEST_DATA_PATH = "data/cve111.csv"  # or wherever your test set is

def evaluate_model():
    print("[INFO] Loading model...")
    model = load_model(MODEL_PATH)

    print("[INFO] Loading tokenizer and scaler...")
    with open(TOKENIZER_PATH, 'rb') as f:
        tokenizer = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)

    print("[INFO] Loading and preprocessing test data...")
    df = pd.read_csv(TEST_DATA_PATH)
    X, y = preprocess_data(df, tokenizer, scaler)

    print("[INFO] Running evaluation...")
    loss, mae = model.evaluate(X, y)
    
    print(f"[RESULT] Loss: {loss}, MAE: {mae}")

if __name__ == "__main__":
    evaluate_model()