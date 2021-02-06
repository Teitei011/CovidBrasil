# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:33:31 2021

@author: stefa
"""

import time
#import modin.pandas as pd
import pandas as pd

tempo_inicial = time.time()

def determine_state_city_or_country(name):
    '''
        This is a hack that only work on this specific scenario
    '''
    if (len(name) == 2):
        return "city"
    elif(name == "Brazil"):
        return "Brazil"
    else:
        return "city"
    

def get_data(dataframe, name):
    index_ = determine_state_city_or_country(name)
    result_dataframe =  dataframe[dataframe[index_].isin([name])]
    
    result_dataframe.loc[:, "daily cases moving average"] = result_dataframe['daily cases'].rolling(window=14).mean() 
    result_dataframe.loc[:, "daily deaths moving average"] =   result_dataframe['daily deaths'].rolling(window=14).mean() 

    
    result_dataframe.pop("city")   
    result_dataframe.to_csv(f"{name}.csv", index=False)
    
def separate_each_city_on_dataframe(dataframe):
    # set the index to be this and don't drop
    dataframe.set_index(keys=['city'], drop=False,inplace=True)
    
    # get a list of names
    city_names = dataframe['city'].unique().tolist()

    
    # now we can perform a lookup on a 'view' of the dataframe
    counter = 0
    for city in city_names:
        counter += 1
        print("Processing: {}  - {:.2f}% ...".format(city, counter*100/5297))
        buffer_dataframe = dataframe.loc[dataframe.city==city]
        buffer_dataframe.to_csv(f"brazil/{city}.csv")

    
    # now you can query all 'joes' 


file_name = "brazil.csv"
#def pre_processing_csv_data(file_name):
teste = pd.read_csv(str(file_name), delimiter=";", error_bad_lines=False)

city = teste.groupby(["municipio", "data"])[['casosAcumulado', 'casosNovos', 'obitosAcumulado', 'obitosNovos']].sum()
city = city.rename(columns={"municipio": "city", "data": "date", 'casosAcumulado': 'cases', 'obitosAcumulado': 'deaths', 'casosNovos' : "daily cases", "obitosNovos": "daily deaths", })

state = teste.groupby(["estado", "data"])[['casosAcumulado', 'casosNovos', 'obitosAcumulado', 'obitosNovos']].sum()
state = state.rename(columns={"estado": "city", "data": "date", 'casosAcumulado': 'cases', 'obitosAcumulado': 'deaths', 'casosNovos' : "daily cases", "obitosNovos": "daily deaths"})

city.to_csv("brazil/brazil_cities.csv")
state.to_csv("brazil/brazil_states.csv")

del teste
del city
del state

cities = pd.read_csv("brazil/brazil_cities.csv")
states = pd.read_csv("brazil/brazil_states.csv")

cities = cities.rename(columns={"municipio": "city", "data": "date"})
states = states.rename(columns={"estado": "city", "data": "date"})

brazil = states.groupby("date")[[ "cases", "daily cases", "deaths", 
                                 "daily deaths"]].sum()

brazil["daily cases moving average"] = brazil['daily cases'].rolling(window=14).mean()
brazil["daily deaths moving average"] = brazil['daily deaths'].rolling(window=14).mean()
brazil.to_csv("Brasil.csv")

separate_each_city_on_dataframe(cities)

#get_data(cities, "Botucatu")
#get_data(cities, "Sorocaba")
#get_data(cities, "São Carlos")
#get_data(cities, "Machado")
#get_data(states, "SP")
#get_data(states, "MG")


print("It took {:.2f} seconds".format(time.time() - tempo_inicial) )