import pandas as pd
from scipy import stats
import numpy as np
import seaborn as sns
import sys 
import matplotlib.pyplot as plt
import pandas_profiling

def load_and_process(url_or_path_to_csv_file):
    
    #method chain 1 (load and Clean data - remove columns and rows, rename columns, deal with missing data, and format data)

    df1 = (
        pd.read_csv(url_or_path_to_csv_file, encoding = "ISO-8859-1")
        .drop(['name', 'day', 'year','h_income', 'cause', 'state', 'county_income', 'comp_income','county_bucket', 'nat_bucket', 'share_black', 'share_hispanic', 'college', 'streetaddress', 'pov', 'city', 'latitude', 'longitude', 'state_fp', 'county_fp', 'tract_ce', 'geo_id', 'county_id', 'namelsad', 'lawenforcementagency'], axis =1)
        .rename(columns={"p_income": "income"})
        .rename(columns = {"share_white": "share_Caucasian"})
        .dropna()
        .query("age != 'Unknown' & armed != 'Unknown' & income != '-'")
    )
    df1['age'] = pd.to_numeric(df1['age'])
    df1['income'] = pd.to_numeric(df1['income'])
    df1['share_Caucasian'] = pd.to_numeric(df1['share_Caucasian'])
    
    #method chain 2 (Process Data - deal with outliers, create new columns, and replace values)

    age_labels = [f"{i} - {i+9}" for i in range(0,80,10)]
    pop_labels = [f"{i} - {i+1000}" for i in range(0,13000,1000)]
    income_labels = [f"{i} - {i+1000}" for i in range(5000,87000,1000)]
    SC_labels = ['Low', 'Medium', 'Half', 'High', 'Very High']
    df2 =(
        df1
        .query("pop < 15000")
        .assign(age_group = lambda df: pd.cut(df['age'], range(0, 90, 10), right=False,labels=age_labels))
        .assign(pop_group = lambda df: pd.cut(df['pop'], range(0, 14000, 1000), right=False, labels=pop_labels))
        .assign(income_bracket = lambda df:pd.cut(df['income'], range(5000,88000,1000), right=False, labels=income_labels))
        .assign(SC_category = lambda df:pd.qcut(x = df['share_Caucasian'], q= 5, precision = 1, labels=SC_labels))
        .reset_index(drop=True) 
        .replace('White','Caucasian')
        .replace('Black','African American')
    )
    return df2