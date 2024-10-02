import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

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
                    data.append({
                        "Прізвище": row[0],
                        "Ім'я": row[1],
                        "По батькові": row[2],
                        "Стать": row[3],
                        "Дата народження": row[4],
                        "Посада": row[5],
                        "Місто": row[6],
                        "Адреса": row[7],
                        "Телефон": row[8],
                        "Email": row[9],
                        "Вік": age
                    })
                except Exception as e:
                    print(f"Помилка обробки рядка: {row} - {e}")
        print("Ok")
        return data
    except Exception as e:
        print(f"Помилка при відкритті CSV файлу: {e}")
        return None

# Функція для підрахунку співробітників за статтю
def count_by_gender(data):
    male_count = sum(1 for person in data if person["Стать"] == "Чоловік")
    female_count = sum(1 for person in data if person["Стать"] == "Жінка")
    print(f"Чоловіків: {male_count}, Жінок: {female_count}")
    
    # Побудова діаграми
    plt.figure(figsize=(6, 6))
    plt.pie([male_count, female_count], labels=["Чоловіки", "Жінки"], autopct='%1.1f%%', colors=['skyblue', 'pink'])
    plt.title("Співвідношення чоловіків та жінок")
    plt.show()

# Функція для підрахунку співробітників за віковими категоріями
def count_by_age_category(data):
    age_groups = {
        "younger_18": 0,
        "18-45": 0,
        "45-70": 0,
        "older_70": 0
    }

    for person in data:
        age = person["Вік"]
        if age < 18:
            age_groups["younger_18"] += 1
        elif 18 <= age <= 45:
            age_groups["18-45"] += 1
        elif 45 < age <= 70:
            age_groups["45-70"] += 1
        else:
            age_groups["older_70"] += 1

    print(f"Молодше 18: {age_groups['younger_18']}")
    print(f"18-45: {age_groups['18-45']}")
    print(f"45-70: {age_groups['45-70']}")
    print(f"Старше 70: {age_groups['older_70']}")
    
    # Побудова діаграми
    plt.figure(figsize=(8, 6))
    plt.bar(age_groups.keys(), age_groups.values(), color=['green', 'blue', 'orange', 'red'])
    plt.title("Кількість співробітників за віковими категоріями")
    plt.ylabel("Кількість співробітників")
    plt.show()

# Функція для підрахунку співробітників за статтю і віковими категоріями
def count_by_gender_and_age_category(data):
    gender_age_groups = {
        "Чоловік": {"younger_18": 0, "18-45": 0, "45-70": 0, "older_70": 0},
        "Жінка": {"younger_18": 0, "18-45": 0, "45-70": 0, "older_70": 0}
    }

    for person in data:
        age = person["Вік"]
        gender = person["Стать"]
        if age < 18:
            gender_age_groups[gender]["younger_18"] += 1
        elif 18 <= age <= 45:
            gender_age_groups[gender]["18-45"] += 1
        elif 45 < age <= 70:
            gender_age_groups[gender]["45-70"] += 1
        else:
            gender_age_groups[gender]["older_70"] += 1

    for gender in gender_age_groups:
        print(f"{gender} молодше 18: {gender_age_groups[gender]['younger_18']}")
        print(f"{gender} 18-45: {gender_age_groups[gender]['18-45']}")
        print(f"{gender} 45-70: {gender_age_groups[gender]['45-70']}")
        print(f"{gender} старше 70: {gender_age_groups[gender]['older_70']}")
        
        # Побудова діаграми
        plt.figure(figsize=(8, 6))
        plt.bar(gender_age_groups[gender].keys(), gender_age_groups[gender].values(), color=['green', 'blue', 'orange', 'red'])
        plt.title(f"Кількість співробітників статі {gender.lower()} за віковими категоріями")
        plt.ylabel("Кількість співробітників")
        plt.show()

# Основна функція
def main():
    csv_file = 'people_data.csv'

    # Читаємо CSV файл
    data = read_csv(csv_file)
    if data is None:
        return

    # Підрахунок співробітників за статтю
    count_by_gender(data)

    # Підрахунок співробітників за віковими категоріями
    count_by_age_category(data)

    # Підрахунок співробітників за статтю і віковими категоріями
    count_by_gender_and_age_category(data)

if __name__ == "__main__":
    main()
