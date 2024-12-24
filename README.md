## **Documentation du projet**

L'objectif de notre projet est de fournir une analyse des prix des ordinateurs portables sur la plateforme eBay afin de comprendre les mécanismes de fixation des prix en fonction des caractéristiques des produits. 

## Comment se connecter pour accéder à l'API d'Ebay
L'API eBay nécessite une authentification pour chaque utilisateur dont vous trouverez la procédure ci-dessous : 
1. Créez un compte developer en suivant ce lien : https://developer.ebay.com/signin?tab=register
2. Après environ 24h vous pourrez trouver vos identifiants dans la partie **Application Keysets** 
3. Les identifiants qui nous intéressent se trouvent dans la partie Production ; il faut faire une demande pour y avoir accès. 
La partie création de compte est ensuite terminée. Il faut maintenant rentrer les identifiants dans notre code. 

## Etapes à suivre pour faire fonctionner notre code
1. Créez un fichier `.env` à la racine du projet (ajoutez le dans le .gitignore pour ne pas push vos identifiants)
2. Ajoutez les lignes suivantes en remplaçant par vos identifiants personnels :
   APP_ID=your_app_id
   CERT_ID=your_cert_id
3. Dans un terminal, entrez `pip install python-dotenv` pour pouvoir exécuter **collect.py**
4. Ensuite veuillez vous référer à notre notebook pour comprendre le déroulement. Celui-ci se nomme notebook.ipynb et détaille tout notre cheminement. 
