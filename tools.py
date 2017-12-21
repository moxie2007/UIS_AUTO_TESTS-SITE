# -*- coding: utf-8 -*-
import time
from time import gmtime, strftime
import datetime
from datetime import datetime
import os, sys, codecs, sqlite3, re

import multiprocessing.dummy as multiprocessing

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

import unittest

import start_uis_test

lk_elements  = pageElements.LK()

class User_config():
	def __init__(self):
		self.env = "lk"


	def set_lk_parametrs(self, path_to_file = 'C:\\CONFIG\\', source_name = 'LK'):
		""" в этом методе читается конфигурационный файл и настройки
		передаются в класс настроек """
		config_file = str(path_to_file) + "uis_autotests.xml"
		try:
			app_xml = etree.parse(config_file)
			root = app_xml.getroot()
			print(root)
			platfom = {}
			try:
				for neighbor in root.iter(source_name):
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
		print(self.url, self.user_name, self.password)
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

# class Uis_tools():
# 	def __init__(self):
		# self.driver = None
class Uis_tools(start_uis_test.Global_unit):
	def __init__(self, driver):
		self.driver = driver


	def init_testrail(self):
	# (!) это может и не работать, нужно отладить после тестов да и вообще, этому тут не место :-)
			try:
				client = APIClient('http://testrail.uiscom.ru/')
				# тут нужен логин и пароль для доступа в тестрейл
				client.user = None
				client.password = None
				return self.client
			except Exception as ex:
				loger.file_log(text = 'Did not initialization testrail' , text_type = 'ERROR  ')

	@property
	def get_driver(self):
	#(C) возвращает экземпляр Драйвера, используется в тексте user case для обращения к созданному объекту драйвера
 		return self.driver

	def sleep_function(self, timeout = 120):
	# (С!) метод хорошо б применить в связке с асинк эвейт для коректного ожидания элементов на странице
		time.sleep(timeOut)
		return 'timeout'
			
	def wait_for_event (self, action, timeout = 120):
		#(С!) новая ожидалка
		driver = self.driver
		p = multiprocessing.Pool()
		timer = time.sleep(timeout)

		results=[]
		for r  in p.imap_unordered(lambda f: f(),[a,b,c]):
			if r:
				break
		print(results)
		p.close()

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

	def execute_console_command(self, command = None, breakONerror = True):
	#(С!) метод выполняющий консольную команду, придумать, как проверять результат
		driver = self.driver
		try:
			result = driver.execute_script(command)
		except Exception as ex:
			loger.file_log(text = 'Can\'t do this (' + str(command) + ').\n command error is:' + str(ex), text_type = 'ERROR  ')
			result = None
			if breakONerror is True:
				self.close_browser
				loger.file_log(text = 'Finish sanity test with Error:', text_type = 'SUCCESS')
				sys.exit()
		return result

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
	# после введения ?testenv=1 необходимость этого отпала. Но быть может пригодится как дополнительный параметр поиска.
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
	# (C) проверяет наличие (видимость) определенного элемента на странице 
	# два способа передачи элемента: как список (например id элемента или xpath), как webdriver element. 
		driver = self.driver
		desired_element = None
		state = False
		element_tyte = None
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
						element_tyte = desired_element.tag_name
					except Exception as ex:
						pass
					break

			except Exception as ex:
				pass
			step += 1
			time.sleep(1)
		return {'state':state, 'element_type': element_tyte, 'element': desired_element}

	def page_scrolling_to_the_element(self, page_object = None):
	# (C) перемещает отображаемую часть страницы к элементу. в метод передается объект webdriver
		driver = self.driver
		if page_object != None:
			try:
				driver.execute_script("return arguments[0].scrollIntoView();", page_object)
			except Exception as ex:
				print('test in page_scrolling_to_the_element:  ',ex)
	
	def elements_list(self, object_type = 'div', search_type = 'contains', mask = 'li', timeOut = 10):
	# (C!)создает список элементов по определенной маске, возвращает количество найденных эллементов и сами элементы в виде готовывых объектов
	# хорошо б придумать нормальный выбор между x-path и css selector
		result = {}
		# None,[None], None]
		driver = self.driver
		step = 1
		looking_type = []
		while step <= timeOut:
			try:
				# оставлено для дебага
				# print("//" + str(object_type) + "[" + str(search_type) + "(@" + str(mask) + ")]")
				elements = driver.find_elements_by_xpath("//" + str(object_type) + "[" + str(search_type) + "(@" + str(mask) + ")]")
				looking_type.append('x-path')
			except:
				pass
			if search_type == None:
				try:
					elements = driver.find_elements_by_css_selector(mask)
					looking_type.append('selector')
				except Exception as ex:
					print('test in elements_list: ',ex)
			try:
				if elements and len(elements) != 0:
					visible_elements = []
					for el in elements:
						if el.is_displayed():
							visible_elements.append(el)
					# result = [len(visible_elements), visible_elements, looking_type]
					result = {'count':len(visible_elements), 'elements':visible_elements, 'type':looking_type}
					break					
			except:
				pass
			step += 1
			time.sleep(1)
		return result

	def abort_test(self):
	# корректное прерывание теста
		self.close_browser
		loger.file_log(text = "Finish sanity test with Error's", text_type = 'SUCCESS')
		sys.exit()
	
	def click_element(self, element_definition, breakONerror = False, timeOut = 120):
	# (C) выполняет нажатие на эллемент
		try:
			current_object = self.displayed_element(element_definition = element_definition, timeOut = timeOut)
			if current_object.get('state') is True:
				self.page_scrolling_to_the_element(page_object = current_object.get('element'))
				current_object.get('element').click()
			else:
				loger.file_log(text = 'can not click ' + str(element_definition) , text_type = 'ERROR  ')
				if breakONerror == True:
					self.abort_test()
		except Exception as ex:
			loger.file_log(text = 'can not find and click ' + str(element_definition) , text_type = 'ERROR  ')
			if breakONerror == True:
				self.abort_test()
	
	def change_value(self, element_definition, text, breakONerror = False):
	# (C) выполняет изменение значения в эллементе (пока, без перемещения курсора к эллементу)
		try:
			current_object = self.displayed_element(element_definition = element_definition)
			if current_object.get('state'):
				current_object.get('element').click()
				current_object.get('element').clear()
				current_object.get('element').send_keys(str(text))
		except Exception as ex:
			loger.file_log(text = 'can not change data in the element ' + str(element_definition) , text_type = 'ERROR  ')
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
	# (C!)выбирает конкретное значение для из выпадающего списка. выпадающий список передается как элемент из pageElements, а значение как строковое наименование
	# пока не готово
		driver = self.driver
		try:
			self.displayed_element(element_definition = dropdown_element)
		except Exception as ex:
			loger.file_log(text = 'Can not scroll' + str(ex) + '\n' + 'URL = ' + str(url) + '\n', text_type = 'ERROR  ')
			if breakONerror is True:
				self.close_browser
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()		

	def lk_sidemenu_navigation(self, item_menu = ['Общие отчёты', 'Аудитория'],  timeOut = 120, breakONerror = True):
	# (!) навигация по основному меню (добавить timeout для while и зацепиться за родителя)
		time_index = 0
		inner_index = 2
		current_elems = []
		# оперделяем какой заголовок отображен (какая страница)
		while True:
			try:
				header_befor_switch = self.get_header_text
				if type(header_befor_switch[0]) is str:
					break
			except:
				pass

			if time_index >= timeOut:
				self.close_browser
				loger.file_log(text = 'Can\'t find Header text from this page', text_type = 'ERROR  ')
				if self.breakONerror == True:
					self.abort_test()
				# break
			time.sleep(1)
			time_index += 1
		# проверяем не открыто ли уже головное меню (например: Общие отчёты, Список обращений, Служебные)
		try:
			mask = 'class, \'x-grid-tree-node-expanded  x-grid-row\''
			elem_list9 = self.elements_list(object_type = 'tr', search_type = 'contains', mask = mask, timeOut = timeOut).get('elements')
			for t in elem_list9:
				if  t.text == item_menu[0]:
					inner_index += 1
					item_menu.remove(item_menu[0])
		except Exception as ex:
			print('lk_sidemenu_navigation:  ', ex)
		time_index = 0
		while True: 
		# ищем пункт меню котовый к нажатию
			mask = 'class, \' x-grid-cell-treecolumn x-grid-cell-first x-grid-cell-last x-unselectable x-grid-cell-treecolumn ul-tree-node-depth-' + str(inner_index) + '\''
			elem_list = self.elements_list(object_type = 'td', search_type = 'contains', mask = mask, timeOut = timeOut).get('elements')
			# проверка, что искомый объект один, формируя список
			for elem in elem_list:
				if elem.text == item_menu[0]:
					current_elems.append(elem)
			if len(current_elems) == 1:
				# self.page_scrolling_to_the_element(page_object = current_elems[0])
				self.click_element(element_definition = current_elems[0], timeOut = timeOut)
				loger.file_log(text = 'Was clicked side menu item: ' + str(current_elems[0].text), text_type = 'SUCCESS')
				inner_index += 1
				item_menu.remove(item_menu[0])
				current_elems.remove(current_elems[0])
			# оставить для дебага
			# if len(current_elems) == 0:
			# 	# item_menu.remove(item_menu[0])
			# 	print('БАБАХЕР', len(elem_list), len(current_elems), inner_index, mask)
			if len(current_elems) > 1:
				loger.file_log(text = 'Was found more than one item. Please check this method: lk_sidemenu_navigation', text_type = 'ERROR  ')
				# тут может быть ошибка
				break
			if len(item_menu) == 0:
				break
			if time_index >= timeOut:
				self.close_browser
				loger.file_log(text = 'Can\'t choose your\'s menu item', text_type = 'ERROR  ')
				break
			time.sleep(1)
			time_index += 1
		# проверка на то, что нужная страница открыта (для этого, текст заголовка должен быть изменен)
		time_index = 0
		while True:
			header_after_switch = self.get_header_text
			if header_after_switch != None:
				if header_befor_switch[1] != header_after_switch[1]:
					loger.file_log(text = 'Switching was done from ' + str(header_befor_switch[0]) + ' to ' + str(header_after_switch[0]), text_type = 'SUCCESS')
					break
			if time_index >= timeOut:
				loger.file_log(text = 'Can\'t choose next item  from west menu', text_type = 'ERROR  ')
				if breakONerror is True:
					self.close_browser		
					break
				break
			time.sleep(1)
			time_index += 1

	def top_menu_navigation(self, tab_name = None, timeOut = 20):
	#(С!) навигация по табам (вкладки вверху, активные выделяются зеленым)
		# ищем элементы\табы на странице (старые и новые) условием выхода из цикла будет нахождение любых
		timer_index = 0
		items_index = 0
		while True:
			# старое меню
			try:
				old_elems = self.elements_list(search_type = None, mask = 'span[id*=-tab] > span[id$=btnInnerEl]', timeOut = 1)
				if old_elems.get('count') != None:
					items_index += 1
			except:
				pass
			# новое меню
			try:
				new_elems = self.elements_list(search_type = None, mask = 'span[class=x-tab-inner]', timeOut = 1)
				if new_elems.get('count') != None:
					items_index += 1
			except:
				pass

			if items_index != 0 :
				elems = new_elems.get('elements') + old_elems.get('elements') 
				break

			if timer_index >= timeOut:
				loger.file_log(text = 'No tab\'s navigation buttons at page', text_type = 'ERROR  ')
				elems = []
				break
			timer_index += 1
		
		if tab_name != None and len(elems) != 0:
			for el in elems:
				try:
					if el.is_displayed() and str(el.text) == str(tab_name):
						try:
							# tab_before = str(self.get_active_top_tab)
							self.click_element(element_definition = el,  breakONerror = True)
							try:
								print(self.get_active_top_tab)
							except:
								pass
							break
						except Exception as ex:
							pass
				except:
					pass
		else:
			loger.file_log(text = 'You used method without tab name or such elements were not found, nothing was done', text_type = 'WARNING')

		# elem_list = self.elements_list(object_type = 'span',  search_type = 'contains',  mask = 'id, \'tab-\'', timeOut = timeOut)[1]
		# elem_list_2 = self.elements_list(object_type = 'span',  search_type = 'contains',  mask = 'data-ref, \'btnInnerEl\'', timeOut = timeOut)[1]
		# tab_names = []
		# element_counter = 0
		# if tab_name != None:
		# 	try:
		# 		for el in elem_list:
		# 			tab_names.append(el.text)
		# 			if el in elem_list_2 and el.is_displayed() and str(el.text) == str(tab_name):
		# 				try:
		# 					tab_before = str(self.get_active_top_tab)
		# 					el.click()
		# 					element_counter += 1
		# 					loger.file_log(text = 'Click was made at: ' + str(tab_name) + ', active tab was switched from '+ str(tab_before) +' to ' + str(self.get_active_top_tab), text_type = 'SUCCESS')
		# 				except Exception as ex:
		# 					print(ex)

		# 		if str(tab_name) not in tab_names:
		# 			loger.file_log(text = 'Tab name is wrong: ' + str(tab_name), text_type = 'ERROR  ')
		# 		if element_counter >= 2:
		# 			loger.file_log(text = 'This element was found' + str(element_counter) + 'times. Check this scenario by hands.', text_type = 'WARNING')
		# 	except Exception as ex:
		# 		print(ex)			
		# else:
		# 	loger.file_log(text = 'You used method without  tab name, nothing was done', text_type = 'WARNING')

	@property
	def get_active_top_tab(self):
	# (! нужно переписать для новой менюшки) ищем активную вкладку на странице (зеленая сверху страницы), этот метод без внутренней проверки, считаем что таковые вкладки есть
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
		for elem in elem_list.get('elements'):
			if elem.text != '':
				result = [elem.text, elem.get_attribute('id')]
				break
		return result

	@property
	def get_active_page_in_list(self):
	# (C) находит активную страницу (это навигация по: В начало,1,2,дальше), по обводке вокруг значения
	# больше одного значения по логике работы метода, быть не должно
		result = [[],{}]
		elems = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'class, \'x-btn x-btn-ul-usual-without-border x-unselectable x-box-item x-toolbar-item x-btn-ul-usual-medium x-btn-pressed\'')
		for elem in elems.get('elements'):
			if elem.text != '':
				result[0].append(elem.text)
				result[1][elem.text] = elem
		if len(result[0]) == 1:
			return result
		else:
			loger.file_log(text = ('Unexpected items count: ', result[1]) , text_type = 'ERROR  ')
			return [[None], {'1':None}]

	def get_total_list_values_count(self, timeOut = 3):
	# (C) поиск значения: Всего записей, со страниц с таблицами возвращает список: текстовое значение и id cтраницы 
		page_items = []
		result = []
		time_index = 0
		page = self.get_header_text
		while True:
			elems = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'class, \'x-toolbar-text x-box-item x-toolbar-item x-toolbar-text-ul\'', timeOut = 1)
			empty_list = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'class, \'x-grid-empty\'', timeOut = 1)
			# если эллементов нет и отображена надпись: Нет записей, прерываем поиск
			if empty_list.get('count') != None and empty_list.get('elements')[0].text == 'Нет записей':
				result.append(0)
				result.append(page)
				break
			# проверяем видимы ли найденные элементы
			for item in elems.get('elements'):
				if '-page-tbtext-displayItem-' in item.get_attribute('id') and self.displayed_element(element_definition = item, timeOut = 1).get('state'):
					page_items.append(item)
			if len(page_items) == 1 and page_items[0].text != '':
				result.append(page_items[0].text.split()[2])
				result.append(page)
				break		
			if len(page_items) > 1:
				loger.file_log(text = 'Was found more than one item. Please check result of the method: get_total_list_values_count', text_type = 'ERROR  ')
				break			
			if time_index >= timeOut:
				loger.file_log(text = 'Can\'t found counter of the items', text_type = 'ERROR  ')
				result.append(None)
				result.append(page)
				break			
			time.sleep(1)
			time_index += 1	
		return result

	@property
	def get_paging_templates_list(self):
	# (C) получение списка всех возможных кнопок для постраничной навигации (возвращает объекты)
		result = [[],{}]
		elems = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'id, \'-page-ul-usualbutton-\'')
		for elem in elems[1]:
			if elem.text != '':
				result[0].append(elem.text)
				result[1][elem.text] = elem
		return result

	@property
	def alert_preset(self):
	# (!C) возвращает количество и список объектов отображаемых иконок с ошибками если таковых нет то возвращает None
	# надо проверить работоспособность
		displayed_elems = []
		elem_list = self.elements_list(object_type = 'div',  search_type = 'contains',  mask = 'role, \'alert\'', timeOut = 10).get('elements')
		for elem in elem_list:
			if elem.is_displayed():
				displayed_elems.append(elem)
		if len(displayed_elems) > 0:
			return [len(displayed_elems), displayed_elems]
		else:
			return None

#-------------------------------------------------------------------------------------------------
	def switch_env(self, selected_element = None, server_name = 'sitecw2.webdev.uiscom.ru',  breakONerror = True):
	# (!)изменяет тестовый сервер в личном кабинете
		driver = self.driver
		url_action_start = self.definition_current_url()
		# ищем окно с текущим сайтом (должно быть одно)
		site_dropdown = self.elements_list(object_type = 'input', mask = 'class, \'x-form-field x-form-text x-form-text-cm-siteselector\'')
		if site_dropdown.get('count') != 1:
			loger.file_log(text = 'Were found ' + str(site_dropdown.get('count')) + ' element\'s. It\'s wrong', text_type = 'ERROR  ')
			if self.breakONerror == True:
				self.abort_test()
		else:	
			# открываем список доступных сайтво
			self.click_element(element_definition = site_dropdown.get('elements')[0], breakONerror = True) 
			obj_servers_list = self.elements_list(object_type = 'li', mask = 'class, \'x-boundlist-item\'')
			if len(obj_servers_list.get('elements')) > 0:
				for current_server_name in obj_servers_list.get('elements'):
					if server_name == current_server_name.text:
						try:
							# скролим список к нужному элементу
							self.page_scrolling_to_the_element(page_object = current_server_name)
							# нажимаем на искомый элемент
							current_server_name.click()
							loger.file_log(text = 'Was clicked at item: (' + str(server_name) + ') from dropdown list' , text_type = 'SUCCESS')
						except Exception as ex:
							loger.file_log(text = 'can not click ' + str(element_definition) , text_type = 'ERROR  ')
							if self.breakONerror == True:
								self.abort_test()
			# если URL сменен то считаем, что смена прошла успешно
			time_index = 0
			while True:
				if str(url_action_start) != str(self.definition_current_url()):
					loger.file_log(text = 'Necessary server was chosen', text_type = 'SUCCESS')
					break
				if time_index >= 20 and breakONerror is True:
					self.close_browser
					loger.file_log(text = 'Can not open necessary URL', text_type = 'ERROR  ')
					loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
					sys.exit()			
				time.sleep(1)
				time_index += 1	

	def login_to(self, url = None, user = None, password = None, breakONerror = True):
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
			self.change_value(element_definition = lk_elements.INPUT('login_e-mail'), text = user)
			self.change_value(element_definition = lk_elements.INPUT('login_password'), text = password)
			self.click_element(element_definition = lk_elements.BUTTON('btn_login'))
		except Exception as ex:
			loger.file_log(text = 'Can not input data (user name or password)', text_type = 'ERROR  ')
			if breakONerror is True:
				self.close_browser
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
				self.close_browser
				loger.file_log(text = 'Can not open necessary URL', text_type = 'ERROR  ')
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
			time.sleep(1)
			time_index += 1	

	def change_top_menu_values(self, menu_item = 'Аккаунт'):
	# (С!G) выбор опций верхнего меню
	# формируем список доступных меню, {'название':}
		menu_values = {'Аккаунт':1,'Сервисы и Статистика':2, 'Управление пользователями':3, 'Сменить пароль':4, 'Добавить наблюдателя ':5, 'Выйти':6}
	# определяем какое значение выставлено сейчас



# ______________________________________________________________________________________________
	def account_click(self):
		elems = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'class, \'x-btn-inner x-btn-inner-ul-linklike-medium\'')
		for item in elems[1]:
			if 'Администратор' in item.text:
				self.click_element(element_definition = item)
		time.sleep(5)
		new_ellems = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'class, \'x-menu-item-text x-menu-item-text-ul x-menu-item-indent\'')
		for new_one in new_ellems[1]:
			try:
				print(new_one.text)
				if 'Аккаунт' in new_one.text:
					self.click_element(element_definition = new_one)
					break
			except Exception as ex:
				peint(ex)

# ______________________________________________________________________________________________
# (!)обработка личного кабинета - Консультант - Каналы - Обратный звонок
	def channels_back_call_choose_of_the_schedule(self, graphik_name = None):
	# (!С) выбираем график показа виджет обратного звонка/ значение None соответствует любое значение
	# проверяем что установлено сейчас
	  # ищем id элемента с текстом: График показа
		lable_item = self.elements_list(object_type = 'label', search_type = 'contains', mask = 'class, \'x-form-item-label x-form-item-label-ul\'')
		for index in lable_item.get('elements'):
			if 'График показа:' == str(index.text):
				current_id = index.get_attribute('id').split('-')[4]
				break
		# определяем, что написано в поле
		if current_id:
			print('1')
			print(self.displayed_element(element_definition =  lk_elements.BUTTON('cons_back_call_schedule_drop_down_btn',mask = current_id), timeOut = 3))
	# если значение есть то проверяем доступно оно для выбора или нет, если значение нет то выбираем любое
	# if 
	# устанавливаем значение
	# проверяем сменилосьли значение
	# проверяем активно оно сейчас лили нет и возвращаем это значение.


