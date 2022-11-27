# API pour requeter et ajouter des entrée à une base de données

## justification des choix : 
Le set de donné choisi est: https://www.kaggle.com/vardan95ghazaryan/top-250-football-transfers-from-2000-to-2018
ce set contient 4700 transfert de joueurs de football.
chaque transfert est identifié par 9 ou 10 attribut ( une colonne est parfois peuplée parfois non)
la structure de ce set de donné est idéale pour être stocké dans une table d'une base de donnée SQL.

## Fonctionnement :
le premier conteneur qui sera lancé est celui qui contient la base de donnée MySQL
le deuxiéme conteneur sera lancé par la suite pour créer la table de donnée , et la populer si ceci n'est pas déja fait.
le troisiéme conteneur est celui qui contient l'API

## Terminaisons de l'API :
L'api contient deux méthodes  : 
une terminaison pour ajouter une entrée  à la base de données ( j'ai pas fait de beaucoup de contrôle sur les données à insérer)
une terminaison pour requeter la base de donnée 

## Utilisation : 
Il suffirait de lancer docker compose en utilisant le fichier compose dans la source de ce repository


