import pandas as pd
import nltk
from nltk import ngrams
from nltk.corpus import stopwords
from collections import Counter
from tqdm import tqdm

# Function to calculate the most common monograms
def calculate_most_common_monograms(column):
    """_summary_

    Returns:
        _type_: _description_
    """
    monograms = []
    
    stop_words = set(stopwords.words('french'))
    
    for text in column.dropna():
        tokens = nltk.word_tokenize(text)
        tokens = [token for token in tokens if token not in stop_words and len(token) > 3]
        monograms.extend(tokens)
    
    # Convert the list of monograms into a DataFrame
    df_monograms = pd.DataFrame(Counter(monograms).most_common(), columns=['Monogram', 'Count'])
    
    return df_monograms

# Function to convert the monograms to a set to speed up the matching process
def convert_monograms_to_set(df_monograms):
    """_summary_

    Args:
        df_monograms (_type_): _description_

    Returns:
        _type_: _description_
    """
    return set(df_monograms['Monogram'])

# Function to find the monograms in a string
def find_words_in_set(input_string, monograms_set):
    """_summary_

    Args:
        input_string (_type_): _description_
        monograms_set (_type_): _description_

    Returns:
        _type_: _description_
    """
    if isinstance(input_string, str):
        words = input_string.split()
        return [word for word in words if word in monograms_set]
    else:
        return []










