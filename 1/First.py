from random import randint as r
import generic as g
import pandas as pd
import hashlib
from time import time

class ID:
    def __init__(self):        
        self.Firstname, self.Lastname, self.Patronymic = g.generate_name()
        x = self.Pasport(*g.generate_passport())
        self.Passport_data = x.__dict__
        self.snils = g.generate_snils()
        self.filled = 1
        self.med_card = self.gen_history(x)

    class Pasport:
        def __init__(self, country, series, number):
            self.country = country
            self.series = series
            self.number = number

    class medecine:
        def __init__(self, passport):
            self.symptoms = g.generate_symp()
            self.doctor = g.generate_doctors()
            self.date = g.generate_visit_time()
            self.date_offset = None 
            self.analyzes = g.generate_an()
            self.bank_card = self.generate_bank_card(passport)

        def generate_bank_card(self, passport):
            passport_data = f"{passport.series}{passport.number}"
            hash_object = hashlib.sha256(passport_data.encode())
            hash_hex = hash_object.hexdigest()
            bank_card_number = int(hash_hex[:16], 16) % (10**16)
            return bank_card_number
            

    def gen_history(self, passport):
        mc = []
        visits = r(1, 6) #6
        for _ in range(visits):
            mc.append(self.medecine(passport).__dict__)
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
game(10_000)  