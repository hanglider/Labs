from random import randint as r
import generic as g

class Pasport:
    country = ""
    series = 0
    number = 0

    def __init__(self, country, series, number):
        self.country = country
        self.series = series
        self.number = number

class ID:
    filled = 0
    Firstname = ""
    Lastname = ""
    Patronymic = ""
    Passport_data = Pasport("", 0, 0)
    snils = 0
    lucky = 50

    def __init__(self):        
        self.Firstname, self.Lastname, self.Patronymic = g.generate_name()
        self.Passport_data = Pasport(*g.generate_passport())
        self.snils = g.generate_snils()
        self.filled = 1

    


class medecine:
    #зачем нам стоимость анализов, если ее можно идентифицировать по самому анализу ?)
    symptoms = []
    doctor = "" 
    date = "" 
    date_offset = 0 
    analyzes = [] 
    bank_card = 0
    def __init__(self, client, date):
        self.symptoms = g.generate_symp()
        self.doctor = g.generate_doctors()
        self.date = date
        self.date_offset = None 
        self.analyzes = g.generate_an()
        self.bank_card = (client.Passport_data.number * 1e7) % 1e16


x = ID()
print(x.Firstname, x.Lastname, x.Patronymic, x.Passport_data.country, x.Passport_data.series, x.Passport_data.number, x.snils, x.filled)
exit()
count_days = 1 
data = []
wait_list = [] 

for i in range(3600*24*count_days):
    if r(0, 100) < 5:
        if len(wait_list) < 1:          #люди которые придут в первый раз 
            t = medecine(ID(), i)
            data
        else:
            if r(0, 10) < 4:
                pass 
        

