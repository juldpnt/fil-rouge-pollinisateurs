# import the libraries
if (!require("dplyr", quietly = TRUE)) {
  install.packages("dplyr")}
if (!require("readr", quietly = TRUE)) {
  install.packages("readr")}
if (!require("tidyr", quietly = TRUE)) {
  install.packages("tidyr")}

library("dplyr")
library("readr")
library("tidyr")

# northern-most, southern-most, western-most and eastern-most points of Metropolitan France
latitude_nord <- 51.065
latitude_sud <- 42.19
longitude_ouest <- -5.15
longitude_est <- 9.325

# import the dataset spipoll_metropole and spipoll_hors_metropole as dataframes
df_spipoll_metropole <- read.csv("data/spipoll_metropole.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)
df_spipoll_hors_metropole <- read.csv("data/spipoll_hors_metropole.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)
# select the columns "collection_id", "longitude" and "latitude" from df_spipoll_metropole and df_spipoll_hors_metropole
df_spipoll_metropole <- df_spipoll_metropole %>% select(longitude, latitude, collection_id)
df_spipoll_hors_metropole <- df_spipoll_hors_metropole %>% select(longitude, latitude, collection_id)

## rows from df_spipoll_metropole that are outside of Metropolitan France : false positives

# rows where latitude is between the northern-most and southern-most points of Metropolitan France
within_latitude_France_df <- df_spipoll_metropole %>% filter(latitude > latitude_sud & latitude < latitude_nord)
# rows where longitude is between the western-most and eastern-most points of Metropolitan France
within_longitude_France_df <- df_spipoll_metropole %>% filter(longitude > longitude_ouest & longitude < longitude_est)

# identify the rows in df_spipoll_metropole that are both in within_latitude_France_df and within_longitude_France_df
within_France_df <- semi_join(within_latitude_France_df, within_longitude_France_df, by = c("collection_id", "longitude", "latitude"))
# add to df_spipoll_hors_metropole the rows that are in df_spipoll_metropole but not in within_France_df
df_spipoll_hors_metropole <- bind_rows(df_spipoll_hors_metropole, anti_join(df_spipoll_metropole, within_France_df, by = c("collection_id", "longitude", "latitude")))
# remove from df_spipoll_metropole the rows that are not in within_France_df
df_spipoll_metropole <- semi_join(df_spipoll_metropole, within_France_df, by = c("collection_id", "longitude", "latitude"))

## rows from df_spipoll_hors_metropole that are inside of Metropolitan France : false negatives

# rows where latitude is between the northern-most and southern-most points of Metropolitan France
within_latitude_France_df <- df_spipoll_hors_metropole %>% filter(latitude > latitude_sud & latitude < latitude_nord)
# rows where longitude is between the western-most and eastern-most points of Metropolitan France
within_longitude_France_df <- df_spipoll_hors_metropole %>% filter(longitude > longitude_ouest & longitude < longitude_est)

# identify the rows in df_spipoll_hors_metropole that are both in within_latitude_France_df and within_longitude_France_df
within_France_df <- semi_join(within_latitude_France_df, within_longitude_France_df, by = c("collection_id", "longitude", "latitude"))
# add to df_spipoll_metropole the rows that are in within_France_df
df_spipoll_metropole <- bind_rows(df_spipoll_metropole, semi_join(df_spipoll_hors_metropole, within_France_df, by = c("collection_id", "longitude", "latitude")))
# remove from df_spipoll_hors_metropole the rows that are in within_France_df
df_spipoll_hors_metropole <- anti_join(df_spipoll_hors_metropole, within_France_df, by = c("collection_id", "longitude", "latitude"))

# save the 2 dataframes as csv files
write.csv(df_spipoll_metropole, "data/spipoll_metropole.csv", row.names = FALSE)
write.csv(df_spipoll_hors_metropole, "data/spipoll_hors_metropole.csv", row.names = FALSE)