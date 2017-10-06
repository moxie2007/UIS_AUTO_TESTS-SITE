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

lk_elements  = pageElements.LK()

class User_config():
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
	# (!) это может и не работать, нужно отладить после тестов да и вообще, этому тут не место :-)
			try:
				client = APIClient('http://testrail.uiscom.ru/')
				# тут нужен логин и пароль для доступа в тестрейл
				client.user = None
				client.password = None
				return self.client
			except Exception as ex:
				loger.file_log(text = 'Did not initialization testrail' , text_type = 'ERROR  ')

	def init_browser(self, product_type = 'ch'):
	# открывает объект Браузера, доделать выбор браузера и добавить настройку полноэкранности
		env = {'ch': webdriver.Chrome, 'ff': webdriver.Firefox}
		try:
			self.driver = env.get(product_type)()
			self.driver.maximize_window()
			print(dir(webdriver))
			return self.driver
		except Exception as ex:
			# print(ex)
			loger.file_log(text = 'Did not initialization Browser' , text_type = 'ERROR  ')

	def close_browser(self):
	# закрывает открытый объект Браузера 
		if self.driver:
			self.driver.quit()
			self.driver = None

	def sleep_function(self, timeout = 120):
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
			# driver.execute_script("return document.title").assertTrue(type(result) == unicode or type(result) == str,"The type of the result is " + str(type(result))).assertEqual("XHTML Test Page", result)
			# driver.execute_script(command)
		except Exception as ex:
			loger.file_log(text = 'Can\'t do this (' + str(command) + ').\n command error is:' + str(ex), text_type = 'ERROR  ')
			result = None
			if breakONerror is True:
				self.close_browser()
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

	def page_scrolling_to_the_element (self, page_object = None):
	# (C) перемещает отображаемую часть страницы к элементу. в метод передается объект webdriver
		driver = self.driver
		if page_object != None:
			try:
				driver.execute_script("return arguments[0].scrollIntoView();", page_object)
			except Exception as ex:
				print(ex)
	
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
	# (C) выполняет нажатие на эллемент
		try:
			current_object = self.displayed_element(element_definition = element_definition, timeOut = timeOut)
			if current_object[0] is True:
				self.page_scrolling_to_the_element(page_object = current_object[2])
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
	# (C) выполняет изменение значения в эллементе (пока, без перемещения курсора к эллементу)
		try:
			current_object = self.displayed_element(element_definition = element_definition)
			if current_object[0] is True:
				current_object[2].click()
				current_object[2].clear()
				current_object[2].send_keys(str(text))
		except Exception as ex:
			# print(ex)
			loger.file_log(text = 'can not change data in the element ' + str(element_definition) , text_type = 'ERROR  ')
			# print('test')
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
				self.close_browser()
				loger.file_log(text = 'Can\'t find Header text from this page', text_type = 'ERROR  ')
				if self.breakONerror == True:
					self.abort_test()
				# break
			time.sleep(1)
			time_index += 1
		# проверяем не открыто ли уже головное меню (например: Общие отчёты, Список обращений, Служебные)
		try:
			mask = 'class, \'x-grid-tree-node-expanded  x-grid-row\''
			elem_list9 = self.elements_list(object_type = 'tr', search_type = 'contains', mask = mask, timeOut = timeOut)[1]
			for t in elem_list9:
				if  t.text == item_menu[0]:
					inner_index += 1
					item_menu.remove(item_menu[0])
		except Exception as ex:
			print(ex)
		time_index = 0
		while True: 
		# ищем пункт меню котовый к нажатию
			mask = 'class, \' x-grid-cell-treecolumn x-grid-cell-first x-grid-cell-last x-unselectable x-grid-cell-treecolumn ul-tree-node-depth-' + str(inner_index) + '\''
			elem_list = self.elements_list(object_type = 'td', search_type = 'contains', mask = mask, timeOut = timeOut)[1]
			# проверка, что искомый объект один, формируя список
			for elem in elem_list:
				if elem.text == item_menu[0]:
					current_elems.append(elem)
			if len(current_elems) == 1:
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
			if len(item_menu) == 0:
				break
			if time_index >= timeOut:
				self.close_browser()
				loger.file_log(text = 'Can\'t choose your\'s menu item', text_type = 'ERROR  ')
				break
			time.sleep(1)
			time_index += 1
		# проверка на то, что нужная страница открыта (для этого, текст заголовка должен быть изменен)
		time_index = 0
		while True:
			header_after_switch = self.get_header_text
			if header_befor_switch[1] != header_after_switch[1]:
				loger.file_log(text = 'Switching was done from ' + str(header_befor_switch[0]) + ' to ' + str(header_after_switch[0]), text_type = 'SUCCESS')
				break
			if time_index >= timeOut:
				self.close_browser()
				loger.file_log(text = 'Can\'t choose next item  from west menu, the page still: ' + str(header_after_switch[0]), text_type = 'ERROR  ')
				break
			time.sleep(1)
			time_index += 1

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
	def get_active_page_in_list(self):
	# (C) находит активную страницу (это навигация по: В начало,1,2,дальше), по обводке вокруг значения
	# больше одного значения по логике работы метода, быть не должно
		result = [[],{}]
		elems = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'class, \'x-btn x-btn-ul-usual-without-border x-unselectable x-box-item x-toolbar-item x-btn-ul-usual-medium x-btn-pressed\'')
		for elem in elems[1]:
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
			if empty_list[0] != None and empty_list[1][0].text == 'Нет записей':
				result.append(0)
				result.append(page)
				break
			# проверяем видимы ли найденные элементы
			for item in elems[1]:
				if '-page-tbtext-displayItem-' in item.get_attribute('id') and self.displayed_element(element_definition = item, timeOut = 1)[0]:
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
	# (!)изменяет тестовый сервер в личном кабинете
		driver = self.driver
		url_action_start = self.definition_current_url()
		# ищем окно с текущим сайтом (должно быть одно)
		site_dropdown = self.elements_list(object_type = 'input', mask = 'class, \'x-form-field x-form-text x-form-text-cm-siteselector\'')
		if site_dropdown[0] != 1:
			loger.file_log(text = 'Were found ' + str(site_dropdown[0]) + ' element\'s. It\'s wrong', text_type = 'ERROR  ')
			if self.breakONerror == True:
				self.abort_test()
		else:	
			# открываем список доступных сайтво
			self.click_element(element_definition = site_dropdown[1][0], breakONerror = True) 
			obj_servers_list = self.elements_list(object_type = 'li', mask = 'class, \'x-boundlist-item\'')
			if len(obj_servers_list[1]) > 0:
				for current_server_name in obj_servers_list[1]:
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
	# (C) поиск записай на странице выбирает формирует список объектов из элементов в таблице шаблонов ответа, в списке только отображенные на странице элементы
		return self.elements_list(object_type = 'table', search_type = 'contains', mask = 'id, \'commonsettings-page-tableview-\'')

	def general_settings_add_template(self, template_name = None, timeOut = 120):
	# (C!) добавление нового шаблона, успешность проверяется по изменению количества записей на странице (в разработке!!!)
		# получаем количество шаблонов
		before_adding_template_values_count = self.get_total_list_values_count()[0]
		# добавляем новый шаблон
		if template_name != None:
			# ищем поле для ввода (поиск нужен потому, что все эллементы кроме страницы логина динамические)
			elems = self.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'textfield-\'')
			print(elems[0])
			for elem in elems[1]:
				try:
					if elem.get_attribute('data-ref') == 'inputEl':
						self.change_value(element_definition = elem, text = template_name)
				except Exception as ex:
					loger.file_log(text = 'Can\'t type the template name', text_type = 'ERROR  ')
			# нажимаем кнопку добавить
			# elems = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'ul-mainbutton\'')	
			# print(elems)	
			elems_test = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'class, \'x-btn x-unselectable x-box-item x-btn-ul-main-medium\'')
			# elems_test = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'commonsettings-page-ul-mainbutton-\'')
			elems_test[1][0].click()
		# проверяем, что значение общего количества шаблонов изменилось
		time_index = 0
		while True:
			value_of_teamplates_after_chang = self.get_total_list_values_count()[0]
			if int(value_of_teamplates_after_chang) - int(before_adding_template_values_count) == 1:
				break
			if time_index >= timeOut:
				loger.file_log(text = 'Templates counter does not correct. It is: ' + str(value_of_teamplates_after_chang), text_type = 'ERROR  ')
				break			
			time.sleep(1)
			time_index += 1	

	def general_settings_delete_templates(self, template_name, timeOut = 120):
	# (C) удаляет шаблон по имени/ ищет шаблон с первой страницы
		paging = 1 # если страниц более одной
		# считаем сколько всего шаблонов есть до удаления
		before_deleting_template_values_count = self.get_total_list_values_count()[0]
		# ТУТ будет цикл, если элемент есть на отображаемой странице то удаляем. если нет, то переходим на следующую и так до последней страницы
		value_parametrs = []
		# получаю список всех страниц и перехожу на первую (для случая многократного удаления на разных страницах)
		pages_with_templates = self.get_paging_templates_list
		if len(pages_with_templates[0]) > 1:
			if self.get_active_page_in_list[0][0] != pages_with_templates[0][0]:
				self.choose_paging_value(page_name = pages_with_templates[0][0])
		while True:
			# получаю список всех страниц доступных для перехода
			pages_with_templates = self.get_paging_templates_list
			# получаю список всех шаблонов отображенных на текущей странице
			list_templates_elements = self.general_settings_get_templates_list
			# находим соответствующий эллемент и получаем номер таблицы в которой он хранится и его собственный номер (реализовать проверки!!!)
			for element in list_templates_elements[1]:
				if element.text == str(template_name):
					value_parametrs.append(element.get_attribute('id').split('-')[3])
					value_parametrs.append(element.get_attribute('id').split('-')[5])
					break
			# если на текущей странице ничего не нашлось, то переходим на следующую. Если нашлось, то выходим из цикла поиска выполняем удаление
			# если страница последняя, а результат отрицательный то тоже выходим	
			if len(value_parametrs) == 0:
				# создаю список с номерами страниц (номера могут быть только int)
				numbers = []
				for number in pages_with_templates[0]:
					try:
						numbers.append(int(number))
					except Exception as ex:
						pass
				# выполняю переход на след страницу для поиска элемента
				if paging in numbers:
					self.choose_paging_value(page_name = paging)
					paging += 1
					time.sleep(1)
				else:
					# обшли все доступные страницы, но шаблона не нашли
					break
			else:
				# удаляемый шаблон найден, выходим из поиска
				break		
		if value_parametrs != []:
			self.click_element(element_definition = lk_elements.BUTTON('remove_template', mask = value_parametrs), timeOut = timeOut)
			# подтверждение удаления (нажатие на кнопку: Да)
			yes_button = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'ul-mainbutton-yes-\'')
			for item in yes_button[1]:
				if 'btnInnerEl' in item.get_attribute('id'):
					self.click_element(element_definition = item, timeOut = timeOut)
					break
			# ожидание удаления, если количество элементов на странице изменилось, то объект удалён
			time_index = 0
			while True:
				value_of_teamplates_after_chang = self.get_total_list_values_count()[0]
				if int(before_deleting_template_values_count) - int(value_of_teamplates_after_chang) == 1:
					loger.file_log(text = 'Template: ' + str(template_name) + ', was successfully deleted', text_type = 'SUCCESS')
					break
				
				if time_index >= timeOut:
					loger.file_log(text = 'Counter of the Templates wasn\'t changed. Deleting of the ' + str(template_name) + ' failed', text_type = 'ERROR  ')
					break			
				time.sleep(1)
				time_index += 1
		else:
			loger.file_log(text = 'Can\'t find such template name: ' + str(template_name), text_type = 'ERROR  ')
	
	def choose_paging_value(self, page_name = None, timeOut = 120, breakONerror = True):
	# (C) нажимает на определенное значение страничной навигации
		# пытаемся определить на какой странице находимся
		try:
			active_template = self.get_active_page_in_list[0]
			if len(active_template) == 1:
				active_template = self.get_active_page_in_list[0]
		except Exception as ex:
			loger.file_log(text = 'Can\'t define active page', text_type = 'ERROR  ')
			if breakONerror is True:
				self.close_browser()
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
		# пытаемся переключить на страницу, имя которой передано в метод
		if page_name != None:
			try:
				self.click_element(element_definition = self.get_paging_templates_list[1].get(str(page_name)), timeOut = timeOut, breakONerror = breakONerror)
			except Exception as ex:
				loger.file_log(text = 'Can\'t click necessary page name:' + str(page_name), text_type = 'ERROR  ')
				if breakONerror is True:
					self.close_browser()
					loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
					sys.exit()
		# необходимо добавить ожидание вместо sleep для проверки результата, получилось сменить страницу или нет.
		time_index = 0
		while True:
			try:
				current_page_index = self.get_active_page_in_list[0][0]
			except:
				pass
			# текущая страница соответствует необходимой
			if str(current_page_index) == str(page_name):
				break
			# переход В начало
			if str(current_page_index) == '1' and page_name == 'В начало':
				break
			# переход по: дальше
			if str(page_name) == 'дальше' and current_page_index != active_template:
				break
			# время ожидания истекло а переход так сделать и не удалось
			if time_index >= timeOut:
				loger.file_log(text = 'Can\'t switch from page: ' + str(active_template) + ', to the: ' + str(page_name), text_type = 'ERROR  ')
				if breakONerror is True:
					self.close_browser()
					loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
					sys.exit()
				break	
			time.sleep(1)
			time_index += 1	





		# try:
		# 	if active_template == self.get_active_page_in_list[0]:
		# 		time.sleep(1)
		# 		print('было: ',active_template, 'было нужно: ', page_name, 'стало: ', self.get_active_page_in_list[1].keys())
		# 	else:
		# 		print('было: ',active_template, 'было нужно: ', page_name, 'стало: ', self.get_active_page_in_list[1].keys())

		# except Exception as ex:
		# 	print('nexp', ex)


	def general_settings_edit_template(self, template_name, new_name, timeOut = 120):
	# (!C) открывает шаблон по имени для редактирования/ ищет шаблон с первой страницы
	# после редактирования ищет измененное имя.
		paging = 1 # если страниц более одной
		# считаем сколько всего шаблонов есть до удаления
		before_deleting_template_values_count = self.get_total_list_values_count()[0]
		# ТУТ будет цикл, если элемент есть на отображаемой странице то удаляем. если нет, то переходим на следующую и так до последней страницы
		value_parametrs = []
		# получаю список всех страниц и перехожу на первую (для случая многократного удаления на разных страницах)
		pages_with_templates = self.get_paging_templates_list
		if len(pages_with_templates[0]) > 1:
			if self.get_active_page_in_list[0][0] != pages_with_templates[0][0]:
				self.choose_paging_value(page_name = pages_with_templates[0][0])
		while True:
			# получаю список всех страниц доступных для перехода
			pages_with_templates = self.get_paging_templates_list
			# получаю список всех шаблонов отображенных на текущей странице
			list_templates_elements = self.general_settings_get_templates_list
			# находим соответствующий эллемент и получаем номер таблицы в которой он хранится и его собственный номер (реализовать проверки!!!)
			for element in list_templates_elements[1]:
				if element.text == str(template_name):
					value_parametrs.append(element.get_attribute('id').split('-')[3])
					value_parametrs.append(element.get_attribute('id').split('-')[5])
					break
			# если на текущей странице ничего не нашлось, то переходим на следующую. Если нашлось, то выходим из цикла поиска выполняем удаление
			# если страница последняя, а результат отрицательный то тоже выходим	
			if len(value_parametrs) == 0:
				# создаю список с номерами страниц (номера могут быть только int)
				numbers = []
				for number in pages_with_templates[0]:
					try:
						numbers.append(int(number))
					except Exception as ex:
						pass
				# выполняю переход на след страницу для поиска элемента
				if paging in numbers:
					self.choose_paging_value(page_name = paging)
					paging += 1
					time.sleep(1)
				else:
					# обшли все доступные страницы, но шаблона не нашли
					break
			else:
				# удаляемый шаблон найден, выходим из поиска
				break		
		if value_parametrs != []:
			self.click_element(element_definition = lk_elements.BUTTON('edit_template', mask = value_parametrs), timeOut = timeOut)
			# находим открытый для редактирования шаблон и изменяем
			template_for_change = self.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'commonsettings-page-textfield-value-\'')
			if template_for_change[0] == 1:
				# получаем динамический эллемент объекта
				# print(template_for_change[1][0].get_attribute('id'))
				template_id = template_for_change[1][0].get_attribute('id').split('-')[4] 
				# меняем значение\имя шаблона
				self.change_value(element_definition = template_for_change[1][0], text = new_name)
			else:
				loger.file_log(text = 'Were found more than one template. Check templates definition in this method: general_settings_edit_template ', text_type = 'ERROR  ')
				self.abort_test()
			# сохраняем измененное значение
			self.click_element(element_definition = lk_elements.BUTTON('save_template_name_icon', mask = template_id), timeOut = 5)

			# проверяем что изменения сделаны.











			# # подтверждение удаления (нажатие на кнопку: Да)
			# yes_button = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'ul-mainbutton-yes-\'')
			# for item in yes_button[1]:
			# 	if 'btnInnerEl' in item.get_attribute('id'):
			# 		self.click_element(element_definition = item, timeOut = timeOut)
			# 		break

	@property
	def define_kapcha_status(self):
	# (С)определяем статус выключателя капча: True включена, False выключена, считаем что элемент уже есть на странице
	# если элемент не успел отрисоваться то будет
		# находим все однотиповые эллементы (текст на странице с переключателем)
		id_is = None
		needed_elements =  self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'cm-switchbox-\'')
		if needed_elements != [None,[None]]:
		# ищем динамическую часть id для переключателя капчи	
			for needed_element in needed_elements[1]:
				try:
					if 'Защита от спама (капча):' in needed_element.text:
						id_is = needed_element.get_attribute('id').split('-')[5]
						break
				except Exception as ex:
					print(ex)					
			if id_is != None:
				# кидаем консольную команду и получаем статус кнопки (хорошо б что-нить еще придумать сюда вместо такого способа)
				kapcha_status = self.execute_console_command(command = "return window.Ext.getCmp('channels-page-cm-switchbox-is_captcha_enabled-" + str(id_is) + "').getValue()")
		return kapcha_status

	def switch_kapcha_status(self, timeOut = 120):
	# (С!)переключаем выключатель капчи
		# определяем текущий статус капчи, если статус определить не удалось считаем что капчи нет на странице
		timer = 0
		while True:
			try:
				previus_kapcha_status = self.define_kapcha_status
				break
			except:
				pass

			if timer >= timeOut:
				loger.file_log(text = 'Can\'t switch tumbler of the  kapcha, Can\'t find kapcha at page', text_type = 'ERROR  ')
				break

			time.sleep(1)
			timer += 1

		# меняем статус
		# находим все однотиповые эллементы (текст на странице с переключателем)
		id_is = None
		needed_elements =  self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'cm-switchbox-\'')
		if needed_elements != [None,[None]]:
		# ищем динамическую часть id для переключателя капчи	
			for needed_element in needed_elements[1]:
				try:
					if 'Защита от спама (капча):' in needed_element.text:
						id_is = needed_element.get_attribute('id').split('-')[5]
						break
				except Exception as ex:
					print(ex)					
			if id_is != None:
				self.click_element(element_definition = lk_elements.SELECT('lk_kons_kapcha_select', mask = id_is))
		# после смены проверяем, что статус сменен и не равен старому
		timer = 0
		while True:
			if previus_kapcha_status != self.define_kapcha_status:
				loger.file_log(text = "Kapcha was changed", text_type = 'SUCCESS')
				break
			if timer >= timeOut:
				loger.file_log(text = 'Can\'t switch tumbler of the  kapcha', text_type = 'ERROR  ')
				break
			timer += 1
			time.sleep(1)
		# возвращаем новый статус капчи

	def konsultant_back_phone(self, kaptcha = False):
		pass