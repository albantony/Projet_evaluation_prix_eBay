## **Analyse des tendances de prix des ordinateurs portables sur eBay**
*Projet réalisé par Antony Albergne, Adam Belkhatir et Noéline Casteil dans le cadre du cours Python pour la Data Science, 2024*

## **1. Objectif du projet**

L'objectif de notre projet est de fournir une analyse des prix des ordinateurs portables sur la plateforme eBay afin de comprendre les mécanismes de fixation des prix en fonction des caractéristiques des produits. Étant donné qu’eBay est une plateforme où les vendeurs fixent eux-mêmes les prix, nous souhaitions explorer si ces prix reflètent effectivement les caractéristiques décrites dans les annonces. En effet, lorsque un utilisateur navigue sur le site la première information qu'il aperçoit est souvent le prix du produit ; dès lors cela soulève la question suivante : dans quelle mesure peut-on utiliser ce prix pour déduire des informations sur la qualité et les caractéristiques du produit ?
Nous avons choisi de nous concentrer sur une catégorie précise : les ordinateurs portables du marché français. Ainsi, les produits analysés présentent des spécificités communes et les prix sont soumis aux mêmes conditions économiques et géopolitiques. 

## **2. Source des données**

Nous nous sommes appuyés pour ce projet sur plusieurs types de données :
- Les données de l'API eBay : La majeure partie des données que nous utilisons sont issues de l'API eBay qui nous a permis de récolter les différentes annonces du site ainsi que des informations sur ces produits. Le recours à l'API était très long et limité à 5000 appels par jour ce qui nous a poussé à effectuer des appels quotidiens et à stocker les données au format CSV (`data3.csv`) afin de bénéficier d'une quantité suffisante de données. 
Afin de rajouter des données il est toutefois possible de faire appel à l'API et compléter notre fichier CSV à l'aide du fichier `data.py` en suivant au préalable la procédure d'authentification suivante : (Nous avons réduit le nombre d'appels à 100 pour rendre l'attente moins longue) 

### **Comment se connecter pour accéder à l'API d'Ebay**
L'API eBay nécessite une authentification pour chaque utilisateur dont vous trouverez la procédure ci-dessous : 
1. Créez un compte developer en suivant ce lien : https://developer.ebay.com/signin?tab=register
2. Après environ 24h vous pourrez trouver vos identifiants dans la partie **Application Keysets** 
3. Les identifiants qui nous intéressent se trouvent dans la partie Production ; il faut faire une demande pour y avoir accès. 
La partie création de compte est ensuite terminée. Il faut maintenant rentrer les identifiants dans notre code. 

### **Etapes à suivre pour faire fonctionner notre code**
1. Créez un fichier `.env` à la racine du projet (ajoutez le dans le .gitignore pour ne pas push vos identifiants)
2. Ajoutez les lignes suivantes en remplaçant par vos identifiants personnels :
   APP_ID=your_app_id
   CERT_ID=your_cert_id
3. Dans un terminal, entrez `pip install python-dotenv` pour pouvoir exécuter `collect.py` et `data.py`
4. Ensuite veuillez vous référer à notre notebook pour comprendre le déroulement. 

- Les données issues de scraping : Nous avons voulu créer un classement moyen de popularité des marques d'high-tech afin d'expliquer au mieux les écarts de prix entre les différents ordinateurs portables. Nous avons pour cela dû collecter les classements de plusieurs sites internet pour en faire une moyenne. Cette procédure est contenue dans le fichier `scraping.py` du dossier `src` et détaillée dans le notebook final. 

## **3. Présentation du rendu**

Notre rapport final se situe dans le fichier `notebook.ipynb`. À l'intérieur de ce fichier vous trouverez tous les éléments (fonctions, graphiques, analyses...) qui nous ont permis de parvenir à une conclusion concernant la fixation des prix des ordinateurs portables sur la plateforme eBay. 
Dans le dossier `src`se trouvent les fichiers annexes appelés dans le notebook final. 
Nous avons également regroupé dans un fichier `requirements.txt`les modules utiles tout au long du projet que nous importons au début du notebook. 

## **4. Conclusion**


