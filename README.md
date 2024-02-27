# Prédiction de présence de pollinisateurs 

## Table des matières
- [Prédiction de présence de pollinisateurs](#prédiction-de-présence-de-pollinisateurs)
  - [Table des matières](#table-des-matières)
  - [Membres du groupe](#membres-du-groupe)
  - [Description du projet](#description-du-projet)
  - [Utilisation du repôt](#utilisation)
  - [Contenu des dossiers](#contenu-des-dossiers)

## Membres du groupe

- Ambroise BERTIN
- Maëlle CORNEC
- Jules DUPONT
- Suzanne GUILTEAUX

## Description du projet

Le projet utilise la base de données du SPIPOLL, un dispositif de suivi des insectes pollinisateurs, créé par le Muséum national d’histoire naturelle et l’Office pour les insectes et leur environnement. Nous explorons les données de suivi participatif avec des approches supervisée et non-supervisée.

## Utilisation 


# Contenu des dossiers
- Approche non supervisée :
Les notebooks relatifs aux méthodes non supervisées se situent dans le dossier Non_supervise. Vous y trouverez deux sous-dossiers intitulés :
- Recherche_motifs_fréquents : contenant les notebooks sur la recherche de motifs fréquents réalisée à des différents niveaux de taxonomie, plus ou moins profonds.

- Clustering_DBSCAN contenant 6 notebooks.
- DBSCAN_clustering_et_métriques et DBSCAN_adjusted_clustering_et_métriques portent sur le clustering des Apidae et Syrphidae. Les cartes générées par DBSCAN (min_smaples indexé (voir ci-dessous) et année par année) sont stockées dans le dossier cartes_clustering_adjustedBase200.
- Dans le notebook DBSCAN_adjusted_clustering_et_métriques, on a indexé l'argument min_samples de l'algorithme DBSCAN sur le taux de croissance annuelle des observations, calculé dans le notebook Active_Users_per_year.
- Grâce aux métriques créées dans le notebook DBSCAN_adjusted_clustering_et_métriques, deux clusters d'intérêt ont été indentifiés, l'un en potentielle déplétion et l'autre perdurant dans le temps de manière surprenante. La situation de ces deux clusters est investiguée dans le notebook Verif_clusters.
- L'approndissement de ces deux cas particuliers nous a conduit à nous interroger sur l'importance d'une approche locale du problème, mise en évidence dans le notebook Observ_per_year_and_dep.
- Enfin, DBSCAN_frelons traite du clustering des populations de frelons asiatiques et européens pour confirmer ou infirmer l'hypothèse selon laquelle les frelons asiatiques tendent à chasser des grandes villes leurs homologues européens.
  
