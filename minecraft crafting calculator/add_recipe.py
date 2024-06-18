import json


recipe_name = 'Портативный складской интерфейс'
data = {
    "место для крафта": "верстак",
    "ресурсы": {
        "Андезитовый корпус": 1,
        "Жёлоб": 1
    },
    "сколько скрафтится": 1
}

file_name = 'recipes/' + recipe_name + '.json'

# Запись данных в JSON файл
with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print(f'JSON файл "{file_name}" успешно создан!')