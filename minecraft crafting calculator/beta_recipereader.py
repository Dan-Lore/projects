import os
import json

def read() -> dict:
    recipes = {}

    # Путь к папке с файлами recipes
    folder_path = 'recipes'

    # Получаем список файлов в папке recipes
    file_list = os.listdir(folder_path)

    # Обрабатываем каждый файл в папке
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        
        # Проверяем, что файл - JSON
        if file_name.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                recipes[file_name[:-5]] = data
    return recipes


if __name__ == "__main__":
    json_str = json.dumps(read(), indent=4, ensure_ascii=False)
    print(json_str)