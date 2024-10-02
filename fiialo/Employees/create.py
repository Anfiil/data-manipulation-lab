import csv
import datetime
from faker import Faker
import random

# Ініціалізація Faker для української мови
fake = Faker('uk_UA')

# Відсоткове співвідношення
total_records = 2000
female_percentage = 0.4
male_percentage = 0.6

female_records = int(total_records * female_percentage)
male_records = int(total_records * male_percentage)

# Функція для генерації запису
def generate_person(gender='male'):
    if gender == 'male':
        last_name = fake.last_name_male()
        first_name = fake.first_name_male()
        middle_name = fake.middle_name_male()
        gender_value = 'Чоловік'
    else:
        last_name = fake.last_name_female()
        first_name = fake.first_name_female()
        middle_name = fake.middle_name_female()
        gender_value = 'Жінка'
    
    year = datetime.date.today().year

    birth_date = fake.date_of_birth(minimum_age=(year-2008), maximum_age=(year-1938))
    job = fake.job()
    city = fake.city()
    address = fake.address()
    phone = fake.phone_number()
    email = fake.email()
    
    return [last_name, first_name, middle_name, gender_value, birth_date, job, city, address, phone, email]

# Генерація даних
data = []
# Додаємо чоловічі записи
for _ in range(male_records):
    data.append(generate_person('male'))

# Додаємо жіночі записи
for _ in range(female_records):
    data.append(generate_person('female'))

# Запис даних у CSV файл
with open('people_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Прізвище', 'Ім’я', 'По батькові', 'Стать', 'Дата народження', 'Посада', 'Місто проживання', 'Адреса проживання', 'Телефон', 'Email'])
    
    # Записуємо всі згенеровані дані
    writer.writerows(data)

print(f"Файл 'people_data.csv' успішно створено з {total_records} записами!")
