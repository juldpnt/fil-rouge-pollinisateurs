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

if (!require("geonames", quietly = TRUE)) {
  install.packages("geonames")}
library("geonames")
# Set the Geonames username
options(geonamesUsername = "spipoll")

# import the dataset as a dataframe
df <- read.csv("data/spipoll.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)

# extract the columns "coordonnees_GPS" and "code_postal"
df <- df %>% select(coordonnees_GPS, code_postal)

# separate the column "coordonnees_GPS" into 2 columns "latitude" and "longitude"
df <- df %>% separate(coordonnees_GPS, c("latitude", "longitude"), sep = ", ", remove = TRUE)

# add empty columns for the GPS coordinates infered from the postal code
df <- df %>% mutate(latitude_CP = NA, longitude_CP = NA)



# Define a function to get coordinates for a vector of postal codes
get_coordinates <- function(postal_codes) {
  coordinates <- data.frame(lat = numeric(length(postal_codes)), lng = numeric(length(postal_codes)))
  for (i in seq_along(postal_codes)) {
    result <- GNpostalCodeSearch(postal_codes[i], country = "FR")
    if (nrow(result) > 0) {
      coordinates[i, ] <- result[1, c("lat", "lng")]
    }
  }
  return(coordinates)
}

# Split the postal codes into batches of 100
postal_code_batches <- split(df$code_postal, ceiling(seq_along(df$code_postal)/100))

# Get the coordinates for each batch and combine them
coordinates <- do.call(rbind, lapply(postal_code_batches, get_coordinates))

# Add the GPS coordinates to the dataframe
df$latitude_CP <- coordinates$lat
df$longitude_CP <- coordinates$lng








# display the first 6 rows of the dataframe
print(head(df))