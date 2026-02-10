import pandas as pd
import numpy as np

def load_data(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)

def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleaning transactional data based on EDA findings.
    """
    df = df.copy()
    df = df.dropna(subset=["CustomerID"])
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    return df

def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds RFM features from cleaned transactional data.
    """
    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = (
        df.groupby("CustomerID")
        .agg({
            "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
            "InvoiceNo": "nunique",
            "TotalPrice": "sum"
        })
        .rename(columns={
            "InvoiceDate": "Recency",
            "InvoiceNo": "Frequency",
            "TotalPrice": "Monetary"
        })
        .reset_index()
    )
    return rfm

def transform_rfm(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Apply transformations to RFM features.
    """
    rfm = rfm.copy()
    rfm["Frequency"] = np.log1p(rfm["Frequency"])
    rfm["Monetary"] = np.log1p(rfm["Monetary"])

    return rfm

def preprocess_data(csv_path: str) -> pd.DataFrame:
    """
    Full preprocessing pipeline:
    raw data -> cleaned transactions -> RFM -> transformed RFM
    """
    df = load_data(csv_path)
    df_clean = clean_transactions(df)
    rfm = build_rfm(df_clean)
    rfm_transformed = transform_rfm(rfm)

    return rfm_transformed