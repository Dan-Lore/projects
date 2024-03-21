import requests
import os.path
from PIL import Image, UnidentifiedImageError

DEBUG = True

base_image_url = 'http://cdn.anime-recommend.ru/previews/'
base_image_path = './images/'

def download_by_id(ids):
    tmp = []
    for id in ids:
        path = base_image_path + str(id) + '.jpg'
        url = base_image_url + str(id) + '.jpg'
        if os.path.exists(path):
            continue
        try:
            img = Image.open(requests.get(url, stream=True).raw)
            img.save(path)
        except UnidentifiedImageError:
            tmp.append(id)
    if len(tmp) > 0:
        print('Не удалось загрузить изображения аниме с такими id:')
        print('\n'.join(map(str, tmp)))
    return


if __name__ == "__main__":
    if DEBUG:
        pass