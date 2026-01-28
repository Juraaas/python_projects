import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
matplotlib.use('TkAgg')

df = pd.read_csv('train.csv')

#print(df.head(5))
#print(df.info())
#print(df.describe())

df.drop('Cabin', axis=1, inplace=True)
df['Age'] = df['Age'].fillna(df['Age'].mean())
df['Age'] = df['Age'].astype(int)

missing_values = df.isnull().sum()
#print(missing_values)

df_copy = df.dropna()
#print(df_copy.describe())
#print(df_copy.info())

'''sns.countplot(x='Survived', data=df_copy)
plt.show()

plt.hist(df_copy['Age'], bins=20, color='skyblue', edgecolor='black')
plt.title('Rozkład wieku pasażerów')
plt.xlabel('Wiek')
plt.ylabel('Liczba pasażerów')
plt.show()

sns.boxplot(x='Pclass', y='Fare', data=df_copy)
plt.title('Cena biletu w zależności od klasy')
plt.show()

sns.scatterplot(x='Age', y='Fare', hue='Survived', data=df_copy)
plt.title('Bilet vs wiek pasażera')
plt.show()

#corr = df_copy.corr()
#sns.heatmap(corr, annot=True, cmap='coolwarm')
#plt.title('Macierz korelacji')
#plt.show()

sns.countplot(x='Survived', hue='Sex', data=df_copy)
plt.title('Przeżycie w zależności od płci')
plt.show()'''

df_encoded = pd.get_dummies(df_copy, columns=['Sex'], drop_first=True)

X = df_encoded[['Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'Sex_male']]
y = df_encoded['Survived']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

