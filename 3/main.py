import hashlib
import bcrypt
import tqdm

def hash_phone_numbers_sha1(phone_numbers):
    hashed_numbers = []
    for number in tqdm.tqdm(phone_numbers, desc="Hashing phone numbers (SHA1)"):
        number_bytes = number.encode('utf-8')
        hash_object = hashlib.sha1(number_bytes)
        hashed_number = hash_object.hexdigest()  
        hashed_numbers.append(hashed_number)
    return hashed_numbers

def hash_strings_with_bcrypt(strings):
    hashed_strings = []
    for string in tqdm.tqdm(strings, desc="Hashing strings with bcrypt"):
        password = string.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        hashed_strings.append(hashed_password.decode('utf-8'))
    
    return hashed_strings

def read_phone_numbers(file_path):
    with open(file_path, 'r') as file:
        phone_numbers = [line.strip() for line in file]
    return phone_numbers

def write_hashed_numbers(file_path, hashed_numbers):
    with open(file_path, 'w') as file:
        for hashed_number in hashed_numbers:
            file.write(hashed_number + '\n')

input_file = 'C:/IT/Labs/Labs/waste/right_pnones_small.txt'
output_file = 'C:/IT/Labs/Labs/waste/hash_bcrypt.txt'
salt = '13'

phone_numbers = read_phone_numbers(input_file)
#hashed_numbers = hash_phone_numbers_sha1(phone_numbers)
hashed_numbers = hash_strings_with_bcrypt(phone_numbers)
write_hashed_numbers(output_file, hashed_numbers)

print(f"Hashed phone numbers have been written to {output_file}")
