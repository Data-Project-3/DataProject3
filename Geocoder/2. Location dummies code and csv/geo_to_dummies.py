# -*- coding: utf-8 -*-
"""
Created on Tue May 10 13:56:03 2022

@author: alvar
"""
import pandas as pd

# cargamos los csv
df = pd.read_csv(r'C:\Users\alvar\Desktop\finalmerged.csv')
geo = pd.read_csv(r'C:\Users\alvar\Desktop\EDEM\2.GITHUB\DataProject3\Geocoder\geocoder.csv')

# unimos ambos para tener la localización en relación con el customerid
merged_left = pd.merge(left=df,right=geo, how='left', left_on='customerid', right_on='customerid')

# creamos una copia
df2 = merged_left.copy() 

# en la copia pasamos las variables country y state a dummies
df2 = pd.get_dummies(df2, columns = ['country', 'state'])

# pasamos el dataframe al csv
df2.to_csv(r'C:\Users\alvar\Desktop\dataset_geo_dummies.csv', index = False)