# Importation of the necessary libraries
from pytaxize import Ids
from pytaxize.itis import hierarchy_full

def get_id(name):
    """
    Fonction permettant d'obtenir l'id d'une espèce à partir de son nom
    """
    # Enregistrement du nom de l'espèce
    nom = Ids(name)
    nom.itis()
    id = 1
    # Extraction de l'id de l'espèce
    for item in nom.ids[nom.name[0]]:
        if item['name'] == nom.name[0]:
            id = item['id']
            break
    return id

def get_hierarchie(id):
    return hierarchy_full(id, as_dataframe=True)

def find_id(id):
    return isinstance(id, str)

def get_famille(name, hierarchie):
    """
    Fonction permettant d'obtenir un dictionnaire avec la 
    classification du nom renseigné
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

def find_unknown_name(name):
    """
    Fonction permettant d'identifier si un nom ne possède pas d'id
    Cela signifie qu'il n'est pas dans les databases de pytaxize
    """
    # Obtention de l'id de l'espèce
    id = get_id(name)
    return not find_id(id)

def get_classification(name):
    """
    Fonction permettant d'obtenir la classification d'une espèce
    """
    # Obtention de l'id de l'espèce
    id = get_id(name)
    if find_id(id):
        id = int(id)
        # Obtention de la hiérarchie de l'espèce
        hierarchie = get_hierarchie(id).to_dict('records')
        # Obtention de la famille de l'espèce
        classification = get_famille(name, hierarchie)
        return classification
    else:
        return None

def get_classification_double(name1, name2):
    """
    Fonction permettant d'obtenir la classification lorsque deux
    espèces sont indiquées
    """
    # Obtention de l'id de l'espèce
    id1 = get_id(name1)
    id2 = get_id(name2)
    if find_id(id1) and find_id(id2):
        id1, id2 = int(id1), int(id2)
        # Obtention de la hiérarchie de l'espèce
        hierarchie1 = get_hierarchie(id1)
        hierarchie2 = get_hierarchie(id2)
        hierarchie = hierarchie1.merge(hierarchie2, how='inner')
        last_name = hierarchie.iloc[-1]['taxonName']
        hierarchie = hierarchie.to_dict('records')
        # Obtention de la famille de l'espèce
        classification = get_famille(last_name, hierarchie)
        return classification
    else:
        return None

def unique_df_values(df, column):
    """
    Fonction permettant d'obtenir les valeurs uniques d'un dataframe
    et de séparer les éléments au niveau de la virgule
    """
    # Obtention des valeurs uniques de la colonne d'intérêt
    unique = df[column].unique()
    unique = list(unique)
    # Séparation au niveau des virgules
    for i in range(len(unique)):
        original_value = unique[i]
        unique[i] = unique[i].replace(' et autres', '')
        unique[i] = [original_value] + unique[i].split(', ')
    return unique

def find_unknown(df, column):
    """
    Fonction permettant de trouver les noms d'espèces
    ne possédant pas d'identifiant dans la database pytaxize
    """
    # Obtention des valeurs uniques de la colonne d'intérêt
    unique = unique_df_values(df, column)
    # Obtention de la classification pour chaque espèce
    size = len(unique)
    unknown = []
    for i in range(size):
        length = len(unique[i])
        print(i, unique[i][0])
        if length == 2:
            if find_unknown_name(unique[i][1]):
                unknown.append(unique[i][0])
        elif length == 3:
            if find_unknown_name(unique[i][1]):
                unknown.append(unique[i][0])
        else:
            unknown.append(unique[i][0])
    return unknown

def get_classification_df(df, column):
    """
    Fonction permettant d'obtenir la classification d'un dataframe
    """
    # Obtention des valeurs uniques de la colonne d'intérêt
    unique = unique_df_values(df, column)
    # Obtention de la classification pour chaque espèce
    size = len(unique)
    print(size)
    dictionary = {}
    for i in range(size):
        length = len(unique[i])
        print(i, unique[i][0])
        if length == 2:
            classification = get_classification(unique[i][1])
            dictionary[unique[i][0]] = classification
        elif length == 3:
            classification = get_classification_double(unique[i][1], unique[i][2])
            dictionary[unique[i][0]] = classification
    return dictionary