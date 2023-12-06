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

## operations on the spipoll dataset

# import the dataset spipoll as a dataframe
df_spipoll <- read.csv("data/spipoll.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)

# extract the columns "collection_\id", "coordonnees_\GPS" and "code_\postal" from df_spipoll
df_spipoll <- df_spipoll %>% select(collection_id, coordonnees_GPS, code_postal)

# separate the column "coordonnees_GPS" into 2 columns "latitude" and "longitude"
df_spipoll <- df_spipoll %>% separate(coordonnees_GPS, c("latitude", "longitude"), sep = ", ", remove = TRUE)


## operations on the governmental "codes postaux" dataset

# import the dataset codes postaux as a dataframe
df_poste <- read.csv("data/datagouv_codespostaux.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)

# separate the columns (separator ;)
df_poste <- df_poste %>% separate(X.Code_commune_INSEE.Nom_de_la_commune.Code_postal.Libell._d_acheminement.Ligne_5, into = c("code_commune_INSEE", "nom_de_la_commune", "code_postal","libelle","ligne_5"), sep = ";")

# extract the column "code_\postal" from df_poste
df_poste <- df_poste %>% select(code_postal)

# identify and remove the rows starting by "97" and "98" in df_poste
df_poste <- df_poste %>% filter(!grepl("^97", code_postal))
df_poste <- df_poste %>% filter(!grepl("^98", code_postal))

## quantifying the amount of data in the spipoll dataset that are in metropolitan France  

# Add a new column 'France metropolitaine' to df_\spipoll with the data that are in df_poste
df_spipoll <- df_spipoll %>% mutate(`France metropolitaine` = code_postal %in% df_poste$code_postal)
#print(head(df_spipoll))

# count the number of rows with TRUE and FALSE
print(df_spipoll %>% count(`France metropolitaine`))

# keep only the first row for each collection_id
df_spipoll <- df_spipoll %>% distinct(collection_id, .keep_all = TRUE)

# separate df_\spipoll into 2 dataframes: df_\spipoll_\metropole and df_\spipoll_\not_metropole
df_spipoll_metropole <- df_spipoll %>% filter(`France metropolitaine` == TRUE)
df_spipoll_hors_metropole <- df_spipoll %>% filter(`France metropolitaine` == FALSE)

# save the 2 dataframes as csv files
write.csv(df_spipoll_metropole, "data/spipoll_metropole.csv", row.names = FALSE)
write.csv(df_spipoll_hors_metropole, "data/spipoll_hors_metropole.csv", row.names = FALSE)