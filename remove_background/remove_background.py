import glob
import os
import re
import rembg
from PIL import Image


folder_path = 'images'
extensions = ['png', 'jpg', 'jpeg', 'webp']

pattern = '|'.join(['.*\.' + ext + '$' for ext in extensions])
files = glob.glob(os.path.join(folder_path, '*'))
images = [file for file in files if re.match(pattern, file)]

for image in images:
    if 'out.' in image:
        continue

    dot_index = image.rfind('.')
    out_image_path = image[:dot_index] + ' out' + image[dot_index:]
    if not os.path.exists(out_image_path):
        cur_image = Image.open(image)
        out_image = rembg.remove(cur_image)
        out_image.save(out_image_path, 'PNG')