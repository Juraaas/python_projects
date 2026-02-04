import pandas as pd
from src.train import train
from src.evaluate import evaluate
from src.models import MODELS
from src.visualization import plot_confusion_matrix

CSV_PATH = "data/raw/train.csv"

results = []
best_model = None
best_model_name = None
best_f1 = -1
best_confusion_matrix = None
best_report = None

for model_name, model_fn in MODELS.items():
    print(f"\nTraining model: {model_name}")

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

    # keep best model (based on F1-score)
    if metrics["f1"] > best_f1:
        best_f1 = metrics["f1"]
        best_model = model
        best_model_name = model_name
        best_confusion_matrix = metrics["confusion_matrix"]
        best_report = metrics["classification_report"]

results_df = (
    pd.DataFrame(results)
    .sort_values(by="f1", ascending=False)
    .reset_index(drop=True)
)

print("\nModel comparison:")
print(results_df)

print(f"\nBest model: {best_model_name}")
print(best_report)

plot_confusion_matrix(best_confusion_matrix, best_model_name)
