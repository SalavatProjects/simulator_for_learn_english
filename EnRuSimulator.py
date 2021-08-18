from striprtf.striprtf import rtf_to_text
import random as rd
from time import sleep
import os

class EnRuWord:
	def __init__(self, en_word, ru_word):
		self.en_word = en_word
		self.ru_word = ru_word


def clean_unnecessary_info(list_for_clean):
	i = 0
	while i < len(list_for_clean):
		list_for_clean[i] = list_for_clean[i].replace('\n', '')
		if list_for_clean[i] == '' or list_for_clean[i] == '\x00':
			del list_for_clean[i]
		else: i += 1

	return list_for_clean

def read_rtf(rtf_list):
	file_name = "MyEnRuWords.rtf"
	is_file_empty = os.stat(file_name)
	if is_file_empty.st_size > 0:
		with open(file_name, "r") as f:
			for line in f.readlines():
				text = rtf_to_text(line)
				en_ru_line = text.encode('ISO-8859-1').decode('windows-1251')
				rtf_list.append(en_ru_line)
		return rtf_list
	elif is_file_empty.st_size == 0:
		raise Exception("This file is empty!")

def splite_line(text_line_list, en_ru_words_list):
	for i in range(len(text_line_list)):
		if ' : ' in text_line_list[i]:
			splitted_line = text_line_list[i].split(' : ')
			ru_words = []
			# если в строке есть запятые, отделяем слова
			if ',' in splitted_line[1]:
				ru_words = splitted_line[1].split(',')
				for j in range(len(ru_words)):
					# если слово начинается с пробела, то убираем его
					if ' ' in ru_words[j]:
						ru_words[j] = ru_words[j][1:]
			elif ',' not in splitted_line[1]:
				ru_words.append(splitted_line[1])

			en_ru_word = EnRuWord(en_word = splitted_line[0], ru_word = ru_words)
			en_ru_words_list.append(en_ru_word)
		elif ' : ' not in text_line_list[i]:
			raise Exception("Отделяйте слово и его перевод(-ы) двоеточием\nдо и после двоеточия оставляйте пробел, это важно!")
	return en_ru_words_list
	

def EnRu_logic(EnRulist):
	print("Введите русский перевод предложенных слов:\n")
	score = 0
	point_unit = 100/len(EnRulist)
	rd.shuffle(EnRulist) # Перемешаем список, чтобы порядок слов был каждый раз разный
	for i in range(len(EnRulist)):		
		
		if len(EnRulist[i].ru_word) == 1:
			print("{0} переводится как: ".format(EnRulist[i].en_word), end = '')						
			user_answer = input()
			if user_answer == EnRulist[i].ru_word[0]:
				score += point_unit
				print("Верно!\n")
			elif user_answer != EnRulist[i].ru_word[0]:
				print("Неверно!\nПравильный ответ '{}'".format(EnRulist[i].ru_word[0]))
		
		# если у слова несколько переводов
		elif len(EnRulist[i].ru_word) > 1:
			print("У слова {0} несколько переводов: ".format(EnRulist[i].en_word))
			used_words = [] # список использованных слов, чтобы избежать повторения
			for j in range(len(EnRulist[i].ru_word)):
				print("Перевод {0}: ".format(j + 1), end = '')
				user_answer = input()
				if (user_answer in EnRulist[i].ru_word) and (user_answer not in used_words):
					used_words.append(user_answer)
				elif user_answer not in EnRulist[i].ru_word:
					print("Неверно! Правильными ответами были: ", end = '')
					for right_answer in EnRulist[i].ru_word:
						print('"{}"'.format(right_answer), end = ', ')
					print('\n')
					break
				elif user_answer in used_words:
					print("Не пытайся использовать одно и то же слово, так не выйдет:)\nВ общем неверно")
					break
				if j == (len(EnRulist[i].ru_word) - 1):
					score += point_unit
					print("Верно!")
			used_words.clear() # очищаем список, чтобы не добавлялись слова из других переводов
	
	return score


def RuEn_logic(EnRulist):
	ru_words_list = [] # создадим список русских слов так их больше

	# заполним список
	for i in range(len(EnRulist)):
		if len(EnRulist[i].ru_word) == 1:
			ru_words_list.append(EnRulist[i].ru_word[0])
		elif len(EnRulist[i].ru_word) > 1:
			for j in range(len(EnRulist[i].ru_word)):
				ru_words_list.append(EnRulist[i].ru_word[j])
	
	rd.shuffle(ru_words_list) # перемешаем список
	score = 0
	point_unit = 100/len(ru_words_list)

	for word in ru_words_list:
		for objects_enruwords in EnRulist:
			if word in objects_enruwords.ru_word:
				print("Слово {0} на английском будет: ".format(word), end = '')
				user_answer = input()
				if user_answer == objects_enruwords.en_word:
					print("Верно!\n")
					score += point_unit
				elif user_answer != objects_enruwords.en_word:
					print("Неверно!\n")
	return score

def check_result(score):
	if score <= 25:
		print("Вы набрали {} баллов\nПлохо, вы запомнили слишком мало слов!".format(score))
	elif (score > 25) and (score <= 50):
		print("Вы набрали {} баллов\nСлабовато, можно лучше!".format(score))
	elif (score > 50) and (score <= 90):
		print("Поздравляю, вы набрали {} баллов\nЭто неплохой результат, вы запомнили больше половины слов, но можно и получше!".format(score))
	elif (score > 90) and (score < 99):
		print("Поздравляю, вы набрали {} баллов\nЭто хороший результат, вы запомнили почти все слова!".format(score))
	elif score == 100:
		print("Поздравляю, вы набрали {} баллов\nЭто отличный результат, вы запомнили все слова!".format(score))


def main():
	text_line_list = [] # список англо-русских слов, собранные из rtf-файла
	text_line_list = read_rtf(text_line_list)
	text_line_list = clean_unnecessary_info(text_line_list)
	en_ru_words_list = [] # список объектов класса EnRuWord
	en_ru_words_list = splite_line(text_line_list, en_ru_words_list)
	print("Тренажер для запоминания английских слов")
	print("\nВведите какой режим вы хотите выбрать:")
	print("[1]: Хочу переводить с английского на русский;")
	print("[2]: Хочу переводить с русского на английский;")
	print("[3]: Мне нравиться хардкор! Хочу переводить с английского на русский и наоборот:)")	
	user_choice = input()
	if user_choice == '1':
		print("Вы выбрали режим [1], приготовтесь")
		sleep(3)
		en_ru_score = round(EnRu_logic(en_ru_words_list))
		check_result(en_ru_score)
	elif user_choice == '2':
		print("Вы выбрали режим [2], приготовтесь")
		sleep(3)
		ru_en_score = round(RuEn_logic(en_ru_words_list))
		check_result(ru_en_score)
	elif user_choice == '3':
		print("Вы выбрали хардокорный режим [3], приготовтесь!")
		sleep(3)
		en_ru_score = round(EnRu_logic(en_ru_words_list))
		print("Вы перевели слова с английского на русский и набрали {} баллов!\nНо это ещё не всё:)".format(en_ru_score))
		print("Теперь надо переводить с русского на английский, приготовтесь!")
		sleep(3)
		ru_en_score = round(RuEn_logic(en_ru_words_list))
		print("Вы перевели слова с русского на английский и набрали {} баллов!".format(ru_en_score))
		total_score = lambda score1, score2: (score1 + score2)/2
		print("Общий итог: {}".format(total_score(en_ru_score, ru_en_score)))
	else:
		raise Exception("Введите номер из предложенных режимов!")

		
	#total_score = EnRu_logic(en_ru_words_list)
	#total_score = RuEn_logic(en_ru_words_list)
#	print(total_score)
#	for i in range(len(en_ru_words_list)):
#		print(("Английское слово: {0:15} | Русский перевод: {1}").format(en_ru_words_list[i].en_word, en_ru_words_list[i].ru_word))


main()