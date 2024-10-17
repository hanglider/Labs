import pandas as pd

numbers = ['89159518539', '89637872649', '89698570777', '89038263485', '89626643998']

def excel_to_dataframe(file_path):
    df = pd.read_excel(file_path, usecols=[0])
    df.columns = ["hashes"]
    return df

# Загрузка данных из xlsx файла
file_path = 'C:\IT\Labs\Labs\waste\data.xlsx'
df = excel_to_dataframe(file_path)

# Сохраните хеши в текстовый файл
df['hashes'].to_csv('hashes.txt', index=False, header=False)

# Сохраните известные номера в текстовый файл
with open('C:\IT\Labs\Labs\waste\numbers.txt', 'w') as file:
    for number in numbers:
        file.write(f"{number}\n")

