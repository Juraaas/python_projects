import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.train import train
from src.evaluate import evaluate
from src.models import MODELS

CSV_PATH = "data/raw/train.csv"

results = []

for model_name, model_fn in MODELS.items():
    print(f"Training model: {model_name}")

    model, X_test, y_test = train(
        model_fn=model_fn,
        csv_path=CSV_PATH
    )

    metrics = evaluate(model, X_test, y_test)

    results.append({
        "model": model_name,
        "accuracy": metrics["accuracy"],
        "precision": metrics["precision"],
        "recall": metrics["recall"],
        "f1": metrics["f1"]
    })

results_df = pd.DataFrame(results).sort_values(
    by="f1", ascending=False
)

print("\nModel comparison:")
print(results_df)