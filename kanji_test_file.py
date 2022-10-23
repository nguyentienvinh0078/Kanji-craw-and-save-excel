# word_mean = 'Nghĩa:   Giải nghĩa: Giản thể của chữ 學 '
# word_mean = "Nghĩa:  Sống, đối lại với tử [死]. Còn sống. Những vật có sống. Sinh sản, nẩy nở. Nuôi, những đồ để nuôi sống đều gọi là sanh. Sống, chưa chín gọi là sanh. Chưa quen, chưa rành. Học trò. Dùng như chữ mạt [末]. Dùng làm tiếng đệm. Tiếng dùng trong tấn tuồng. Ta quen đọc là chữ sinh.  Giải nghĩa: Sống, đối lại với tử [死]. "
# short_mearn_list = word_mean.split('Giải nghĩa:')[0].split('Nghĩa:')[1].strip().split('.')
# short_mearn_list = [line.strip() for line in short_mearn_list]
# # short_mearn_list = word_mean.split('Giải nghĩa:')[1].strip().split('.')
# # short_mearn_list = [line.strip() for line in short_mearn_list]
# if '' in short_mearn_list: short_mearn_list.remove('')

# short_mearn = '&&'.join(short_mearn_list)
# print(short_mearn)

# import re
# strokes = 'Số nét: 20 '

# strokes_number = int(re.findall(r'\d+', strokes)[0])

# print(strokes_number)


# sound_text = """訓:ひ    -び    -か"""
# sound_text = sound_text.replace('訓:', '')
# sound_text_list = [string.replace('\xa0', '&&') for string in sound_text]
# sound_text_list = ''.join(sound_text_list).split('&&')
# while '' in sound_text_list:
#     sound_text_list.remove('')

# print(sound_text_list)

# from kanji_db import *

# print(''.join(kanji_n5_data['1']))

import json, os
from multiprocessing.sharedctypes import Value

def json_read(json_file):
    resultData = {}
    with open(json_file, mode='r', encoding='utf-8') as json_file:
        resultData = json.load(json_file)
    return resultData


ROOT_DIR = os.path.dirname(__file__)
OUT_SOURCE_FOLDER = 'Kanji Mina Excel Result'
OUT_SOURCE_FOLDER_PATH = os.path.join(ROOT_DIR, OUT_SOURCE_FOLDER)

DATABASE_FOLDER = 'Kanji Database'
DATABASE_FOLDER_PATH = os.path.join(ROOT_DIR, DATABASE_FOLDER)

STROKES_KANJI_FOLDER = 'Kanji Strokes Images'
STROKES_KANJI_FOLDER_PATH = os.path.join(ROOT_DIR, DATABASE_FOLDER, STROKES_KANJI_FOLDER)

course_kanji_data_jellyfish = json_read('Course_kanji_craw_data.json')
onkun_data = json_read('onkun.json')

input_data = course_kanji_data_jellyfish
course = 'Course'

output = course_kanji_data_jellyfish

for lesson, wordlist in course_kanji_data_jellyfish['Course'].items():
    for i in range(0, len(wordlist)):
        output['Course'][lesson][i].update(onkun_data['Course'][lesson][i])

 
# print(kanji_words_data['Course']['1'])

kanji_words_data_file_name = 'Course_kanji_craw_update_full.json'
kanji_words_data_path = os.path.join(DATABASE_FOLDER_PATH, STROKES_KANJI_FOLDER, kanji_words_data_file_name)

with open(kanji_words_data_path, mode='w', encoding='utf-8') as json_file:
    json.dump(output, json_file, indent=4, separators=(',', ': '), ensure_ascii=False)

# isSave = True
# json_file_name = f'kanji_course_data.json'

# n4_kanji_data = json_read('N4_kanji_data.json')['N4']
# n5_kanji_data = json_read('N5_kanji_data.json')['N5']

# kanji_data = {
#     "Course": {
#         **n5_kanji_data, 
#         **n4_kanji_data
#     }
# }

# if isSave:
#     with open(json_file_name, mode='w', encoding='utf-8') as json_file:
#         json.dump(kanji_data, json_file, indent=4, separators=(',', ': '), ensure_ascii=False)