import pandas as pd
import numpy as np
from utils import load_data
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Charger les données
df = load_data('data_cleaned.csv')

# Encodage des colonnes catégoriques avant l'imputation
df = pd.get_dummies(df, columns=['Marque', 'Condition','Couleur'], drop_first=True)
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

# Initialisation du modèle
model = LinearRegression()

# Entraînement du modèle
model.fit(X_train, y_train)

# Prédictions sur l'ensemble de test
y_pred = model.predict(X_test)

# Afficher les coefficients du modèle
coefficients = pd.DataFrame(model.coef_, X.columns, columns=['Coefficient'])
print(coefficients.round(3))

# Évaluation du modèle
print("R² Score:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", mean_squared_error(y_test, y_pred))

"""
Coefficient
RAM                            0.239
Stockage                       0.106
Taille écran                   0.130
Rang                          -0.020
PPI                            0.288
Couleur_blanc                 -0.031
Couleur_bleu                   0.020
Couleur_gris                   0.050
Couleur_marron                -0.034
Couleur_noir                  -0.001
Couleur_rose                   0.027
Couleur_rouge                 -0.001
Couleur_vert                   0.009
Marque_Alienware               0.038
Marque_Apple                   0.204
Marque_Asus                    0.015
Marque_Chuwi                  -0.008
Marque_Clevo                   0.017
Marque_Dell                    0.038
Marque_Fujitsu                 0.001
Marque_GPD                     0.024
Marque_Gigabyte               -0.000
Marque_Google                 -0.004
Marque_HP                      0.009
Marque_Huawei                  0.009
Marque_Jumper                 -0.000
Marque_LG                      0.016
Marque_Lenovo                  0.030
Marque_MSI                     0.043
Marque_Medion                 -0.010
Marque_Microsoft               0.008
Marque_Panasonic               0.091
Marque_Razer                   0.019
Marque_Samsung                -0.011
Marque_Sony                    0.024
Marque_Teclast                 0.005
Marque_Toshiba                -0.050
Condition_Occasion            -0.251
Condition_Ouvert              -0.001
Condition_Parfait état        -0.066
Condition_Très bon état       -0.147
Condition_État correct        -0.128
December                       0.024
R² Score: 0.5758412764853613
MAE: 0.38413452085748034
RMSE: 0.25176115006955174
"""