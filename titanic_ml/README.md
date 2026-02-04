# Titanic Survival Prediction – Machine Learning Pipeline

This project demonstrates a complete machine learning workflow using the classic Titanic dataset.
The focus is not only on model performance, but on building a clean, modular and reproducible ML pipeline.

---

## Project goal

The goal of this project is to:
- perform exploratory data analysis (EDA),
- build a robust preprocessing pipeline,
- train and compare multiple classification models,
- evaluate model performance using appropriate metrics.

---

## Dataset

The project uses the **Titanic dataset**, where the task is to predict passenger survival based on selected features such as age, gender and ticket class.

Target variable:
- `Survived` (0 = did not survive, 1 = survived)

---

## Project structure
```
titanic_ml/
├── data/
│ └── raw/
│ └── train.csv
│ └── test.csv
│
├── notebooks/
│ └── eda.ipynb
│
├── src/
│ ├── data_processing.py
│ ├── models.py
│ ├── train.py
│ ├── evaluate.py
│ ├── visualization.py
│
├── main.py
├── requirements.txt
└── README.md
```
---

## Machine Learning workflow

1. **Exploratory Data Analysis**
   - Performed in a Jupyter notebook (`notebooks/eda.ipynb`)
   - Analysis of feature distributions, missing values and relationships with the target

2. **Data preprocessing**
   - Implemented using `scikit-learn` Pipelines and `ColumnTransformer`
   - Numerical features:
     - missing values imputed with mean
   - Categorical features:
     - missing values imputed with most frequent value
     - one-hot encoding applied

3. **Models**
   The following models are trained using the same preprocessing pipeline:
   - Decision Tree
   - Logistic Regression
   - Random Forest

4. **Evaluation**
   - Models are evaluated on a held-out test set
   - Metrics used:
     - Accuracy
     - Precision
     - Recall
     - F1-score
   - Confusion matrix is analyzed for the best-performing model

---

## Model comparison

| Model               | Accuracy | Precision | Recall | F1-score |
|--------------------|----------|-----------|--------|----------|
| Random Forest      | ~0.82    | ~0.78     | ~0.74  | ~0.76    |
| Logistic Regression| ~0.80    | ~0.79     | ~0.67  | ~0.72    |
| Decision Tree      | ~0.78    | ~0.72     | ~0.70  | ~0.71    |

The **Random Forest** model achieved the best overall performance based on F1-score.

---
## Next steps

Planned improvements:
- Hyperparameter tuning using GridSearchCV
- Feature importance analysis
- Additional feature engineering
---