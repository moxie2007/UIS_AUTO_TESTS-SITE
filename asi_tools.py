import sys, time
import tools, start_uis_test, pageElements
import loger 
from loger import Loger as loger

# создаем объект, для использования модуля описывающего элементы на страницах
lk_elements  = pageElements.LK()

class Asi_tools(tools.Uis_tools):
	def __init__(self, driver):
		self.driver = driver

#ШФБЛОН(! Этой опции больше нет все методы перенести и перепроверить) консультант -- Общие настройки -- Шаблоны сообщений
	@property
	def general_settings_get_templates_list(self):
	# (C) поиск записай на странице выбирает формирует список объектов из элементов в таблице шаблонов ответа, в списке только отображенные на странице элементы
		return self.elements_list(object_type = 'table', search_type = 'contains', mask = 'id, \'commonsettings-page-tableview-\'')

	def login_to_yandex(self, url = None, user = None, password = None, breakONerror = True):
		print(login,password,url)
		# логин в систему		
		try:
			self.goto(url, breakONerror)			
		except Exception as ex:
			loger.file_log(text = 'Can not open URL' + str(ex) + '\n' + 'URL = ' + str(url) + '\n', text_type = 'ERROR  ')
			if breakONerror is True:
				self.close_browser
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()	
		try:
			self.change_value(element_definition = lk_elements.INPUT('login_yandex'), text = user)
			self.change_value(element_definition = lk_elements.INPUT('password_yandex'), text = password)
			self.click_element(element_definition = lk_elements.BUTTON('btn_login_yandex'))
		except Exception as ex:
			loger.file_log(text = 'Can not input data (user name or password)', text_type = 'ERROR  ')
			if breakONerror is True:
				self.close_browser
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
			
			# time_index = 0
			# # проверка на то, что открыто именно то, что мы и ожидали. по умолчанию открывается: Обзорный отчет 
			# while True:
			# 	try:
			# 		header = self.get_header_text
			# 		if header[0] == 'Обзорный отчет':
			# 			loger.file_log(text = 'Open page done. URL is ' + str(url), text_type = 'SUCCESS')
			# 			break
			# 	except:
			# 		pass
			# 	if time_index >= 20 and breakONerror is True:
			# 		self.close_browser
			# 		loger.file_log(text = 'Can not open necessary URL', text_type = 'ERROR  ')
			# 		loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
			# 		sys.exit()
			# 	time.sleep(1)
			# 	time_index += 1	