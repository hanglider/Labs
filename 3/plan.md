# md5
## 1
У нас есть файл `phones.txt` `hashes.txt`
## 2
Запускаем вот этот скрипт и получаем файл `cracked.txt`
```
hashcat -m 0 -a 3 -O --opencl-device-types 2 -w 3 C:\IT\Labs\Labs\waste\hashes.txt 89?d?d?d?d?d?d?d?d?d -o C:\IT\Labs\Labs\waste\cracked.txt
```
## 3
Парсим полученный файл и находим соль 
```
f = open("C:/IT/Labs/Labs/waste/phones.txt")
phones = []
for i in f.read().split():
    phones.append(int(i)) 
results = open("C:/IT/Labs/Labs/waste/cracked1.txt").read().split()
results= [int(i[-11:]) for i in results]
for k in results:
    counter = 0
    salt = k-phones[0]
    for v in results:
        if v-salt in phones:
            counter +=1
    if counter == len(phones):
        break
print(salt)
with open("C:/IT/Labs/Labs/waste/right_phones1.txt", 'w') as file:
    for item in results:
        file.write(f"{item - salt}\n")
```

Получаем значение соли - "41224301", и записываем новый файлик номера с вычетом соли
## 4
На всякий случай ctrl + f проверяем есть ли изначальные 5 номеров в полученном right_phones.txt **и да, они есть!!!

# sha1

## 1
Берем файл с номерами `right_pnones.txt` и хешируем его 
```
def hash_phone_numbers(phone_numbers):
    hashed_numbers = []
    for number in phone_numbers:
        number_bytes = number.encode('utf-8')
        hash_object = hashlib.sha1(number_bytes)
        hashed_number = hash_object.hexdigest()  
        hashed_numbers.append(hashed_number)
    return hashed_numbers
```
## 2
Запускаем взлом с помощью hashcat этим скриптом
```
hashcat -m 100 -a 3 -o C:\IT\Labs\Labs\waste\cracked_sha1.txt C:\IT\Labs\Labs\waste\hash_sha1.txt 89?d?d?d?d?d?d?d?d?d
```

![[Pasted image 20241024150849.png]]
## 3
Это хеширование я сделал без соли. Проверим есть ли исходные номера в `cracked_sha1.txt` 

# bcrypt

## 1 
Берем файл с номерами `right_pnones_small.txt` (всего 1000 номеров) и хешируем его 
## 2
Запускаем вот такой скрипт
```
hashcat -m 3200 -a 3 -o C:\IT\Labs\Labs\waste\cracked_bcrypt.txt C:\IT\Labs\Labs\waste\hash_bcrypt.txt 89?d?d?d?d?d?d?d?d?d
```
![[Pasted image 20241024161832.png]]
Это займет примерно 1057 лет 