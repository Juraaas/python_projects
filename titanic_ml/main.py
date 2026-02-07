import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import (
    cross_val_predict,
    StratifiedKFold,
    GridSearchCV
)
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from src.train import train
from src.predict import predict
from src.models import MODELS, RANDOM_FOREST_PARAM_GRID
from src.visualization import plot_confusion_matrix, plot_feature_importance
from src.data_processing import FEATURE_COLUMNS, TARGET_COLUMN

TRAIN_PATH = "data/raw/train.csv"
TEST_PATH = "data/raw/test.csv"


df_train = pd.read_csv(TRAIN_PATH)
X = df_train[FEATURE_COLUMNS]
y = df_train[TARGET_COLUMN]

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

results = []

best_model_fn = None
best_model_name = None
best_f1 = -1
best_confusion_matrix = None
best_report = None

for model_name, model_fn in MODELS.items():
    print(f"\nEvaluating model: {model_name}")

    model = model_fn()

    y_pred = cross_val_predict(
        model,
        X,
        y,
        cv=cv
    )

    acc = accuracy_score(y, y_pred)
    prec = precision_score(y, y_pred)
    rec = recall_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    cm = confusion_matrix(y, y_pred)
    report = classification_report(y, y_pred)

    results.append({
        "model": model_name,
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1
    })

    if f1 > best_f1:
        best_f1 = f1
        best_model_fn = model_fn
        best_model_name = model_name
        best_confusion_matrix = cm
        best_report = report


results_df = (
    pd.DataFrame(results)
    .sort_values(by="f1", ascending=False)
    .reset_index(drop=True)
)

print("\nModel comparison (Baseline CV):")
print(results_df)

print(f"\nBest baseline model: {best_model_name}")
print(best_report)

plot_confusion_matrix(best_confusion_matrix, f"{best_model_name} (baseline)")

baseline_f1 = best_f1

grid = GridSearchCV(
    estimator=best_model_fn(),
    param_grid=RANDOM_FOREST_PARAM_GRID,
    scoring="f1",
    cv=cv,
    n_jobs=-1
)

grid.fit(X, y)

best_grid_model = grid.best_estimator_
grid_f1 = grid.best_score_

print("\nGridSearch results:")
print(f"Baseline CV F1: {baseline_f1:.3f}")
print(f"Tuned CV F1:    {grid_f1:.3f}")

print("\nBest parameters found:")
print(grid.best_params_)

y_pred_gs = cross_val_predict(
    best_grid_model,
    X,
    y,
    cv=cv
)

cm_gs = confusion_matrix(y, y_pred_gs)
report_gs = classification_report(y, y_pred_gs)

print("\nClassification report after GridSearch:")
print(report_gs)

plot_confusion_matrix(
    cm_gs,
    f"{best_model_name} (after GridSearch)"
)

final_model = best_grid_model
final_model.fit(X, y)

rf_model = final_model.named_steps["classifier"]
preprocessor = final_model.named_steps["preprocessing"]

feature_names = preprocessor.get_feature_names_out()
importances = rf_model.feature_importances_

fi_df = (
    pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    })
    .sort_values(by="importance", ascending=False)
)

print("\nTop feature importances:")
print(fi_df.head(10))

plot_feature_importance(
    fi_df,
    top_n=10,
    title="Top 10 Feature Importances - Tuned Random Forest",
    save_path="assets/feature_importance.png"
)

test_predictions = predict(
    final_model,
    TEST_PATH
)

print("\nSample predictions:")
print(test_predictions[:10])

MODEL_PATH = "models/tuned_random_forest.pkl"

joblib.dump(final_model, MODEL_PATH)

print(f"\nFinal model saved to: {MODEL_PATH}")
