from random import randint as r
from random import choice
import generic as g
import pandas as pd
import hashlib
from time import time
from datetime import timedelta, datetime
from tqdm import tqdm
import multiprocessing
import dask.dataframe as dd
import numpy as np

stack_uniqueness_for_passport_data = []
stack_uniqueness_for_snils = []

class ID:
    def __init__(self):        
        self.Firstname, self.Lastname, self.Patronymic = g.generate_name()
        x = self.Pasport(*g.generate_passport())
        #while x in stack_uniqueness_for_passport_data:
        #    x = self.Pasport(*g.generate_passport())
        #stack_uniqueness_for_passport_data.append(x)
        self.Passport_data = x.__dict__
        r = g.generate_snils()
        #while r in stack_uniqueness_for_snils:
        #    r = g.generate_snils()
        #stack_uniqueness_for_snils.append(r)
        self.snils = r
        self.filled = 1
        self.med_card = self.gen_history(x)

    class Pasport:
        def __init__(self, country, series, number):
            self.country = country
            self.series = series
            self.number = number

    class medecine:
        def __init__(self, passport, last_analysis_time=None):
            self.symptoms = g.generate_symp()
            self.doctor = g.generate_doctors()
            self.date, self.date_offset = g.generate_visit_time()

            if isinstance(self.date, str):
                self.date = datetime.strptime(self.date, "%Y-%m-%d %H:%M")

            if isinstance(self.date_offset, str):
                self.date_offset = datetime.strptime(self.date_offset, "%Y-%m-%d %H:%M")
            
            if last_analysis_time:
                min_visit_time = last_analysis_time + timedelta(hours=24)
                if self.date < min_visit_time:
                    self.date = min_visit_time
            self.analyzes = g.generate_an()
            self.bank_card = self.Card(passport).__dict__  

        class Card:
            def __init__(self, passport):
                self.pay_system = choice(['SWIFT', 'TON', 'TON']) #можно настроить вероятность
                self.bank = choice(['Сбер', 'Т-банк', 'Сбер'])    #можно настроить вероятность
                self.bank_card_number = self.generate_bank_card_number(passport)

            def generate_bank_card_number(self, passport):
                passport_data = f"{passport.series}{passport.number}"
                hash_object = hashlib.sha256(passport_data.encode())
                hash_hex = hash_object.hexdigest()
                bank_card_number = int(hash_hex[:16], 16) % (10**16)  
                return bank_card_number                

    def gen_history(self, passport):
        mc = []
        last_analysis_time = None
        visits = r(1, 6) #6
        for _ in range(visits):
            medicine_entry = self.medecine(passport, last_analysis_time).__dict__
            mc.append(medicine_entry)            
            last_analysis_time = medicine_entry['date_offset'] 
        return mc 
    
def generate_id_data(n):
    return [ID().__dict__ for _ in tqdm(range(n), desc="Progress")]
    #return [ID().__dict__ for _ in range(n)]

def show_time(f):
    seconds = time() - f
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    print(f"{int(minutes)}m {sec:.2f}s")
        
def game_parallel(x):                                  #####FIRST
    f = time()
    num_workers = multiprocessing.cpu_count() 
    strings = x
    chunk_size = strings // num_workers

    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(generate_id_data, [chunk_size] * num_workers)

    a = []
    for result in results:
        a.extend(result)

    print(f"Now we have data")
    show_time(f)

    t = pd.DataFrame(a)

    print(f"Now we have data_frame")
    show_time(f)
    print(f"Saving...")

    t.to_excel('data_set.xlsx', index=False, engine='openpyxl')  ###

    print(f"Finish", end=" ")
    show_time(f)

def generate_id_data_as_columns(n):
    
    #"""Генерация данных в формате столбцов (numpy массивов)"""
    firstnames, lastnames, patronymics, passports, snils, med_cards = [], [], [], [], [], []

    for _ in tqdm(range(n), desc="Progress"):
    #for _ in range(n):
        id_obj = ID()
        firstnames.append(id_obj.Firstname)
        lastnames.append(id_obj.Lastname)
        patronymics.append(id_obj.Patronymic)
        passports.append(str(id_obj.Passport_data))
        snils.append(id_obj.snils)
        med_cards.append(str(id_obj.med_card))  # преобразуем сложные данные в строки для примера

    # Преобразуем данные в numpy массивы
    data = {
        'Firstname': np.array(firstnames, dtype='object'),
        'Lastname': np.array(lastnames, dtype='object'),
        'Patronymic': np.array(patronymics, dtype='object'),
        'Passport': np.array(passports, dtype='object'),
        'SNILS': np.array(snils, dtype='object'),
        'Med_Card': np.array(med_cards, dtype='object')
    }

    return data

def game_parallel_optimized(x):
    f = time()
    num_workers = multiprocessing.cpu_count()  
    strings = x
    chunk_size = strings // num_workers

    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(generate_id_data_as_columns, [chunk_size] * num_workers)

    # Объединение данных из всех процессов
    combined_data = {key: np.concatenate([result[key] for result in results]) for key in results[0]}

    print(f"Now we have data", end=" ")
    show_time(f)

    # Быстрое создание DataFrame из заранее подготовленных данных
    t = pd.DataFrame(combined_data)

    print(f"Now we have data_frame", end=" ")
    show_time(f)
    print(f"Saving...")

    t.to_excel('data_set.xlsx', index=False, engine='openpyxl')  ###

    print(f"Finish", end=" ")
    show_time(f)

def game_dask(x):
    f = time()
    num_workers = multiprocessing.cpu_count()
    strings = x
    chunk_size = strings // num_workers

    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(generate_id_data_as_columns, [chunk_size] * num_workers)

    combined_data = {key: np.concatenate([result[key] for result in results]) for key in results[0]}

    print(f"Now we have data", end=" ")
    show_time(f)    

    # Создание Dask DataFrame
    ddf = dd.from_pandas(pd.DataFrame(combined_data), npartitions=num_workers)

    print(f"Now we have data_frame", end=" ")
    show_time(f)  
    print(f"Saving...")

    # Запись в файл через Dask
    ddf.to_parquet('data_set.parquet', engine='pyarrow')

    print(f"Finish", end=" ")
    show_time(f)

k = 3
n = 1_0_0

if __name__ == "__main__":
    if k == 1:
        game_parallel(n)
        print()
    elif k == 2:
        game_parallel_optimized(n)
        print()
    elif k == 3:
        game_dask(n)