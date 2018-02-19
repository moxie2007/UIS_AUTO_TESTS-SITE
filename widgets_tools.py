import sys, time
import tools, start_uis_test, pageElements
import loger 
from loger import Loger as loger

# создаем объект, для использования модуля описывающего элементы на страницах
lk_elements  = pageElements.LK()

class Wg_tools(tools.Uis_tools):
	def __init__(self, driver):
		self.driver = driver

#(! Этой опции больше нет все методы перенести и перепроверить) консультант -- Общие настройки -- Шаблоны сообщений
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
			print(elems.get('count'))
			for elem in elems.get('elements'):
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
			elems_test.get('elements')[0].click()
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
			for item in yes_button.get('elements'):
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
			if template_for_change.get('count') == 1:
				# получаем динамический эллемент объекта
				# print(template_for_change[1][0].get_attribute('id'))
				template_id = template_for_change.get('elements')[0].get_attribute('id').split('-')[4] 
				# меняем значение\имя шаблона
				self.change_value(element_definition = template_for_change.get('elements')[0], text = new_name)
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

	def black_list_add_new_address(self, ip_idress, comment, breakONerror = True):
	# !(C) добавляем новый IP в черный список.
		# запоминаем количество уже имеющихся записей
		addresses_count_before_adding = self.get_total_list_values_count()[0]
		# вводим IP
		# ищем контейнер с текстом: Добавить шаблон, что - бы получить id (такое значение должно быть только одно).
		text_items = []
		for item in self.elements_list(search_type = None, mask = 'div[id^=commonsettings-page-container-] * label').get('elements'):
			try:
				if (item.text) != 0:
					text_items.append([item.text, item])
			except Exception as ex:
				print('widgets_tools.black_list_add_new_address:  ', ex)
		if len(text_items) == 1:
			id_mask = text_items[0][1].get_attribute('id').split('-')[4]
		else:
			loger.file_log(text = 'Can\'t add new ip to the black list. Labels count should be one, but we have: ' + str(len(text_items)), text_type = 'ERROR  ')
			self.close_browser()
			loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
			sys.exit()	
		# вводим ip и коментарий
		self.change_value(element_definition = lk_elements.INPUT("konsultant_black_list_add_ip", mask = id_mask), text = ip_idress)
		self.change_value(element_definition = lk_elements.INPUT("konsultant_black_list_add_comment", mask = str(int(id_mask) + 1)), text = comment)
		time.sleep(5)


		# нажимаем кнопку добавить
		# проверяем результат (изменилось значение: Всего записей)


		# определяем на какой странице находимся
		return [id_mask]

# Сайтфон
	@property
	def sitephone_define_kapcha_status(self):
	# (СG)определяем статус выключателя капча: True включена, False выключена, считаем что элемент уже есть на странице
		result = {'status_of_lable':None,'id_is':None}
		needed_elements =  self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'sitephone-page-cm-switchbox-is_captcha_enabled-\'')
		if needed_elements.get('count') >= 1:	
			for needed_element in needed_elements.get('elements'):
				try:
					if 'Защита от спама (капча)' in needed_element.text:
						result['id_is'] = needed_element.get_attribute('id').split('-')[5]
						break
				except Exception as ex:
					print('sitephone_define_kapcha_status:  ', ex)
			
			if result.get('id_is') != None:
				# кидаем консольную команду и получаем статус кнопки (хорошо б что-нить еще придумать сюда вместо такого способа)
				result['status_of_lable'] = self.execute_console_command(command = "return window.Ext.getCmp('sitephone-page-cm-switchbox-is_captcha_enabled-" + str(result.get('id_is')) + "').getValue()")
			else:
				loger.file_log(text = 'Can\'t define button status', text_type = 'ERROR  ')
				self.close_browser
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
		else:
			loger.file_log(text = 'Can\'t find CAPTCHA text at page' , text_type = 'ERROR  ')
			self.close_browser
			loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
			sys.exit()
		return result

	def sitephone_change_kapcha_status(self, label_state = False, timeOut = 120):
	# (СG)переключаем выключатель капчи
		# определяем какое щас состояние
		before_labele_state = self.sitephone_define_kapcha_status
		# если состояние отличное от нужного ищем id по тексту перед кнопкой 
		if before_labele_state.get('status_of_lable') == label_state:
			loger.file_log(text = 'Label in status:' + str(label_state) + ', and should not be changed', text_type = 'SUCCESS')
			after_labele_state = before_labele_state
			result = None
		else:
			# жмем на кнопку
			self.click_element(element_definition = lk_elements.LABELE('sitephone_kaptcha_lable', mask = str(before_labele_state.get('id_is'))), timeOut = timeOut)
			time_index = 0
			# ожидаем результата. состояние должно смениться от текущего
			while time_index <= timeOut:
				after_labele_state = self.sitephone_define_kapcha_status
				if after_labele_state.get('status_of_lable') != before_labele_state.get('status_of_lable'):
					loger.file_log(text = 'The state of the kapcha label was changed from: ' + str(before_labele_state.get('status_of_lable')) + ', to the: ' + str(after_labele_state.get('status_of_lable')), text_type = 'SUCCESS')
					result = True
					break
				if time_index <= timeOut:
					loger.file_log(text = 'Can\'t change kapcha label status', text_type = 'ERROR  ')
					result = False
					break
				time.sleep(1)
				time_index += 1	
		return {'lable_state': after_labele_state.get('status_of_lable'), 'operation_status':result}

	@property
	def sitephone_define_display_at_site_status(self):
	# (СG)определяем статус выключателя показывать на сайте: True включен, False выключен, считаем что элемент уже есть на странице
		# result = {'status_of_lable':None,'id_is':None}
		result = {}
		needed_elements =  self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'sitephone-page-cm-switchbox-is_visible-\'')
		if type(needed_elements.get('count')) == int:	
			for needed_element in needed_elements.get('elements'):
				try:
					if 'Показывать на сайте' in needed_element.text:
						result['id_is'] = needed_element.get_attribute('id').split('-')[5]
						break
				except Exception as ex:
					print('sitephone_define_show_at_site_status:  ', ex)
			
			if result.get('id_is') != None:
				# кидаем консольную команду и получаем статус кнопки (хорошо б что-нить еще придумать сюда вместо такого способа)
				result['status_of_lable'] = self.execute_console_command(command = "return window.Ext.getCmp('sitephone-page-cm-switchbox-is_visible-" + str(result.get('id_is')) + "').getValue()")
			else:
				loger.file_log(text = 'Can\'t define button status', text_type = 'ERROR  ')
		else:
			loger.file_log(text = 'Can\'t find "Show at site" text at page' , text_type = 'ERROR  ')
		return result
	
	def sitephone_change_display_at_site_status(self, label_state = False, timeOut = 120):
	# (СG)переключаем выключатель Показывать на сайте
		# определяем какое щас состояние
		before_labele_state = self.sitephone_define_display_at_site_status
		# если состояние отличное от нужного ищем id по тексту перед кнопкой 
		if before_labele_state.get('status_of_lable') == label_state:
			loger.file_log(text = 'Label in status:' + str(label_state) + ', and should not be changed', text_type = 'SUCCESS')
			after_labele_state = before_labele_state
			result = None
		else:
			# жмем на кнопку
			self.click_element(element_definition = lk_elements.LABELE('sitephone_display_at_site_lable', mask = str(before_labele_state.get('id_is'))), timeOut = timeOut)
			time_index = 0
			# ожидаем результата. состояние должно смениться от текущего
			step_await = self.wait_for_results()
			while time_index <= timeOut:
				after_labele_state = self.sitephone_define_display_at_site_status
				if after_labele_state.get('status_of_lable') != before_labele_state.get('status_of_lable'):
					loger.file_log(text = 'The state of the kapcha label was changed from: ' + str(before_labele_state.get('status_of_lable')) + ', to the: ' + str(after_labele_state.get('status_of_lable')), text_type = 'SUCCESS')
					result = True
					break
				if time_index <= timeOut:
					loger.file_log(text = 'Can\'t change kapcha label status', text_type = 'ERROR  ')
					result = False
					break
				time.sleep(1)
				time_index += 1	
		return {'lable_state': after_labele_state.get('status_of_lable'), 'operation_status':result}

	@property
	def sitephone_define_checkbox_disp_at_pc(self):
	# (CG) определяем состояние чек-бокса: Показывать на устройствах ПК (метод без проверки наличия элемента на странице)
		result = {}
		needed_elements =  self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'sitephone-page-checkboxfield-desktop-\'')
		# если найдены объекты, то в цикле по ним, ищем статус нашего.
		if type(needed_elements.get('count')) == int:
			for check_item in needed_elements.get('elements'):
				# определяем какой из объектов основной, у этого объекта нет свойства: data-ref
				if type(check_item.get_attribute('data-ref')) == type(None):
					# таокой элемент должен быть один, если нет сообщаем в лог берется только первое значение
					object_class = check_item.get_attribute('class') # вынесено для того, что бы все проверки проводить над одним объектом (переключение на странице)
					if 'x-form-cb-checked' in object_class:
						if result.get('object_id') == None:
							result['state'] = True
							result['object_id'] = check_item.get_property('id')
							if 'x-item-disabled' in object_class:
								result['status'] = False
							else:
								result['status'] = True
						else:
							loger.file_log(text = 'In the method (widget_tools.sitephone_define_checkbox_disp_at_pc) were found more than one object at page' , text_type = 'WARNING')
					else: #продумать логику этого условия, может работать не корректно
						if result.get('object_id') == None:
							result['state'] = False
							result['object_id'] = check_item.get_property('id')
							if 'x-item-disabled' in object_class:
								result['status'] = False
							else:
								result['status'] = True
						else:
							loger.file_log(text = 'In the method (widget_tools.sitephone_define_checkbox_disp_at_pc) were found more than one object at page' , text_type = 'WARNING')
		# result: state - выбран\невыбран, status - активен\неактивен, id - элемента
		return result

	@property
	def sitephone_define_checkbox_disp_at_sitephone(self):
	# (CG) определяем состояние чек-бокса: Показывать на устройствах Смартфон (метод без проверки наличия элемента на странице)
		result = {}
		needed_elements =  self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'sitephone-page-checkboxfield-mobile-\'')
		# если найдены объекты, то в цикле по ним, ищем статус нашего.
		if type(needed_elements.get('count')) == int:
			for check_item in needed_elements.get('elements'):
				# определяем какой из объектов основной, у этого объекта нет свойства: data-ref
				if type(check_item.get_attribute('data-ref')) == type(None):
					# таокой элемент должен быть один, если нет сообщаем в лог берется только первое значение
					object_class = check_item.get_attribute('class') # вынесено для того, что бы все проверки проводить над одним объектом (переключение на странице)
					if 'x-form-cb-checked' in object_class:
						if result.get('object_id') == None:
							result['state'] = True
							result['object_id'] = check_item.get_property('id')
							if 'x-item-disabled' in object_class:
								result['status'] = False
							else:
								result['status'] = True
						else:
							loger.file_log(text = 'In the method (widget_tools.sitephone_define_checkbox_disp_at_sitephone) were found more than one object at page' , text_type = 'WARNING')
					else: #продумать логику этого условия, может работать не корректно
						if result.get('object_id') == None:
							result['state'] = False
							result['object_id'] = check_item.get_property('id')
							if 'x-item-disabled' in object_class:
								result['status'] = False
							else:
								result['status'] = True
						else:
							loger.file_log(text = 'In the method (widget_tools.sitephone_define_checkbox_disp_at_sitephone) were found more than one object at page' , text_type = 'WARNING')
		# result: state - выбран\невыбран, status - активен\неактивен, id - элемента
		return result

	@property
	def sitephone_define_checkbox_disp_at_tablet(self):
	# (CG) определяем состояние чек-бокса: Показывать на устройствах Планшет (метод без проверки наличия элемента на странице)
		result = {}
		needed_elements =  self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'sitephone-page-checkboxfield-tablet-\'')
		# если найдены объекты, то в цикле по ним, ищем статус нашего.
		if type(needed_elements.get('count')) == int:
			for check_item in needed_elements.get('elements'):
				# определяем какой из объектов основной, у этого объекта нет свойства: data-ref
				if type(check_item.get_attribute('data-ref')) == type(None):
					# таокой элемент должен быть один, если нет сообщаем в лог берется только первое значение
					object_class = check_item.get_attribute('class') # вынесено для того, что бы все проверки проводить над одним объектом (переключение на странице)
					if 'x-form-cb-checked' in object_class:
						if result.get('object_id') == None:
							result['state'] = True
							result['object_id'] = check_item.get_property('id')
							if 'x-item-disabled' in object_class:
								result['status'] = False
							else:
								result['status'] = True
						else:
							loger.file_log(text = 'In the method (widget_tools.sitephone_define_checkbox_disp_at_tablet) were found more than one object at page' , text_type = 'WARNING')
					else: #продумать логику этого условия, может работать не корректно
						if result.get('object_id') == None:
							result['state'] = False
							result['object_id'] = check_item.get_property('id')
							if 'x-item-disabled' in object_class:
								result['status'] = False
							else:
								result['status'] = True
						else:
							loger.file_log(text = 'In the method (widget_tools.sitephone_define_checkbox_disp_at_tablet) were found more than one object at page' , text_type = 'WARNING')
		# result: state - выбран\невыбран, status - активен\неактивен, id - элемента
		return result

	@property
	def sitephone_define_fieldstate_text_at_banner(self):
	# (CG) определяем состояние поле ввода: Текст на баннере (метод без проверки наличия элемента на странице)
		result = {}
		needed_elements =  self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'sitephone-page-textfield-title-\'')
		# проверяем нашлись ли объекты на странице
		id_mask = None
		if type(needed_elements.get('count')) == int:
			for object_item in needed_elements.get('elements'):
				# выбираем родительский объект поля: Текст на баннере
				if type(object_item.get_attribute('data-ref')) == type(None):
					values_object_id = object_item.get_attribute('id').split('-')
					for value in values_object_id:
						try:
							id_mask = int(value)
							break
						except:
							pass
			# через маску родительского объекта, получаем значение из поля ввода
			if type(id_mask) == int:
				input_object = self.displayed_element(element_definition = lk_elements.INPUT("sitephone_banner_text_field", mask = id_mask))
				if input_object.get('state'):
					result['text'] = input_object.get('element').get_attribute('value')			
				# проверяем отображена ли иконка ошибок, после того как текст получен, должна и иконка быть
				error_icon_object = self.displayed_element(element_definition = lk_elements.INPUT("sitephone_banner_text_error_icon", mask = id_mask), timeOut = 0.5)
				if error_icon_object.get('state'):
					result['error_icon_state'] = True
				else:
					result['error_icon_state'] = False		
		return result

						






	@property
	def sitephone_define_animation_status(self):
	# (СG)определяем статус выключателя Анимация: True включена, False выключена, считаем что элемент уже есть на странице
		result = {'status_of_lable':None,'id_is':None}
		needed_elements =  self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'sitephone-page-cm-switchbox-is_animation_enabled-\'')
		if needed_elements.get('count') >= 1:	
			for needed_element in needed_elements.get('elements'):
				try:
					if 'Анимация:' in needed_element.text:
						result['id_is'] = needed_element.get_attribute('id').split('-')[5]
						break
				except Exception as ex:
					print('sitephone_define_animation_status:  ', ex)
			
			if result.get('id_is') != None:
				# кидаем консольную команду и получаем статус кнопки (хорошо б что-нить еще придумать сюда вместо такого способа)
				result['status_of_lable'] = self.execute_console_command(command = "return window.Ext.getCmp('sitephone-page-cm-switchbox-is_animation_enabled-" + str(result.get('id_is')) + "').getValue()")
			else:
				loger.file_log(text = 'Can\'t define button status', text_type = 'ERROR  ')
				self.close_browser
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
		else:
			loger.file_log(text = 'Can\'t find Animation text at page' , text_type = 'ERROR  ')
			self.close_browser
			loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
			sys.exit()
		return result

	def sitephone_change_animation_status(self, label_state = False, timeOut = 120):
	# (СG)переключаем выключатель Показывать на сайте
		# определяем какое щас состояние
		before_labele_state = self.sitephone_define_animation_status
		# если состояние отличное от нужного ищем id по тексту перед кнопкой 
		if before_labele_state.get('status_of_lable') == label_state:
			loger.file_log(text = 'Label in status:' + str(label_state) + ', and should not be changed', text_type = 'SUCCESS')
			after_labele_state = before_labele_state
			result = None
		else:
			# жмем на кнопку
			self.click_element(element_definition = lk_elements.LABELE('sitephone_animation_lable', mask = str(before_labele_state.get('id_is'))), timeOut = timeOut)
			time_index = 0
			# ожидаем результата. состояние должно смениться от текущего
			while time_index <= timeOut:
				after_labele_state = self.sitephone_define_animation_status
				if after_labele_state.get('status_of_lable') != before_labele_state.get('status_of_lable'):
					loger.file_log(text = 'The state of the Animation label was changed from: ' + str(before_labele_state.get('status_of_lable')) + ', to the: ' + str(after_labele_state.get('status_of_lable')), text_type = 'SUCCESS')
					result = True
					break
				if time_index <= timeOut:
					loger.file_log(text = 'Can\'t change Animation label status', text_type = 'ERROR  ')
					result = False
					break
				time.sleep(1)
				time_index += 1	
		return {'lable_state': after_labele_state.get('status_of_lable'), 'operation_status':result}

	@property
	def sitephone_define_delayed_call_status(self):
	# (СG)определяем статус выключателя Отложенный звонок: True включена, False выключена, считаем что элемент уже есть на странице
		result = {'status_of_lable':None,'id_is':None}
		needed_elements =  self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'sitephone-page-cm-switchbox-is_delayed_call_enabled-\'')
		if needed_elements.get('count') >= 1:	
			for needed_element in needed_elements.get('elements'):
				try:
					if 'Отложенный звонок' in needed_element.text:
						result['id_is'] = needed_element.get_attribute('id').split('-')[5]
						break
				except Exception as ex:
					print('sitephone_define_delayed_call_status:  ', ex)
			
			if result.get('id_is') != None:
				# кидаем консольную команду и получаем статус кнопки (хорошо б что-нить еще придумать сюда вместо такого способа)
				result['status_of_lable'] = self.execute_console_command(command = "return window.Ext.getCmp('sitephone-page-cm-switchbox-is_delayed_call_enabled-" + str(result.get('id_is')) + "').getValue()")
			else:
				loger.file_log(text = 'Can\'t define button status', text_type = 'ERROR  ')
				self.close_browser
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
		else:
			loger.file_log(text = 'Can\'t find delayed call text at page' , text_type = 'ERROR  ')
			self.close_browser
			loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
			sys.exit()
		return result		

	def sitephone_change_delayed_call_status(self, label_state = False, timeOut = 120):
	# (СG)переключаем выключатель Отложенный звонок
		# определяем какое щас состояние
		before_labele_state = self.sitephone_define_delayed_call_status
		# если состояние отличное от нужного ищем id по тексту перед кнопкой 
		if before_labele_state.get('status_of_lable') == label_state:
			loger.file_log(text = 'Label in status:' + str(label_state) + ', and should not be changed', text_type = 'SUCCESS')
			after_labele_state = before_labele_state
			result = None
		else:
			# жмем на кнопку
			self.click_element(element_definition = lk_elements.LABELE('sitephone_delayed_call_lable', mask = str(before_labele_state.get('id_is'))), timeOut = timeOut)
			time_index = 0
			# ожидаем результата. состояние должно смениться от текущего
			while time_index <= timeOut:
				after_labele_state = self.sitephone_define_delayed_call_status
				if after_labele_state.get('status_of_lable') != before_labele_state.get('status_of_lable'):
					loger.file_log(text = 'The state of the delayed call label was changed from: ' + str(before_labele_state.get('status_of_lable')) + ', to the: ' + str(after_labele_state.get('status_of_lable')), text_type = 'SUCCESS')
					result = True
					break
				if time_index <= timeOut:
					loger.file_log(text = 'Can\'t change delayed call label status', text_type = 'ERROR  ')
					result = False
					break
				time.sleep(1)
				time_index += 1	
		return {'lable_state': after_labele_state.get('status_of_lable'), 'operation_status':result}

	def sitephone_checkbox_show_at_devices_status(self, device = 'Смартфон'):
	# определяет статус чекбокса: Показывать на устройстве. Считаем что параметр: Показывать на сайте, ВКЛ.

		check_box = {}
		result = {}
		needed_elements = self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'-checkboxfield-\'')
		counter = 0
		for element in needed_elements.get('elements'):
			if str(element.text) == str(device):
				check_box['name'] = str(element.text)
				check_box['element'] = element
				check_box['id_is'] = str(element.get_attribute('id').replace('-boxLabelEl',''))
				counter += 1
		check_box['items_count'] = counter

		result['status_of_checkbox'] = self.execute_console_command(command = "return window.Ext.getCmp('" + str(check_box.get('id_is')) + "').getValue('checked')")

		return result








# консультант -- Распределение обращений
	@property
	def define_chats_distribution_state(self):
	# (!C) метод определяющий Включено\Выключено распределение чатов на странице Распределение обращений
		# находим динамическую часть id переключателя (по тексту перед выключателем)
		needed_elements =  self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'chatprocessing-page-cm-switchbox-is_chat_distribution_enabled-\'')
		if needed_elements.get('count') >= 1:
			for needed_element in needed_elements.get('elements'):
				try:
					if 'Настройка распределения чатов' in needed_element.text:
						id_is = needed_element.get_attribute('id').split('-')[5]
						break
				except Exception as ex:
					print('setting_distribution_of_chats:  ', ex)
			if id_is != None:
				# кидаем консольную команду и получаем статус кнопки (хорошо б что-нить еще придумать сюда вместо такого способа)
				status_of_distribution_of_chats = self.execute_console_command(command = "return window.Ext.getCmp('chatprocessing-page-cm-switchbox-is_chat_distribution_enabled-" + str(id_is) + "').getValue()")
			else:
				loger.file_log(text = 'Can\'t define button status', text_type = 'ERROR  ')
				self.close_browser()
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
		return [str(status_of_distribution_of_chats), str(id_is)]

	def setting_distribution_of_chats(self, to_state = False, timeOut =120):
	# (!C) метод Вкл\Выкл распределение чатов (метод будет перенесен в другое место).
		method_state = []
		current_state = self.define_chats_distribution_state
		# определяем состояние переключателя (id находим по тексту перед выключателем)
		if str(to_state) == str(current_state[0]):
			loger.file_log(text = 'Button already in necessary state', text_type = 'SUCCESS')
		else:
			# выполняем нажатие на кнопку
			self.click_element(element_definition = lk_elements.SELECT('lk_kons_chats_distribution', mask = current_state[1]))
			# проверяем, что переключение произошло
			time_stamp = 0
			while True:
				if str(self.define_chats_distribution_state[0]) == str(to_state):
					loger.file_log(text = 'Chats distribution state was changed to the: ' + str(to_state), text_type = 'SUCCESS')
					method_state.append(str(True))
					break
				if time_stamp >= timeOut:
					loger.file_log(text = 'Click to the button was done but state wasn\'t changed', text_type = 'ERROR  ')
					method_state.append(str(False))
					break			
				time.sleep(1)
				time_index += 1
		return method_state

# Консультант - Внешний вид
	def cons_view_change_widget_position(self, place = 'br', open_dd_by = 'txt', timeOut = 120):
	# (C) исходим из того, что вкладка: Внешний вид, уже открыта
	# значения отображения: (br:"снизу справа", bl:"снизу слева", cr:"по центру справа", cl:"по центру слева", ur:"сверху справа", ul:"сверху слева")
	# значения по нажатию на какой эллемент будет открываться список, определяющий где будет располагаться виджет.(значения: {'txt':'text','dd':'dropdown'})
		current_element = []
		positions = {'br':"снизу справа", 'bl':"снизу слева", 'cr':"по центру справа", 'cl':"по центру слева", 'ur':"сверху справа", 'ul':"сверху слева"}
		# на ходим текст для выпадающего списка со значениями, которые определяют положение виджета на странице
		elements = self.elements_list(object_type = 'label', search_type = 'contains', mask = 'class, \'x-form-item-label x-form-item-label-ul   x-unselectable\'')
		for element in elements.get('elements'):
			try:
				if 'Положение на сайте' in element.text:
					current_element.append(element)
			except Exception as ex:
				print('Error in cons_change_widget_position: ' + str(ex))
		if len(current_element) != 1:
			loger.file_log(text = 'Was found more than one necessary element at View widget page, it\'s wrong', text_type = 'ERROR  ')
		else:
			# определяем эллементы для нажатия
			type_click = {'txt':current_element[0],'dd':self.displayed_element(element_definition = lk_elements.SELECT('lk_kons_view_dd', mask = current_element[0].get_attribute('id').split('-')[5])).get('element')}
			# проверяем какое значение уже выбрано и если нужно, то выбираем новое, если не нужно то не меняем.
			current_value =  type_click.get('dd').get_attribute('value')
			if positions.get(place) == current_value:
				loger.file_log(text = 'Necessary value: ' + str(positions.get(place)) + ' already chosen. We have no necessary to change', text_type = 'SUCCESS')
			else:
				# нажимаем на элемент
				self.click_element(element_definition = type_click.get(open_dd_by))
				# проверяем, что список открыт
				dropdown_items = self.elements_list(object_type = 'li', search_type = 'contains', mask = 'class, \'x-boundlist-item\'').get('elements')
				for item in dropdown_items:
					if positions.get(place) == item.text:
						self.click_element(element_definition = item)
						break
				# проверяем, что переключение произошло и выводим в лог результат
				time_index = 0
				while time_index <= timeOut:
					if current_value != type_click.get('dd').get_attribute('value'):
						loger.file_log(text = 'Necessary value: ' + str(positions.get(place)) + ', was chosen', text_type = 'SUCCESS')
						result = True
						break
					if time_index <= timeOut:
						loger.file_log(text = 'Necessary value: ' + str(place) + ', was not chosen. current selection: ' + str(current_value), text_type = 'ERROR  ')
						result = False
						break
					time.sleep(1)
					time_index += 1
		# возвращаем статус смены. и текущий выбор
		return {'result':result,'result_place':type_click.get('dd').get_attribute('value')}

	@property
	def cons_view_define_animation_status(self):
	# (GC) определяем состояние контрола: Анимация, True=включено, False=выключено
		result = {'status_of_lable':None,'id_is':None}
		needed_elements =  self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'uisettings-page-cm-switchbox-is_animation_enabled-\'')
		if needed_elements.get('count') >= 1:	
			for needed_element in needed_elements.get('elements'):
				try:
					if 'Анимация' in needed_element.text:
						result['id_is'] = needed_element.get_attribute('id').split('-')[5]
						break
				except Exception as ex:
					print('setting_distribution_of_chats:  ', ex)
			
			if result.get('id_is') != None:
				# кидаем консольную команду и получаем статус кнопки (хорошо б что-нить еще придумать сюда вместо такого способа)
				result['status_of_lable'] = self.execute_console_command(command = "return window.Ext.getCmp('uisettings-page-cm-switchbox-is_animation_enabled-" + str(result.get('id_is')) + "').getValue()")
			else:
				loger.file_log(text = 'Can\'t define button status', text_type = 'ERROR  ')
				self.close_browser
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
		else:
			loger.file_log(text = 'Can\'t find Animation text at page' , text_type = 'ERROR  ')
			self.close_browser
			loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
			sys.exit()
		return result

	def cons_view_change_animation_lable_status(self, label_state = True, timeOut = 120):
	# (CG) изменяем состояние лейбла Анимация на странице Внешний вид Консультанта.
		# определяем какое щас состояние
		before_labele_state = self.cons_view_define_animation_status
		# если состояние отличное от нужного ищем id по тексту перед кнопкой 
		if before_labele_state.get('status_of_lable') == label_state:
			loger.file_log(text = 'Label in status:' + str(label_state) + ', and should not be changed', text_type = 'SUCCESS')
			after_labele_state = before_labele_state
			result = None
		else:
			# жмем на кнопку
			self.click_element(element_definition = lk_elements.LABELE('cons_view_animation_lable', mask = str(before_labele_state.get('id_is'))), timeOut = timeOut)
			time_index = 0
			# ожидаем результата. состояние должно смениться от текущего
			while time_index <= timeOut:
				after_labele_state = self.cons_view_define_animation_status
				if after_labele_state.get('status_of_lable') != before_labele_state.get('status_of_lable'):
					loger.file_log(text = 'The state of the Label was changed from: ' + str(before_labele_state.get('status_of_lable')) + ', to the: ' + str(after_labele_state.get('status_of_lable')), text_type = 'SUCCESS')
					result = True
					break
				if time_index <= timeOut:
					loger.file_log(text = 'Can\'t change Label status', text_type = 'ERROR  ')
					result = False
					break
				time.sleep(1)
				time_index += 1	
		return {'lable_state': after_labele_state.get('status_of_lable'), 'operation_status':result}


	def  cons_view_define_color_number(self):
		# нефига не так пересмотреть логику
	# определяем какой сейчас выбран цвет для Консультанта, определяем по номеру цвета. (окно такое на странице одно и по этому ищем по типу)
		# находим объект: цветовая палитра
		result = {}
		color_piker = self.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'uisettings-page-ul-colorfield-banner_color-\'')
		# проверяем что такой элемент один, если да то открываем (нажатием)
		if color_piker.get('count') == 1:
			self.click_element(element_definition = color_piker.get('elements')[0])
			# проверяем, что открылось окно с выбором цветовая
			# color_field = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'class, \'x-field x-form-item x-form-item-ul x-form-type-text x-box-item x-field-ul x-hbox-form-item x-form-item-no-label x-form-dirty\'')
			color_field = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'uisettings-page-textfield-colorPickerField-\'')
			for index in color_field.get('elements'):
				print(index.get_attribute('style'))
				print('\n')
			result = {'count':color_field.get('count'),'style':color_field.get('elements')[0].get_attribute('value'), 'TEXT':color_field.get('elements')[0].text}



		else:
			loger.file_log(text = 'Were found more than one element, it\'s wrong. Exception in the method: wg.cons_view_define_color_number' , text_type = 'ERROR  ')
		
		return result

#



	# ------------------------------------------------------------------------------------------------





	
# временная заглушка для дашей, потом удалю
	def error_looks(self, timeOut = 2):
		result = 'None'
		try:
			items = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-title\'', timeOut = timeOut)
			for item in items.get('elements'):
				if item.text == 'Ошибка':
					# print('internal_error')
					result = 'Error'
					break
		except Exception as ex:
			result = str(ex)
		return result
