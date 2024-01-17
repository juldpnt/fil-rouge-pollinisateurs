# Importation of the necessary libraries
import pandas as pd
from pytaxize import Ids
from pytaxize.itis import hierarchy_full

tableau = pd.DataFrame(columns=['Ordre', 'Super famille', 'Famille', 'Sous famille', 'Genre', 'Espèce'])

def get_id(name):
    """
    Fonction permettant d'obtenir l'id d'une espèce à partir de son nom
    """
    # Enregistrement du nom de l'espèce
    nom = Ids(name)
    nom.itis()
    # Extraction de l'id de l'espèce
    for item in nom.ids[nom.name[0]]:
        if item['name'] == nom.name[0]:
            id = int(item['id'])
            break
    return id

def get_hierarchie(id):
    return hierarchy_full(id, as_dataframe=True)

def get_famille(name, hierarchie):
    """
    """
    # Obtention de l'ordre, de la famille, du genre et de l'espèce
    order_name, super_family_name, family_name, sub_family_name, genus_name, species_name = '', '', '', '', '', ''
    for item in hierarchie:
        if item['parentName'] != name:
            if item['rankName'] == 'Order':
                order_name = item['taxonName']
            elif item['rankName'] == 'Superfamily':
                super_family_name = item['taxonName']
            elif item['rankName'] == 'Family':
                family_name = item['taxonName']
            elif item['rankName'] == 'Subfamily':
                sub_family_name = item['taxonName']
            elif item['rankName'] == 'Genus':
                genus_name = item['taxonName']
            elif item['rankName'] == 'Species':
                species_name = item['taxonName']
        else:
            break
    # Création d'un tableau avec les informations
    new_data = {'Ordre': order_name, 
                'Super famille': super_family_name,
                'Famille': family_name, 
                'Sous famille': sub_family_name,
                'Genre': genus_name, 
                'Espèce': species_name}
    return new_data

def get_classification(name):
    """
    Fonction permettant d'obtenir la classification d'une espèce
    """
    # Obtention de l'id de l'espèce
    id = get_id(name)
    # Obtention de la hiérarchie de l'espèce
    hierarchie = get_hierarchie(id).to_dict('records')
    # Obtention de la famille de l'espèce
    classification = get_famille(name, hierarchie)
    return classification

def get_classification_double(name1, name2):
    """
    Fonction permettant d'obtenir la classification lorsque deux
    espèces sont indiquées
    """
    # Obtention de l'id de l'espèce
    id1 = get_id(name1)
    id2 = get_id(name2)
    # Obtention de la hiérarchie de l'espèce
    hierarchie1 = get_hierarchie(id1)
    hierarchie2 = get_hierarchie(id2)
    hierarchie = hierarchie1.merge(hierarchie2, how='inner')
    last_name = hierarchie.iloc[-1]['taxonName']
    hierarchie = hierarchie.to_dict('records')
    # Obtention de la famille de l'espèce
    classification = get_famille(last_name, hierarchie)
    return classification

def unique_df_values(df, column):
    """
    Fonction permettant d'obtenir les valeurs uniques d'un dataframe
    """
    # Obtention des valeurs uniques de la colonne d'intérêt
    unique = df[column].unique()
    unique = list(unique)
    # Séparation au niveau des virgules
    for i in range(len(unique)):
        unique[i] = unique[i].replace(' et autres', '')
        unique[i] = unique[i].split(', ')
    return unique

def get_classification_df(df, column):
    """
    Fonction permettant d'obtenir la classification d'un dataframe
    """
    # Obtention des valeurs uniques de la colonne d'intérêt
    unique = unique_df_values(df, column)
    # Obtention de la classification pour chaque espèce
    size = len(unique)
    dictionary = {}
    for i in range(size):
        length = len(unique[i])
        if length == 1:
            print(unique[i][0])
            classification = get_classification(unique[i][0])
            dictionary[unique[i][0]] = classification
        elif length == 2:
            print(unique[i][0], unique[i][1])
            classification = get_classification_double(unique[i][0], unique[i][1])
            dictionary[unique[i][0]] = classification
        else:
            print('Erreur')
    return dictionary