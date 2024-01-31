import pandas as pd
import nltk
from nltk import ngrams
from nltk.corpus import stopwords
from collections import Counter
from tqdm import tqdm

# Import spipoll.csv as a pandas dataframe
spipoll = pd.read_csv("././data/spipoll.csv",low_memory=False)

# Extract relevant columns from the spipoll dataframe
plantes = spipoll[['collection_id', 'plante_sc', 'plante_fr',
       'plante_precision', 'plante_inconnue', 'plante_caractere',
       'photo_fleur', 'photo_plante', 'photo_feuille']]

#--------------------------------------------------------------
# shrinking the data in two phases
#--------------------------------------------------------------

# Phase 1: shrinking the data by grouping by collection_id

# Keep only the first row for each unique value of collection_id
plantes = plantes.drop_duplicates(subset='collection_id', keep='first')
# Save the extracted columns as a csv file
plantes.to_csv("data/plantes/plantes.csv", index=False)

# Phase 2: shrinking the data by removing duplicates in plante_sc

# extract a subset from plantes named plantes_subset with only the rows that contain unique values for plante_sc
plantes_subset = plantes.drop_duplicates(subset='plante_sc')
# save as a csv file
plantes_subset.to_csv("data/plantes/plantes_subset.csv", index=False)

#--------------------------------------------------------------
# data augmentation
#--------------------------------------------------------------

from plant_functions import calculate_most_common_monograms, convert_monograms_to_set, find_words_in_set

# Adding a column named data_augmentation to plantes_subset
plantes_subset.insert(2, 'data_augmentation', [None]*len(plantes_subset))

# Calculate the most common monograms in the column plante_sc
df_monograms = calculate_most_common_monograms(plantes_subset['plante_sc'])

# Convert the monograms to a set to speed up the matching process
monograms_set = convert_monograms_to_set(df_monograms)

# Fill in the column data_augmentation with the most common monograms from plante_sc
plantes_subset['data_augmentation'] = plantes_subset['plante_sc'].apply(lambda x: find_words_in_set(x, monograms_set))

# If you want to display the progress of the apply function, you can wrap it with tqdm
plantes_subset['data_augmentation'] = list(tqdm(plantes_subset['plante_sc'].apply(lambda x: find_words_in_set(x, monograms_set))))
























