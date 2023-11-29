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

# merge the 4 dataframes into one
df <- rbind(df1, df2, df3, df4)

# Declare unused variables
unused_vars <- c('collection_nom', 'user_pseudo', 'user_email', 'commentaire', 'photo_lieu', 'code_postal', 'distance_ruche', 'collection_heure_fin', 'insecte_photo_1', 'insecte_photo_2', 'date_creation_bdd', 'date_update_bdd')

# Remove unused variables from the dataframe
df <- df %>% select(-unused_vars)

# save the dataframe as a csv file
write.csv(df, "data/spipoll.csv", row.names = FALSE)