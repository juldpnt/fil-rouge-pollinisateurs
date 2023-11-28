# load packages
if (!require("dplyr", quietly = TRUE)) {
  install.packages("dplyr")
}

if (!require("readr", quietly = TRUE)) {
  install.packages("readr")
}

library("dplyr")
library("readr")

# read the txt data of the 4 files in the folder 'data'
df1 <- suppressMessages(read_tsv("data/spipoll_1_200k_202311130947.txt"))
df2 <- suppressMessages(read_tsv("data/spipoll_200k_400k_202311130949.txt"))
df3 <- suppressMessages(read_tsv("data/spipoll_400k_200k_202311130959.txt"))
df4 <- suppressMessages(read_tsv("data/spipoll_600k_75k_202311131020.txt"))

## dataframes contain non redundant information, no overlap (see first 2 rows)

# merge the 4 dataframes into one
df <- rbind(df1, df2, df3, df4)

# # Gives the first 6 rows
# print("First 6 rows")
# print(head(df))
# print('\n')

# # Gives a statistical summary of the data
# print("Statistical summary of the data \n")
# print(summary(df))
# print("\n")

# # Gives the structure of the data
# print("Structure of the data \n")
# print(str(df, list.len = 0))
# print("\n")

# # Gives the number of unique values in each column
# print("Unique values in each column \n")
# print(df %>%
#   summarise_all(n_distinct) %>% as.vector()) 

# # Gives the number of missing values in each column
# print("Missing values in each column \n")
# print(summary(sapply(df, function(x) sum(is.na(x)))))

## Déclaration des variables selon leur type

# # Déclare les variables numériques dans une liste
# numerical_vars <- df[sapply(df, is.numeric)]
# # Affiche les variables numériques
# print(numerical_vars)

# # Déclare les variables catégorielles dans une liste
# categorical_vars <- df[sapply(df, is.character)]
# # Affiche les variables catégorielles
# print(categorical_vars)

# Déclare les variables temporelles dans une liste
date_vars <- df[sapply(df, is.Date)]


# # remove specific columns
# df %>% select(-c("commentaire", "coordonnees_GPS")) -> df
