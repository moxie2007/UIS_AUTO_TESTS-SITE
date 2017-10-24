import tools, start_uis_test, pageElements
import loger 
from loger import Loger as loger

# создаем объект, для использования модуля описывающего элементы на страницах
lk_elements  = pageElements.LK()

class Wg_tools(tools.Uis_tools):
	def __init__(self, driver):
		self.driver = driver

# консультант -- Общие настройки -- Шаблоны сообщений
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
		if needed_elements != [None,[None]]:
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

# консультант -- Внешний вид

# консультант -- Распределение обращений