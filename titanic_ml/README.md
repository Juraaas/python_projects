# Titanic Survival Prediction – Machine Learning Pipeline

This project demonstrates a complete machine learning workflow using the classic Titanic dataset.
The focus is not only on model performance, but on building a clean, modular and reproducible ML pipeline with correct evaluation methodology.

---

## Project goal

The goal of this project is to:
- perform exploratory data analysis (EDA),
- build a robust preprocessing pipeline,
- train and compare multiple classification models,
- evaluate models using cross-validation,
- tune the best-performing model using hyperparameter optimization.

---

## Dataset

The project uses the **Titanic dataset**, where the task is to predict passenger survival based on selected features such as age, gender and ticket class.

- `train.csv` contains the target variable `Survived`
- `test.csv` does not contain target labels and is used only for final predictions


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
│ ├── predict.py
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

3. **Baseline model comparison**
   - Multiple models are evaluated using **stratified cross-validation**:
     - Decision Tree
     - Logistic Regression
     - Random Forest
   - Evaluation metrics:
     - Accuracy
     - Precision
     - Recall
     - F1-score
   - Confusion matrix is analyzed for the best-performing baseline model

4. **Hyperparameter tuning**
   - Hyperparameter optimization is performed **only for the best baseline model**
   - GridSearchCV is used with stratified cross-validation
   - Model performance before and after tuning is compared using F1-score

5. **Final model training and prediction**
   - The tuned model is retrained on the full training dataset
   - Final predictions are generated for the unseen test dataset using the same preprocessing pipeline

---

## Model comparison

| Model               | Accuracy | Precision | Recall | F1-score |
|--------------------|----------|-----------|--------|----------|
| Random Forest      | ~0.82    | ~0.78     | ~0.74  | ~0.76    |
| Logistic Regression| ~0.79    | ~0.75     | ~0.69  | ~0.72    |
| Decision Tree      | ~0.80    | ~0.75     | ~0.73  | ~0.74    |

The **Random Forest** model achieved the best overall performance based on F1-score.

## Hyperparameter tuning results

Hyperparameter tuning using GridSearchCV resulted in an improved cross-validation F1-score
compared to the baseline Random Forest model, confirming the impact of optimized hyperparameters
on classification performance.

Confusion matrices are analyzed both before and after tuning to better understand changes
in model behavior.
---
## Feature importance

Feature importance analysis was performed using the tuned Random Forest model.
The results indicate that passenger gender, ticket class and fare have the strongest influence
on survival prediction, while age provides additional but less dominant signal.

This analysis helps interpret model decisions and highlights key factors driving predictions.
Feature importance visualization is implemented as a reusable utility function to keep the main experiment logic clean and modular.
---
## Next steps
Completed improvements:
- Hyperparameter tuning using GridSearchCV
- Feature importance analysis for the tuned model
---