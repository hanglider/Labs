import pandas as pd
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

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
