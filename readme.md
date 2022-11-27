# API pour requeter et ajouter des entrées à une base de données

## justification des choix : 
Le set de donné choisi est: https://www.kaggle.com/vardan95ghazaryan/top-250-football-transfers-from-2000-to-2018.  
Ce set contient 4700 transfert de joueurs de football.  
Chaque transfert est identifié par 9 ou 10 attribut (une colonne contient parfois des donnée, d'autres fois c'est un NaN).  
La structure de ce set de donné est idéale pour être stockée dans une table d'une base de donnée SQL.

## Fonctionnement :
Le premier conteneur qui sera lancé est celui qui contient la base de donnée MySQL.  
Le deuxiéme conteneur sera lancé par la suite pour créer la table de donnée , et la charger les données dedans si ceci n'est pas déja fait.  
Le troisiéme conteneur est celui qui contient l'API , et qui sera lancé à la suite du deuxiéme conteneur.  

## Terminaisons de l'API :
L'api contient deux terminaisons:   
* Une terminaison (post) pour ajouter une ligne à la base de données ( je n'ai pas fait de beaucoup de contrôles sur les données à insérer).  
* Une terminaison pour requeter la base de donnée.  

## Utilisation : 
Il suffit de lancer docker compose en utilisant le fichier compose dans la source de ce repository.  


