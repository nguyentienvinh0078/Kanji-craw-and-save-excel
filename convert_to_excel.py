import xlsxwriter
import json
import os
from util import json_write, json_read

def button_options(width=90, height=35, x_offset=10, y_offset=16, url='internal:HOME!A1', font_size=11):
    return {
        'width': width, 'height': height,
        'x_offset': x_offset, 'y_offset': y_offset,
        'font': {'name': 'Times New Roman', 'color': 'white', 'size': font_size, 'bold': True},
        'align': {'vertical': 'middle', 'horizontal': 'center'},
        'gradient': {'colors': ['#00B050', '#00B050']},
        'line': {'color': '#00B050', 'width': 0},
        'url': url,
    }

def get_sheet_data(word_list):
    sheet_data = []
    for word in word_list:
        word_index = word['index']
        vn_sound = word['vn_sound']
        kanji = word['word']
        strokes_image_path = ''

        onyomi_example = word['onyomi_example']
        onyomi_example = onyomi_example.split('###')
        onyomi_example = [f'** {text}' for text in onyomi_example]
        onyomi_example = '\n'.join(onyomi_example)

        kunyomi_example = word['onyomi_example']
        kunyomi_example = kunyomi_example.split('###')
        kunyomi_example = [f'** {text}' for text in kunyomi_example]
        kunyomi_example = '\n'.join(kunyomi_example)

        japanese_char = "** 訓(Onyomi)" + onyomi_example.strip() + '\n={}\n'.format('='*36) + '** 訓(Kunyomi)' + kunyomi_example.strip()
        japanese_char = japanese_char.replace('** 訓(Onyomi)**', '** 訓(Onyomi):')
        japanese_char = japanese_char.replace('** 訓(Kunyomi)**', '** 訓(Kunyomi):')

        content1 = word['components'] + word['comments']
        content1 = "** Thành phần: " + word['components'] + '\n={}\n'.format('='*40) + '** Comments: ' + word['comments']

        content2 = word['related_kanjis']

        link_mazi = word['kanji_mazzi_url']
        sheet_data.append([word_index, vn_sound, kanji, strokes_image_path, japanese_char, content1, content2, link_mazi])
    return sheet_data

ZOOM_PERCENT_SHEET_NORMAL = 95
ZOOM_PERCENT_SHEET_ALL = 30

database_folder = 'Kanji Database'
output_folder = 'Output'
stroke_image_folder = 'Stroke Image'
stroke_image_path = os.path.join(database_folder, stroke_image_folder)

n5_db_fname = 'N5_database.json'
n4_db_fname = 'N4_database.json'
course_db_fname = 'Course_database.json'

base_out_fname = 'ByVing'

courses = ['N5', 'N4', 'Course'] 
courses = ['Course'] 
def main():
    courses = ['Course'] 
    courses = ['N5', 'N4', 'Course'] 

    for course in courses:
        print("\n>> Course: ", course)
        base_fname = course_db_fname.split('_')[1].replace('.json', '')
        input_file_name = f'{course}_{base_fname}.json'

        input_file_path = os.path.join(database_folder, input_file_name)
        input_data = json_read(input_file_path)

        output_file_name = f'{course} Kanji {base_out_fname}.xlsx'
        output_file_path = os.path.join(output_folder, output_file_name)
        try: 
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
        except Exception as bug:
            print(f'Create folder {output_folder} EROOR', bug)
            break
        
        print(f">> Open: [ {output_file_path} ]")
        workbook = xlsxwriter.Workbook(output_file_path)   

        # ============================================================
        home_sheet_name = 'HOME'
        all_sheet_name = 'ALL'

        # ================== SHEET NAME: ALL =========================
        print(f">> Create sheet: {home_sheet_name}")
        worksheet = workbook.add_worksheet(home_sheet_name) 
        worksheet.hide_gridlines(2) # Hide_gridlines Options: 0) Don’t hide gridlines. 1)Hide printed gridlines only. 2) Hide screen and printed gridlines
        
        total_lesson = len(input_data[course])
        total_row_home_control = 5
        total_col_home_control = int(total_lesson / total_row_home_control)

        # x_offset_home_control = 8 if course!='Course' else 8
        x_offset_home_control = 8
        y_offset_home_control = 9 if course!='Course' else 6
        
        first_lesson = 26 if course=='N4' else 1

        for row in range(x_offset_home_control, x_offset_home_control + total_row_home_control):
            worksheet.set_row(row, height=60)
            for col in range(y_offset_home_control, y_offset_home_control + total_col_home_control):
                if row == x_offset_home_control and col == y_offset_home_control:
                    options = button_options(width=150, x_offset=0, y_offset=0, url=f'internal:{all_sheet_name}!A1')
                    worksheet.insert_textbox(row-3, col+1, f"KANJI {all_sheet_name}", options)
                
                lesson_name = first_lesson + total_col_home_control * (row - x_offset_home_control) + (col - y_offset_home_control)

                options = button_options(url=f'internal:{lesson_name}!A1')
                worksheet.insert_textbox(row, col, f"Bài {lesson_name}", options)
                
                worksheet.set_column(row, col, width=15)
                worksheet.write_string(row, col, '', workbook.add_format({'border': 2}))
        
        # ================== SHEET NAME: ALL =========================
        print(f">> Create sheet: {all_sheet_name}")
        worksheet = workbook.add_worksheet('ALL') 
        worksheet.set_zoom(ZOOM_PERCENT_SHEET_ALL) # zoom level: 31%
        worksheet.hide_gridlines(2) # Hide_gridlines Options: 0) Don’t hide gridlines. 1)Hide printed gridlines only. 2) Hide screen and printed gridlines

        end_sheet_index = total_lesson + 1
        button_middel_sheet_index = 7

        worksheet.set_row(0, height=150)

        home_sheet_options = button_options(width=400, height=150 ,x_offset=20, y_offset=20, url=f'internal:{home_sheet_name}!A1', font_size=40)
        worksheet.insert_textbox(0, button_middel_sheet_index, home_sheet_name, home_sheet_options)
        bottom_sheet_options = button_options(width=400, height=150 ,x_offset=20, y_offset=20, url=f'internal:{all_sheet_name}!A{end_sheet_index}', font_size=40)
        worksheet.insert_textbox(0, button_middel_sheet_index+2, f"CUỐI TRANG", bottom_sheet_options)

        worksheet.insert_textbox(end_sheet_index, button_middel_sheet_index, home_sheet_name, home_sheet_options)
        top_sheet_options = button_options(width=400, height=150 ,x_offset=20, y_offset=20, url=f'internal:{all_sheet_name}!A1', font_size=40)
        worksheet.insert_textbox(end_sheet_index, button_middel_sheet_index+2, f"ĐẦU TRANG", top_sheet_options)
            
        for lesson, word_list in input_data[course].items():
            row = (int(lesson)-26 if course=='N4' else int(lesson)-1) + 1
            total_columnn_all = len(word_list)
            worksheet.set_row(row, height=187.5)

            for col in range(total_columnn_all + 1):
                if col == 0:
                    worksheet.set_column(row, col, width=15)
                    worksheet.write_string(row, col, f'B{lesson}', workbook.add_format({
                            'font': 'Times New Roman', 'font_size': 40, 'bold': True, 'color': '#00B050',
                            'text_wrap': True, 'align': 'center', 'valign': 'vcenter',
                        })
                    )
                else:
                    word = word_list[col-1]['word']
                    file_name = f'{lesson}_{col}_{word}.png'
                    strokes_image_path = os.path.join(database_folder, stroke_image_folder, lesson, file_name)

                    worksheet.set_column(row, col, width=35)
                    worksheet.write_string(row, col, '', workbook.add_format({'border': True}))

                    word_url = f'internal:{lesson}!A{col}' if col<4 else f'internal:{lesson}!A{col+2}'
                    worksheet.insert_image(row, col, strokes_image_path, {
                        'x_scale': 1, 'y_scale': 1,
                        'url': word_url
                    })
        
        for lesson, word_list in input_data[course].items():
            sheet_data = get_sheet_data(word_list)
            sheet_data.insert(0, ['🔢STT', '📝ÂM HÁN VIỆT', '🈴CHỮ HÁN', '✒📌NÉT VIẾT', '🎶ÂM TIẾT', '📘Ý NGHĨA', '🔎MAZZI', '', ''])
            
            print('\r' + f">> Create sheet: {lesson}")
            worksheet = workbook.add_worksheet(f'{lesson}')
            worksheet.set_zoom(ZOOM_PERCENT_SHEET_NORMAL) # zoom level: 80%
            worksheet.hide_gridlines(2) # Hide_gridlines Options: 0) Don’t hide gridlines. 1)Hide printed gridlines only. 2) Hide screen and printed gridlines

            total_row = len(sheet_data)
            for row in range(total_row):
                word = sheet_data[row][2]
                total_column = len(sheet_data[row])

                if row == 0:
                    worksheet.set_row(row, height=30)
                    for col in range(total_column - 2):
                        worksheet.write_string(row, col, sheet_data[row][col], workbook.add_format({
                            'font': 'Cambria', 'font_size': 16, 'color': '#002060', 'bg_color': '#92D050', 'bold': True,
                            'text_wrap': True, 'align': 'center', 'valign': 'vcenter',
                            'border': True
                        }))
                else:
                    worksheet.set_row(row, height=187.5)

                    for col in range(len(sheet_data[row])):
                        item = sheet_data[row][col]
                        # ============== WORD INDEX =================
                        if col == 0:
                            worksheet.set_column(row, col, width=12)
                            worksheet.write_number(row, col, int(item), workbook.add_format({
                                    'font': 'Times New Roman', 'font_size': 16, 'bold': True,
                                    'text_wrap': True, 'align': 'center', 'valign': 'vcenter',
                                    'border': True
                                })
                            )

                        # ============== VN SOUND =================
                        elif col == 1:
                            worksheet.set_column(row, col, width=25)
                            worksheet.write_string(row, col, item, format)
                            worksheet.write_string(row, col, item, workbook.add_format({
                                    'font': 'Times New Roman', 'font_size': 16, 'bold': True,
                                    'text_wrap': True, 'align': 'center', 'valign': 'vcenter',
                                    'border': True
                                })
                            )

                        # ============== KANJI =================
                        elif col == 2:
                            worksheet.set_column(row, col, width=20)
                            worksheet.write_string(row, col, item, workbook.add_format({
                                    'font': 'MS Mincho', 'color': '#00B050', 'font_size': 72, 'bold': True,
                                    'text_wrap': True, 'align': 'center', 'valign': 'vcenter',
                                    'border': True
                                })
                            )

                        # ============== STROKES IMAGE =================
                        elif col == 3:
                            #----------------------------------------------------------
                            file_name = f'{row}_{word}.png'
                            strokes_image_path = os.path.join(STROKES_KANJI_FOLDER_PATH, lesson, file_name)

                            worksheet.set_column(row, col, width=35)
                            worksheet.write_string(row, col, '', workbook.add_format({'border': True}))
                            worksheet.insert_image(row, col, strokes_image_path, {
                                'x_scale': 1, 'y_scale': 1,
                                'url': f'{SEARCH_DOMAIN_2}{word}'
                            })
                        
                        # ============== JAPANESE CHAR SOUND =================
                        elif col == 4:
                            worksheet.set_column(row, col, width=70)
                            worksheet.write_string(row, col, item, workbook.add_format({
                                    'font': 'Times New Roman', 'font_size': 14,
                                    'text_wrap': True, 'align': 'left', 'valign': 'vcenter',
                                    'border': True
                                })
                            )

                        # ============== SHORT MEAN =================
                        elif col == 5:
                            worksheet.set_column(row, col, width=70)
                            worksheet.write_string(row, col, item, workbook.add_format({
                                    'font': 'Times New Roman', 'font_size': 13,
                                    'text_wrap': True, 'align': 'left', 'valign': 'vcenter',
                                    'border': True
                                })
                            )

                        # ============== MAZZI SEARCH URL =================
                        elif col == 6:
                            options = button_options(width=100, x_offset=22, y_offset=100, url=item)
                            worksheet.insert_textbox(row, col, f"Tra cứu", options)

                            worksheet.set_column(row, col, width=20)
                            worksheet.write_string(row, col, '', workbook.add_format({'border': True}))

                        elif col == 7:
                            worksheet.set_column(row, col, width=20)
                            if row == 1:
                                options = button_options(x_offset=20, y_offset=100, url=f'internal:{home_sheet_name}!A1')
                                worksheet.write_string(row, col, '', workbook.add_format({'border': False}))
                                worksheet.insert_textbox(row, col, home_sheet_name, options)

                            elif row == 2:
                                home_condition = lesson != f'{first_lesson}'
                                back_url = f'internal:{int(lesson)-1}!A1' if home_condition else f'internal:{home_sheet_name}!A1'
                                options = button_options(x_offset=20, y_offset=100, url=back_url)
                                worksheet.write_string(row, col, '', workbook.add_format({'border': False}))
                                worksheet.insert_textbox(row, col, f"TRƯỚC", options)

                            elif row == 3:
                                first_condition = lesson != f'{first_lesson + total_lesson - 1}'
                                netx_url = f'internal:{int(lesson) + 1}!A1' if first_condition else f'internal:{home_sheet_name}!A1'
                                options = button_options(x_offset=20, y_offset=100, url=netx_url)
                                worksheet.write_string(row, col, '', workbook.add_format({'border': False}))
                                worksheet.insert_textbox(row, col, f"SAU", options)

                        elif col == 8:
                            worksheet.set_column(row, col, width=40)
                            if row == 1:            
                                worksheet.write_string(row, col, f'BÀI HIỆN TẠI: {lesson}', workbook.add_format({
                                        'font': 'Times New Roman', 'font_size': 20, 'bold': True, 'color': '#00B050',
                                        'text_wrap': True, 'align': 'center', 'valign': 'vcenter',
                                    })
                                )

                            elif row == 2:          
                                home_condition = lesson != f'{first_lesson}'
                                text_msg_cell = f'BÀI TRƯỚC: {int(lesson)-1}' if home_condition else home_sheet_name
                                worksheet.write_string(row, col, text_msg_cell, workbook.add_format({
                                        'font': 'Times New Roman', 'font_size': 20, 'bold': True, 'color': '#00B050',
                                        'text_wrap': True, 'align': 'center', 'valign': 'vcenter',
                                    })
                                )

                            elif row == 3:          
                                first_condition = lesson != f'{first_lesson + total_lesson - 1}'
                                text_msg_cell = f'BÀI SAU: {int(lesson)+1}' if first_condition else home_sheet_name
                                worksheet.write_string(row, col, text_msg_cell, workbook.add_format({
                                        'font': 'Times New Roman', 'font_size': 20, 'bold': True, 'color': '#00B050',
                                        'text_wrap': True, 'align': 'center', 'valign': 'vcenter',
                                    })
                                )
                
                end_sheet_index = total_row
                button_middel_sheet_index = 4
                home_sheet_options = button_options(width=155, x_offset=20, y_offset=20, url=f'internal:{home_sheet_name}!A1')
                worksheet.insert_textbox(end_sheet_index, button_middel_sheet_index, home_sheet_name, home_sheet_options)
                
                top_sheet_options = button_options(width=155, x_offset=20, y_offset=20, url=f'internal:{int(lesson)}!A1')
                worksheet.insert_textbox(end_sheet_index, button_middel_sheet_index+1, f"ĐẦU TRANG", top_sheet_options)
                
        workbook.close()
    print(f">> Create OKE!!")

if __name__ == '__main__':
    main()