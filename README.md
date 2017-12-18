# OC_Projet_5

## Init all class structure
Add sql module and make a connection

## Parser les données du fichier csv
Mettre en place une méthode de mise à jour de la bdd  
Il faut :  
1. Une boucle qui lit chaque ligne de mon fichier csv  
2. Une méthode de mise en forme pour une ligne csv  
3. Une méthode pour sauvegarder les informations
4. Un attribut qui définis la qté max d'enregistrement par requête
5. Une Méthode lecture des données présentente en Base de données
6. Une méthode de comparaison entre les données de la DB et du CSV
7. Une méthode de mise à jour des informations en bdd
 
## Fonctionnalitées attendues
1. Lecture des catégories pour un nom donné
2. Lecture de la liste des aliments associés à une categorie
3. Lecture du meilleur aliment dans la liste des aliments des catégories  
de l'aliment sélectionné
4. Lecture de la liste des aliments sauvegardés de l'utilisateur
5. Sauvegarde d'un aliment pour un utilisateur

## Mise en place des méthodes
1. lecture de catégorie  
    -- display_food_category(self)
2. lecture des aliments  
    -- display_category_food_list(self)
3. lecture d'un aliment de substitution  
    -- display_food_description(self)
3. lecture des aliments pour un utilisateur  
    -- display_my_food_list(self)
5. sauvegarde  
    -- add_user_food(self)    