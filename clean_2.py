def clean_text(input_text):
	input_text = input_text.replace('音', 'Onyomi')
	input_text = input_text.replace('訓', 'Kunyomi')

	input_text = input_text.replace('"', ' ')

	input_text = input_text.replace('：', ':')
	input_text = input_text.replace(': ', ':')
	input_text = input_text.replace(' :', ':')
	input_text = input_text.replace(' : ', ':')
	input_text = input_text.replace(':', ': ')

	input_text = input_text.replace('】', ']')
	input_text = input_text.replace(']', '] ')
	input_text = input_text.replace('【', '[')
	input_text = input_text.replace('[', ' [')

	input_text = input_text.replace('（', '(')
	input_text = input_text.replace('）', ')')

	input_text = input_text.replace('\u3000', ' ')
	input_text = input_text.replace('\t', '$$')
	input_text = input_text.replace('\n', '$$')

	input_text = input_text.replace('$$', '$')
	input_text = input_text.replace(' $', '$')
	input_text = input_text.replace('$ ', '$')
	input_text = input_text.replace('$', '\n')

	while '\n\n' in input_text:
		input_text = input_text.replace('\n\n', '\n')

	input_text = input_text.split('\n')
	temp_text = []
	for text in input_text:
		while '  ' in text:
			text = text.replace('  ', ' ')
		temp_text.append(text)
	input_text = temp_text

	input_text = [text.strip() for text in input_text if text]
	input_text = '\n'.join(input_text)

	input_text = input_text.split('Onyomi:')
	temp_text = []
	for text in input_text:
		if 'Onyomi' in text:
			text = text.replace('Onyomi', '音')
		if 'Kunyomi' not in text:
			text = text + 'Kunyomi:\n'
		text = 'Onyomi:' + text
		temp_text.append(text)
	input_text = temp_text

	input_text = '\n'.join(input_text)

	input_text = input_text.replace('Onyomi', '$$音(Onyomi)')
	input_text = input_text.replace('Kunyomi', '訓(Kunyomi)')

	input_text = input_text.replace('訓(Kunyomi)', '\n訓(Kunyomi)')
	input_text = input_text.replace('\n\n訓(Kunyomi)', '\n訓(Kunyomi)')
	input_text = input_text.replace('訓(Kunyomi)\n\n', '訓(Kunyomi)\n')

	input_text = input_text.split('\n')
	input_text = [text.strip() for text in input_text if text]
	input_text = '\n'.join(input_text)

	input_text = input_text.split('$$')[2:]

	count = 0
	for text in input_text:
		count += 1
		onyomi = text.split('\n訓(Kunyomi):')[0]
		kunyomi = text.split('\n訓(Kunyomi):')[1]

		if onyomi.endswith('\n'):
			onyomi = onyomi[:-1]

		if kunyomi.endswith('\n'):
			kunyomi = kunyomi[:-1]

		onyomi = onyomi.replace('\n', '[*]')
		kunyomi = kunyomi.replace('\n', '[*]')

		print('{', end='')
		print('"onyomi": "{}"'.format(onyomi), end=',')
		print('"kunyomi": "{}"'.format(kunyomi), end='')
		if count != len(input_text):
			print('},')
		else:
			print('}')

	# print(count, end='')

input_text = """
音：シュ	日本酒（に　ほん　しゅ）：rượu Nhật Bản
訓：さけ/さか：rượu	酒屋（さか　や）：quán rượu
音：テイ	"規定（きてい）：quy định
定規（じょうぎ）：thước kẻ
予定（よてい）：dự định
安定的（あんていてき）：tính ổn định"
訓：	
音：レイ：ví dụ	"例文（れい　ぶん）：mẫu câu
例外（れい　がい）：ngoại lệ
例年（れい　ねん）： hàng năm"
"訓：たと・える：so sánh
　　たと・えば：ví dụ"	
音：チョウ	"調子（ちょう　し）：cuộc điều tra
調味料（ちょう　み　りょう）：gia vị
調査（ちょう　さ）：điều tra"
"訓：しら・べる：tra xét 
　　ととの・う/える：thu "	
音：シ	"支店（し　てん）：chi nhánh
支払い（し　はら　い）：thanh toán, chi trả"
訓：ささ・える：giúp đỡ	
音：カ	"過去（か　こ）：quá khứ
過半数（か　はん　すう）：đa số; đại đa số
過程（か　てい）： quá trình; giai đoạn"
"音：す・ぎる：đi qua;nhiều
　　す・ごす：dùng (thìgiờ)"	
音：キン/ゴン	"転勤（てん　きん）：chuyển việc  (chuyển nơi làm việc )
勤務（きん　む）：công việc
勤勉（きん　べん）：cần cù; chăm chỉ;"
訓：つと・める：làm việc	
音：タク	"自宅（じたく）：nhà riêng
帰宅（きたく）：về nhà
住宅（じゅうたく）：nhà ở
お宅（おたく）：nhà (kính ngữ)"
訓：	
音：セイ	製品（せいひん）：sản phẩm
訓：	
音：セイ・ショウ	"男性（だんせい）：nam giới
女性（じょせい）：nữ giới
性質（せいしつ）：tính chất"
訓：	
音：ヨウ/ショウ	"同様（どう　よう）：đồng dạng
おかげ様で（おかげ　さま　で）：cảm ơn
(bày tỏ sự cảm ơn khi nhận được sự giúp đỡ)
様子（よう　す）：vẻ bề ngoài; phong thái; dáng "
訓：さま：tiếng xưng hô đi sau tên người biểu thị sự kính trọng	＿＿様（さま）：ngài
音：カン	"感謝（かん　しゃ）：biết ơn
感心（かん　しん）：quan tâm
感動（かん　どう）：sự cảm động"
訓：かん・じる：cảm thấy	


"""
clean_text(input_text)
input()