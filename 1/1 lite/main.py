from random import randint as r
from random import choice
from random import sample
import generic as g
import pandas as pd
import zlib
from time import time
from datetime import timedelta, datetime
from tqdm import tqdm
import doctors

stack_uniqueness_for_passport_data = set()
stack_uniqueness_for_snils = set()
banki = []
pay_system = []

class ID:
    def __init__(self):        
        self.Firstname, self.Lastname, self.Patronymic = g.generate_name()
        x = self.Pasport(*g.generate_passport())
        #while x in stack_uniqueness_for_passport_data:
        #    x = self.Pasport(*g.generate_passport())
        #stack_uniqueness_for_passport_data.add(x)
        self.Passport_data = x.__dict__
        r = g.generate_snils()
        #while r in stack_uniqueness_for_snils:
        #    r = g.generate_snils()
        #stack_uniqueness_for_snils.add(r)
        self.snils = r
        self.med_card = self.gen_history(x)

    class Pasport:
        def __init__(self, country, series, number):
            self.country = country
            self.series = series
            self.number = number

    class medecine:
        def __init__(self, passport, last_analysis_time=None):
            self.doctor = choice(list(doctors.doctor_symptoms.keys()))
            self.symptoms = sample(doctors.doctor_symptoms[self.doctor], r(1, 2))#self.symptoms = g.generate_symp()
            #self.doctor = choice(list(doctors.doctor_symptoms.keys()))#self.doctor = g.generate_doctors()
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
                self.pay_system = g.get_pay_system() 
                self.bank = g.get_bank()
                self.bank_card_number = self.generate_bank_card_number(passport)

            def generate_bank_card_number(self, passport):
                passport_data = f"{passport.series}{passport.number}"
                crc32_hash = zlib.crc32(passport_data.encode())  # Генерация CRC32 хеша
                bank_card_number = crc32_hash % (10**16)   
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

def show_time(f):
    seconds = time() - f
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    print(f"{int(minutes)}m {sec:.2f}s")

def get_bank():
    global banki  # Указываем, что мы изменяем глобальную переменную
    bank = ["Сбер", "Т-банк", "ВТБ"]
    d = {}
    print(f"Указывайте число от 0 до 100 для каждого банка. Общая сумма должна быть 100.")
    total = 0

    for key in bank:
        probability = int(input(f"Какую вероятность вы хотите у {key}: "))
        d[key] = probability
        total += probability

    if total != 100:
        print(f"Ошибка: сумма вероятностей должна быть равна 100. Сейчас: {total}")
        return get_bank()

    banki = []
    for key in d.keys():
        banki += [key for _ in range(d[key])]

def get_pay_system():
    global pay_system  # Указываем, что мы изменяем глобальную переменную
    bank = ["МИР", "VISA", "MASTERCARD"]
    d = {}
    print(f"Указывайте число от 0 до 100 для каждой платежной системы. Общая сумма должна быть 100.")
    total = 0

    for key in bank:
        probability = int(input(f"Какую вероятность вы хотите у {key}: "))
        d[key] = probability
        total += probability

    if total != 100:
        print(f"Ошибка: сумма вероятностей должна быть равна 100. Сейчас: {total}")
        return get_pay_system()

    pay_system = []
    for key in d.keys():
        pay_system += [key for _ in range(d[key])]


if __name__ == "__main__":
    f = time()
    get_bank()
    get_pay_system()
    t = pd.DataFrame([ID().__dict__ for _ in tqdm(range(50_000), desc="Progress")])

    print(f"Now we have data_frame", end=' ')
    show_time(f)
    print(f"Saving...")

    t.to_json('C:\IT\Labs\Labs\waste\data_set.json', force_ascii=False, orient='records', lines=True, date_format='iso', date_unit='s')

    print(f"Finish", end=" ")
    show_time(f)
    print(t.head())