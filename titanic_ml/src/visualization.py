import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_confusion_matrix(cm, model_name: str):
    plt.figure(figsize=(5, 4))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False
    )
    plt.title(f"Confusion Matrix – {model_name}")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.show()

def plot_feature_importance(
    fi_df: pd.DataFrame,
    top_n: int = 10,
    title: str = "Top Feature Importances"
):
    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=fi_df.head(top_n),
        x="importance",
        y="feature"
    )
    plt.title(title)
    plt.tight_layout()
    plt.show()