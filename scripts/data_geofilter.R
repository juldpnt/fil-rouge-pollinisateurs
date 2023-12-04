# Import the libraries
# load packages
if (!require("dplyr", quietly = TRUE)) {
  install.packages("dplyr")}
library("dplyr")

if (!require("readr", quietly = TRUE)) {
  install.packages("readr")}
library("readr")

library(ggplot2)
library(gridExtra)

# Import the dataset as a dataframe
df <- read.csv("data/spipoll.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)

# extract the columns "coordonnees_GPS" and "code_postal"
df <- df %>% select(coordonnees_GPS, code_postal)

# display the first 6 rows of the dataframe
print(head(df))