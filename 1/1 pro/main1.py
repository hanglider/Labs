import numpy as np
import pandas as pd
import hashlib
from time import time
from datetime import timedelta, datetime
from random import randint as r, choice
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import shared_memory
import multiprocessing
import generic as g
import dask.dataframe as dd

const = 10**16

# Pre-cached pools of symptoms and doctors
symptoms_pool = [g.generate_symp() for _ in range(5000)]
doctor_pool = [g.generate_doctors() for _ in range(50)]

class ID:
    def __init__(self):        
        self.Firstname, self.Lastname, self.Patronymic = g.generate_name()
        self.Passport_data = self.Pasport(*g.generate_passport()).__dict__
        self.snils = g.generate_snils()
        self.med_card = self.gen_history()

    class Pasport:
        def __init__(self, country, series, number):
            self.country = country
            self.series = series
            self.number = number

    class medecine:
        def __init__(self, passport, last_analysis_time=None):
            self.symptoms = choice(symptoms_pool)
            self.doctor = choice(doctor_pool)
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
                self.pay_system = choice(['SWIFT', 'TON', 'TON'])
                self.bank = choice(['Сбер', 'Т-банк', 'Сбер'])
                self.bank_card_number = self.generate_bank_card_number(passport)

            def generate_bank_card_number(self, passport):
                passport_data = f"{passport['series']}{passport['number']}"
                hash_object = hashlib.sha256(passport_data.encode())
                hash_hex = hash_object.hexdigest()
                bank_card_number = int(hash_hex[:16], 16) % const
                return bank_card_number

    def gen_history(self):
        mc = []
        last_analysis_time = None
        visits = r(1, 6)
        for _ in range(visits):
            medicine_entry = self.medecine(self.Passport_data, last_analysis_time).__dict__
            mc.append(medicine_entry)
            last_analysis_time = medicine_entry['date_offset']
        return mc 

def generate_id_data_as_columns(n):
    """Генерация данных в формате столбцов (numpy массивов)"""
    firstnames, lastnames, patronymics, passports, snils, med_cards = [], [], [], [], [], []

    for _ in range(n):
        id_obj = ID()
        firstnames.append(id_obj.Firstname)
        lastnames.append(id_obj.Lastname)
        patronymics.append(id_obj.Patronymic)
        passports.append(str(id_obj.Passport_data))
        snils.append(id_obj.snils)
        med_cards.append(str(id_obj.med_card))

    data = {
        'Firstname': np.array(firstnames, dtype='object'),
        'Lastname': np.array(lastnames, dtype='object'),
        'Patronymic': np.array(patronymics, dtype='object'),
        'Passport': np.array(passports, dtype='object'),
        'SNILS': np.array(snils, dtype='object'),
        'Med_Card': np.array(med_cards, dtype='object')
    }
    return data

def save_data_to_excel(data):
    df = pd.DataFrame(data)
    df.to_excel('data_set.xlsx', index=False, engine='openpyxl')

def worker_task(chunk_size):
    return generate_id_data_as_columns(chunk_size)

def game_parallel_optimized(num_records):
    start_time = time()

    # Определение числа потоков в зависимости от числа доступных ядер CPU
    num_workers = multiprocessing.cpu_count()
    chunk_size = num_records // num_workers

    # Использование ProcessPoolExecutor для запуска параллельных задач
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(worker_task, [chunk_size] * num_workers))

    # Объединение результатов
    combined_data = {key: np.concatenate([result[key] for result in results]) for key in results[0]}

    print(f"Data generated", end=" ")
    show_time(start_time)

    t = pd.DataFrame(combined_data)
    t.to_json('C:\IT\Labs\Labs\waste\data_set.json', force_ascii=False, orient='records', lines=True, date_format='iso', date_unit='s')
    print(f"Finish", end=" ")
    show_time(start_time)

def show_time(f):
    seconds = time() - f
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    print(f"{int(minutes)}m {sec:.2f}s")

if __name__ == "__main__":
    game_parallel_optimized(50_000)
