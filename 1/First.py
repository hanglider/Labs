

###########################################################
###у меня почему-то прога стала в 4 раза дольше работать###
###########################################################


from random import randint as r
from random import choice
import generic as g
import pandas as pd
import hashlib
from time import time
from datetime import timedelta

stack_uniqueness_for_passport_data = []
stack_uniqueness_for_snils = []

class ID:
    def __init__(self):        
        self.Firstname, self.Lastname, self.Patronymic = g.generate_name()
        x = self.Pasport(*g.generate_passport())
        while x in stack_uniqueness_for_passport_data:
            x = self.Pasport(*g.generate_passport())
        stack_uniqueness_for_passport_data.append(x)
        self.Passport_data = x.__dict__
        r = g.generate_snils()
        while r in stack_uniqueness_for_snils:
            r = g.generate_snils()
        stack_uniqueness_for_snils.append(r)
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
    
def game(x):
    f = time()
    a = []
    strings = x*5
    for i in range(strings):
        a.append(ID().__dict__)

    t = pd.DataFrame(a)

    t.to_excel('data_set.xlsx', index=False, engine='openpyxl') ###

    seconds = time() - f
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    print(f"{int(hours)}h {int(minutes)}m {sec:.2f}s {strings} strings")
    
#for i in range(0, 5):
#    game(10**i)
game(1_00)  