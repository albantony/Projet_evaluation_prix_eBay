import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import load_data

df = load_data('data_cleaned.csv')

# On regroupe par prix et condition
prix_group = df.groupby(['Marque', 'Condition'])['Prix'].mean().reset_index()

# Afficher les moyennes des prix par marque et état
print(prix_group)

# Heatmap
pivot_table = prix_group.pivot(index='Marque', columns='Condition', values='Prix')

# Tracer la heatmap
plt.figure(figsize=(12,8))
sns.heatmap(pivot_table, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Moyenne des Prix par Marque et État")
plt.show()
