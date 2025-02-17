# author: Ahmed Rizk
# date: 2022-03-24


''' A script that sets a universal seed, reads the dataset used for the analysis
 from specified path, and processes the data for the EDA.

 Usage: read_process_script.py --read_path=<read_path> --processed_path=<processed_path>

 Options:
 --read_path=<read_path>  path of the file to read
 --processed_path=<processed_path>  path to the processed dataset object created, before the training/testing split

'''

import numpy as np
import pandas as pd
from docopt import docopt
from analysis.split_drop import split_drop
import pickle

opt = docopt(__doc__)

np.random.seed(1)

def read_trim(read_path):
    data = pd.read_csv(read_path)
    reduced_data = data[['EFSIZE', 'USHRWK', 'ATINC', 'HLEV2G', 'EFINVA', 'EFMJIE', 'EFATINC', 'EFMJSI']]
    return reduced_data


def process(data, processed_path):
    data = data.drop(columns = 'USHRWK') 
    data = data.loc[data['ATINC'] != 99999996] 
    processed = data[["EFINVA","EFSIZE","EFMJIE"]]
    return processed    # should I split into 3?



def train_test_drop(data, dropped_col):
    X_train, Y_train, X_test, Y_test = split_drop(data, 0.3, 123, dropped_col)
    return X_train, Y_train, X_test, Y_test
    
    
def pickle_save(name, variable):
    with open(name,"wb") as f:
        pickle.dump(variable, f)


def main(read_path, processed_path):
    reduced_data = read_trim(read_path)
    processed = process(reduced_data, processed_path)
    X_train, Y_train, X_test, Y_test = train_test_drop(processed, "EFINVA")
    pickle_save("data/processed/X_train.pkl",X_train)
    pickle_save("data/processed/Y_train.pkl", Y_train)
    pickle_save("data/processed/X_test.pkl", X_test)
    pickle_save("data/processed/Y_test.pkl", Y_test)
    pickle_save("data/processed/processed.pkl", processed)
    pickle_save("data/processed/reduced_data.pkl", reduced_data)
    
main(opt["--read_path"], opt["--processed_path"])



