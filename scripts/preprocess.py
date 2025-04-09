import pandas as pd
import numpy as np
import re
import string
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def preprocess_data(df):
    df = df.drop(['cwe_name'], axis=1, errors='ignore')
    df = df.dropna()

    # One-hot encode categorical variables
    df = pd.get_dummies(df, columns=['access_vector', 'access_authentication'], drop_first=True)

    # Label encode object columns (except text)
    
    def preprocess_text(text):
        text = text.lower()  # Lowercase
        text = re.sub(r'\d+', '', text)  # Remove digits
        text = re.sub(f"[{re.escape(string.punctuation)}]", '', text)  # Remove punctuation
        text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
        return text

    # Apply to all summaries
    df['summary'] = df['summary'].astype(str).apply(preprocess_text)
    
    text_col = 'summary'
    for col in df.columns:
        if df[col].dtype == 'object' and col != text_col:
            df[col] = df[col].astype('category').cat.codes
    for col in df.columns:
        if df[col].dtype == 'bool':
            df[col] = df[col].astype(int)

    text_data = df[text_col].values
    structured_data = df.drop(columns=['cvss', text_col]).values
    y = df['cvss'].values

    # Normalize structured data
    scaler = StandardScaler()
    structured_data_scaled = scaler.fit_transform(structured_data)

    # Tokenize summary text
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(text_data)
    sequences = tokenizer.texts_to_sequences(text_data)
    padded_sequences = pad_sequences(sequences, maxlen=100, padding='post', truncating='post')

    return text_data, structured_data_scaled, padded_sequences, y, tokenizer, scaler
