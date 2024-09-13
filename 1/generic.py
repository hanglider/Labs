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

def generate_visit_time():
    start_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    random_time = start_time + timedelta(minutes = r(0, (end_time - start_time).seconds // 60))
    return random_time.strftime("%H:%M")

def generate_name():
        if r(0, 1):
            return Firstnames.female_names[r(0, len(Firstnames.female_names) - 1)], Lastnames.female_surnames[r(0, len(Lastnames.female_surnames) - 1)], Patronymic.female_patronymics[r(0, len(Patronymic.female_patronymics) - 1)]
        else:
            return Firstnames.male_names[r(0, len(Firstnames.male_names) - 1)], Lastnames.surnames[r(0, len(Lastnames.surnames) - 1)], Patronymic.male_patronymics[r(0, len(Patronymic.male_patronymics) - 1)]
        
def generate_doctors():
    return doctors.doctor_specialties[r(0, len(doctors.doctor_specialties) - 1)]

def generate_symp():
    return [sample(symptoms.symptoms, r(1, 11))] #11

def generate_an():
    return [sample(analyzes.medical_tests, r(1, 6))] #6
