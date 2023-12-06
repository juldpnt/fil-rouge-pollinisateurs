# import the libraries
if (!require("dplyr", quietly = TRUE)) {
  install.packages("dplyr")}
library("dplyr")

if (!require("readr", quietly = TRUE)) {
  install.packages("readr")}
library("readr")

if (!require("tidyr", quietly = TRUE)) {
  install.packages("tidyr")}
library("tidyr")

# import the dataset spipoll_metropole and spipoll_hors_metropole as dataframes
df_spipoll_metropole <- read.csv("data/spipoll_metropole.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)
df_spipoll_hors_metropole <- read.csv("data/spipoll_hors_metropole.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)

# # Count the number of rows where latitude is greater than the southern-most point of Metropolitan France
# pseudo_northern_hemisphere_rows <- df_spipoll_metropole %>% filter(latitude > 41.19) %>% nrow()

# # Count the number of rows where latitude is less than the southern-most point of Metropolitan France
# pseudo_southern_hemisphere_rows <- df_spipoll_metropole %>% filter(latitude < 41.19) %>% nrow()

# print(paste("Number of rows matching the latitude of Metropolitan France: ", pseudo_northern_hemisphere_rows))
# print(paste("Number of rows matching the latitude of Metropolitan France: ", pseudo_southern_hemisphere_rows))

# # Add the number of rows from both hemispheres
# total_rows <- pseudo_northern_hemisphere_rows + pseudo_southern_hemisphere_rows

# # Check if the total matches the number of rows in the dataframe
# if (total_rows == nrow(df_spipoll_metropole)) {
#   print("The total matches the number of rows in the dataframe.")
# } else {
#   print("The total does not match the number of rows in the dataframe.")
# }

# Filter the rows where latitude is less than the southern-most point of Metropolitan France
pseudo_southern_hemisphere_df <- df_spipoll_metropole %>% filter(latitude < 41.19)

# Convert the 'code_postal' column of both data frames to character
df_spipoll_hors_metropole$code_postal <- as.character(df_spipoll_hors_metropole$code_postal)
pseudo_southern_hemisphere_df$code_postal <- as.character(pseudo_southern_hemisphere_df$code_postal)

# Add these rows to df_spipoll_hors_metropole
df_spipoll_hors_metropole <- bind_rows(df_spipoll_hors_metropole, pseudo_southern_hemisphere_df)
# Remove these rows from df_spipoll_metropole
df_spipoll_metropole <- df_spipoll_metropole %>% filter(latitude >= 41.19)

# # Count the number of rows where latitude is less than the southern-most point of Metropolitan France
# print(pseudo_southern_hemisphere_rows <- df_spipoll_metropole %>% filter(latitude < 41.19) %>% nrow())

# save the 2 dataframes as csv files
write.csv(df_spipoll_metropole, "data/spipoll_metropole.csv", row.names = FALSE)
write.csv(df_spipoll_hors_metropole, "data/spipoll_hors_metropole.csv", row.names = FALSE)























