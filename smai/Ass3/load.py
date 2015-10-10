import sys
import os
import numpy as np

def load(reload=False):
    DATA_DIR = 'bank-additional'
    if reload:
        thedata = np.genfromtxt(
            'bank-additional/bank-additional-full.csv',           # file name
            skip_header=1,          # lines to skip at the top
            skip_footer=0,          # lines to skip at the bottom
            delimiter=';',          # column delimiter
            dtype= "float32, |S25, |S25,|S25,|S25,|S25,|S25,|S25,|S25,|S25,float32, float32, float32, float32, |S25, float32,float32,float32,float32,float32,|S25 ",        # data type
            filling_values=0,       # fill missing values with 0
            #usecols = (0,2,3,5),    # columns to read
            names=["age", "job", "marital", "education", "default", "housing", "loan", "contact", "month", "day_of_week", "duration", "campaign", "pdays", "previous", "poutcome", "empvarrate", "conspriceidx", "consconfidx", "euribor3m", "nremployed" , "y"])

            
        with open(os.path.join(DATA_DIR, 'bank-additional.np'), 'w') as f:
            np.save(f, thedata)
    else:
        with open(os.path.join(DATA_DIR, 'bank-additional.np')) as f:
            thedata = np.load(f)
    return thedata


def main():
     load(True)



if __name__ == "__main__":
    main()