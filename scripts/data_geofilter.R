# load packages
if (!require("dplyr", quietly = TRUE)) {
  install.packages("dplyr")
}

if (!require("readr", quietly = TRUE)) {
  install.packages("readr")
}

library("dplyr")
library("readr")

# read the txt data of the 4 files in the folder 'data'
df1 <- suppressMessages(read_tsv("data/spipoll_1_200k_202311130947.txt"))
df2 <- suppressMessages(read_tsv("data/spipoll_200k_400k_202311130949.txt"))
df3 <- suppressMessages(read_tsv("data/spipoll_400k_200k_202311130959.txt"))
df4 <- suppressMessages(read_tsv("data/spipoll_600k_75k_202311131020.txt"))

# merge the 4 dataframes into one
df <- rbind(df1, df2, df3, df4)

# extract the columns "coordonnees_GPS" and "code_postal"
df <- df %>% select(coordonnees_GPS, code_postal)

# display the first 6 rows of the dataframe
head(df)