import pandas as pd
from scipy import stats
import numpy as np
import seaborn as sns

def load_and_process(url_or_path_to_csv_file):
    
    #method chain 1 (load and Clean data - remove columns an rows, rename columns, deal with missing data, and format data)

    df1 = (
        pd.read_csv(url_or_path_to_csv_file, encoding = "ISO-8859-1")
        .drop(['name', 'day', 'year','h_income','county_income', 'comp_income','county_bucket', 'nat_bucket', 'share_black', 'share_hispanic', 'college', 'streetaddress', 'pov', 'city', 'latitude', 'longitude', 'state_fp', 'county_fp', 'tract_ce', 'geo_id', 'county_id', 'namelsad', 'lawenforcementagency'], axis =1)
        .rename(columns={"p_income": "income"})
        .dropna().reset_index(drop=True)
        .query("age != 'Unknown' & cause != 'Unknown' & armed != 'Unknown'")  
    )
    df1['age'] = pd.to_numeric(df1['age'])
    df1['income'] = pd.to_numeric(df1['income'])
    df1['share_white'] = pd.to_numeric(df1['share_white'])
    
    #method chain 2 (Process Data - deal with outliers and create new columns)

    age_labels = [f"{i} - {i+9}" for i in range(0,80,10)]
    pop_labels = [f"{i} - {i+1000}" for i in range(0,13000,1000)]
    income_labels = [f"{i} - {i+1000}" for i in range(5000,87000,1000)]
    urate_labels = ['0.0 - 0.05', '0.06 - 0.08', '0.09 - 0.11', '0.12 - 0.15', '0.15 - 0.51']
    SW_labels = ['Low', 'Medium', 'Half', 'High', 'Very High']
    df2 =(
        df1
        .query("pop < 15000")
        .assign(age_group = lambda x: pd.cut(x['age'], range(0, 90, 10), right=False,labels=age_labels))
        .assign(pop_group = lambda df: pd.cut(df['pop'], range(0, 14000, 1000), right=False, labels=pop_labels))
        .assign(income_bracket = lambda df:pd.cut(df['income'], range(5000,88000,1000), right=False, labels=income_labels))
        .assign(urate_level = lambda df: pd.qcut(x = df['urate'], q= 5, precision = 2, labels=urate_labels))
        .assign(SW_category = lambda df:pd.qcut(x = df['share_white'], q= 5, precision = 1, labels=SW_labels))
        .reset_index(drop=True) 
    )
    return df2