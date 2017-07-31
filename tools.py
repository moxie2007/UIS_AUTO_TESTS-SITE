# -*- coding: utf-8 -*-
import time
from time import gmtime, strftime
import datetime
from datetime import datetime
import os, sys, codecs, sqlite3, re

from xml.etree import ElementTree as etree

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import pageElements
import loger 
from loger import Loger as loger
from testrail import *

lk_elements  = pageElements.LK()

class Use_config():
	def __init__(self):
		self.env = "lk"


	def set_lk_parametrs(self, path_to_file = 'C:\\CONFIG\\'):
		""" в этом методе читается конфигурационный файл и настройки
		передаются в класс настроек """
		config_file = str(path_to_file) + "uis_autotests.xml"
		try:
			app_xml = etree.parse(config_file)
			root = app_xml.getroot()
			platfom = {}
			try:
				for neighbor in root.iter('LK'):
					# так как значение параметра одно порядок значения не имеет, но если значений будет много, НУЖНО будет внести изменения в код
					for index in neighbor.attrib.values():
						for second_index in neighbor.attrib.keys():
							platfom[second_index] = str(index)
			except Exception as ex:
				pass
			self.url = platfom.get("url")
			self.user_name = platfom.get("user")
			self.password = platfom.get("password")
		except Exception as ex:
			pass
		return self.url, self.user_name, self.password
	
	@property
	def get_login_url(self):
		return self.url
	
	@property
	def get_user_name(self):
		return self.user_name
	
	@property
	def get_pass(self):
		return self.password

class Uis_tools(object):
	def __init__(self):
		self.driver = None


	def init_testrail(self):
	# это может и не работать, нужно отладить после тестов
			try:
				client = APIClient('http://testrail.uiscom.ru/')
				# тут нужен логин и пароль для доступа в тестрейл
				client.user = None
				client.password = None
				return self.client
			except Exception as ex:
				loger.file_log(text = 'Did not initialization testrail' , text_type = 'ERROR  ')

	def init_browser(self, product_type = 'Chrome'):
	# открывает объект Браузера, доделать выбор браузера и добавить настройку полноэкранности
		try:
			self.driver = webdriver.Chrome()
			self.driver.maximize_window()
			return self.driver
		except Exception as ex:
			# print(ex)
			loger.file_log(text = 'Did not initialization Browser' , text_type = 'ERROR  ')

	def close_browser(self):
	# закрывает открытый объект Браузера 
		if self.driver:
			self.driver.quit()
			self.driver = None

	def goto(self, url = None, breakONerror = False, delete_cookies = False):
	# осуществляет переход по URL 
		driver = self.driver
		self.url = url
		self.breakONerror = breakONerror
		if delete_cookies == True:
			try:
				driver.delete_all_cookies()
				loger.file_log(text = "Cookies were deleted", text_type = 'SUCCESS')
			except Exception as ex:
				loger.file_log(text = 'Can\'t delete cookies', text_type = 'ERROR  ')
		try:
			driver.get(url)
		except Exception as ex:
			loger.file_log(text = 'can not open URL. URL = ' + str(self.url) , text_type = 'ERROR  ')
			if self.breakONerror == True:
				self.abort_test()

	def element_is(self, element_definition = None):
	# проверяет наличие определенного элемента на странице
		self.element = None
		driver = self.driver
		try:
			self.element = driver.find_element_by_id(element_definition[0])
			return self.element
		except:
			pass
		try:
			self.element = driver.find_element_by_css_selector(element_definition[0])
			return self.element
		except:
			pass
		try:
			self.element = driver.find_element_by_link_text(element_definition[0])
			return self.element
		except:
			pass
		try:
			self.element = driver.find_element_by_xpath(element_definition[0])
			return self.element
		except:
			pass
		if self.element == None:
			return None
	
	def page_is(self, element_definition = None):
	# проверяет отображение страницы для определённого элемента
	# после введения ?testenv=1 необходимость этого отпала.
		self.element = None
		driver = self.driver
		try:
			self.element = driver.find_element_by_id(element_definition[1])
			return self.element
		except:
			pass
		try:
			self.element = driver.find_element_by_css_selector(element_definition[1])
			return self.element
		except:
			pass
		try:
			self.element = driver.find_element_by_xpath(element_definition[1])
			return self.element
		except:
			pass
		if self.element == None:
			return None # проверяет наличие определенной страницы
	
	def displayed_element(self, element_definition, timeOut = 20):
	# проверяет наличие (видимость) определенного элемента на странице
		driver = self.driver
		desired_element = None
		state = False
		elementTyte = None
		step = 1
		while step <= timeOut:
			try:
				# поиск статического объекта (xpath, id и так далее)
				if type(element_definition) is list:
					desired_element = self.element_is(element_definition)
				else:
				# поиск по объекту, в метод передан объект
					desired_element = element_definition
				if desired_element.is_displayed():
					state = True
					try:
						elementTyte = desired_element.tag_name
					except Exception as ex:
						pass
					break

			except Exception as ex:
				pass
			step += 1
			time.sleep(1)
		return [state, elementTyte, desired_element]	
	
	def elements_list (self, object_type = 'div', search_type = 'contains', mask = 'li',  timeOut = 10):
	# создает список элементов по определенной маске, возвращает количество найденных эллементов и сами элементы в виде готовывых объектов
		result = [None,[None]]
		driver = self.driver
		step = 1
		while step <= timeOut:
			try:
				# оставлено для дебага
				# print("//" + str(object_type) + "[" + str(search_type) + "(@" + str(mask) + ")]")
				elements = driver.find_elements_by_xpath("//" + str(object_type) + "[" + str(search_type) + "(@" + str(mask) + ")]")
			except:
				pass	
			try:
				if elements and len(elements) != 0:
					result = [len(elements), elements]
					break					
			except:
				pass
			step += 1
			time.sleep(1)
		return result
	
	def abort_test(self):
	# корректное прерывание теста
		self.close_browser()
		loger.file_log(text = "Finish sanity test with Error's", text_type = 'SUCCESS')
		sys.exit()
	
	def click_element(self, element_definition, breakONerror = False, timeOut = 120):
	# выполняет нажатие на эллемент
		try:
			current_object = self.displayed_element(element_definition = element_definition, timeOut = timeOut)
			if current_object[0] is True:
				current_object[2].click()
			else:
				loger.file_log(text = 'can not click ' + str(element_definition) , text_type = 'ERROR  ')
				if self.breakONerror == True:
					self.abort_test()
		except Exception as ex:
			loger.file_log(text = 'can not find and click ' + str(element_definition) , text_type = 'ERROR  ')
			if self.breakONerror == True:
				self.abort_test()
	
	def change_value(self, element_definition, text, breakONerror = False):
	# выполняет изменение значения в эллементе (пока, без перемещения курсора к эллементу)
		try:
			current_object = self.displayed_element(element_definition = element_definition)
			if current_object[0] is True:
				current_object[2].click()
				current_object[2].clear()
				current_object[2].send_keys(str(text))
		except Exception as ex:
			print(ex)
			loger.file_log(text = 'can not change data in the element ' + str(element_definition) , text_type = 'ERROR  ')
			print('test')
			if breakONerror == True:
				self.abort_test()
	
	def definition_current_url(self, breakONerror = True):
	# определяет текущий URL браузера
		driver = self.driver
		try:
			url =  driver.current_url
		except Exception as ex:
			loger.file_log(text = 'can not click ' + str(element_definition) , text_type = 'ERROR  ')
			if self.breakONerror == True:
						self.abort_test()
		return url
	
	def choose_from_dropdown(self, dropdown_element = None, current_item = None):
	# выбирает конкретное значение для из выпадающего списка. выпадающий список передается как элемент из pageElements, а значение как строковое наименование
	# пока не готово
		driver = self.driver
		try:
			self.displayed_element(element_definition = dropdown_element)
		except Exception as ex:
			loger.file_log(text = 'Can not scroll' + str(ex) + '\n' + 'URL = ' + str(url) + '\n', text_type = 'ERROR  ')
			if breakONerror is True:
				self.close_browser()
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()		

	def lk_sidemenu_navigation(self, item_menu = ['Общие отчёты', 'Аудитория'],  timeOut = 120, breakONerror = True):
	# навигация по основному меню (добавить timeout для while и зацепиться за родителя)
		time_index = 0
		inner_index = 2
		current_elems = []


		# elem_list2 = self.elements_list(object_type = 'tr', search_type = 'contains', mask = 'class, \'x-grid-tree-node-expanded  x-grid-row\'', timeOut = timeOut)
		# for index in elem_list2[1]:
		# 	if index.text != '' and index.text == item_menu[0]:
		# 		item_menu.remove(item_menu[0])
		# 		print('вскрытие:', index.text)
		# print('+'*10)
		# ищем открытый родитель и сдвигаем на подменю
		try:
			mask = 'class, \'x-grid-tree-node-expanded  x-grid-row\''
			elem_list9 = self.elements_list(object_type = 'tr', search_type = 'contains', mask = mask, timeOut = timeOut)[1]
			for t in elem_list9:
				if  t.text == item_menu[0]:
					inner_index += 1
					item_menu.remove(item_menu[0])
				# print(t.text)
		except Exception as ex:
			print(ex)
		# print('+'*10)
		# time.sleep(20)

		while True: 
		# ищем пункт меню котовый к нажатию
			mask = 'class, \' x-grid-cell-treecolumn x-grid-cell-first x-grid-cell-last x-unselectable x-grid-cell-treecolumn ul-tree-node-depth-' + str(inner_index) + '\''
			elem_list = self.elements_list(object_type = 'td', search_type = 'contains', mask = mask, timeOut = timeOut)[1]
			# проверка что искомый объект один, формирая список
			# print(len(elem_list))
			for elem in elem_list:
				# print(elem.text)
				if elem.text == item_menu[0]:
					current_elems.append(elem)


			if len(current_elems) == 1:
				# print(current_elems[0].get_attribute('id'))
				self.click_element(element_definition = current_elems[0], timeOut = timeOut)
				loger.file_log(text = 'Was clicked side menu item: ' + str(current_elems[0].text), text_type = 'SUCCESS')
				inner_index += 1
				item_menu.remove(item_menu[0])
				current_elems.remove(current_elems[0])
				# print('try', item_menu, current_elems, inner_index)

			if len(current_elems) == 0:
				# item_menu.remove(item_menu[0])
				print('БАБАХЕР', len(elem_list), len(current_elems), inner_index, mask)


			if len(current_elems) > 1:
				print('ПЕЧАЛЬКА', len(current_elems), inner_index, mask)

			if len(item_menu) == 0:
				# print('break')
				break

			if time_index >= timeOut:
				self.close_browser()
				loger.file_log(text = 'Can\'t choose your\'s menu item', text_type = 'ERROR  ')
				break
			time.sleep(1)
			time_index += 1	





		# while len(item_menu) != 0:
		# 	for elem in elem_list:
		# 		if item_menu


		# elem_list = self.elements_list(object_type = 'img', search_type = 'contains', mask = 'class, \' x-tree-elbow-img x-tree-elbow-end-plus x-tree-expander\'', timeOut = timeOut)[1]
		# for elem in elem_list:
		# 	try:
		# 		if elem.get_attribute('role') == 'presentation':
		# 			print(elem.)
		# 	except Exception as ex:
		# 		print(ex)
		



		# 		if len(item_menu) != 0 and elem_list:
		# 			# выбираем все объекты текст которых соответствует иикомому
		# 			current_ites = []
		# 			for elem in elem_list:
		# 				if elem.text == 



		# 				if elem.text == item_menu[0]:
		# 					# print('Жму на ' + str(item_menu[0]))
		# 					self.click_element(element_definition = elem, timeOut = timeOut)
		# 					loger.file_log(text = 'Was clicked side menu item: ' + str(elem.text), text_type = 'SUCCESS')
		# 					item_menu.remove(item_menu[0])
		# 					# time.sleep(2) # это настройка для дебага и в рабочей версии тут быть не должна
		# 					if len(item_menu) != 0:
		# 						pass
		# 						# print('остался ' + str(item_menu[0]))
		# 					break
		# 		else:
		# 			break
		# 	except Exception as ex:
		# 		loger.file_log(text = 'ошибка в навигации бокового меню', text_type = 'ERROR  ')
		# 		print('sidemenu: ',ex)
		# 		if breakONerror is True:
		# 			self.close_browser()
		# 			loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
		# 			sys.exit()
			
		# 	if time_index >= timeOut:
		# 		self.close_browser()
		# 		loger.file_log(text = 'Can\'t choose your\'s menu item', text_type = 'ERROR  ')
		# 		break
		# 	time.sleep(1)
		# 	time_index += 1	

		# return 	elem_list
	
	def top_menu_navigation(self, tab_name = None, timeOut = 20):
	# навигация по табам (вкладки вверху, активные выделяются зеленым)
		elem_list = self.elements_list(object_type = 'span',  search_type = 'contains',  mask = 'id, \'tab-\'', timeOut = timeOut)[1]
		elem_list_2 = self.elements_list(object_type = 'span',  search_type = 'contains',  mask = 'data-ref, \'btnInnerEl\'', timeOut = timeOut)[1]
		tab_names = []
		element_counter = 0
		if tab_name != None:
			try:
				for el in elem_list:
					tab_names.append(el.text)
					if el in elem_list_2 and el.is_displayed() and str(el.text) == str(tab_name):
						try:
							tab_before = str(self.get_active_top_tab)
							el.click()
							element_counter += 1
							loger.file_log(text = 'Click was made at: ' + str(tab_name) + ', active tab was switched from '+ str(tab_before) +' to ' + str(self.get_active_top_tab), text_type = 'SUCCESS')
						except Exception as ex:
							print(ex)
				if str(tab_name) not in tab_names:
					loger.file_log(text = 'Tab name is wrong: ' + str(tab_name), text_type = 'ERROR  ')
				if element_counter >= 2:
					loger.file_log(text = 'This element was found' + str(element_counter) + 'times. Check this scenario by hands.', text_type = 'WARNING')
			except Exception as ex:
				print(ex)			
		else:
			loger.file_log(text = 'You used method without  tab name, nothing was done', text_type = 'WARNING')

	@property
	def get_active_top_tab(self):
	# ищем активную вкладку на странице (зеленая сверху страницы), этот метод без внутренней проверки, считаем что таковые вкладки есть
		elem_list = self.elements_list(object_type = 'a',  search_type = 'contains',  mask = 'class, \'x-tab-active\'')[1]	
		active_tab = []
		try:
			for elem in elem_list:
				active_tab.append(str(elem.text))
		except:
			pass
		if len(active_tab) == 1:
			return active_tab[0]
		else:
			# такого быть в принципене может, но вдруг
			return False

	@property
	def get_header_text(self):
	# получаем заголовок страницы и id заголовка 
		result = None
		elem_list = self.elements_list(object_type = 'div',  search_type = 'contains',  mask = 'id, \'-headerText-\'', timeOut = 10)
		for elem in elem_list[1]:
			# if self.displayed_element(element_definition = elem) and elem.text != '':
			if elem.text != '':
				result = [elem.text, elem.get_attribute('id')]
				break
		return result

	@property
	def alert_preset(self):
	# возвращает количество и список объектов отображаемых иконок с ошибками если таковых нет то возвращает None
	# надо проверить работоспособность
		displayed_elems = []
		elem_list = self.elements_list(object_type = 'div',  search_type = 'contains',  mask = 'role, \'alert\'', timeOut = 10)[1]
		for elem in elem_list:
			if elem.is_displayed():
				displayed_elems.append(elem)
		if len(displayed_elems) > 0:
			return [len(displayed_elems), displayed_elems]
		else:
			return None

#-------------------------------------------------------------------------------------------------
	def switch_env(self, selected_element = None, server_name = 'sitecw2.webdev.uiscom.ru',  breakONerror = True):
	# изменяет тестовый сервер в личном кабинете ()
		driver = self.driver
		url_action_start = self.definition_current_url()
		self.click_element(element_definition = lk_elements.SELECT(element = selected_element), breakONerror = True)
		obj_servers_list = self.elements_list(object_type = 'li', mask = 'class, \'x-boundlist-item\'')
		if len(obj_servers_list[1]) > 0:
			for current_server_name in obj_servers_list[1]:
				if server_name == current_server_name.text:
					try:
						# скролим список к нужному элементу
						driver.execute_script("return arguments[0].scrollIntoView();", current_server_name)
						# нажимаем на искомый элемент
						current_server_name.click()
						loger.file_log(text = 'Was clicked at item: (' + str(server_name) + ') from dropdown list' , text_type = 'SUCCESS')
					except Exception as ex:
						loger.file_log(text = 'can not click ' + str(element_definition) , text_type = 'ERROR  ')
						if self.breakONerror == True:
							self.abort_test()
				# тут надо сделать проверку что сервер сменен правильно !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		time_index = 0
		while True:
			if str(url_action_start) != str(self.definition_current_url()):
				loger.file_log(text = 'Necessary server was chosen', text_type = 'SUCCESS')
				break
			if time_index >= 20 and breakONerror is True:
				self.close_browser()
				loger.file_log(text = 'Can not open necessary URL', text_type = 'ERROR  ')
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()			
			time.sleep(1)
			time_index += 1	

	def login_to(self, url = None, user = None, password = None, breakONerror = True):
	# логин в систему
		try:
			self.init_browser()
		except:
			loger.file_log(text = 'initialization Browser fail', text_type = 'ERROR  ')
			if breakONerror == True:
				abort_test()			
		try:
			self.goto(url, breakONerror)			
		except Exception as ex:
			loger.file_log(text = 'Can not open URL' + str(ex) + '\n' + 'URL = ' + str(url) + '\n', text_type = 'ERROR  ')
			if breakONerror is True:
				self.close_browser()
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()	
		try:
			self.change_value(element_definition = lk_elements.INPUT('login_e-mail'), text = user)
			self.change_value(element_definition = lk_elements.INPUT('login_password'), text = password)
			self.click_element(element_definition = lk_elements.BUTTON('btn_login'))
		except Exception as ex:
			loger.file_log(text = 'Can not input data (user name or password)', text_type = 'ERROR  ')
			if breakONerror is True:
				self.close_browser()
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
		
		time_index = 0
		# проверка на то, что открыто именно то, что мы и ожидали. по умолчанию открывается: Обзорный отчет 
		while True:
			try:
				header = self.get_header_text
				if header[0] == 'Обзорный отчет':
					loger.file_log(text = 'Open page done. URL is ' + str(url), text_type = 'SUCCESS')
					break
			except:
				pass
			if time_index >= 20 and breakONerror is True:
				self.close_browser()
				loger.file_log(text = 'Can not open necessary URL', text_type = 'ERROR  ')
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
			time.sleep(1)
			time_index += 1	

# обработка личного кабинета - Консультант - Общие настройки - Шаблоны сообщений
	@property
	def general_settings_get_templates_list(self):
	# поиск записай на странице выбирает формирует список объектов из элементов в таблице шаблонов ответа, в списке только отображенные на странице элементы
		return self.elements_list(object_type = 'table', search_type = 'contains', mask = 'id, \'commonsettings-page-tableview-\'')

	def general_settings_add_template(self, template_name = None):
	# добавление нового шаблона (в разработке!!!)
		if template_name != None:
			print(template_name)
			# ищем поле для ввода (поиск нужен потому, что все эллементы кроме страницы логина динамические)
			elems = self.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'textfield-\'')[1]
			for elem in elems:
				try:
					if elem.get_attribute('data-ref') == 'inputEl':
						self.change_value(element_definition = elem, text = template_name)
				except Exception as ex:
					print(ex)
			# нажимаем кнопку добавить
			elems = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'ul-mainbutton\'')
			
			elems_test = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'class, \'x-btn x-unselectable x-box-item x-btn-ul-main-medium\'')
			elems_test[1][0].click()
			# try:
			# 	print(elems_test)
			# except:
			# 	ptint('looser')

			# for elem in elems[1]:
			# 	try:
			# 		if elem.get_attribute('data-ref') == 'btnInnerEl' and elem.text == 'Добавить':
			# 			self.click_element(element_definition = elem)
			# 	except Exception as ex:
			# 		print(ex)
	

	def get_total_list_values_count(self, timeOut = 20):
	# поиск значения: Всего записей, со страниц с таблицами возвращает или текстовое значение или None
		page_items = []
		result = None
		time_index = 0

		print(self.get_header_text)

		# while True:
		# 	elems = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'class, \'x-toolbar-text x-box-item x-toolbar-item x-toolbar-text-ul\'')
		# 	# проверяем видимы ли найденные элементы
		# 	for item in elems:
		# 		if self.displayed_element(element_definition = item, timeOut = 1)[0]:
		# 			page_items.append(item)
		# 			#-----
		# 			print(item.text)

		# 	if len(page_items) == 1 and page_items[0].text != '':
		# 		result = page_items[0].text.split()[2]
		# 		break
		# 	if elems[0] > 1:
		# 		try:
		# 			for qw in elems[1]:
		# 				try:
		# 					print(qw.text, qw.get_attribute('id'))
		# 				except Exception as ex:
		# 					print (ex)
		# 		except Exception as ex:
		# 			print (ex)
		# 		loger.file_log(text = 'Was found more than one item. Please check result of the method: get_total_list_values_count', text_type = 'ERROR  ')
		# 		break
		# 	if time_index >= timeOut:
		# 		loger.file_log(text = 'Can\'t found counter of the items', text_type = 'ERROR  ')
		# 		break
		# 	time.sleep(1)
		# 	time_index += 1	
		# return result

	

