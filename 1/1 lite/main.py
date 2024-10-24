from random import randint as r
from random import choice                           
from random import sample
import generic as g
import pandas as pd                                 
import hashlib                                      
from time import time                               
from datetime import timedelta, datetime            
from tqdm import tqdm                               
import doctors
import xml.etree.ElementTree as ET                  

stack_uniqueness_for_passport_data = set()
stack_uniqueness_for_snils = set()
banki = []
pay_system = []
const = 10*16

# class ID:
#     def __init__(self):        
#         self.Firstname, self.Lastname, self.Patronymic = g.generate_name()
#         x = self.Pasport(*g.generate_passport())
#         while x in stack_uniqueness_for_passport_data:
#             x = self.Pasport(*g.generate_passport())
#         stack_uniqueness_for_passport_data.add(x)
#         self.Passport_data = x.__dict__
#         r = g.generate_snils()
#         while r in stack_uniqueness_for_snils:
#             r = g.generate_snils()
#         stack_uniqueness_for_snils.add(r)
#         self.snils = r
#         self.med_card = self.med_card = self.Medecine(x, None).__dict__

#     class Pasport:
#         def __init__(self, country, series, number):
#             self.country = country
#             self.series = series
#             self.number = number

#     class Medecine:
#         def __init__(self, passport, last_analysis_time=None):
#             self.doctor = choice(list(doctors.doctor_symptoms.keys()))
#             self.symptoms = sample(doctors.doctor_symptoms[self.doctor], r(1, 2))
#             self.date, self.date_offset = g.generate_visit_time()

#             if isinstance(self.date, str):
#                 self.date = datetime.strptime(self.date, "%Y-%m-%d %H:%M")

#             if isinstance(self.date_offset, str):
#                 self.date_offset = datetime.strptime(self.date_offset, "%Y-%m-%d %H:%M")
            
#             if last_analysis_time:
#                 min_visit_time = last_analysis_time + timedelta(hours=24)
#                 if self.date < min_visit_time:
#                     self.date = min_visit_time
#             self.analyzes = g.generate_an()
#             self.total_analysis_cost = sum(analyze[1] for analyze in self.analyzes)
#             self.bank_card = self.Card(passport).__dict__  

#         class Card:
#             def __init__(self, passport):
#                 self.pay_system = choice(pay_system)
#                 self.bank = choice(banki)
#                 self.bank_card_number = self.generate_bank_card_number(passport)

#             def generate_bank_card_number(self, passport):
#                 passport_data = f"{passport.series}{passport.number}"
#                 hash_object = hashlib.sha256(passport_data.encode())
#                 hash_hex = hash_object.hexdigest()
#                 bank_card_number = int(hash_hex, 16) % const
#                 return bank_card_number                

#     def gen_history(self, passport):
#         mc = []
#         last_analysis_time = None
#         visits = r(1, 6) #6
#         for _ in range(visits):
#             medicine_entry = self.Medecine(passport, last_analysis_time).__dict__
#             mc.append(medicine_entry)            
#             last_analysis_time = medicine_entry['date_offset'] 
#         return mc 

class ID:
    def __init__(self):        
        self.Firstname, self.Lastname, self.Patronymic = g.generate_name()
        x = self.Pasport(*g.generate_passport())
        while x in stack_uniqueness_for_passport_data:
            x = self.Pasport(*g.generate_passport())
        stack_uniqueness_for_passport_data.add(x)
        self.Passport_data = x.__dict__
        r = g.generate_snils()
        while r in stack_uniqueness_for_snils:
            r = g.generate_snils()
        stack_uniqueness_for_snils.add(r)
        self.snils = r
        med_card_instance = self.Medecine(x, None)
        # Устанавливаем отдельные поля для каждого атрибута класса Medecine
        self.doctor = med_card_instance.doctor
        self.symptoms = med_card_instance.symptoms
        self.date = med_card_instance.date
        self.date_offset = med_card_instance.date_offset
        self.analyzes = med_card_instance.analyzes
        self.total_analysis_cost = med_card_instance.total_analysis_cost
        self.bank_card_pay_system = med_card_instance.bank_card.pay_system
        self.bank_card_bank = med_card_instance.bank_card.bank
        self.bank_card_number = med_card_instance.bank_card.bank_card_number

    class Pasport:
        def __init__(self, country, series, number):
            self.country = country
            self.series = series
            self.number = number

    class Medecine:
        def __init__(self, passport, last_analysis_time=None):
            self.doctor = choice(list(doctors.doctor_symptoms.keys()))
            self.symptoms = sample(doctors.doctor_symptoms[self.doctor], r(1, 2))
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
            self.total_analysis_cost = sum(analyze[1] for analyze in self.analyzes)
            self.bank_card = self.Card(passport)  # Экземпляр вложенного класса Card

        class Card:
            def __init__(self, passport):
                self.pay_system = choice(pay_system)
                self.bank = choice(banki)
                self.bank_card_number = self.generate_bank_card_number(passport)

            def generate_bank_card_number(self, passport):
                passport_data = f"{passport.series}{passport.number}"
                hash_object = hashlib.sha256(passport_data.encode())
                hash_hex = hash_object.hexdigest()
                bank_card_number = str(int(hash_hex, 16))[:16] 
                return bank_card_number


def show_time(f):
    seconds = time() - f
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    print(f"{int(minutes)}m {sec:.2f}s")

def get_bank():
    global banki  
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
    global pay_system  
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

import xml.dom.minidom as minidom

def dict_to_xml(tag, d):
    """
    Конвертирует словарь в XML.
    :param tag: корневой тег
    :param d: словарь с данными
    :return: элемент XML
    """
    elem = ET.Element(tag)
    for key, val in d.items():
        child = ET.Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

def save_to_xml(data_frame, filepath):
    """
    Сохраняет DataFrame в XML файл.
    :param data_frame: DataFrame для сохранения
    :param filepath: путь для сохранения XML
    """
    root = ET.Element("dataset")  # Корневой элемент

    for _, row in data_frame.iterrows():
        record_elem = dict_to_xml("record", row.to_dict())
        root.append(record_elem)

    # Создание строки XML с форматированием
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # Сохранение в файл
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)


if __name__ == "__main__":
    print(f"Введити количество записей: ", end="")
    n = int(input())
    n = max(50_000, n)
    get_bank()
    get_pay_system()
    f = time()
    t = pd.DataFrame([ID().__dict__ for _ in tqdm(range(n), desc="Progress")])

    print(f"Now we have data_frame", end=' ')
    show_time(f)
    print(f"Saving...")

    save_to_xml(t, 'C:\\IT\\Labs\\Labs\\waste\\data_set.xml')

    print(f"Finish", end=" ")
    show_time(f)