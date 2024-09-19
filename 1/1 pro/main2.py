import numpy as np
import pandas as pd
from random import randint as r
from random import choice
import generic as g
import hashlib
from time import time
from datetime import timedelta, datetime
from tqdm import tqdm
import concurrent.futures as cf
import dask.dataframe as dd
import multiprocessing

const = 10**16

# Пул для симптомов и врачей с ленивой инициализацией
symptoms_pool = None
doctor_pool = None

def get_symptoms_pool():
    global symptoms_pool
    if symptoms_pool is None:
        symptoms_pool = [g.generate_symp() for _ in range(5000)]
    return symptoms_pool

def get_doctor_pool():
    global doctor_pool
    if doctor_pool is None:
        doctor_pool = [g.generate_doctors() for _ in range(50)]
    return doctor_pool

class ID:
    def __init__(self):
        self.Firstname, self.Lastname, self.Patronymic = g.generate_name()
        x = self.Passport(*g.generate_passport())
        self.Passport_data = x.__dict__
        r = g.generate_snils()
        self.snils = r
        self.med_card = self.gen_history(x)

    class Passport:
        def __init__(self, country, series, number):
            self.country = country
            self.series = series
            self.number = number

    class Medicine:
        def __init__(self, passport, last_analysis_time=None):
            self.symptoms = choice(get_symptoms_pool())
            self.doctor = choice(get_doctor_pool())
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
                self.pay_system = choice(['SWIFT', 'TON', 'TON'])  # Можно настроить вероятность
                self.bank = choice(['Сбер', 'Т-банк', 'Сбер'])     # Можно настроить вероятность
                self.bank_card_number = self.generate_bank_card_number(passport)

            def generate_bank_card_number(self, passport):
                passport_data = f"{passport.series}{passport.number}"
                hash_object = hashlib.sha256(passport_data.encode())
                hash_hex = hash_object.hexdigest()
                bank_card_number = int(hash_hex[:16], 16) % const
                return bank_card_number

    def gen_history(self, passport):
        mc = []
        last_analysis_time = None
        visits = r(1, 6)
        for _ in range(visits):
            medicine_entry = self.Medicine(passport, last_analysis_time).__dict__
            mc.append(medicine_entry)
            last_analysis_time = medicine_entry['date_offset']
        return mc

def show_time(f):
    seconds = time() - f
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    print(f"{int(minutes)}м {sec:.2f}с")

def generate_id_data_as_columns(n):
    """Генерация данных в формате столбцов (numpy массивов)"""
    firstnames, lastnames, patronymics, passports, snils, med_cards = [], [], [], [], [], []

    for _ in tqdm(range(n), desc="Прогресс"):
        id_obj = ID()
        firstnames.append(id_obj.Firstname)
        lastnames.append(id_obj.Lastname)
        patronymics.append(id_obj.Patronymic)
        passports.append(str(id_obj.Passport_data))
        snils.append(id_obj.snils)
        med_cards.append(str(id_obj.med_card))  # Преобразуем сложные данные в строки для примера

    data = {
        'Firstname': np.array(firstnames, dtype='object'),
        'Lastname': np.array(lastnames, dtype='object'),
        'Patronymic': np.array(patronymics, dtype='object'),
        'Passport': np.array(passports, dtype='object'),
        'SNILS': np.array(snils, dtype='object'),
        'Med_Card': np.array(med_cards, dtype='object')
    }

    return data

def game_dask(x):
    f = time()
    num_workers = multiprocessing.cpu_count()
    strings = x
    chunk_size = max(1000, strings // num_workers)

    # Используем ProcessPoolExecutor вместо multiprocessing.Pool
    with cf.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(generate_id_data_as_columns, chunk_size) for _ in range(num_workers)]
        results = [f.result() for f in futures]

    # Объединяем результаты
    combined_data = {key: np.concatenate([result[key] for result in results]) for key in results[0]}

    print("Данные готовы", end=" ")
    show_time(f)

    # Создаем Dask DataFrame
    ddf = dd.from_pandas(pd.DataFrame(combined_data), npartitions=num_workers)

    print("DataFrame готов", end=" ")
    show_time(f)
    print("Сохранение...")

    # Сохраняем в Parquet
    ddf.to_parquet('data_set.parquet', engine='pyarrow')

    print("Завершено", end=" ")
    show_time(f)

if __name__ == "__main__":
    game_dask(50_000)
