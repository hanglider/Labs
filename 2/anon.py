import pandas as pd
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import Firstnames

def calculate_k_anonymity(data_frame, quasi_identifiers, k):

    group_counts = data_frame.groupby(quasi_identifiers).size()
    
    return all(group_counts >= k)

def xml_to_dataframe(filepath):
    """
    Читает XML файл и преобразует его в DataFrame.
    :param filepath: путь к XML файлу
    :return: DataFrame
    """
    tree = ET.parse(filepath)
    root = tree.getroot()

    all_records = []
    for record in root.findall("record"):
        record_data = {}
        for field in record:
            record_data[field.tag] = field.text
        all_records.append(record_data)

    df = pd.DataFrame(all_records)
    return df

def mask_passport_data(data_frame):
    def mask_field(passport_data):
        # Заменяем содержимое на только страну
        passport_dict = passport_data.split(',')  # Разделяем по запятой
        country = [item for item in passport_dict if 'country' in item]  # Извлекаем страну
        return f"{{{', '.join(country)}}}"  # Формируем строку только с страной

    # Применяем функцию к столбцу Passport_data
    data_frame['Passport_data'] = data_frame['Passport_data'].apply(mask_field)
    return data_frame

def mask_snils(data_frame):
    # Функция для маскирования СНИЛСа
    def mask_snils(snils):
        # Заменяем все символы, кроме первой цифры, на '*'
        return snils[0] + '*' * (len(snils) - 1)
    
    # Применяем функцию к столбцу с СНИЛСом
    data_frame['snils'] = data_frame['snils'].apply(mask_snils)
    return data_frame

def anonymize_med_card(data_frame):
    # Заменяем всё содержимое в 'med_card' на '*****'
    data_frame['med_card'] = data_frame['med_card'].apply(lambda x: "*****")
    return data_frame

def find_worst_k_anonymity(data_frame):
    # Группируем строки после обезличивания и считаем их частоту
    grouped_counts = data_frame.groupby(list(data_frame.columns)).size()
    
    # Сортируем по возрастанию значений k-анонимности (меньшие значения k менее анонимны)
    worst_k_values = grouped_counts.nsmallest(5)
    
    # Выводим результаты
    for idx, (group, count) in enumerate(worst_k_values.items(), 1):
        print(f"{idx}. Group: {group} - k-anonymity: {count}")
    
    return worst_k_values

def anonymize_name_fields(data_frame, male_names=Firstnames.male_names, female_names=Firstnames.female_names):
    def get_gender(firstname):
        if firstname in male_names:
            return "Мужчина"
        elif firstname in female_names:
            return "Женщина"
        else:
            return "Неизвестно"  # Если имя не найдено в обоих списках

    # Заменяем поле Firstname на пол
    data_frame['Firstname'] = data_frame['Firstname'].apply(get_gender)
    # Заменяем поля Lastname и Patronymic на *****
    data_frame['Lastname'] = '*****'
    data_frame['Patronymic'] = '*****'

def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    for key, val in d.items():
        child = ET.Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

def save_to_xml(data_frame, filepath):
    root = ET.Element("dataset")  

    for _, row in data_frame.iterrows():
        record_elem = dict_to_xml("record", row.to_dict())
        root.append(record_elem)

    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
