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

Les notebooks se situent dans le dossier du même nom à la racine. Dans ce dossier se trouvent les Jupyter notebooks propres à aux approches supervisée et non supervisée. 
Le sous-dossier Non_supervise comprend lui-même deux sous-dossiers relatifs aux méthodes employées : Recherche_motifs_frequents et Clustering_DBSCAN. 

- Pour la partie non-supervisée:
  Le premier contient : 
  - MF_plantes_insectes_TaxEspeces avec une recherche de motifs fréquents par rapport au taxon "genre" de l'insecte
  - Recherche_MF_plantes_insectes_taxGeneraux qui se focalise cette fois-ci sur l'ordre de l'insecte.
  Ces deux notebooks s'appuient sur les données spipoll.csv .
  Le troisième notebook (Exploration_Motifs_fréquents_V2) permet la recherche de motifs fréquents à des niveaux de taxonomie beaucoup plus bas et s'appuie sur la version non prétraitée des données (sans l'augmentation taxonomique, soit la version transmise initialement par le Museum).  

  Le dossier Clustering_DBSCAN comprend quant à lui 6 notebooks : 
  - DBSCAN_clustering_et_métriques et DBSCAN_adjusted_clustering_et_métriques portent sur le clustering des Apidae et Syrphidae. Les cartes générées par DBSCAN (min_smaples indexé (voir ci-dessous) et année par année) sont stockées dans le dossier cartes_clustering_adjustedBase200.
  - Dans le notebook DBSCAN_adjusted_clustering_et_métriques, on a indexé l'argument min_samples de l'algorithme DBSCAN sur le taux de croissance annuelle des observations, calculé dans le notebook Active_Users_per_year.
  - Grâce aux métriques créées dans le notebook DBSCAN_adjusted_clustering_et_métriques, deux clusters d'intérêt ont été indentifiés. Leurs situations respectives est investiguée dans le notebook Verif_clusters.
  - L'approndissement de ces deux cas particuliers nous a conduit à nous interroger sur l'importance d'une approche locale du problème, mise en évidence dans le notebook Observ_per_year_and_dep.
  - Enfin, DBSCAN_frelons traite du clustering des populations de frelons asiatiques et européens pour confirmer ou infirmer l'hypothèse selon laquelle les frelons asiatiques tendent à chasser des grandes villes leurs homologues européens.
  - L'ensemble de ces notebooks s'appuient sur les données spipoll.csv .
  
- Pour la partie supervisée:

  - Deux notebooks sont disponibles. Ils permettent de comprendre les différents modules développés pour la prédiction de richesse spécifique.

  - Ensuite, certains scripts peuvent être lancés. Les scripts peuvent se lancer via la commande `python nom_du_script.py` dans un terminal. Les modules se trouvent dans le dossier models ainsi que dans models/supervised.