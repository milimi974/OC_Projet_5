def test(self):
    csv_foods = []

    args = {
        'PK_id': 0,
        'code': '0000066655',
        'link': 'http://www.yoso.fr',
        'name': "Moutarde à l'Ancienne",
        'uri': "Moutarde à l'Ancienne",
        'description': "Les ingrédients sont listés par ordre d'importance (quantité)."
                       "Liste des ingrédients : Eau, graines de moutarde, vinaigre d'alcool,"
                       "sel, vin blanc (contient sulfites), sucre, épices, acidifiant : "
                       "acide citrique, conservateur : disulfite de potassium."
                       "Substances ou produits provoquant des allergies ou intolérances : "
                       "Moutarde, Anhydride sulfureux et sulfites",
        'level': 'a',
        'created': "2017-11-05 14:45:20",
        'modified': "2017-11-05 14:45:20",
        'shops': "Grand Frais,Auchan",
        'categories': "Epicerie,Condiments,Sauces,Moutardes,Moutardes à l'ancienne",
    }

    csv_foods.append(Food(args))
    args = {
        'PK_id': 0,
        'code': '0000066656',
        'link': 'http://www.yoso.fr',
        'name': "Mousse Au Café - Nova - 216 g (4 * 54 g)",
        'uri': "Mousse Au Café - Nova - 216 g (4 * 54 g)",
        'description': "Les ingrédients sont listés par ordre d'importance (quantité)."
                       "Liste des ingrédients : Eau, graines de moutarde, vinaigre d'alcool,"
                       "sel, vin blanc (contient sulfites), sucre, épices, acidifiant : "
                       "acide citrique, conservateur : disulfite de potassium."
                       "Substances ou produits provoquant des allergies ou intolérances : "
                       "Moutarde, Anhydride sulfureux et sulfites",
        'level': 'b',
        'created': "2017-11-05 14:45:20",
        'modified': "2017-11-05 14:45:20",
        'shops': "Grand Frais,Auchan,Leclerc",
        'categories': "Epicerie,Condiments,Sauces,Moutardes,Mousses lactées,Mousses sucrées,Mousses au café",
    }

    csv_foods.append(Food(args))
    Main.__create_foods(csv_foods)