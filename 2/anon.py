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
        passport_dict = passport_data.split(',') 
        country = [item for item in passport_dict if 'country' in item] 
        return f"{{{', '.join(country)}}}"  

    data_frame['Passport_data'] = data_frame['Passport_data'].apply(mask_field)
    return data_frame

def anonymize_date_in_dataframe(data_frame, key):
    data_frame[key] = '2023'
    return data_frame

def anonymize_payment_info(df):
    df['bank_card_pay_system'] = '*****'
    df['bank_card_number'] = '*****'
    
    return df

def mask_snils(data_frame):
    def mask_snils(snils):
        return snils[0] + '*' * (len(snils) - 1)
    
    data_frame['snils'] = data_frame['snils'].apply(mask_snils)
    return data_frame

def anonymize_med_card(data_frame):
    data_frame['med_card'] = data_frame['med_card'].apply(lambda x: "*****")
    return data_frame

def remove_column(df, key):
    df[key] = '*****'
    return df

def anonymize_total_analysis_cost(df):
    # Функция для присвоения диапазона на основе стоимости
    def cost_range(cost):
        if int(cost) <= 2000:
            return 'Low'
        elif 2000 < int(cost) <= 4000:
            return 'Medium'
        else:
            return 'High'
    
    # Применяем анонимизацию
    df['total_analysis_cost'] = df['total_analysis_cost'].apply(cost_range)
    return df

def find_worst_k_anonymity(data_frame):
    grouped_counts = data_frame.groupby(list(data_frame.columns)).size()
    
    worst_k_values = grouped_counts.nsmallest(5)
    
    total_count = len(data_frame)
    
    res = []
    for idx, (group, count) in enumerate(worst_k_values.items(), 1):
        percent = (count / total_count) * 100
        print(f"{idx}. - k-anonymity: {count} ({percent:.2f}%)")
        res.append(count)
    
    return min(res) > 9 

def anonymize_name_fields(data_frame, male_names=Firstnames.male_names, female_names=Firstnames.female_names):
    def get_gender(firstname):
        if firstname in male_names:
            return "Мужчина"
        elif firstname in female_names:
            return "Женщина"

    data_frame['Firstname'] = data_frame['Firstname'].apply(get_gender)
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