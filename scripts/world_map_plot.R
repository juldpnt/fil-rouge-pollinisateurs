# Load necessary libraries
if (!require("ggplot2", quietly = TRUE)) {
  install.packages("ggplot2")
}
if (!require("maps", quietly = TRUE)) {
  install.packages("maps")
}
if (!require("dplyr", quietly = TRUE)) {
  install.packages("dplyr")
}
if (!require("readr", quietly = TRUE)) {
  install.packages("readr")
}
if (!require("tidyr", quietly = TRUE)) {
  install.packages("tidyr")}

library("ggplot2")
library("maps")
library("dplyr")
library("readr")
library("tidyr")

# # import the dataset spipoll as a dataframe
# df_spipoll <- read.csv("data/spipoll.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)

# # extract the column "coordonnees_\GPS" from df_spipoll
# df_spipoll <- df_spipoll %>% select(coordonnees_GPS)

# # separate the column "coordonnees_GPS" into 2 columns "latitude" and "longitude"
# df_spipoll <- df_spipoll %>% separate(coordonnees_GPS, c("latitude", "longitude"), sep = ", ", remove = TRUE)

# # Convert latitude and longitude to numeric
# df_spipoll$latitude <- as.numeric(df_spipoll$latitude)
# df_spipoll$longitude <- as.numeric(df_spipoll$longitude)

# # Get the world map data
# world_map <- map_data("world")

# # Create the 1st plot
# ggplot() +
#   geom_polygon(data = world_map, aes(x = long, y = lat, group = group), fill = "lightblue", color = "white", size = 0.1) +
#   geom_point(data = df_spipoll, aes(x = longitude, y = latitude), color = "red", size = 1, alpha = 0.5) +
#   coord_map("mercator", xlim=c(-180,180)) +
#   theme_minimal() +
#   theme(panel.grid = element_blank(),
#         axis.ticks = element_blank(),
#         axis.text = element_blank(),
#         axis.title = element_blank()) +
#   labs(title = "World Map Plot", caption = "Source: Your Data Source")
# ggsave("figures/world_map.png", dpi = 300)

## Creating a filtered world map based on the "codes postaux" filtering from data_geofilter.R

# import the datasets as dataframes
df_spipoll_hors_metropole <- read.csv("data/spipoll_hors_metropole.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)
df_spipoll_metropole <- read.csv("data/spipoll_metropole.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)

# convert the columns longitude and latitude to numeric
df_spipoll_hors_metropole$longitude <- as.numeric(df_spipoll_hors_metropole$longitude)
df_spipoll_hors_metropole$latitude <- as.numeric(df_spipoll_hors_metropole$latitude)
df_spipoll_metropole$longitude <- as.numeric(df_spipoll_metropole$longitude)
df_spipoll_metropole$latitude <- as.numeric(df_spipoll_metropole$latitude)

# get the world map data
world_map <- map_data("world")

# create the 2nd plot with code_postal as label
ggplot() +
  geom_polygon(data = world_map, aes(x = long, y = lat, group = group), fill = "lightblue", color = "white", size = 0.1) +
  #geom_point(data = df_spipoll_hors_metropole, aes(x = longitude, y = latitude), color = "red", size = 1, alpha = 0.5) +
  geom_point(data = df_spipoll_metropole, aes(x = longitude, y = latitude), color = "green", size = 1, alpha = 0.1) +
  #geom_text(data = df_spipoll_hors_metropole, aes(x = longitude, y = latitude, label = collection_id), color = "#ffa602", size = 1, alpha = 1, nudge_x = 0.1, nudge_y = 0.1) +
  coord_map("mercator", xlim=c(-180,180)) +
  theme_minimal() +
  theme(panel.grid = element_blank(),
        axis.ticks = element_blank(),
        axis.text = element_blank(),
        axis.title = element_blank()) +
  labs(title = "World Map Plot", caption = "Source: Your Data Source")
ggsave("figures/world_map_filtered.png", dpi = 300)










