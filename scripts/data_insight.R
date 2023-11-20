# load packages
if (!require("dplyr", quietly = TRUE)) {
  install.packages("dplyr")
}

if (!require("readr", quietly = TRUE)) {
  install.packages("readr")
}

library("dplyr")
library("readr")

# read the txt data  
df <- read_tsv("data/spipoll_1_200k_202311130947.txt")

print(length(unique(df$user_id)))

# Gives the first 6 rows
print("First 6 rows")
print(head(df))

# Gives a statistical summary of the data
print("Statistical summary of the data \n")
print(summary(df))
print("\n")

# Gives the structure of the data
print("Structure of the data \n")
print(str(df, list.len = 0))
print("\n")

# Gives the number of unique values in each column
print("Unique values in each column \n")
print(df %>%
  summarise_all(n_distinct) %>% as.vector()) 

# Gives the number of missing values in each column
print("Missing values in each column \n")
print(summary(sapply(df, function(x) sum(is.na(x)))))



# remove specific columns
df %>% select(-c("commentaire", "coordonnees_GPS")) -> df
