import dask.dataframe as dd 
import ast
import json
import re

ddf = dd.read_parquet('data_set.parquet')

first_row = ddf.head(1)
print(first_row.iloc[0])  

firstname = first_row.iloc[0]['Firstname']
lastname = first_row.iloc[0]['Lastname']
patronymic = first_row.iloc[0]['Patronymic']
pasport = ast.literal_eval(first_row.iloc[0]['Passport'])
med_card = first_row.iloc[0]['Med_Card']
print(f"Firstname: {firstname} \nLastname: {lastname}\nPatronymic: {patronymic}\nPasport: {pasport}")
print(f"Country: {pasport['country']} \nSeries: {pasport['series']} \nNumber: {pasport['number']}")
print(f"Med_card: {type(med_card)}")