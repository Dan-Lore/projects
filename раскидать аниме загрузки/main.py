from os import listdir, makedirs, rename
from os.path import isfile, join, exists
from shutil import copyfile, move


cur_path = 'C:/Users/smoln/Downloads/'
meanword = '[Anime365]'
extinsion = '.mp4'

list = listdir(cur_path)
titles = []
for name in list:
    if meanword in name:
        a = name.find(meanword) + len(meanword) + 1
        b = name.find(' - ')
        c = name.find('(')
        title = name[a:b]
        new_path = cur_path + title + '/'
        if not exists(new_path):
            makedirs(new_path)
        move(cur_path + name, new_path + name[a:c] + extinsion)