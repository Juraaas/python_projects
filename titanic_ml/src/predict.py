import pandas as pd
from src.data_processing import FEATURE_COLUMNS

def predict(model, csv_path: str):
    """
    Generate predictions for test dataset.
    """
    df = pd.read_csv(csv_path)
    X = df[FEATURE_COLUMNS]

    predictions = model.predict(X)
    return predictions