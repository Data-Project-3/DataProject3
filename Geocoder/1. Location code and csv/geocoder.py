# -*- coding: utf-8 -*-
"""
Created on Thu May  5 00:17:49 2022

@author: alvar
"""
import pandas as pd
import reverse_geocoder as rg

df = pd.read_csv(r'C:\Users\alvar\Desktop\finalmerged.csv')

# cogemos las columnas de ubicacion
df_loc = df[['customerid', 'longitude_gps', 'latitude_gps']]

# sacamos las coordenadas de cada clienteid
rg.search((df_loc.latitude_gps[1], df_loc.longitude_gps[1]))

# creamos columnas con el pais y el estado de las coordenadas
df_loc['country'] = df_loc.apply(lambda x: rg.search((x['latitude_gps'], x['longitude_gps']))[0]['cc'], axis=1)
df_loc['state'] = df_loc.apply(lambda x: rg.search((x['latitude_gps'], x['longitude_gps']))[0]['admin1'], axis=1)

# pasamos el dataframe al csv
df_loc.to_csv(r'C:\Users\alvar\Desktop\geocoder.csv', index = False)