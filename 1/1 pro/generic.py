from random import randint as r
from random import sample 
import Firstnames, Patronymic, Lastnames, doctors, symptoms, analyzes
from datetime import datetime, timedelta

def generate_passport():
    country = ['Россия', 'Беларусь', 'Казахстан'][r(0, 2)]
    if country == 'Россия':
        series = ''.join([str(r(0, 9)) for _ in range(4)])
        number = ''.join([str(r(0, 9)) for _ in range(6)])
    elif country == 'Беларусь':
        series = ''.join([chr(r(65, 90)) for _ in range(2)])  
        number = ''.join([str(r(0, 9)) for _ in range(7)])
    elif country == 'Казахстан':
        series = ''.join([chr(r(65, 90)) for _ in range(2)])  
        number = ''.join([str(r(0, 9)) for _ in range(7)])
    return country, series, number
    
def generate_snils():
    return '{}-{}-{} {}'.format(
    str(r(100, 999)),
    str(r(100, 999)),
    str(r(100, 999)),
    str(r(10, 99))
)

def get_bank():
    x = r(1, 100)
    if x < 21:
        return "Сбер"
    elif x < 51:
        return "Т-банк"
    return "ВТБ"

def get_pay_system():
    x = r(1, 100)
    if x < 21:
        return "VISA"
    elif x < 51:
        return "MASTERCARD"
    return "МИР"

def generate_visit_time():
    start_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    random_time = start_time + timedelta(minutes=r(0, (end_time - start_time).seconds // 60))
    year = 2023
    month = r(1, 12)
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = r(1, 31)
    elif month in [4, 6, 9, 11]:
        day = r(1, 30)
    else:
        day = r(1, 28)

    visit_time_1 = datetime(year, month, day, random_time.hour, random_time.minute)
    
    hours_offset = r(24, 72)
    visit_time_2 = visit_time_1 + timedelta(hours=hours_offset)
    
    return visit_time_1.strftime("%Y-%m-%d %H:%M"), visit_time_2.strftime("%Y-%m-%d %H:%M")

def generate_name():
        if r(0, 1):
            return Firstnames.female_names[r(0, len(Firstnames.female_names) - 1)], Lastnames.female_surnames[r(0, len(Lastnames.female_surnames) - 1)], Patronymic.female_patronymics[r(0, len(Patronymic.female_patronymics) - 1)]
        else:
            return Firstnames.male_names[r(0, len(Firstnames.male_names) - 1)], Lastnames.surnames[r(0, len(Lastnames.surnames) - 1)], Patronymic.male_patronymics[r(0, len(Patronymic.male_patronymics) - 1)]
        
def generate_doctors():
    return doctors.doctor_specialties[r(0, len(doctors.doctor_specialties) - 1)]

def generate_symp():
    return [sample(symptoms.symptoms, r(1, 10))] 

def generate_an():
    selected_tests = sample(list(analyzes.medical_tests_with_prices.items()), r(1, 5))
    return selected_tests