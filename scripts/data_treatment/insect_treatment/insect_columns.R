# Traitement pour avoir le maximum  d'information possible pour chaque insecte

# Chargement de la base de donnée
data <- read.csv("data/spipoll.csv", header = TRUE, sep = ",")
# Sélection des colonnes qui nous intéressent
colonnes <- c("insecte_sc", "insecte_fr", "insecte_denominationPlusPrecise")
data_reduite <- data[colonnes]
# Renommage des colonnes
colnames(data_reduite) <- c("insecte_sc", "insecte_fr", "insecte_pp")
# Enregistrement du tableau
write.csv(data_reduite, "data/insect_columns.csv", row.names = FALSE)