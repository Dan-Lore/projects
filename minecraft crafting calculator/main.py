import json

import beta_recipereader


recipes = beta_recipereader.read()

def update_dict(input_dict, second_dict) -> None:
    for key, value in second_dict.items():
        if key in input_dict:
            input_dict[key] += value
        else:
            input_dict[key] = value


def count_resources(recipe, rec_count) -> dict:
    global recipes
    if recipe not in recipes:
        return {recipe: rec_count}

    total_resources = {}
    for resource, res_count in recipes[recipe]['ресурсы'].items():
        temp = count_resources(resource, rec_count * res_count / recipes[recipe]['сколько скрафтится'])
        update_dict(total_resources, temp)

    return total_resources

to_craft = {"Механическая пила": 5, 
            "Автономный активатор": 3,
            "Линейный каркас": 12, 
            "Портативный складской интерфейс": 2,
            "Жёлоб": 1
            }

required_resources = {}
for item, count in to_craft.items():
    update_dict(required_resources, count_resources(item, count))

json_str = json.dumps(required_resources, indent=4, ensure_ascii=False)
print(json_str)