#########################################################
# Dénombrement des colonnes
#########################################################

# Read the CSV file
data <- read.csv("data/insect_columns.csv")

# Count the number of elements per column
column_counts <- colSums(!is.na(data))

# Print the column counts
print("Nombre de valeurs non nulles par colonne :")
print(column_counts)

#########################################################
# Remplacement de insecte_sc par insecte_pp et suppression de insecte_pp
#########################################################

# Replace the value of insecte_sc with insecte_pp if insecte_pp exists
if ("insecte_pp" %in% colnames(data)) {
    data$insecte_sc <- ifelse(!is.na(data$insecte_pp),
                              data$insecte_pp,
                              data$insecte_sc)
}

# Remove the column insecte_pp
data <- data[, !colnames(data) %in% "insecte_pp"]

# Count the number of elements per column
column_counts <- colSums(!is.na(data))

# Print the column counts
print("On remplace insecte_sc par insecte_pp et on supprime insecte_pp.")
print("Nombre de valeurs non nulles par colonne :")
print(column_counts)

#########################################################
# Supprime les lignes NA Insecte inconnu
#########################################################

# Remove the rows where insecte_fr is 'Insecte inconnu' and insecte_sc is NA in data
data <- data[!((data$insecte_fr == 'Insecte inconnu' | is.na(data$insecte_fr)) & 
               (data$insecte_sc == 'Insecte inconnu' | is.na(data$insecte_sc))), ]

# Count the number of elements per column
column_counts <- colSums(!is.na(data))

# Print the column counts
print("On supprime les lignes NA et/ou Insecte inconnu.")
print("Nombre de valeurs non nulles par colonne :")
print(column_counts)

#########################################################
# Apprendre quelles sont les valeurs sans insecte_sc
#########################################################

# Create a table with only the rows that do not have values in their insecte_sc column
missing_values_table <- data[is.na(data$insecte_sc), ]

# Count the number of elements per column
column_counts <- colSums(!is.na(missing_values_table))

# Print the column counts
print(column_counts)

# Count the number of unique values in the insecte_fr column
unique_values <- unique(missing_values_table$insecte_fr)

print("Valeurs uniques dans la colonne insecte_fr, qui n'ont pas d'informations dans la colonne insecte_sc :")
print(length(unique_values))
print("Ces valeurs sont :")
print(unique_values)

# Count the occurrences of each unique value in the insecte_fr column of missing_values_table
value_counts <- table(missing_values_table$insecte_fr)

# Print the value counts
print("Occurrences des valeurs uniques dans la colonne insecte_fr :")
print(value_counts)

#########################################################
# Création d'une table avec les valeurs de insecte_sc non nulles
#########################################################

# Create a table with only the rows that have values in their insecte_sc column
# data_with_insecte_sc <- data[!is.na(data$insecte_sc), ]
# data_with_insecte_sc <- data_with_insecte_sc[!(data_with_insecte_sc$insecte_sc == 'autres'), ]

# Remove the column insecte_fr
# data_with_insecte_sc <- data_with_insecte_sc[, !colnames(data_with_insecte_sc) %in% "insecte_fr"]

# Save the table as a CSV file
# write.csv(data_with_insecte_sc, "data/insect_sc_short.csv", row.names = FALSE)

#########################################################
# Création d'une table avec les valeurs de insecte_sc nulles
# qui ont été remplacées par des valeurs de insecte_fr corrigées
#########################################################

# Listes des remplaceemnts à faire
original <- c('Les Mouches difficiles à déterminer', 'Les Coléoptères difficiles à déterminer',
              'Les Moustiques, Tipules et autres diptères Nématocères',
              'Les Chenilles et fausses-Chenilles', 'Les Syrphes difficiles à déterminer',
              'Les Terebrants Chalcidiens et autres', 'Les Epeires et autres Araneidae',
              'Les Punaises difficiles à déterminer', 'Les Syrphes aux fémurs enflés',
              'Les Tachinaires difficiles à déterminer', 'Les Punaises prédatrices ternes')
remplacement <- c('Diptera', 'Coleoptera', 'Nematocera', 'Lepidoptera', 'Syrphinae', 'Chalcidoidea',
                  'Araneidae', 'Heteroptera', 'Syrphinae', 'Tachinidae', 'Lygus lineolaris')

for (i in 1:length(original)) {
    data$insecte_sc <- ifelse(is.na(data$insecte_sc) & data$insecte_fr == original[i],
                                                        remplacement[i],
                                                        data$insecte_sc)
}

data_long <- data[!(data$insecte_sc == 'autres'), ]

# Ne garder que la colonne insecte_sc
data_long <- data_long[, !colnames(data_long) %in% "insecte_fr"]

write.csv(data_long, "data/insect_sc.csv", row.names = FALSE)

# Count the number of unique values in the data_long table
unique_value <- length(unique(data_long))

print("Nombre de valeurs uniques dans la colonne insecte_sc de la table data_long :")
print(unique_value)

#########################################################
# Suppression de toutes les lignes dont les valeurs apparaisent moins de 100 fois
#########################################################
