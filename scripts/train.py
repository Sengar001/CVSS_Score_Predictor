import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Dropout, Concatenate
from tensorflow.keras.callbacks import EarlyStopping

from scripts.preprocess import preprocess_data

def build_model(text_input_shape, struct_input_shape):
    # Text input branch
    text_input = Input(shape=(text_input_shape,))
    x1 = Embedding(input_dim=1000, output_dim=64, input_length=text_input_shape)(text_input)
    x1 = LSTM(64)(x1)

    # Structured input branch
    struct_input = Input(shape=(struct_input_shape,))
    x2 = Dense(64, activation='relu')(struct_input)
    x2 = Dropout(0.3)(x2)

    # Combine
    combined = Concatenate()([x1, x2])
    x = Dense(64, activation='relu')(combined)
    x = Dropout(0.3)(x)
    output = Dense(1, activation='linear')(x)

    model = Model(inputs=[text_input, struct_input], outputs=output)
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def train():
    df = pd.read_csv("data/cve111.csv")
    text_data, structured_data_scaled, padded_sequences, y, tokenizer, scaler = preprocess_data(df)

    # Train-test split
    X_text_train, X_text_test, X_struct_train, X_struct_test, y_train, y_test = train_test_split(
        padded_sequences, structured_data_scaled, y, test_size=0.2, random_state=42
    )

    # Model
    model = build_model(X_text_train.shape[1], X_struct_train.shape[1])
    model.fit(
        [X_text_train, X_struct_train], y_train,
        validation_split=0.2,
        epochs=10,
        batch_size=32,
        callbacks=[EarlyStopping(patience=3, restore_best_weights=True)]
    )

    # Evaluation
    y_pred = model.predict([X_text_test, X_struct_test]).flatten()
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")

    # Save model and tools
    os.makedirs("models", exist_ok=True)
    model.save("models/model.keras")
    joblib.dump(tokenizer, "models/tokenizer.pkl")
    joblib.dump(scaler, "models/scaler.pkl")

if __name__ == "__main__":
    train()
