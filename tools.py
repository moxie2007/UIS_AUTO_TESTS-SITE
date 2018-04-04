# -*- coding: utf-8 -*-
import time
from time import gmtime, strftime
import datetime
# from datetime import datetime
import os, sys, codecs, sqlite3, re

# import multiprocessing.dummy as multiprocessing

from xml.etree import ElementTree as etree

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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

class User_config(start_uis_test.Global_unit):
	def __init__(self):
		self.env = "lk"


	def set_lk_parametrs(self, path_to_file = 'C:\\CONFIG\\', source_name = 'LK'):
		""" в этом методе читается конфигурационный файл и настройки
		передаются в класс настроек """
		config_file = str(path_to_file) + "uis_autotests.xml"
		try:
			app_xml = etree.parse(config_file)
			root = app_xml.getroot()
			platfom = {}
			try:
				for neighbor in root.iter(str(source_name)):
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
			
	def wait_for_results (self, time_data = None, time_out = 120):
	#(С) новая ожидалка, что бы работало, этот метод нужно разместить до и после исполняемого модуля. 
	# Первый вызов формирует значение начала ожидани, второй конец и проверку на таймаут. в time_data ставим значение первого вызова
		# определяем текущее время и записываем его в словарь
		today = datetime.datetime.today() # системный вызов
		method_state = False
		result = time_data
		while True:
			# если это первый вход, то записываем время начала действия
			if time_data == None:
				result = {}
				result['start_time'] = today.timestamp()
				break
			# если это проверка на тайм_аут 
			if type(time_data) == dict and time_data.get('start_time') != None:
				result['current_time'] = today.timestamp()
				method_state = True
				break
		# если есть два значения для расчета интервала, то вычисляем разницу
		if method_state:
			if time_data.get('current_time') - time_data.get('start_time') >= time_out:
				result['result'] = True
			else:
				result['result'] = False
		else:
			result['result'] = False		
		return result

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
		step_await = self.wait_for_results()
		while True:
			method_status = False
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
					method_status = True
			except Exception as ex:
				pass
			if method_status:
				break
			if self.wait_for_results(time_data = step_await, time_out = timeOut).get('result'):
				break
			time.sleep(0.1)
		return {'state':state, 'element_type': element_tyte, 'element': desired_element}

	def page_scrolling_to_the_element(self, page_object = None):
	# (C) перемещает отображаемую часть страницы к элементу. в метод передается объект webdriver
		driver = self.driver
		if page_object != None:
			try:
				driver.execute_script("return arguments[0].scrollIntoView();", page_object)
			except Exception as ex:
				print('test in page_scrolling_to_the_element:  ',ex)

	def get_parent(self, current_object = None):
	# (CG!)возвращает родительский объект (на один вверх)
		return current_object.find_element_by_xpath('..')
	
	def elements_list(self, object_type = 'div', search_type = 'contains', mask = 'li', timeOut = 10):
	# (C)создает список элементов по определенной маске, возвращает количество найденных эллементов и сами элементы в виде готовывых объектов
	# хорошо б придумать нормальный выбор между x-path и css selector
		result = {}
		# None,[None], None]
		driver = self.driver
		step = 1
		step_await = self.wait_for_results()
		looking_type = []
		while True:
			try:
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
					result = {'count':len(visible_elements), 'elements':visible_elements, 'type':looking_type}
					break					
			except:
				pass
			if self.wait_for_results (time_data = step_await, time_out = timeOut).get('result'):
				break				
		return result

	def abort_test(self):
	# корректное прерывание теста
		self.close_browser
		loger.file_log(text = "Finish sanity test with Error's", text_type = 'SUCCESS')
		sys.exit()
	
	def click_element(self, element_definition, breakONerror = False, scroll_to_element = True, timeOut = 120):
	# (C) выполняет нажатие на эллемент
		try:
			current_object = self.displayed_element(element_definition = element_definition, timeOut = timeOut)
			if current_object.get('state'):
				if scroll_to_element:
					self.page_scrolling_to_the_element(page_object = current_object.get('element'))
				current_object.get('element').click()
			else:
				loger.file_log(text = 'can not click ' + str(element_definition) , text_type = 'ERROR  ')
				if breakONerror:
					self.abort_test()
		except Exception as ex:
			loger.file_log(text = 'can not find and click ' + str(element_definition) , text_type = 'ERROR  ')
			if breakONerror:
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
			loger.file_log(text = 'Сan\'t change data in the element ' + str(element_definition) , text_type = 'ERROR  ')
			if breakONerror:
				self.abort_test()
	
	def move_cursor_to_the_object(self, current_object = None):
	#(С!G) Наводим курсор мыши на объект
		driver = self.driver
		if current_object != None:
			hover = ActionChains(driver).move_to_element(current_object)
			hover.perform()
			time.sleep(0.2) # потому, что следующее действие доступно быстрее чем может быть выполнено
		else:
			loger.file_log(text = 'You can\'t move mouse to the None object' , text_type = 'ERROR  ')

	def get_tab_name(self, time_out = 120):
	# (СG) метод определяющий текст вкладки браузера.
		driver = self.driver
		step_await = self.wait_for_results()
		result = None
		while True:
			method_status = False
			try:
				result = driver.title
			except:
				pass
			if type(result) == str:
				method_status = True
			if method_status:
				break
			if self.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
				loger.file_log(text = 'Time is out, can\'t define tab name' , text_type = 'ERROR  ')
				break
		return result
	
	def definition_current_url(self, breakONerror = False, time_out = 120):
	# определяет текущий URL браузера
		driver = self.driver
		step_await = self.wait_for_results()
		while True:
			method_status = False
			try:
				url =  driver.current_url
				method_status = True
			except Exception as ex:
				pass
			if method_status:
				break
			if self.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
				loger.file_log(text = 'Time is out, can\'t define URL' , text_type = 'ERROR  ')
				break
		if method_status:
			return url
		else:
			if breakONerror:
				self.abort_test()
			else:
				return None
	
	def choose_from_dropdown(self, dropdown_element = None, current_item = None):
	# (C!)выбирает конкретное значение для из выпадающего списка. выпадающий список передается как элемент из pageElements, а значение как строковое наименование
	# пока не готово, проверить что нигде не использую и УДАЛИТЬ!!!
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
		method_status = False
		inner_index = 2
		current_elems = []
		step_await = self.wait_for_results()
		# оперделяем какой URL до изменения страницы (какая страница)
		while True:
			try:
				old_url = self.definition_current_url()
				# header_befor_switch = self.get_header_text
				if type(old_url) is str:
					break
			except:
				pass
			if self.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
				self.close_browser
				loger.file_log(text = 'Can\'t find Header text from this page', text_type = 'ERROR  ')
				if self.breakONerror == True:
					self.abort_test()
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
		step_await = self.wait_for_results()
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
			if self.wait_for_results (time_data = step_await, time_out = timeOut).get('result'):
				self.close_browser
				loger.file_log(text = 'Can\'t choose your\'s menu item', text_type = 'ERROR  ')
				break
		# проверка на то, что нужная страница открыта (для этого, url должен измениться)
		step_await = self.wait_for_results()
		while True:
			new_url = self.definition_current_url()
			if new_url != old_url:
				loger.file_log(text = 'West menu items switching was done', text_type = 'SUCCESS')
				method_status = True
				break
			if self.wait_for_results (time_data = step_await, time_out = timeOut).get('result'):
				loger.file_log(text = 'Can\'t choose next item  from west menu', text_type = 'ERROR  ')
				if breakONerror is True:
					self.close_browser		
					break
				break
		return method_status

	def top_menu_navigation(self, tab_name = None, timeOut = 20, new_elemets_status = False):
	#(С!) навигация по табам (вкладки вверху, активные выделяются зеленым)
		# ищем элементы\табы на странице (старые и новые) условием выхода из цикла будет нахождение любых или тайм аут
		timer_index = 0
		tabs_status = {} # словарь с найденными типаме меню: старое и новое
		elems = [] #текстовые значения, присутствующих вкладок\кнопок на странице
		while True:
			# старое меню, получаем названия вкладок (если на странице есть аналогичные кнопки с день, месяц, то они тоже тут)
			try:
				old_elems = self.elements_list(search_type = None, mask = 'span[id*=-tab] > span[id$=btnInnerEl]', timeOut = 1)
				if old_elems.get('count') != None:
					tabs_status['old_elems'] = old_elems.get('elements')
			except:
				pass
			# новое меню, получаем значения вкладок
			if new_elemets_status == False: #когда Даши уйдут на бой оставим только: else
				try:
					new_elems = self.elements_list(search_type = None, mask = 'span[class=x-tab-inner]', timeOut = 1)
					if new_elems.get('count') != None:
						tabs_status['new_elems'] = new_elems.get('elements')
				except:
					pass
			else:
			# ищем все табы (новый алгоритм)
				try:
					new_elems = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'data-boundview, \'-tabbar-tabbar-mode-\'')
					if new_elems.get('count') != None:
						tabs_status['new_elems'] = new_elems.get('elements')
				except:
					pass
			# если хоть что-то нашли выходим из поиска элементов
			if len(tabs_status) != 0:
				break
			
			if timer_index >= timeOut:
				loger.file_log(text = 'No tab\'s navigation buttons at page', text_type = 'ERROR  ')
				elems = []
				break
			timer_index += 1
		
		# собираем общий список найденных вкладок, обходя результат в цикле
		for tab_name_was_found in tabs_status.keys():
			elems += tabs_status.get(tab_name_was_found)

		# тут подумать и как-нить правильнее переделать
		if tab_name != None and len(elems) != 0:
			for el in elems:
				try:
					if el.is_displayed() and str(el.text) == str(tab_name):
						try:
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
	# получаем заголовок страницы и id заголовка (у дашбордов нет названия)
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
		page = self.get_header_text
		step_await = self.wait_for_results()
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
			if self.wait_for_results (time_data = step_await, time_out = time_out).get('result'):		
				loger.file_log(text = 'Can\'t found counter of the items', text_type = 'ERROR  ')
				result.append(None)
				result.append(page)
				break			
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

	def identity_of_the_child_to_the_parent(self, parent = None, child = None):
	# (C!G) определяем принадлежит ли дочерний объект родительскому. оба значения должны передаваться как WebDriver объекты
		result = {}
		# ищем всех потомков от родительского объекта
		try:
			children = parent.find_elements_by_tag_name('*')
			if child in children:
				result['result'] = True
			else:
				result['result'] = False
		except Exception as ex:
			loger.file_log(text = 'Can\'t get children for parent object. Check method: tools.identity_of_the_child_to_the_parent', text_type = 'ERROR  ')
			result['result'] = False		
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
	
	@property
	def move_to_new_active_tab(self):
	# переход на новую вновь открытую вкладку браузера
		driver = self.driver
		driver.switch_to_window(driver.window_handles[-1])

#-------------------------------------------------------------------------------------------------
	def switch_env(self, selected_element = None, server_name = 'sitecw2.webdev.uiscom.ru',  breakONerror = True, time_out = 120):
	# (!)изменяет тестовый сервер в личном кабинете
		method_status = False
		# driver = self.driver
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
					method_status = True
					break
				if time_index >= 20 and breakONerror is True:
					self.close_browser
					loger.file_log(text = 'Can not open necessary URL', text_type = 'ERROR  ')
					loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
					sys.exit()			
				time.sleep(1)
				time_index += 1
			return	method_status

	def login_to(self, url = None, user = None, password = None, breakONerror = True, time_out = 120):
	# логин в систему
		method_status = False		
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
		# проверка на то, что открыто именно то, что мы и ожидали. в заголовке вкладки появиться должно брендирование
		step_await = self.wait_for_results()
		brend_names = ['UIS','CoMagic']
		while True:
			method_status = False
			for brand in brend_names:
				if brand in self.get_tab_name(time_out = 2):
					loger.file_log(text = 'Open page done. URL is {}'.format(str(url)), text_type = 'SUCCESS')
					method_status = True
			if method_status:
				break
			if self.wait_for_results (time_data = step_await, time_out = time_out).get('result'):		
				loger.file_log(text = 'Can\'t found counter of the items', text_type = 'ERROR  ')
				break
		if method_status:
			pass
		else:
			loger.file_log(text = 'Can not open necessary URL', text_type = 'ERROR  ')
			if breakONerror:
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				self.abort_test()


	def login_to_system(self, url = None, user = None, password = None, breakONerror = True, system_is = None):
	# логин в системы интеграции и лк боя
		try:
			self.goto(url, breakONerror)
		except Exception as ex:
			loger.file_log(text = 'Can not open URL' + str(ex) + '\n' + 'URL = ' + str(url) + '\n', text_type = 'ERROR  ')
			if breakONerror is True:
				self.close_browser
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
		if system_is == 'Comagic':
			try:
				self.change_value(element_definition = lk_elements.INPUT('login_comagic'), text = user)
				self.change_value(element_definition = lk_elements.INPUT('password_comagic'), text = password)
				self.click_element(element_definition = lk_elements.BUTTON('btn_login_comagic'))
			except Exception as ex:
				loger.file_log(text = 'Can not input data (user name or password)', text_type = 'ERROR  ')
				if breakONerror is True:
					self.close_browser
					loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
					sys.exit()
			# TODO: сделать проверку на то, что открыто именно то, что мы и ожидали. по умолчанию открывается - if header[0] == 'Авторизация':
		elif system_is == 'Yandex':
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
				# TODO: сделать проверку на то, что открыто именно то, что мы и ожидали. по умолчанию открывается - if header[0] == 'Авторизация':
		elif system_is == 'Google':
			try:
				self.change_value(element_definition = lk_elements.INPUT('login_google'), text = user)
				self.click_element(element_definition = lk_elements.BUTTON('btn_next_login_google'))
				self.change_value(element_definition = lk_elements.INPUT('password_google'), text = password)
				self.click_element(element_definition = lk_elements.BUTTON('btn_next_pwd_google'))
			except Exception as ex:
				loger.file_log(text = 'Can not input data (user name or password)', text_type = 'ERROR  ')
				if breakONerror is True:
					self.close_browser
					loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
					sys.exit()
				# TODO: сделать проверку на то, что открыто именно то, что мы и ожидали. по умолчанию открывается - if header[0] == 'Google AdWords':

	def change_top_menu_values(self, menu_item = 'Аккаунт'):
	# (С!G) выбор опций верхнего меню
	# формируем список доступных меню, {'название':}
		menu_values = {'Аккаунт':1,'Сервисы и Статистика':2, 'Управление пользователями':3, 'Сменить пароль':4, 'Добавить наблюдателя ':5, 'Выйти':6}
	# определяем какое значение выставлено сейчас

	def login_toLK_by_admin(self, adm_login = 'login', adm_pass = 'pass', user_id = '1103', stend_url = 'url', timeOut = 120, login_name_for_user = 'Администратор',breakONerror = False):
	# выполняет логин через админку, не проверяет что логин выполнен
		method_result = {} # то что будет возвращено по завершение выполнения метода
		filtering_type = 'ID' # параметр, по которому будет осуществляться фильтрация пользователей (пока это ID)
		# login_name_for_user = 'Admin for testing'
		# login_name_for_user = 'Администратор' #пользователь клиента под которым мы выполняем вход
		method_status = True #статус выполнения метода
		error_text = 'Can\'t find icon: Clients' #текст для ошибок, которые используются во время ожидания
		# открываем админку соответствующего стенда
		self.goto(url = stend_url)
		# находим поля ввода и кнопку логина на форме
		login_input = self.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'lf-textfield-login\'')
		pass_input = self.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'lf-textfield-password\'')
		login_btn = self.elements_list(object_type = 'tbody', search_type = 'contains', mask = 'class, \'x-btn-small x-btn-icon-small-left\'')
		# проверяем что эллементов не больше 3-х (по доному на тип)
		try:
			if sum([int(login_input.get('count')),int( pass_input.get('count')),int(login_btn.get('count'))]) != 3:
				method_status = False
		except:
			method_status = False

		# вводим логин пароль админа и жмем кнопку 
		if method_status:
			self.change_value(element_definition = login_input.get('elements')[0], text = adm_login)
			self.change_value(element_definition = pass_input.get('elements')[0], text = adm_pass)
			self.click_element(element_definition = login_btn.get('elements')[0])
		else:
			loger.file_log(text = 'Count objects that were found is wrong. Check objeckts definition in method: login_toLK_by_admin' , text_type = 'ERROR  ')
		# ожидаем в течении таймаута, появление иконки: Клиенты (в виде папки)
		time_index = 0
		while True:
			method_status = False
			# находим все иконки на странице 
			icons_tabs = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'class, \'ux-desktop-shortcut-text\'')
			# ищем клиентов и если находим то нажимаем
			try:
				if int(icons_tabs.get('count')) >= 1:
					for clients in icons_tabs.get('elements'):
						if clients.text == 'Клиенты':
							self.click_element(element_definition = clients)
							method_status = True
							break
			except:
				loger.file_log(text = 'Can\'t find icon: Clients', text_type = 'ERROR  ')
			# если нашли и нажали на иконку Клиенты, то выходим из цикла
			if method_status:
				break
			if time_index >= timeOut:
				self.close_browser
				loger.file_log(text = 'Can\'t find icon: Clients', text_type = 'ERROR  ')
				if breakONerror is True:
					loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
					sys.exit()
			time.sleep(1)
			time_index += 1
		# ищем иконку смайла: Клиенты, и нажимаем
		if method_status:
			time_index = 0
			while True:
				method_status = False
				# ищем текст под иконкой смайлика
				cliens_menu = self.elements_list(object_type = 'li', search_type = 'contains', mask = 'id, \'apps-window-shortcut\'')
				if int(cliens_menu.get('count')) >= 1:
					for item_menu in cliens_menu.get('elements'):
						if item_menu.text == 'Клиенты':
							self.click_element(element_definition = item_menu)
							method_status = True
							break
				if method_status:
					break
				if time_index >= timeOut:
					self.close_browser
					loger.file_log(text = 'Can\'t find icon: Clients', text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						sys.exit()
				time.sleep(1)
				time_index += 1
		# находим вкладку ID и наводим на неё курсор что бы получить иконку выпадающего меню
		if method_status:
			parent_object = None
			time_index = 0
			while True:
				method_status = False
				# ищем все вкладке в таблице: Клиенты
				cliens_menu = self.elements_list(object_type = 'td', search_type = 'contains', mask = 'class, \'x-grid3-hd x-grid3-cell x-grid3-td-\'')
				if type(cliens_menu.get('count')) == int:
					for item_menu in cliens_menu.get('elements'):
						# как только находим нужный столбик наводим курсор, что б получить иконку выпадающего меню
						if str(item_menu.text) == str(filtering_type):
							id_tab = item_menu
							self.move_cursor_to_the_object(current_object = item_menu)
							method_status = True
							parent_object = item_menu
							break
				if method_status:
					break
				if time_index >= timeOut:
					self.close_browser
					loger.file_log(text = 'Can\'t find icon: Clients', text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						sys.exit()
				time.sleep(1)
				time_index += 1
		# находим и нажимаем выпадающее меню (стрелка\треугольнк вниз)
		if method_status:
			time_index = 0
			while True:
				method_status = False
				# ищем все вкладке в таблице: Клиенты
				cliens_menu = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'class, \'x-grid3-hd-btn\'')
				if int(cliens_menu.get('count')) >= 1:
					for item_menu in cliens_menu.get('elements'):
						# как только находим нужный объект (треугольник) проверяем что он в нужной шапке столбика находится
						if self.identity_of_the_child_to_the_parent(parent = parent_object, child = item_menu):
							# нажимаем на этот элемент
							self.click_element(element_definition = item_menu)
							method_status = True
							break
				if method_status:
					break
				if time_index >= timeOut:
					self.close_browser
					loger.file_log(text = 'Can\'t find icon: Clients', text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						sys.exit()
				time.sleep(1)
				time_index += 1
		# ищем строчку с надписью: Фильтр, и наводим курсор, что бы получить меню
		if method_status:
			time_index = 0
			while True:
				method_status = False
				# ищем все строчки в открывшемся меню
				cliens_menu = self.elements_list(object_type = 'li', search_type = 'contains', mask = 'id, \'x-menu-el-ext-comp-\'')
				if int(cliens_menu.get('count')) >= 1:
					for item_menu in cliens_menu.get('elements'):
						# как только находим строку в меню с текстом: Фильтр, наводим курсор
						if str(item_menu.text) == 'Фильтр':
							self.move_cursor_to_the_object(current_object = item_menu)
							method_status = True
							parent_object = item_menu
							break
				if method_status:
					break
				if time_index >= timeOut:
					loger.file_log(text = 'Can\'t find icon: Clients', text_type = 'ERROR  ')
					break
					if breakONerror is True:
						self.close_browser
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						sys.exit()
				time.sleep(1)
				time_index += 1
		# находим и вводим в поле со значением: равно(=) нужный id клиента
		if method_status:
			time_index = 0
			while True:
				method_status = False
				# ищем все строчки в открывшемся меню картинку\иконку равно
				field_with_eaqul_icon = self.elements_list(object_type = 'img', search_type = 'contains', mask = 'class, \'x-menu-item-icon ux-rangemenu-eq\'')
				if int(field_with_eaqul_icon.get('count')) == 1:
					# определяем родительский объект
					parent_object = self.get_parent(current_object = field_with_eaqul_icon.get('elements')[0])
					# находим все поля для ввода данных
					input_fields = self.elements_list(object_type = 'input', search_type = 'contains', mask = 'type, \'text\'')
					# обходим все найденные эллементы и находим тот, который принадлежит родительскому
					if type(input_fields.get('count')) == int:
						for field in input_fields.get('elements'):
						# ищем поле ввода именно для для значения равно					
							if  self.identity_of_the_child_to_the_parent(parent = parent_object, child = field).get('result'):
								self.change_value(element_definition = field, text = user_id, breakONerror = False)
								method_status = True
								break
				if method_status:
					break
				if time_index >= timeOut:
					loger.file_log(text = 'Can\'t find icon: Clients', text_type = 'ERROR  ')
					if breakONerror is True:
						self.close_browser
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						sys.exit()
					break
				time.sleep(1)
				time_index += 1
		# закрываем все выпадающие окна, нажатием на header окна Клиентов (если таковой не найден, то долго будет ждать)
		if method_status:
			block_header = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'class, \'x-window-header x-window-header-noborder x-unselectable x-panel-icon startmenu-apps-icon x-window-draggable\'')
			if type(block_header.get('count')) == int:
				self.click_element(element_definition = block_header.get('elements')[0])
		if method_status:
			time_index = 0
			while True:
				method_status = False
				client_ids = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'class, \'x-grid3-cell-inner x-grid3-\'')
				for client_name in client_ids.get('elements'):
					if client_name.text == str(user_id):
						# находим нужного клиента, узнаем его тип и вызываем контекстное меню
						# находим родительский объект от id поля
						parent_line_object = self.get_parent(self.get_parent(client_name))
						type_filds  = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'class, \'x-grid3-cell-inner x-grid3-col-12\'')
						for type_field in type_filds.get('elements'):
							if self.identity_of_the_child_to_the_parent(parent = parent_line_object, child = type_field).get('result'):
								method_result['client_type'] =  type_field.text
						try:
							method_result['client_id'] = client_name.text
							print('клиент: {}'.format(client_name.text))
							ActionChains(self.driver).move_to_element(client_name)
							ActionChains(self.driver).context_click(client_name).perform()
							method_status = True
							break
						except Exception as ex:
							loger.file_log(text = 'Can\'t open context menu. Check that you have current defenition of the items in the clients table', text_type = 'ERROR  ')
							if breakONerror is True:
								self.close_browser
								loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
								sys.exit()
				if method_status:
					break
				if time_index >= timeOut:
					self.close_browser
					loger.file_log(text = 'Can\'t find icon: Clients', text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						sys.exit()
				time.sleep(1)
				time_index += 1
		# нажимаем на кнопку: перейти в приложение
		if method_status:
			method_status = False
			dd_menus = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'class, \'x-menu-item-text\'')
			if dd_menus.get('count') >= 1:
				for dd_move_to in dd_menus.get('elements'):
					if dd_move_to.text == 'Перейти в клиентское приложение':
						self.click_element(element_definition = dd_move_to)
						method_status = True
						break
		# ожидаем появления менюшки пользователя: Выберите пользователя
		if method_status:
			time_index = 0
			while True:
				method_status = False
				# ищем полное, текст + иконка выпадашка, поле где указано наименование пользователя
				all_users_field = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'class, \'x-panel-body x-panel-body-noheader x-panel-body-noborder\'')
				if all_users_field.get('count') == 1:
					parent_field = all_users_field.get('elements')[0]
					# ищем текстовое поле и получаем текущее значение
					text_fields = self.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'ext-comp-\'')
					if int(text_fields.get('count')) >= 1:
						for text_fied in text_fields.get('elements'):
							if self.identity_of_the_child_to_the_parent(parent = parent_field, child = text_fied).get('result'):
								# проверяем значение пользователя под которым хотим войти и если не совпадает с: login_name_for_user, меняем
								# если значение еще не прогрузилось (длинна текста меньше нуля), то ничего не делаем
								if len(text_fied.get_attribute('value')) >= 1:
									if str(text_fied.get_attribute('value')) == str(login_name_for_user):
										# находим и нажимаем кнопку: Перейти
										move_to_btn = self.elements_list(object_type = 'button', search_type = 'contains', mask = 'class, \' x-btn-text\'')
										if type(move_to_btn.get('count')) == int:
											for btn_move_to in move_to_btn.get('elements'):
												if btn_move_to.text == 'Перейти':
													self.click_element(element_definition = btn_move_to)
													method_status = True
													break
									# если нет то нужно выбрать соответствующее значение - тут надо доделать
									else:
										# ищем все элементы - стрелки, для открытия выпадающего списка
										all_arrow_elements = self.elements_list(object_type = 'img', search_type = 'contains', mask = 'class, \'x-form-trigger x-form-arrow-trigger\'')
										# в цикле ищем элемент с родителем от окна с текстом и как находим нажимаем что бы полусить список значений
										if type(all_arrow_elements.get('count')) == int:
											for  arrow_element in all_arrow_elements.get('elements'):
												if self.identity_of_the_child_to_the_parent(parent = parent_field, child = arrow_element).get('result'):
													self.click_element(element_definition = arrow_element)
													break
										# ищем все элементы открывшегося списка с именами
										list_all_users_names = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'class, \'x-combo-list-item\'')
										# формируем словарь {текст:объект} со всеми значениями списка
										if type(list_all_users_names.get('count')) == int:
											names_list = {}
											for current_name in list_all_users_names.get('elements'):
												try:
													names_list[current_name.text] = current_name
												except:
													pass
											# проверяем есть ли пользователь в списке достуных имен клиентов 
											if login_name_for_user in names_list.keys():
												self.page_scrolling_to_the_element(page_object = names_list.get(login_name_for_user))
												self.click_element(element_definition = names_list.get(login_name_for_user))
											# находим кнопку: Перейти и нажимаем
												move_to_btn = self.elements_list(object_type = 'button', search_type = 'contains', mask = 'class, \' x-btn-text\'')
												if type(move_to_btn.get('count')) == int:
													for btn_move_to in move_to_btn.get('elements'):
														if btn_move_to.text == 'Перейти':
															self.click_element(element_definition = btn_move_to)
															method_status = True
															break
											else:
												error_text = 'No such user name for Client\'s'		
								else:
									pass
				if method_status:
					break
				if time_index >= timeOut:
					self.close_browser
					loger.file_log(text = error_text, text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						sys.exit()
				time.sleep(1)
				time_index += 1
		# переходим на вновь открытую вкладку и проверяем, что мы перешли
		if method_status:
			# ожидаем пока вкладок в браузере станет две
			time_index = 0
			while True:
				method_status = False
				# предполагаем, что изначально у нас одно окно, по этому ожидаем, когда окон станет два. И как только находим такое, то выходим из цикла
				if len(self.driver.window_handles) == 2:
					method_status = True
				if method_status:
					break
				if time_index >= timeOut:
					self.close_browser
					loger.file_log(text = 'Count of the browser windows not eaqul two', text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						sys.exit()
				time.sleep(1)
				time_index += 1

			self.move_to_new_active_tab
			new_url = str(self.definition_current_url()) + '?testenv=1'
			self.goto(new_url)
			method_status = True
		return method_result

	def opening_client_from_agent_lk(self, agent_client_id = None, user_for_login = None, timeOut = 120, breakONerror = False):
		method_status = True
	# (C!)открываем Личный Кабинет клиента через Агентский ЛК/ предполагаем, что ЛК агента уже открыт
		# проверяем на каком листе находимся и если необходимо то переходим
		result = {}
		time_index = 0
		while True:
			method_status = False
			try:
				# если вкладка корретная то переходим дальше
				if self.get_header_text[0] == 'Мои клиенты':
					method_status = True
				else:
					# если удалось определить вкладку и она не: Мои клиенты, по пробуем перейти на: Мои клиенты
					# проверка нужна потому, что тип может быть и None
					if type(self.get_header_text[0]) == str:
						self.lk_sidemenu_navigation(item_menu = ['Мои клиенты'])
			except:
				pass
			if method_status:
				break
			if time_index >= timeOut:
				loger.file_log(text = 'Can\'t find page. Method: opening_client_from_agent_lk', text_type = 'ERROR  ')
				if breakONerror is True:
					loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
					sys.exit()
			time.sleep(1)
			time_index += 1
		# получаем список всех доступных клиентов {}
		time_index = 0
		while True:
			method_status = False
			try:
				# ищем общие родительские объекты: строки - клиенты
				agent_clients = self.elements_list(object_type = 'table',  search_type = 'contains',  mask = 'id, \'agentsapps-page-tableview\'', timeOut = 1)
				if type(agent_clients.get('count')) == int:
					# для каждого клиента агента определяем id и название и иконку для последующего перехода
					for current_client in agent_clients.get('elements'):
						client_credentials = {}
						# id конкретного клиента
						id_list = self.elements_list(object_type = 'td',  search_type = 'contains',  mask = 'data-columnid, \'agentsapps-page-gridcolumn-id\'')
						if type(id_list.get('count')) == int:
							for current_id in id_list.get('elements'):
								if self.identity_of_the_child_to_the_parent(parent = current_client, child = current_id).get('result'):
									client_credentials['client_object'] = current_client
									break
						# имя клиента
						client_names_list = self.elements_list(object_type = 'td',  search_type = 'contains',  mask = 'data-columnid, \'agentsapps-page-cm-namecolumn-name-\'')
						# client_names_list = self.elements_list(object_type = 'div',  search_type = 'contains',  mask = 'class, \'x-grid-cell-inner\'')
						if type(client_names_list.get('count')) == int:
							for current_name in client_names_list.get('elements'):
								if self.identity_of_the_child_to_the_parent(parent = current_client, child = current_name).get('result'):
									client_credentials['client_name'] = current_name.text
									break
						# иконка для перехода в ЛК клиента
						move_icons = self.elements_list(object_type = 'img',  search_type = 'contains',  mask = 'data-qtip-ownercmp, \'agentsapps-page-ul-actioncolumn-id-\'')
						if type(move_icons.get('count')) == int:
							for current_icon in move_icons.get('elements'):
								if self.identity_of_the_child_to_the_parent(parent = current_client, child = current_icon).get('result'):
									client_credentials['icon'] = current_icon
									break
						# если найдены все параметры, то выходим из поиска со статусом True
						if len(client_credentials) >= 2:
							result[current_id.text] = client_credentials
							method_status = True			
			except Exception as ex:
				pass
			if method_status:
				break
			if time_index >= timeOut:
				loger.file_log(text = 'Can\'t find client\'s. Method: opening_client_from_agent_lk', text_type = 'ERROR  ')
				if breakONerror is True:
					loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
					sys.exit()
			time.sleep(1)
			time_index += 1
		# нажимаю на иконку клиента для заданного id
		self.click_element(element_definition = result.get(agent_client_id).get('icon'))
		# ожидаем появление меню для выбора конкретного пользователя под кем будет выполнен вход
		time_index = 0
		while True:
			method_status = False
			user_names = self.elements_list(object_type = 'input',  search_type = 'contains',  mask = 'id, \'agentsapps-page-ul-combobox-user_id-\'')
			if type(user_names.get('count')) == int:
				# проверяем подсвеченное имя и если оно совпадает с заданным, то ничего не делаем если нет, то меняем 
				for user_name in user_names.get('elements'):
					if user_name.get_attribute('value') == user_for_login:
						method_status = True
						break
					else:
						# находим общего родителя для текста и кнопки открывающей выпадающий список пользователей
						parent = self.get_parent(current_object = self.get_parent(current_object = user_name))
						# находим все кнопки на странице для открытия выпадающих списков
						drop_down_buttons =  self.elements_list(object_type = 'div',  search_type = 'contains',  mask = 'id, \'-trigger-picker\'')
						if type(drop_down_buttons.get('count')) == int:
							for dd_button in drop_down_buttons.get('elements'):
								if self.identity_of_the_child_to_the_parent(parent = parent, child = dd_button).get('result'):
									# открываем список нажатием на подходящюю кнопку
									self.click_element(element_definition = dd_button)					         
									break
						# получаем список всех доступных пользователей (в появившемся списке)
						users_list_dd = self.elements_list(object_type = 'div',  search_type = 'contains',  mask = 'data-boundview, \'agentsapps-page-ul-boundlist-\'')
						if type(users_list_dd.get('count')) == int:
							# перебираем каждого пользователя сравнивая с заданным (подумать, можноли блок этот переделать)
							while len(users_list_dd.get('elements')) != 0:
								item = users_list_dd.get('elements').pop()
								if str(user_for_login) == str(item.text):
									self.click_element(element_definition = item)
									method_status = True
									break
						# если пройдя по всем пользователям, нужного не нашли то выходим из цикла (если пользователя НЕТ, то будет несколько записей в ЛОГ файле)
						if len(users_list_dd.get('elements')) == 0 and method_status == False:
							loger.file_log(text = 'Can\'t find user:\t{}. Method: opening_client_from_agent_lk'.format(user_for_login), text_type = 'ERROR  ')
							break
					# ищем кнопку: Перейти и нажимаем на неё
				if method_status:
					login_btns = self.elements_list(object_type = 'span',  search_type = 'contains',  mask = 'id, \'agentsapps-page-ul-mainbutton-log_in_as_app-\'')
					if type(login_btns.get('count')) == int:
						for login_btn in login_btns.get('elements'):
							if 'btnInnerEl' in login_btn.get_attribute('id'):
								self.click_element(element_definition = login_btn)
								method_status = True
								break							
			if method_status:
				break
			if time_index >= timeOut:
				loger.file_log(text = 'Can\'t find client\'s. Method: opening_client_from_agent_lk', text_type = 'ERROR  ')
				break
				if breakONerror is True:
					loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
					sys.exit()
			time.sleep(1)
			time_index += 1
		# ожидаем загрузки страницы ЛК клиента (загрузку определяем по наличию)
		time_index = 0
		while True:
			method_status = False
			top_menu_user_name = self.elements_list(object_type = 'span',  search_type = 'contains',  mask = 'id, \'main-actionbutton-username_button-\'')
			if type(top_menu_user_name.get('count')) == int:
				for item in top_menu_user_name.get('elements'):
					if item.get_attribute('data-ref') == 'btnInnerEl':
						if item.text == user_for_login:
							loger.file_log(text = 'Agent\'s clint(id): {},\twas login to the personal account with User:{}'.format(agent_client_id, user_for_login), text_type = 'SUCCESS')
							method_status = True
							break
			if method_status:
				break
			if time_index >= timeOut:
				loger.file_log(text = 'Can\'t find client\'s. Method: opening_client_from_agent_lk', text_type = 'ERROR  ')
				break
				if breakONerror is True:
					loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
					sys.exit()
			time.sleep(1)
			time_index += 1
		return result

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
	# (G!С) выбираем график показа виджет обратного звонка/ значение None соответствует любое значение
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


