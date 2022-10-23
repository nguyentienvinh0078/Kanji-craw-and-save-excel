from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from selenium.webdriver.support import expected_conditions as EC

from Driver import Driver
from util import json_write, json_read
import os, re

def get_word_data(driver, word):
    for __ in range(3):
        try:
            input_ele = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/header/div[1]/div[4]/div/div/div[2]/div/input')
            input_ele.send_keys(word)
            sleep(0.1)

            search_btn_ele = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/header/div[1]/div[4]/div/div/div[2]/div/i[2]')
            search_btn_ele.click()
            sleep(0.25)

            print(f'>> Word: [ {word} ]')

            kanji_main_info_ele = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div')
            pronoun_data = []
            if len(kanji_main_info_ele) > 0:
                for i in range(1, len(kanji_main_info_ele) + 1):
                    [pronoun_label_ele] = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[{i}]/span')
                    pronoun_label_text = pronoun_label_ele.text

                    try:
                        [pronoun_item_ele] = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[{i}]/p')
                        pronoun_text = pronoun_item_ele.text.replace('】', ']').replace('【', ' [')
                    except:
                        pronoun_item_ele = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[{i}]/div/span')
                        pronoun_text = []
                        if len(pronoun_item_ele) > 0:
                            for j in range(1, len(pronoun_item_ele) + 1):
                                component_ele = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[{i}]/div/span[{j}]')
                                pronoun_text.append(component_ele.text)
                            pronoun_text = '###'.join(pronoun_text)

                    pronoun = f"{pronoun_label_text}###{pronoun_text}"
                    pronoun_data.append(pronoun)
            print(f'>> Pronoun: [ {pronoun_data} ]')
            sleep(0.1)

            comment_eles = driver.find_elements(By.XPATH, '/html/body/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[3]/div/div/div[2]/div')
            comment_data = []
            if len(comment_eles) > 0:
                for i in range(1, len(comment_eles) + 1):
                    [comment_ele] = driver.find_elements(By.XPATH, f'/html/body/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[3]/div/div/div[2]/div[{i}]/div[2]/div[1]/div[2]')
                    comment = comment_ele.text[0].upper() + comment_ele.text[1:]
                    comment_data.append(comment)
            print(f'>> Comments: [ {comment_data} ]')
            sleep(0.1)

            kanji_similar_eles = driver.find_elements(By.XPATH, '/html/body/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[4]/div/div/div')
            kanji_similar_data = []
            if len(kanji_similar_eles) > 0:
                for i in range(1, len(kanji_similar_eles) + 1):
                    [kanji_similar_ele] = driver.find_elements(By.XPATH, f'/html/body/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[4]/div/div/div[{i}]/div/h1')
                    kanji_similar_text = kanji_similar_ele.text

                    [kanji_similar_percent_ele] = driver.find_elements(By.XPATH, f'/html/body/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[4]/div/div/div[{i}]/div/span')
                    kanji_similar_percent_text = kanji_similar_percent_ele.text

                    kanji_similar = f"{kanji_similar_text}###{kanji_similar_percent_text}"
                    kanji_similar_data.append(kanji_similar)
            print(f'>> Similar kanji: [ {kanji_similar_data} ]')
            sleep(0.1)

            kanji_related_tab = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div/div[1]/a[2]')
            kanji_related_tab.click()
            sleep(0.5)

            related_word_data = []
            related_word_eles = driver.find_elements(By.XPATH, f'/html/body/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div/div[2]/div/ul/li')
            if len(related_word_eles) > 0:
                for i in range(1, len(related_word_eles) + 1):
                    related_word_char_ele = driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div/div[2]/div/ul/li[{i}]/p[1]')
                    related_word_char_text = related_word_char_ele.text.replace('】', ']').replace('【', ' [').strip()
                
                    related_word_mean_ele = driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div/div[2]/div/ul/li[{i}]/p[2]')
                    related_word_mean_text = related_word_mean_ele.text.replace(': ', '').strip().title()

                    related_word = f"{related_word_char_text}###{related_word_mean_text}"
                    related_word_data.append(related_word)
            print(f'>> Related word: [ {related_word_data} ]')
            sleep(0.1)

            result_data =  {
                'status': 'success', 
                'pronoun_data': pronoun_data,
                'comment_data': comment_data,
                'kanji_similar_data': kanji_similar_data,
                'related_word_data': related_word_data
            }
            sleep(0.1)

            close_btn_ele = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/header/div[1]/div[4]/div/div/div[2]/div/i[1]')
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

            close_btn_ele = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/header/div[1]/div[4]/div/div/div[2]/div/i[1]')
            close_btn_ele.click()
            sleep(0.25)
            continue

    return result_data


kanji_jdict_domain = 'https://jdict.net/search?keyword=&type=kanji'

database_folder = 'Kanji Database'
kanji_stroke_folder = 'Stroke Image'
craw_data_file_name = 'words_craw_update.json'
result_data_file_name = 'Course_jdict.json'

kanji_words = json_read(os.path.join(database_folder, craw_data_file_name))

the_driver = Driver()
driver = the_driver.init_driver()
driver.get(kanji_jdict_domain)

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
            lesson_data.append({
                'word_index': word_index,
                **word_data
            })  
        else:
            lesson_data.append({
                'word_index': word_index,
                'lesson': lesson,
                'status': 'failed'
            })  

        course_data.update({
            f"{lesson}": lesson_data,
        })

    json_write(f'{database_folder}\\{result_data_file_name}', {f"{course}": course_data})

driver.quit()