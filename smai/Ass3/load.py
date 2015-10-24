import sys
import os
import numpy as np

def load(filename):
    DATA_DIR = 'bank'
    
    thedata = np.genfromtxt(
        os.path.join(DATA_DIR, filename),           # file name
        skip_header=1,          # lines to skip at the top
        skip_footer=0,          # lines to skip at the bottom
        delimiter=';',          # column delimiter
        dtype= "float32, |S25, |S25, |S25, |S25, float32, |S25, |S25, |S25, |float32, |S25, float32, float32, float32, float32, |S25, |S25 ",        # data type
        filling_values=0,       # fill missing values with 0
        #usecols = (0,2,3,5),    # columns to read
        names=["age", "job", "marital", "education", "default", "balance","housing" ,"loan", "contact", "day_of_week", "month",  "duration", "campaign", "pdays", "previous", "poutcome", "y"])

    return thedata


def main():
    filename = 'bank-full.csv'
    load(filename)



if __name__ == "__main__":
    main()