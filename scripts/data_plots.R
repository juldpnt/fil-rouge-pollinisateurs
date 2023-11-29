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

## Declare the type of the variables

# Declare the temporal variables in a list
temporal_vars <- c('collection_date', 'collection_heure_debut')

# Declare the categorical variables in a list
categorical_vars <- setdiff(names(df)[sapply(df, is.character)], temporal_vars)
# Convert the categorical variables to factors
df[categorical_vars] <- lapply(df[categorical_vars], as.factor)
# Display the categorical variables
# print(categorical_vars)

# Declare the binary variables in a list
binary_vars <- c('protocole_long', 'plante_inconnue', 'fleur_ombre', 'insecte_vu_sur_fleur')
# Convert the binary variables to logical variables
df[binary_vars] <- lapply(df[binary_vars], as.logical)

# Declare the numerical variables in a list
numerical_vars <- c('nb_validation', 'nb_suggestion')

## Plot the distribution of the variables

# List to store the subplots
plot_list <- list()

# Plot the distribution of the numerical variables
for (var in numerical_vars) {
  # Plot the distribution of the numerical variable
  p <- ggplot(df, aes_string(x = var)) +
    geom_histogram() +
    labs(title = paste("Distribution de la variable ", var)) +
    xlab(var)
  # Adds the subplot to the list
  plot_list[[var]] <- p
}

# Plot the distribution of the binary variables
for (var in binary_vars) {
  # Plot the distribution of the binary variable
  p <- ggplot(df, aes_string(x = var)) +
    geom_bar() +
    labs(title = paste("Distribution de la variable ", var)) +
    xlab(var)
  # Adds the subplot to the list
  plot_list[[var]] <- p
}

# Plot the distribution of the categorical variables


# Plot the distribution of the temporal variables


# Combine all the subplots in a single plot
combined_plot <- do.call(grid.arrange, c(plot_list, ncol = 2))

# Display the combined plot
print(combined_plot)

# Save the combined plot
ggsave("figures/distribution_variables.png", combined_plot, width = 20, height = 20, units = "cm")
