# author: Ahmed Rizk
# date: 2022-03-24

''' A script that sets a universal seed, reads the dataset used for the analysis
 from specified path, and processes the data for the EDA.

 Usage: read_process_script.py <read_path> <processed_path> <train_path> <test_path>

 Options:
 --read_path=<read_path>  path of the file to read
 --processed_path=<processed_path>  path to the processed dataset object created, before the training/testing split
 --train_path=<train_path> path to the training data
 --test_path=<test_path> path to the testing data

'''

import numpy as np
import pandas as pd
from docopt import docopt
from analysis.split_drop import split_drop

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
    

def write_to_csv(data, path, filename):
    data.to_csv(path + filename, index=True)
    
    

def main(read_path, processed_path, train_path, test_path):
    print("1")
    reduced_data = read_trim(read_path)
    print("2")
    processed = process(reduced_data, processed_path)
    print("3")
    X_train, Y_train, X_test, Y_test = train_test_drop(processed, "EFINVA")
    print("4")
    write_to_csv(X_train, train_path,"X_train.csv")
    print("5")
    write_to_csv(Y_train, train_path, "Y_train.csv")
    print("6")
    write_to_csv(X_test, test_path, "X_test.csv")
    print("7")
    write_to_csv(Y_test, test_path ,"Y_test.csv")
    print("8")
    write_to_csv(processed, processed_path, "processed.csv")
    print("9")
    
    
main(opt["<read_path>"], opt["<processed_path>"], opt["<train_path>"], opt["<test_path>"])


