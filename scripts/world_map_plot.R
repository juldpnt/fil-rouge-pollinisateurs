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

library("ggplot2")
library("maps")
library("dplyr")
library("readr")

# read the txt data  
df <- read_tsv("data/spipoll_1_200k_202311130947.txt")

# Split the coordonnees_GPS column into latitude and longitude
df$latitude <- sapply(strsplit(df$coordonnees_GPS, ","), `[`, 1)
df$longitude <- sapply(strsplit(df$coordonnees_GPS, ","), `[`, 2)

# Convert latitude and longitude to numeric
df$latitude <- as.numeric(df$latitude)
df$longitude <- as.numeric(df$longitude)

# Get the world map data
world_map <- map_data("world")

# Create the plot
ggplot() +
  geom_polygon(data = world_map, aes(x = long, y = lat, group = group), fill = "lightblue", color = "white", size = 0.1) +
  geom_point(data = df, aes(x = longitude, y = latitude), color = "red", size = 1, alpha = 0.5) +
  coord_map("mercator", xlim=c(-180,180)) +
  theme_minimal() +
  theme(panel.grid = element_blank(),
        axis.ticks = element_blank(),
        axis.text = element_blank(),
        axis.title = element_blank()) +
  labs(title = "World Map Plot", caption = "Source: Your Data Source")
ggsave("test.png", dpi = 300)