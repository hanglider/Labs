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