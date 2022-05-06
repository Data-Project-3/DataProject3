# -*- coding: utf-8 -*-
"""
Created on Thu May  5 00:17:49 2022

@author: alvar
"""
import pandas as pd
from geopy.point import Point
from geopy.geocoders import Nominatim

df = pd.read_csv(r'C:\Users\alvar\Desktop\merged_missingvalues_solved.csv')

geolocator=Nominatim(user_agent='Prueba')

for i in range(len(df)):
    lat = (df['longitude_gps'][i])
    lang = (df['latitude_gps'][i])
    while i<len(df):
        i+=1
    location = geolocator.reverse([lat,lang])
    print(location.address)
