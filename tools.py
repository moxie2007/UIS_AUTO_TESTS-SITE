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
		# self.client = None
	

	def init_testrail(self):
			try:
				client = APIClient('http://testrail.uiscom.ru/')
				# тут нужен логин и пароль для доступа в тестрейл
				client.user = None
				client.password = None
				return self.client
			except Exception as ex:
				loger.file_log(text = 'Did not initialization testrail' , text_type = 'ERROR  ')

	def init_browser(self, product_type = 'Chrome'):
		""" открывает объект Браузера """
		try:
			self.driver = webdriver.Firefox()
			self.driver.maximize_window()
			return self.driver
		except Exception as ex:
			# print(ex)
			loger.file_log(text = 'Did not initialization Browser' , text_type = 'ERROR  ')

	def close_browser(self):
		""" закрывает открытый объект Браузера """
		if self.driver:
			self.driver.quit()
			self.driver = None

	def goto(self, url = None, breakONerror = False):
		""" осуществляет переход по URL """
		driver = self.driver
		self.url = url
		self.breakONerror = breakONerror
		
		try:
			driver.delete_all_cookies()
		except Exception as ex:
			ptint(ex)
		print(driver.get_cookies())
		
		try:
			# print(url)
			print(url)
			time.sleep(10)
			driver.get(url)
			time.sleep(10)
			driver.get(url)
			time.sleep(10)
		except Exception as ex:
			loger.file_log(text = 'can not open URL. URL = ' + str(self.url) , text_type = 'ERROR  ')
			if self.breakONerror == True:
				self.abort_test()

	def element_is(self, element_definition = None):
		""" проверяет наличие определенного элемента на странице """
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
		# проверяет отображение страницы для определённого эллемента
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
	
	def displayed_element(self, element_definition, timeOut = 10):
		# проверяет наличие (видимость) определенного элемента на странице
		driver = self.driver
		desired_element = None
		# element = None
		state = False
		elementTyte = None
		step = 1
		while step <= timeOut:
			try:
				desired_element = self.element_is(element_definition)
				if desired_element.is_displayed() is True:
					state = True
					try:
						elementTyte = self.element_is(element_definition).tag_name
					except Exception as ex:
						pass
					break
			except Exception as ex:
				pass
			step += 1
			time.sleep(1)
		return [state, elementTyte, desired_element]	
	
	def elements_list (self, object_type = 'div', search_type = 'contains', mask = 'li',  timeOut = 10):
		# создает список эллементов по определенной маске, возвращает количество найденных эллементов и сами эллементы в виде готовывых объектов
		result = [None,[None,None]]
		driver = self.driver
		step = 1
		while step <= timeOut:
			try:
				elements = driver.find_elements_by_xpath("//" + str(object_type) + "[" + str(search_type) + "(@" + str(mask) + ")]")
			except:
				pass		
			try:
				if len(elements) != 0:
					result = [len(elements), elements]
					break					
			except:
				pass
			step += 0.5
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
			loger.file_log(text = 'can not click ' + str(element_definition) , text_type = 'ERROR  ')
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
			if breakONerror == True:
				self.abort_test()
	
	def definition_current_url (self, breakONerror = True):
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

		# для вхлда использовать логин и пароль к сайту
	def login_to(self, url = None, user = None, password = None, breakONerror = True):
		# логин в систему (в разработке: убрать проверку если активен попап)
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
		# проверка на то, что открыто именно то, что мы и ожидали.
		while True:
			print(str(url),  self.definition_current_url())
			if str(url) == self.definition_current_url():
				loger.file_log(text = 'Open URL done. URL = ' + str(url), text_type = 'SUCCESS')
				break
			if time_index >= 20 and breakONerror is True:
				self.close_browser()
				loger.file_log(text = 'Can not open necessary URL', text_type = 'ERROR  ')
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
			time.sleep(1)
			time_index += 1	

	def switch_env(self, selected_element = None, server_name = 'sitecw2.webdev.uiscom.ru',  breakONerror = True):
		# изменяет тестовый сервер в личном кабинете ()
		driver = self.driver
		url_action_start = self.definition_current_url()
		self.click_element(element_definition = lk_elements.SELECT(element = selected_element), breakONerror = True)

		# combobox_list = self.displayed_element(element_definition = lk_elements.COMBOBOX(element = 'test_site'))
		# print(combobox_list)
		
		obj_servers_list = self.elements_list(object_type = 'li', mask = 'class, \'x-boundlist-item\'')

		if len(obj_servers_list[1]) > 0:
			for current_server_name in obj_servers_list[1]:
				if server_name == current_server_name.text:
					print(current_server_name.text)
					try:
						# скролим список к нужному элементу
						driver.execute_script("return arguments[0].scrollIntoView();", current_server_name)
						# нажимаем на искомый элемент
						current_server_name.click()
					except Exception as ex:
						loger.file_log(text = 'can not click ' + str(element_definition) , text_type = 'ERROR  ')
						if self.breakONerror == True:
							self.abort_test()
		

				# тут надо сделать проверку что сервер сменен правильно !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		time_index = 0
		time.sleep(5) #тут нужен нормальный тайм аут
		while True:
			if 'Id=8868' in str(self.definition_current_url()):
				loger.file_log(text = 'Necessary server was chosen', text_type = 'SUCCESS')
				break
			if time_index >= 20 and breakONerror is True:
				self.close_browser()
				loger.file_log(text = 'Can not open necessary URL', text_type = 'ERROR  ')
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
			
			time.sleep(1)
			time_index += 1	

	def lk_mainMenu_navigation (self, item_menu = ['Общие отчёты', 'Аудитория'],  timeOut = 120, breakONerror = True):
	# навигация по основному меню (добавить timeout для while)
		while len(item_menu) != 0:

			try:
				elem_list = self.elements_list(object_type = 'table', search_type = 'contains', mask = 'id, \'ul-treeview-1025\'',  timeOut = 10)[1]
				print(item_menu)
				
				if len(item_menu) != 0:
					for elem in elem_list:
						if elem.text == item_menu[0]:
							print('Жму на ' + str(item_menu[0]))
							elem.click()
							item_menu.remove(item_menu[0])
							if len(item_menu) != 0:
								print('остался ' + str(item_menu[0]))
							time.sleep(2)
							break
				else:
					break

			except Exception as ex:
				loger.file_log(text = 'Can not ', text_type = 'ERROR  ')
				print(ex)
				if breakONerror is True:
					self.close_browser()
					loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
					sys.exit()
		return 	elem_list


