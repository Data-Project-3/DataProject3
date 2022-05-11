# -*- coding: utf-8 -*-
"""
Created on Thu May  5 00:17:49 2022
@author: alvar
"""
import pandas as pd
from functools import partial
from geopy.point import Point
from geopy.geocoders import Nominatim
from pandasql import sqldf
import pandas as pd
from sklearn import datasets
import os  
os.makedirs(r'C:\Users\Ismail\Downloads', exist_ok=True)  
os.getcwd()
df = pd.read_csv(r'C:\Users\Ismail\Downloads\train_previous_loans.csv')



df["creationdate"] = pd.to_datetime(df["creationdate"])
df["approveddate"] = pd.to_datetime(df["approveddate"])
df["closeddate"] = pd.to_datetime(df["closeddate"])
df["firstduedate"] = pd.to_datetime(df["firstduedate"])
df["firstrepaiddate"] = pd.to_datetime(df["firstrepaiddate"])
df['delta_repayed'] = (df['firstrepaiddate']-df['firstduedate'])
df['delta'] = (df['approveddate']-df['creationdate'])
df['delta_closed'] = (df['closeddate']-df['creationdate'])
df['money_won'] = (df['totaldue']-df['loanamount'])

q = "SELECT count (*), customerid , SUM (loanamount) , SUM(delta) , SUM(delta_repayed), SUM(delta_closed) , SUM(money_won) FROM df group by customerid "
sqldf(q, globals())

d = sqldf(q, globals())

dz = pd.DataFrame(data=d)

dz.rename(columns = {'count (*)':'number_of_Loans', 'SUM (loanamount)':'accumlated_loan_given', 'SUM(delta)':'accumlated_timediff', 'SUM(delta_repayed)':'first-repay', 'SUM(delta_closed)':'time-to-payoff', 'SUM(money_won)':'accumulated_money_won'}, inplace = True)

dz.to_csv("calculated-previousloans-train-new.csv", index=False)
