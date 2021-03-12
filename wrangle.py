import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

from env import host, user, password

def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def new_telco_data():
    '''
    This function reads the telco_churn data from the Codeup db into a df,
    write it to a csv file, and returns the df.
    '''
    # Create SQL query.
    sql_query = ''' select customer_id, monthly_charges, tenure, total_charges
                    from customers
                    where contract_type_id = 3;
                    '''
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('telco_churn'))
    
    return df

def acquire_telco(cached=True):
    '''
    This function reads in telco_churn data from Codeup database and writes data to
    a csv file if cached == False or if cached == True reads in telco df from
    a csv file, returns df.
    '''
    if cached == False or os.path.isfile('telco_df.csv') == False:
        
        # Read fresh data from db into a DataFrame.
        df = new_telco_data()
        
        # Write DataFrame to a csv file.
        df.to_csv('telco_df.csv')
        
    else:
        
        # If csv file exists or cached == True, read in data from csv.
        df = pd.read_csv('telco_df.csv', index_col=1)
        df = df.iloc[:,1:]
        # df = df.drop(columns='Unnamed: 0')
        
    return df

def clean_telco(df):
    '''Takes in a df of telco data and cleans the data by replacing blanks and dropping null values. 
    The total_charges column is then converted to float
    
    return: df, a cleaned pandas dataframe'''
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df = df.dropna()
    df['total_charges'] = df.total_charges.astype(float)
    return df

def split_telco(df, stratify_by=None):
    """
    Crude train, validate, test split
    To stratify, send in a column name
    """
    
    if stratify_by == None:
        train, test = train_test_split(df, test_size=.2, random_state=123)
        train, validate = train_test_split(df, test_size=.3, random_state=123)
    else:
        train_validate, test = train_test_split(df, test_size=.2, random_state=123, stratify=df[stratify_by])
        train, validate = train_test_split(train_validate, test_size=.3, random_state=123, stratify=train_validate[stratify_by])
    
    return train, validate, test

def wrangle_telco(split=False):
    '''
    wrangle_telco will read in our student grades as a pandas dataframe,
    clean the data
    split the data
    return: train, validate, test sets of pandas dataframes from telco if split = True
    '''
    df = clean_telco(acquire_telco())
    if split == True:
        return split_telco(df)
    else:
        return df