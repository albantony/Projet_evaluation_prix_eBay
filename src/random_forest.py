import pandas as pd
import numpy as np
from utils import load_data
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Charger les données
df = load_data('data_cleaned.csv')

# Encodage des colonnes catégoriques avant l'imputation
df = pd.get_dummies(df, columns=['Couleur','Marque', 'Condition'], drop_first=True)
df['Month'] = pd.to_datetime(df['Date de publication']).dt.month
df['December'] = df['Month'].apply(lambda x: 1 if x == 12 else 0)

# Supprimer les colonnes inutiles
df = df.drop(columns=['ID','Date de publication','Month'])

# Imputation des valeurs manquantes par KNN
imputer = KNNImputer(n_neighbors=5)
df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

# Définir les features et la target
X = df_imputed.drop(columns=['Prix'])
y = np.log(df_imputed['Prix'])  # Transformation logarithmique de la variable cible

# Normalisation des caractéristiques
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Modèle de forêt aléatoire
rf_model = RandomForestRegressor(random_state=42)

# Recherche en grille pour l'optimisation des hyperparamètres
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Meilleurs hyperparamètres
print("Meilleurs hyperparamètres:", grid_search.best_params_)

# Prédictions sur l'ensemble de test avec le meilleur modèle
y_pred_rf = grid_search.best_estimator_.predict(X_test)

# Évaluation du modèle de forêt aléatoire
print("Forêt aléatoire")
print("R² Score:", r2_score(y_test, y_pred_rf))
print("MAE:", mean_absolute_error(y_test, y_pred_rf))
print("RMSE:", mean_squared_error(y_test, y_pred_rf))