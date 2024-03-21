import json
import requests
import os.path
from PIL import Image, UnidentifiedImageError
from colr import Colr
from math import ceil, log2

import images_dowloader

json_file = 'Dan_Lore_animes.json'
base_anime_url = 'https://shikimori.me/animes/'
base_image_url = 'http://cdn.anime-recommend.ru/previews/'
base_image_path = './images/'

arr = []
data = []
with open(json_file, 'r', encoding='utf-8') as json_data:
    data = json.load(json_data)
    for ind, x in enumerate(data):
        additional_stats =  {'counter': 0, 'coef': 0, 'opponents': []}
        x |= additional_stats
        if x['status'] == 'completed':
            arr.append(ind)
print(len(arr))

images_dowloader.download_by_id([data[i]['target_id'] for i in arr])

def play(mem1_id, mem2_id):
    data[mem1_id]['opponents'].append(mem2_id)
    data[mem2_id]['opponents'].append(mem1_id)
    print(data[mem1_id]['target_title'], '  или  ', data[mem2_id]['target_title'])
    print(base_anime_url + str(data[mem1_id]['target_id']), base_anime_url + str(data[mem2_id]['target_id']), sep='\n')
    response = int(input('Выберите участника 1 или 2: '))
    if response == 1:
        data[mem1_id]['counter'] += 1
        return (mem1_id, mem2_id)
    else:
        data[mem2_id]['counter'] += 1
        return (mem2_id, mem1_id)
    
def grouped(iterable, n):
    return zip(*[iter(iterable)]*n)

key_score = lambda x: data[x]['score']
key_counter = lambda x: data[x]['counter']

win = sorted(arr[:8], key= key_score, reverse=True)
lose = []
max_num_rounds = ceil(log2(len(win)))

for round in range(max_num_rounds):
    tmp_win = []
    tmp_lose = []
    for i in range(0, len(win) - 1, 2):
        (winner, loser) = play(win[i], win[i - 1])
        tmp_win.append(winner)
        tmp_lose.append(loser)
    for i in range(0, len(lose) - 1, 2):
        (winner, loser) = play(lose[i], lose[i - 1])
        tmp_win.append(winner)
        tmp_lose.append(loser)
    if len(win) % 2 == 1:
        data[win[-1]]['counter'] += 1
        tmp_win.append(win[-1])
    if len(lose) % 2 == 1:
        data[lose[-1]]['counter'] += 1
        tmp_win.append(lose[-1])
    win = sorted(tmp_win, key=key_counter, reverse=True)
    lose = sorted(tmp_lose, key=key_counter, reverse=True)

arr = win + lose
for i in arr:
    for j in data[i]['opponents']:
        data[i]['coef'] += data[j]['counter']
arr.sort(key=lambda x: (data[x]['counter'], data[x]['coef']), reverse=True)

print('\nRating:')
for i in arr:
    print(data[i]['target_title'])
    image = Image.open(base_image_path + str(data[i]['target_id']) + '.jpg')
    image.show()