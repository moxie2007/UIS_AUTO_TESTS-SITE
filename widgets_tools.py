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
		for item in self.elements_list(search_type = None, mask = 'div[id^=commonsettings-page-container-] * label')[1]:
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

# консультант -- каналы -- обратный звонок\Сайтфон
	@property
	def define_kapcha_status(self):
		kapcha_status = None
	# (С)определяем статус выключателя капча: True включена, False выключена, считаем что элемент уже есть на странице
	# если элемент не успел отрисоваться то будет
		# находим все однотиповые эллементы (текст на странице с переключателем)
		id_is = None
		needed_elements =  self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'cm-switchbox-\'')
		if needed_elements != [None,[None], None]:
		# ищем динамическую часть id для переключателя капчи	
			for needed_element in needed_elements[1]:
				try:
					if 'Защита от спама (капча):' in needed_element.text:
						id_is = needed_element.get_attribute('id').split('-')[5]
						break
				except Exception as ex:
					print('define_kapcha_status:  ', ex)					
			if id_is != None:
				# кидаем консольную команду и получаем статус кнопки (хорошо б что-нить еще придумать сюда вместо такого способа)
				kapcha_status = self.execute_console_command(command = "return window.Ext.getCmp('channels-page-cm-switchbox-is_captcha_enabled-" + str(id_is) + "').getValue()")
		return kapcha_status

	def switch_kapcha_status(self, timeOut = 120):
	# (С!)переключаем выключатель капчи
		# определяем текущий статус капчи, если статус определить не удалось считаем, что капчи НЕТ на странице
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
		if needed_elements != [None,[None],None]:
		# ищем динамическую часть id для переключателя капчи	
			for needed_element in needed_elements[1]:
				try:
					if 'Защита от спама (капча):' in needed_element.text:
						id_is = needed_element.get_attribute('id').split('-')[5]
						break
				except Exception as ex:
					print('switch_kapcha_status:  ', ex)					
			if id_is != None:
				self.click_element(element_definition = lk_elements.SELECT('lk_kons_kapcha_select', mask = id_is))
		# после смены проверяем, что статус сменен и не равен старому
		timer = 0
		while True:
			if previus_kapcha_status != self.define_kapcha_status:
				loger.file_log(text = "The Kapcha switch was clicked, current status is: " + str(self.define_kapcha_status), text_type = 'SUCCESS')
				break
			if timer >= timeOut:
				loger.file_log(text = 'Can\'t switch tumbler of the  kapcha', text_type = 'ERROR  ')
				break
			timer += 1
			time.sleep(1)
		# возвращаем новый статус капчи

# консультант -- Распределение обращений
	@property
	def define_chats_distribution_state(self):
	# (!C) метод определяющий Включено\Выключено распределение чатов на странице Распределение обращений
		# находим динамическую часть id переключателя (по тексту перед выключателем)
		needed_elements =  self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'chatprocessing-page-cm-switchbox-is_chat_distribution_enabled-\'')
		if needed_elements != [None,[None], None]:
			for needed_element in needed_elements[1]:
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
		for element in elements[1]:
			try:
				if 'Положение на сайте' in element.text:
					current_element.append(element)
			except Exception as ex:
				print('Error in cons_change_widget_position: ' + str(ex))
		if len(current_element) != 1:
			loger.file_log(text = 'Was found more than one necessary element at View widget page, it\'s wrong', text_type = 'ERROR  ')
		else:
			# определяем эллементы для нажатия
			type_click = {'txt':current_element[0],'dd':self.displayed_element(element_definition = lk_elements.SELECT('lk_kons_view_dd', mask = current_element[0].get_attribute('id').split('-')[5]))[2]}
			# проверяем какое значение уже выбрано и если нужно, то выбираем новое, если не нужно то не меняем.
			current_value =  type_click.get('dd').get_attribute('value')
			if positions.get(place) == current_value:
				loger.file_log(text = 'Necessary value: ' + str(positions.get(place)) + ' already chosen. We have no necessary to change', text_type = 'SUCCESS')
			else:
				# нажимаем на элемент
				self.click_element(element_definition = type_click.get(open_dd_by))
				# проверяем, что список открыт
				dropdown_items = self.elements_list(object_type = 'li', search_type = 'contains', mask = 'class, \'x-boundlist-item\'')[1]
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
	def cons_view_define_animation_state(self):
	# (GC) определяем состояние контрола: Анимация, True=включено, False=выключено
		result = {'status_of_animation':None,'id_is':None}
		needed_elements =  self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'uisettings-page-cm-switchbox-is_animation_enabled-\'')
		
		if needed_elements != [None,[None], None]:
			for needed_element in needed_elements[1]:
				try:
					if 'Анимация' in needed_element.text:
						result['id_is'] = needed_element.get_attribute('id').split('-')[5]
						break
				except Exception as ex:
					print('setting_distribution_of_chats:  ', ex)
			
			if result.get('id_is') != None:
				# кидаем консольную команду и получаем статус кнопки (хорошо б что-нить еще придумать сюда вместо такого способа)
				result['status_of_animation'] = self.execute_console_command(command = "return window.Ext.getCmp('uisettings-page-cm-switchbox-is_animation_enabled-" + str(result.get('id_is')) + "').getValue()")
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

	def cons_view_change_animation_lable_stat(self):
		pass








	

