import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping

from preprocess import preprocess_data
from train import build_model

def retrain(new_data_path):
    df = pd.read_csv(new_data_path)
    text_data, structured_data_scaled, padded_sequences, y, tokenizer, scaler = preprocess_data(df)

    X_text_train, X_text_test, X_struct_train, X_struct_test, y_train, y_test = train_test_split(
        padded_sequences, structured_data_scaled, y, test_size=0.2, random_state=42
    )

    model = build_model(X_text_train.shape[1], X_struct_train.shape[1])
    model.fit(
        [X_text_train, X_struct_train], y_train,
        validation_split=0.2,
        epochs=10,
        batch_size=32,
        callbacks=[EarlyStopping(patience=3, restore_best_weights=True)]
    )

    y_pred = model.predict([X_text_test, X_struct_test]).flatten()
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"[RETRAIN] Mean Squared Error: {mse}")
    print(f"[RETRAIN] R^2 Score: {r2}")

    model.save("models/model.keras")
    joblib.dump(tokenizer, "models/tokenizer.pkl")
    joblib.dump(scaler, "models/scaler.pkl")

if __name__ == "__main__":
    retrain("data/new_data.csv")
