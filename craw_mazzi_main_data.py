from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from selenium.webdriver.support import expected_conditions as EC

from Driver import Driver
from html2image import Html2Image
from util import json_write, json_read
import os, re
import shutil

def get_word_data(driver, word):
    for __ in range(3):
        try:
            sleep(1)
            kanji_tab_ele = driver.find_element(By.XPATH, '/html/body/app-root/div/div[1]/div/app-header-search/div[1]/div[1]/div[2]/div/button[2]')
            kanji_tab_ele.click()
            sleep(0.25)

            input_ele = driver.find_element(By.XPATH, '/html/body/app-root/div/div[1]/div/app-header-search/div[1]/div[1]/div[1]/div[2]/input')
            input_ele.send_keys(word)
            sleep(0.25)

            search_btn_ele = driver.find_element(By.XPATH, '/html/body/app-root/div/div[1]/div/app-header-search/div[1]/div[1]/div[1]/div[2]/div/button')
            search_btn_ele.click()
            sleep(0.5)

            print(f'>> Word: [ {word} ]')

            try:
                stroke_ele = driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-search-kanji/div[1]/div/div/div/div[2]/div[1]/app-kanji/div/div[1]/div[2]/div[1]/div[3]')
                stroke = int(re.findall(r'\d+', stroke_ele.text)[0])
                print(f'>> Stroke: [ {stroke} ]')
            except:
                stroke = 10
                
            sleep(0.25)

            draw_again_btn_ele = driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-search-kanji/div[1]/div/div/div/div[2]/div[1]/app-kanji/div/div[1]/div[2]/div[2]/div/app-kanji-draw/div/div[2]/button')
            draw_again_btn_ele.click()
            sleep(0.5)

            wait_draw_time = 4
            if stroke > 4: wait_draw_time = int(stroke * 1.25)
            if stroke > 10: wait_draw_time = int(stroke * 1)
            for i in range(wait_draw_time):
                # key = ['|', '/', '\\', '/', '\\']
                key_animate = [
                     "[==         ]", "[ ==        ]", "[  ==       ]", "[   ==      ]", "[    ==     ]", "[     ==    ]", "[      ==   ]", "[       ==  ]",
                     "[        == ]", "[         ==]", "[         ==]", "[        == ]", "[       ==  ]", "[      ==   ]", "[     ==    ]", "[    ==     ]",
                     "[   ==      ]", "[  ==       ]", "[ ==        ]", "[==         ]"
                ]
                for j in range(len(key_animate)):
                    print('\r' + f">> Wait draw time: {key_animate[j]} [{wait_draw_time-i:>3}s ]", end='', flush=True)
                    sleep(0.05)
            print('\r' + f">> Wait draw time: {key_animate[len(key_animate)-1]} [ {'OKE':>3} ]", end='', flush=True)
            print('')

            vn_sound_ele = driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-search-kanji/div[1]/div/div/div/div[2]/div[1]/app-kanji/div/div[1]/div[2]/div[1]/h2/span[2]/span')
            vn_sound = vn_sound_ele.text[1:].strip()

            print(f">> VN sound: [ {vn_sound} ]")
            sleep(0.25)

            try:
                onyomi_ele = driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-search-kanji/div[1]/div/div/div/div[2]/div[1]/app-kanji/div/div[1]/div[2]/div[1]/div[1]/span[2]')
                onyomi = onyomi_ele.text.replace('    ', '')
                onyomi = [text.strip() for text in onyomi.split('-')]
                onyomi = '###'.join(onyomi)
            except:
                onyomi = ''
            print(f">> Onyomi: [ {onyomi} ]")
            sleep(0.25)

            try:
                kunyomi_ele = driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-search-kanji/div[1]/div/div/div/div[2]/div[1]/app-kanji/div/div[1]/div[2]/div[1]/div[2]/span[2]')
                kunyomi = kunyomi_ele.text
                kunyomi = [text.strip() for text in kunyomi.split('    ')]
                kunyomi = '###'.join(kunyomi)
            except:
                kunyomi = ''
            print(f">> Kunyomi: [ {kunyomi} ]")
            sleep(0.25)

            word_mean_ele = driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-search-kanji/div[1]/div/div/div/div[2]/div[1]/app-kanji/div/div[1]/div[2]/div[1]/div[5]')
            word_mean = word_mean_ele.text

            print(f">> Word mean: [{word_mean}\n]")
            sleep(0.25)

            word_image_holder_ele = driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-search-kanji/div[1]/div/div/div/div[2]/div[1]/app-kanji/div/div[1]/div[2]/div[2]/div/app-kanji-draw/div/div[1]')
            word_image_svg_code = word_image_holder_ele.get_attribute('innerHTML')

            print(f">> Image svg code: [ {word_image_svg_code[:50]} .... {word_image_svg_code[-50:]}]")
            sleep(0.25)

            result_data = {
                'status': 'success',
                'word': word,
                'stroke': stroke,
                'vn_sound': vn_sound,
                'onyomi': onyomi,
                'kunyomi': kunyomi,
                'word_mean': word_mean,
                'word_image_svg_code':  word_image_svg_code.replace('rgba(0, 0, 0, 0)', 'rgba(47, 187, 80, 1)')
            }
            sleep(0.25)

            close_btn_ele = driver.find_element(By.XPATH, '/html/body/app-root/div/div/div/app-header-search/div[1]/div[1]/div[1]/div[2]/button[1]')
            close_btn_ele.click()
            sleep(0.25)

            break
        except Exception as bug:
            result_data =  {
                'status': 'failed', 
                'reason': bug, 
                'function': 'get_word_data(word)', 
                'value': word
            }

            close_btn_ele = driver.find_element(By.XPATH, '/html/body/app-root/div/div/div/app-header-search/div[1]/div[1]/div[1]/div[2]/button[1]')
            close_btn_ele.click()
            sleep(0.25)
            continue

    return result_data

def save_svg_image(code, img_name, path, size=(250, 250)):
    try: 
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as bug:
        # print('Create folder EROOR', bug)
        return
    
    list_dir_file = os.listdir(path)

    if img_name in list_dir_file:
        os.remove(f"{path}\\{img_name}")
    
    html_to_image = Html2Image()
    html_to_image.screenshot(html_str=code, save_as=img_name, size=size)
    sleep(0.25)
    shutil.move(img_name, path)
    sleep(0.25)

kanji_mazzi_domain = 'https://vi.mazii.net/vi-VN/search/kanji/'

database_folder = 'Kanji Database'
kanji_stroke_folder = 'Stroke Image'
craw_data_file_name = 'words_craw_update.json'
result_data_file_name = 'Course_mazzi.json'

kanji_words = json_read(os.path.join(database_folder, craw_data_file_name))

the_driver = Driver()
driver = the_driver.init_driver(opt='mazzi')
driver.get(kanji_mazzi_domain)

course = 'Course'
course_data = {}
for lesson, word_list in kanji_words[course].items():
    lesson_data = []
    for word in word_list:
        word_index = word_list.index(word) + 1
        print('\n' + '-' * 120)
        print(f'>> Lesson: [ {lesson} ] - Index: [ {word_index} ] - Word: [ {word} ]')
        word_data = get_word_data(driver, word)
        if word_data['status'] == 'success':
            stroke_img_file_name = f"{lesson}_{word_index}_{word}.png"
            stroke_img_save_folder = f"{database_folder}\\{kanji_stroke_folder}\\{lesson}"
            save_svg_image(
                code=word_data['word_image_svg_code'],
                img_name=stroke_img_file_name,
                path=stroke_img_save_folder
            )
            print(f'>> Save Stroke Image: [ Success ]')

            lesson_data.append({
                'word_index': word_index,
                **word_data
            })  
        else:
            lesson_data.append({
                'word_index': word_index,
                'lesson': lesson,
                'word': word,
                'status': 'failed'
            })  

        course_data.update({
            f"{lesson}": lesson_data,
        })

        json_write(f'{database_folder}\\{result_data_file_name}', {f"{course}": course_data})

driver.quit()