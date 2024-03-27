import pandas as pd
from pathlib import Path

def process_data(data, existing_data, excel_path):
    if data:
        new_df = pd.DataFrame(data)
        updated_df = pd.concat([existing_data, new_df], ignore_index=True)
        updated_df.to_excel(excel_path, index=False)
        print("Файл оновлено новинами")
    else:
        print("Новин не знайдено")

def read_file(excel_path):    
    if Path(excel_path).exists():
        existing_data = pd.read_excel(excel_path)
    else:
        existing_data = pd.DataFrame(columns=["site", "date", "title", "link"])
    existing_titles = set(existing_data['title'])
    return existing_data, existing_titles

def load_dict_from_file(file_path):
    # Инициализация пустого словаря
    months = {}

    # Попытка открыть файл и чтение строк
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Убедитесь, что строка содержит данные перед обработкой
                line = line.strip()
                if line:
                    # Разделение строки на ключ и значение и удаление лишних символов
                    parts = line.strip("',").split("': '")
                    if len(parts) == 2:
                        key, value = parts
                        months[key] = value
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла {file_path}: {e}")

    return months