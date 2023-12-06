# load packages
if (!require("dplyr", quietly = TRUE)) {
  install.packages("dplyr")
}

if (!require("readr", quietly = TRUE)) {
  install.packages("readr")
}

library("dplyr")
library("readr")

# import the dataset spipoll as a dataframe
df_spipoll <- read.csv("data/spipoll.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)

# # give the number of missing values for column code_postal
# print("Number of missing values for column code_postal")
# print(sum(is.na(df_spipoll$code_postal)))
# print("\n")

# Gives the first 6 rows
print("First 6 rows")
print(head(df))
print('\n')

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