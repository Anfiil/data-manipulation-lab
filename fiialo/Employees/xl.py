import csv
import os
from openpyxl import Workbook
from datetime import datetime

# Функція для підрахунку віку
def calculate_age(birth_date):
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Функція для читання CSV файлу
def read_csv(file_path):
    if not os.path.exists(file_path):
        print("Помилка: файл CSV не знайдено.")
        return None

    data = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)  # Пропускаємо заголовок
            for row in reader:
                try:
                    birth_date = datetime.strptime(row[4], '%Y-%m-%d')
                    age = calculate_age(birth_date)
                    full_record = row + [age]  # Додаємо вік до запису
                    data.append(full_record)
                except Exception as e:
                    print(f"Помилка обробки рядка: {row} - {e}")
        return data
    except Exception as e:
        print(f"Помилка при відкритті CSV файлу: {e}")
        return None

# Функція для створення XLSX файлу
def create_xlsx(data, output_file):
    try:
        workbook = Workbook()
        
        # Створюємо аркуш "all" і додаємо всі дані з CSV
        all_sheet = workbook.active
        all_sheet.title = "all"
        all_sheet.append(['Прізвище', 'Ім’я', 'По батькові', 'Стать', 'Дата народження', 'Посада', 'Місто проживання', 'Адреса проживання', 'Телефон', 'Email', 'Вік'])
        for row in data:
            all_sheet.append(row[:-1])  # Додаємо всі поля без додаткового віку

        # Створення інших аркушів і фільтрація за віком
        age_groups = {
            "younger_18": lambda age: age < 18,
            "18-45": lambda age: 18 <= age <= 45,
            "45-70": lambda age: 45 < age <= 70,
            "older_70": lambda age: age > 70
        }

        for sheet_name, condition in age_groups.items():
            sheet = workbook.create_sheet(sheet_name)
            sheet.append(['№', 'Прізвище', 'Ім’я', 'По батькові', 'Дата народження', 'Вік'])
            filtered_data = [row for row in data if condition(row[-1])]
            for i, row in enumerate(filtered_data, start=1):
                sheet.append([i, row[0], row[1], row[2], row[4], row[-1]])  # Прізвище, Ім’я, По батькові, Дата народження, Вік

        # Збереження файлу
        workbook.save(output_file)
        print("Ok")

    except Exception as e:
        print(f"Помилка при створенні XLSX файлу: {e}")

# Основна функція
def main():
    csv_file = 'people_data.csv'
    xlsx_file = 'people_data.xlsx'

    # Читаємо CSV файл
    data = read_csv(csv_file)
    if data is None:
        return
    
    # Створюємо XLSX файл
    create_xlsx(data, xlsx_file)

if __name__ == "__main__":
    main()
