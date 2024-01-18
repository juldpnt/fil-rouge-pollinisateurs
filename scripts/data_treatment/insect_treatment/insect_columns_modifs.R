#########################################################
# Fonction utile
#########################################################

calculate_column_counts <- function(data) {
  # Count the number of elements per column
  column_counts <- colSums(!is.na(data))

  # Print the column counts
  print("Nombre de valeurs non nulles par colonne :")
  print(column_counts)

  # Count the number of unique values per column
  unique_counts <- sapply(data, function(x) length(unique(x)))

  # Print the unique value counts
  print("Nombre de valeurs uniques par colonne :")
  print(unique_counts)
}

#########################################################
# Dénombrement des colonnes
#########################################################

# Read the CSV file
data <- read.csv("data/insect_columns.csv")

# Count the number of elements per column
column_counts1 <- colSums(!is.na(data))

# Print the column counts
print("Etape 1 : Avant traitement des colonnes")
calculate_column_counts(data)

#########################################################
# Remplacement de insecte_sc par insecte_pp et suppression de insecte_pp
#########################################################

# # Replace the value of insecte_sc with insecte_pp if insecte_pp exists
# if ("insecte_pp" %in% colnames(data)) {
#   data$insecte_sc <- ifelse(!is.na(data$insecte_pp),
#                             data$insecte_pp,
#                             data$insecte_sc)
# }

# # Print the column counts
# print("Etape 2 : Remplacement de insect_sc par insect_pp")
# calculate_column_counts(data)

# Remove the column insecte_pp
data <- data[, !colnames(data) %in% "insecte_pp"]

#########################################################
# Supprime les lignes NA Insecte inconnu
#########################################################

# Remove rows where insecte_fr is 'Insecte inconnu' and insecte_sc is NA in data
data <- data[!((data$insecte_fr == "Insecte inconnu"
                | is.na(data$insecte_fr)) &
                 (data$insecte_sc == "Insecte inconnu"
                  | is.na(data$insecte_sc))), ]

# Count the number of elements per column
column_counts <- colSums(!is.na(data))

# Print the column counts
print("Etape 3 : Suppression des lignes NA/NA, Insecte inconnu/Insecte inconnu")
calculate_column_counts(data)

#########################################################
# Apprendre quelles sont les valeurs sans insecte_sc
#########################################################

# Create a table with rows that do not have values in their insecte_sc column
missing_values_table <- data[is.na(data$insecte_sc), ]

# Print the column counts
print("Etape 4 : Création d'un tableau des lignes sans insecte_sc")
calculate_column_counts(missing_values_table)

# Show the unique values in the insecte_fr column
unique_values <- unique(missing_values_table$insecte_fr)
print("Les valeurs uniques de la colonne insecte_fr sont :")
print(unique_values)

# Count the occurrences of each unique value
value_counts <- table(missing_values_table$insecte_fr)
print("Occurrences des valeurs uniques dans la colonne insecte_fr :")
print(value_counts)

# Listes des remplaceemnts à faire
original <- c("Les Mouches difficiles à déterminer",
              "Les Coléoptères difficiles à déterminer",
              "Les Moustiques, Tipules et autres diptères Nématocères",
              "Les Chenilles et fausses-Chenilles",
              "Les Syrphes difficiles à déterminer",
              "Les Terebrants Chalcidiens et autres",
              "Les Epeires et autres Araneidae",
              "Les Punaises difficiles à déterminer",
              "Les Syrphes aux fémurs enflés",
              "Les Tachinaires difficiles à déterminer",
              "Les Punaises prédatrices ternes")
remplacement <- c("Diptera", "Coleoptera", "Nematocera",
                  "Lepidoptera", "Syrphinae", "Chalcidoidea",
                  "Araneidae", "Heteroptera", "Syrphinae",
                  "Tachinidae", "Lygus lineolaris")

for (i in 1:length(original)) {
  data$insecte_sc <- ifelse(is.na(data$insecte_sc) &
                              data$insecte_fr == original[i],
                            remplacement[i],
                            data$insecte_sc)
}

data <- data[!(data$insecte_sc == "autres"), ]

# Ne garder que la colonne insecte_sc
data <- data[, !colnames(data) %in% "insecte_fr"]

write.csv(data, "scripts/data_treatment/insect_treatment/data_insects/insect_sc_modified_without_pp.csv", row.names = FALSE)
