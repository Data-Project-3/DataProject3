# -*- coding: utf-8 -*-
"""
Created on Tue May 10 19:18:26 2022

@author: rafap
"""

import os #Sistema Operativo
import pandas as pd #Gestionar dataframes
import numpy as np #Numeric python
import matplotlib.pyplot as plt #Graficos
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from datetime import datetime, date

#Where are we directory wise

os.getcwd()
os.chdir('C:/Users/rafap/Desktop/EDEM/6. Data Projects/3. TercerDataProject')
os.getcwd()


tr_performance = pd.read_csv("train_performance.csv", sep=',', decimal=';')
tr_datos_demog = pd.read_csv("train_datos_demograficos.csv", sep=',', decimal=';')
tr_prev_loan = pd.read_csv("train_previous_loan.csv", sep=',', decimal=';')
#Isma worked on train loan
realloan = pd.read_csv("calculated-previousloans-train-new.csv", sep=',', decimal=';')


#################################

#Merging dataset performance and demographic data with the primary key
#Demographic data ahs sesnsitive data about the client


df = tr_datos_demog.merge(tr_performance, how='inner', on='customerid')


#################################

#Make our target variable into binary (good_bad_flag into binary)
#We copy all the info into another dataframe as original must be left untouched

# df.head()
config_df = df.copy()
config_df["good_bad_flag"] = config_df["good_bad_flag"].apply(lambda x: 0 if x=='Bad' else 1) #Changing good to 1, bad to 0 
config_df["good_bad_flag"].value_counts()

#################################



#As the referredby variable has an 87% of missing variables 
#We will convert referred_by to binary, referred or not referred


config_df["referredby"].value_counts()
config_df['referredby'] = config_df['referredby'].fillna(0)
config_df['referred'] = config_df['referredby'].apply(lambda x: 0 if x==0 else 1) #Changing strings to 1 (referred), everything to 0 (not referred)
config_df.drop('referredby', axis=1, inplace=True)


#################################



#Turning birthdate into age so we can use it as a variable

config_df['age'] = pd.to_datetime(config_df.birthdate)


def from_dob_to_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

config_df['realage'] = config_df['age'].apply(lambda x: from_dob_to_age(x))
config_df.drop(['age', 'birthdate'], axis=1, inplace=True)



#################################



#We need to change variables, loanamount and totaldue to floats instead of objects
config_df.dtypes
config_df['loanamount'].isna().sum()
config_df['totaldue'].isna().sum()

config_df['loanamount'] = pd.to_numeric(config_df['loanamount'],errors = 'coerce')
config_df['totaldue'] = pd.to_numeric(config_df['totaldue'],errors = 'coerce')




#################################



#As the bank_branch_clients variable has a 99% of missing variables 
#We will convert bank_branch_clients to binary, has a bank branch or not

print(config_df['bank_branch_clients'].unique())
config_df['bank_branch_clients'].describe()
config_df['bank_branch_clients'].isna().sum()
config_df['bank_branch_clients'] = config_df['bank_branch_clients'].fillna('Unknown')

config_df['bank_branch_clients'] = config_df['bank_branch_clients'].apply(lambda x: 0 if x== 'Unknown' else 1) 



#################################


#Counting how the rate of the loan now
config_df['TipoInteresAhora'] = ((config_df['totaldue'] - config_df['loanamount']) / (config_df['loanamount'] * config_df['termdays']))*100





#################################




#Use onehotencoding to make categorical data into numerical 
#Preprocessing to be able to do it
#Na values transforming into another category 'Unknown'


#Bank account
print(config_df['bank_account_type'].unique())
config_df['bank_account_type'].isna().sum()


#Bank name clients
print(config_df['bank_name_clients'].unique())
config_df['bank_name_clients'].isna().sum()


#Employment status clients
print(config_df['employment_status_clients'].unique())
config_df['employment_status_clients'].describe()
config_df['employment_status_clients'].isna().sum()
config_df['employment_status_clients'] = config_df['employment_status_clients'].fillna('Unknown')


#Level of education
print(config_df['level_of_education_clients'].unique())
config_df['level_of_education_clients'].describe()
config_df['level_of_education_clients'].isna().sum()
config_df['level_of_education_clients'] = config_df['level_of_education_clients'].fillna('Unknown')



#Putting all categorical values into a dataframe to make onehotencoding
encoded_df = config_df[['bank_account_type', 'bank_name_clients', 'employment_status_clients', 'level_of_education_clients']].copy()


#One hot encoding
ohe = OneHotEncoder(sparse = False)
ohe_fit = ohe.fit(encoded_df)
X_ohe = pd.DataFrame(ohe.fit_transform(encoded_df))
X_ohe.columns = pd.DataFrame(ohe_fit.get_feature_names())
ohe.get_feature_names()


#Renaming after onehot encoding
del(encoded_df)

#To take out the tuple of thee name column 
def rename(col):
    if isinstance(col, tuple):
        col = '_'.join(str(c) for c in col)
    return col

#Renaming bank account type
bank_account_df = X_ohe.copy()
bank_account_df.drop(bank_account_df.iloc[:, 3:], inplace = True, axis = 1)
bank_account_df.columns = map(rename, bank_account_df.columns)
bank_account_df.columns = bank_account_df.columns.str.replace('x0', 'bank_account')


#Renaming level of education clients
level_of_edu_df = X_ohe.copy()
level_of_edu_df.drop(level_of_edu_df.iloc[:, :-5], inplace = True, axis = 1)
level_of_edu_df.columns = map(rename, level_of_edu_df.columns)
level_of_edu_df.columns = level_of_edu_df.columns.str.replace('x3', 'level_of_education_clients')


#Renaming employment status clients
employment_status_client_df = X_ohe.copy()
employment_status_client_df = employment_status_client_df.iloc[:, 21:28]
employment_status_client_df.columns = map(rename, employment_status_client_df.columns)
employment_status_client_df.columns = employment_status_client_df.columns.str.replace('x2', 'employment_status_client')


#Renaming bank name clients
bank_name_client_df = X_ohe.copy()
bank_name_client_df = bank_name_client_df.iloc[:, 3:21]
bank_name_client_df.columns = map(rename, bank_name_client_df.columns)
bank_name_client_df.columns = bank_name_client_df.columns.str.replace('x1', 'bank_name_client')



#Join all the dataframes
result = pd.concat([bank_account_df, level_of_edu_df , bank_name_client_df, employment_status_client_df ], axis=1, join='inner')


#Delete auxiliaries dataframes
del(bank_name_client_df , level_of_edu_df , bank_account_df, employment_status_client_df )
#Check X_ohe dataframe is the same as result dataframe and delete
del(X_ohe, ohe, ohe_fit)


#Merge dataframes: onehotencoding (result) and config_df
#Take away the transformewd columns
config_df.drop(['bank_account_type', 'bank_name_clients', 'employment_status_clients', 'level_of_education_clients'], axis=1, inplace=True) 
merged_df = pd.concat([config_df, result ], axis=1, join='inner')



#Delete auxiliaries dataframes
del(config_df, result)

#################################




#Dropping latitude and longitude columns

config_df.drop(['latitude_gps', 'longitude_gps'], axis=1, inplace=True) 


#Now we are going to try and find out with latitude and longitude the places where our 
#clients are

#import geocoder
#config_df['lat'].dropna()
#config_df['long'].dropna()

#config_df['latitude_gps'] = pd.to_numeric(config_df['latitude_gps'])
#config_df['long'] = pd.to_numeric(config_df['long'], downcast="float")
#def geo_rev(x):
#    g = geocoder.osm([x.lat, x.long], method='reverse').json
#    if g:
#        return g.get('country')
#    else:
#        return 'no country'

#config_df[['lat', 'long']].apply(geo_rev, axis=1)






#################################



#It does not make a difference we won't do this transformation 
#We will drop both creationdate

merged_df.drop(['creationdate', 'approveddate'], axis=1, inplace=True) 


#All the loan are approved in July
#config_df['month'] = pd.DatetimeIndex(config_df['approveddate']).month

#Time difference between approveddate - creationdate and
# test dataframe; the columns must be in a datetime format;# test dataframe; the columns must be in a datetime format;
#for col in config_df.columns:
#    if config_df[col].dtype == 'object':
#        try:
#            config_df[col] = pd.to_datetime(config_df[col])
#        except ValueError:
#            pass

#config_df.dtypes
#config_df['difference_time'] = (config_df.approveddate - config_df.creationdate)
# create a column with timedelta as total hours, as a float type
#config_df['tot_hour_diff'] = (config_df.approveddate - config_df.creationdate) / pd.Timedelta(hours=1)
#(This last column is in hours)
#config_df.drop(['difference_time', 'approveddate', 'creationdate'], axis=1, inplace=True) 
#config_df['tot_hour_diff'].describe()



#################################





#Meanwhile on the dataframe real_loan, lets make transformations


realloan.dtypes

#We need to change variables, accumlated_loan_given and accumulated_money to floats instead of objects

realloan['accumlated_loan_given'].isna().sum()
realloan['accumulated_money_won'].isna().sum()

realloan['accumlated_loan_given'] = pd.to_numeric(realloan['accumlated_loan_given'],errors = 'coerce')
realloan['accumulated_money_won'] = pd.to_numeric(realloan['accumulated_money_won'],errors = 'coerce')



#Was client late for the first payment?

realloan['is_late_for_firstpay'] = [0 if x < 0 else 1 for x in realloan['first-repay']]
# 0 he was not late for first pay, 1 he was late for first pay




final = merged_df.merge(realloan, how='inner', on='customerid')

final2 = merged_df.merge(realloan, how='outer', on='customerid')
final.to_csv('preprocessed.csv')

final2.to_csv('processed.csv')











