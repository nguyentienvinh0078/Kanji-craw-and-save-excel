import os, json, sys
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from kanji_db import *
from html2image import Html2Image
import re
import shutil

class KanjiCrawler:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            try:
                application_path = os.path.dirname(os.path.realpath(__file__))
            except NameError:
                application_path = os.getcwd()

        self.root_dir = application_path
        self.folder = 'Kanji Database'
        self.kanji_words_data_file = 'kanji_words_data.json'

        self.save_folder = 'Kanji Strokes Images' 

        self.kanji_search_domain = 'https://vi.mazii.net/search/kanji?dict=javi&query='
        self.kanji_data = {}
        self.kanji_words = self.json_read(os.path.join(self.root_dir, self.folder, self.kanji_words_data_file))

        self.get_data()
        
    def json_read(self, json_file):
        resultData = {}
        with open(json_file, mode='r', encoding='utf-8') as json_file:
            resultData = json.load(json_file)
        return resultData

    def json_write(self, json_file_path, json_data):
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, separators=(',', ': '), ensure_ascii=False)

    def init_driver(self, opt='hide'):
        options = webdriver.ChromeOptions()
        options.add_argument('--log-level=3')
        options.add_argument('--start-maximized')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        if opt == 'hide' or '':
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-blink-features=AutomationControlled')
        if opt == 'diswin':
            options.add_argument("--window-position=-10000,0")
        elif opt == 'headless':
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        
        # options.add_experimental_option ("prefs", {
        #     "profile.managed_default_content_settings.images": 2,
        #     "profile.default_content_settings.popups": 0,
        #     "download.default_directory": f"{self.root_dir}",
        #     "directory_upgrade": True,
        #     "safebrowsing_for_trusted_sources_enabled": False,
        #     "safebrowsing.enabled": False,
        # })

        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=options) 
        return driver

    def get_data(self, isSave=True):
        
        print('>> Trình duyệt đang được khởi động....', end='')
        self.driver = self.init_driver()
        # self.driver.set_window_size(960, 1080)
        self.driver.get(self.kanji_search_domain)
        sleep(2)
        print('\r' + '>> Trình duyệt đã bật.................')
        
        json_file_name = f'kanji_craw_data.json'
        json_save_path = os.path.join(self.root_dir, self.folder, self.save_folder, json_file_name)
        
        course_data = {}
        course = 'Course'

        input_data = self.kanji_words[course]
        for lesson, word_list in input_data.items():
            lesson_data = []

            self.driver.get(self.kanji_search_domain)
            sleep(2)
            for word in word_list:
                word_index = word_list.index(word) + 1
                print('\n' + '-' * 120)
                print(f'>> Bài số [{lesson}] - Chữ số [{word_index}] : [{word}]', end='')

                lesson_path = os.path.join(self.root_dir, self.folder, self.save_folder, lesson)
                image_name = f'{word_index}_{word}.png'
                # create folder if not exists
                try: 
                    if not os.path.exists(lesson_path):
                        os.makedirs(lesson_path)
                except Exception as bug:
                    # print('Create folder EROOR', bug)
                    return

                if image_name in os.listdir(lesson_path):
                    print(f"---/ File: [{image_name}] đã tồn tại, bỏ qua lưu....")
                else:
                    for __ in range(5):
                        try:
                            for __ in range(3):
                                try:
                                    search_box_element = self.driver.find_element(By.CSS_SELECTOR, "input[id='search-text-box']")
                                    search_box_element.send_keys(word)
                                    break
                                except:
                                    continue
                            sleep(0.25)

                            for __ in range(3):
                                try:
                                    search_button_element = WebDriverWait(self.driver, 10).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[id='search-button'] > div"))
                                    )
                                    search_button_element.click()
                                    break
                                except:
                                    continue
                            sleep(1)
                            
                            try:
                                strokes_element = WebDriverWait(self.driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='pronoun-item']"))
                                )
                                strokes = int(re.findall(r'\d+', strokes_element.text)[0])
                                print(f' - Số nét: [{strokes}]')
                            except Exception as bug:
                                print('Strokes ERROR: ', bug)        
                            sleep(0.25)

                            for __ in range(3):
                                try:
                                    draw_again_button_element = WebDriverWait(self.driver, 10).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='kanji-draw-again'] > button"))
                                    )
                                    draw_again_button_element.click()
                                    break
                                except:
                                    continue
                            sleep(0.25)
                            
                            wait_draw_time = 4
                            if strokes > 4: 
                                wait_draw_time = int(strokes * 1.25)
                            if strokes > 10:
                                wait_draw_time = int(strokes * 1)
                            for i in range(wait_draw_time):
                                key = ['|', '/', '\\', '/', '\\']
                                for j in range(len(key)):
                                    print('\r' + f">> Thời gian đợi: {key[j]} {wait_draw_time-i:>2}s", end='', flush=True)
                                    sleep(0.2)
                            print('\r' + f">> Thời gian đợi: Đã xong.")

                            try:
                                vietnamese_sound_element = WebDriverWait(self.driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "h2[class='pronoun-item']"))
                                )
                                vietnamese_sound_text = vietnamese_sound_element.text  
                                if '-' in vietnamese_sound_text:
                                    vietnamese_sound = (vietnamese_sound_element.text).split('-')[1].strip()  
                                else:
                                    vietnamese_sound = ''

                            except Exception as bug:
                                print('vn_sound ERROR: ', bug)
                            sleep(0.25)

                            try:
                                janpanese_char_sound_element = WebDriverWait(self.driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='pronoun-item japanese-char']"))
                                )
                                janpanese_char_sound_text = janpanese_char_sound_element.text.replace('訓:', '').replace('音:', '')
                                janpanese_char_sound_list = [string.replace('\xa0', '&&') for string in janpanese_char_sound_text]
                                janpanese_char_sound = []
                                for c in janpanese_char_sound_list:
                                    if c == ' ': janpanese_char_sound.append('&&')
                                    else: janpanese_char_sound.append(c)
                                janpanese_char_sound = ''.join(janpanese_char_sound)
                                janpanese_char_sound = janpanese_char_sound.split('&&&&&&&&')
                            except Exception as bug:
                                print("jp_char ERROR: ", bug)
                            sleep(0.25)

                            try:
                                word_mean_element = WebDriverWait(self.driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='short-mean']"))
                                )
                                word_mean = word_mean_element.text
                                if word_mean == '':
                                    short_mearn_list = word_mean.split('Giải nghĩa:')[0].split('Nghĩa:')[1].strip().split('.')
                                    short_mearn_list = [line.strip() for line in short_mearn_list]
                                    if '' in short_mearn_list: short_mearn_list.remove('')
                                else:
                                    short_mearn_list = word_mean.split('Giải nghĩa:')[1].strip().split('.')
                                    short_mearn_list = [line.strip() for line in short_mearn_list]
                                    if '' in short_mearn_list: short_mearn_list.remove('')
                                short_mearn = '&&'.join(short_mearn_list)
                            except Exception as bug:
                                print("word_mearn ERROR: ", bug)
                            sleep(0.25)
                            
                            print(f"---/ Bộ: {vietnamese_sound}") 
                            print(f"---/ Phát âm: {janpanese_char_sound}") 
                            print(f"---/ Nghĩa: {short_mearn}") 
                            
                            try:
                                kanji_word_svg_element = WebDriverWait(self.driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, f"div[id='image-holder-{word}']"))
                                )
                                kanji_word_svg_code = kanji_word_svg_element.get_attribute('innerHTML')
                            except Exception as bug:
                                print('kanji word svg ERROR: ', bug)
                            sleep(0.25)
                            # kanji_word_svg_code = f"""
                            #     <body style="background: white;">
                            #         {kanji_word_svg_code}
                            #     </body>
                            # """

                            html_to_image = Html2Image()
                            html_to_image.screenshot(html_str=kanji_word_svg_code, save_as=image_name, size=(250, 250))
                            sleep(0.1)
                            shutil.move(image_name, lesson_path)
                            
                            lesson_data.append({
                                "word_index": str(word_index),
                                "vn_sound": vietnamese_sound,
                                "strokes": str(strokes),
                                "kanji": word,
                                "japanese_char": janpanese_char_sound,
                                "short_mean": short_mearn,
                                "link_mazi": f"{self.kanji_search_domain}{word}",
                                "svg_code": f"{kanji_word_svg_code}",
                            })

                            course_data.update({
                                f"{lesson}": lesson_data,
                            })

                            for __ in range(3):
                                try:
                                    clear_search_button_element = WebDriverWait(self.driver, 10).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[id='clear-search-text'] > div"))
                                    )
                                    clear_search_button_element.click()
                                    break
                                except:
                                    continue
                            sleep(0.25)
                            break
                        except Exception as bug:
                            print('ERROR range(3): ', bug)
                            for __ in range(3):
                                try:
                                    clear_search_button_element = WebDriverWait(self.driver, 10).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[id='clear-search-text'] > div"))
                                    )
                                    clear_search_button_element.click()
                                    break
                                except:
                                    continue
                            sleep(0.25)
                            continue

            self.kanji_data.update({
                f"{course}": course_data,
            })
            if isSave: self.json_write(json_save_path, self.kanji_data)
        
        print('\n' + '-' * 120)
        print('>> Đang đóng trình duyệt!...', end='')
        self.driver.close()
        self.driver.quit()
        print('\r' + '>> Đóng thành công!...      ')

def main():
    os.system('cls')
    kanjiCrawler = KanjiCrawler()

if __name__ == '__main__':
    main()