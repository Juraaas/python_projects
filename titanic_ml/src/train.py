import pandas as pd
from sklearn.model_selection import train_test_split
from src.models import decision_tree_model
from src.data_processing import FEATURE_COLUMNS, TARGET_COLUMN

def load_data(csv_path: str) -> pd.DataFrame:
    """
    Load raw dataset from CSV.
    """
    return pd.read_csv(csv_path)


def split_features_target(df: pd.DataFrame):
    """
    Split dataset into features (X) and target (y).
    """
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    return X, y


def train(model_fn, csv_path: str, test_size: float = 0.2, random_state: int = 42):
    """
    Train ML model pipeline and return trained model and test data.
    """
    df = load_data(csv_path)
    X, y = split_features_target(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    model = model_fn()
    model.fit(X_train, y_train)

    return model, X_test, y_test
