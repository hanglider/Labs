from anon import *

print("Чтение данных...")
data = xml_to_dataframe('C:/IT/Labs/Labs/waste/data_set.xml')

if input('Обезличить пасспортные данные [y/n]') == "y":
    mask_passport_data(data)
if input('Обезличить данные снилса [y/n]') == "y":
    mask_snils(data)
if input('Обезличить ФИО [y/n]') == "y":
    anonymize_name_fields(data)
if input('Обезличить платежные данные [y/n]') == "y":
    anonymize_payment_info(data)    
if input('Обезличить дату визита [y/n]') == "y":
    anonymize_date_in_dataframe(data, 'date')
if input('Обезличить дату получения анализов [y/n]') == "y":
    anonymize_date_in_dataframe(data, 'date_offset')
if input('Удалить данные анализов [y/n]') == "y":
    remove_column(data, 'analyzes')
if input('Удалить данные симптомов [y/n]') == "y":
    remove_column(data, 'symptoms')
if input('Удалить данные врача [y/n]') == "y":
    remove_column(data, 'doctor')
if input('Расщепить стоимость анализов [y/n]') == "y":
    anonymize_total_analysis_cost(data)

print(find_worst_k_anonymity(data))

print("Сохранение датасета...")

save_to_xml(data, 'C:/IT/Labs/Labs/waste/data_set_new.xml')

# k = 10
# quasi_identifiers = ['Passport_data']
# is_k_anonymous = calculate_k_anonymity(data, quasi_identifiers, k)
# print(f"DataFrame удовлетворяет k-анонимности (k={k}): {is_k_anonymous}")


