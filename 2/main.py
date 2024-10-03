from anon import *

data = xml_to_dataframe('C:/IT/Labs/Labs/waste/data_set.xml')
mask_passport_data(data)
# save_to_xml(data, 'C:/IT/Labs/Labs/waste/data_set_new.xml')
print(data)

k = 10
quasi_identifiers = ['Passport_data']
is_k_anonymous = calculate_k_anonymity(data, quasi_identifiers, k)
print(f"DataFrame удовлетворяет k-анонимности (k={k}): {is_k_anonymous}")


