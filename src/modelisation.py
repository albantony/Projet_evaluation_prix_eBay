# Suppression des colonnes inutiles
import pandas as pd
import numpy as np
from utils import load_data
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


df = load_data('data_cleaned.csv')
df = df.drop(columns=['ID','Date de publication'])

# Remplir les valeurs manquantes
# Remplir les valeurs manquantes
df['Stockage'].fillna(df['Stockage'].median(), inplace=True)
df['PPI'].fillna(df['PPI'].median(), inplace=True)
df['RAM'].fillna(df['RAM'].median(), inplace=True)
df['Taille écran'].fillna(df['Taille écran'].median(), inplace=True)
df['Rang'].fillna(df['Rang'].median(), inplace=True)

# Remplacer les valeurs manquantes dans Condition par 'Occasion'
df['Condition'] = df['Condition'].fillna('Occasion')


# Encodage des colonnes catégoriques
df = pd.get_dummies(df, columns=['Condition', 'Marque', 'Couleur'], drop_first=True)

# Vérification
print(df.info())


# Définir les features et la target
X = df.drop(columns=['Prix'])
y = df['Prix']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialisation du modèle
model = LinearRegression()

# Entraînement
model.fit(X_train, y_train)


# Prédictions sur l'ensemble de test
y_pred = model.predict(X_test)

# Évaluation
print("R² Score:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", mean_squared_error(y_test, y_pred, squared=False))

coefficients = pd.DataFrame({'Feature': X.columns, 'Coefficient': model.coef_})
print(coefficients)
