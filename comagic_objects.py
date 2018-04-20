import tools
from loger import Loger as loger

class LK(tools.Uis_tools):
	def __init__(self, driver):
		self.driver = driver

	def get_object(self, time_out = 0.5, debug = False, **kwargs):
	# (С!)метод поиска типовых объектов на странице, выдергивает первое соответствие.
	# пример передаваемых параметров
	# search_mask = {'main_type':None, 'search_type': None, 'mask': None}, - обязательно
	# element_length = {'type':None, 'length':None}, 
	# additional_parameter = {'type':None, 'value': None},  полное равенство
	# parent = {'state_type':False, 'parent_object':None})

		# задаем входные параметры
		search_mask = kwargs.get('search_mask')
		element_length = kwargs.get('element_length')
		additional_parameter = kwargs.get('additional_parameter')
		parent = kwargs.get('parent')
		# определяем выходной параметр
		result = {}
		# определяем совокупность заданных условий (ели нужно, что бы сработало не одно условие а сразу несколько)
		output_index = 0 # это параметр: сколько должно условий сработать для определения объекта
		for option in kwargs:
			if option != None:
				output_index += 1
		# поиск элементов
		step_await = self.wait_for_results()
		elements = {}
		while True:
			method_status = False
			elements = self.elements_list(object_type = search_mask.get('main_type'), search_type = search_mask.get('search_type'), mask = search_mask.get('mask'), timeOut = 0.1)
			# проверяем нашлись ли объекты и если да то ищем конкретный
			if type(elements.get('count')) == int:
				counter_index = 1 # единица - потому что первое условие: search_mask, всегда должно быть
				for item in elements.get('elements'):
					# обработка по условию: количество значений в свойстве
					if element_length != None:
						if len(item.get_attribute(element_length.get('type')).split('-')) == int(element_length.get('length')):
							if debug:
								loger.file_log(text = 'Найден эллемент на странице, через: длинну свойства тега: {}'.format(search_mask.get('search_type')) , text_type = 'DEBUG  ')
							counter_index += 1
					# обработка по условию: соответствие наименование свойства (например класс)
					if additional_parameter != None:
						if item.get_attribute(str(additional_parameter.get('type'))) == additional_parameter.get('value'):
							if debug:
								loger.file_log(text = 'Найден эллемент на странице, по вторичному признаку: {}'.format(additional_parameter.get('type')) , text_type = 'DEBUG  ')
							counter_index += 1
					# (!)проверяем является ли указанный объект родителем для найденного=перебираемого в цикле
					if parent != None:
						if self.identity_of_the_child_to_the_parent(parent = parent.get('parent_object').get('object'), child = item).get('result'):
							if debug:
								loger.file_log(text = 'Найден эллемент на странице, по вторичному признаку: {}'.format('parent/child') , text_type = 'DEBUG  ')
							counter_index += 1
					# проверяем что все условия поиска выполнены
					if counter_index == output_index:
						if debug:
							loger.file_log(text = 'Все условия поиска, их: {}, выполнены!'.format(output_index), text_type = 'DEBUG  ')
						method_status = True
						break
					else:
						counter_index = 1 # единица - потому что первое условие: search_mask, всегда должно быть
			if method_status:
				result['object'] = item
				break
			if self.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
				break
		return result

# сопоставление технических объектов мнемоникам	
	def ONOFF_BUTTON(self, element_definition = None, mask = {}, debug = False, time_out = 0.2):
	# Консультант - Чат - Оснавные настройки
		# подсказка к кнопке: Показывать на сайте
		if element_definition == 'consultant_displayed_at_site_btn_main_settings':
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'id, \'chat-page-cm-switchbox-is_visible-\''}, element_length = {'type':'id', 'length':7}, debug = debug, time_out = time_out)

	def CHECKBOX(self, element_definition = None, mask = {}, debug = False, time_out = 0.2):
	# Консультант - Чат - Оснавные настройки
		# показывать на устройствах
		if element_definition == 'consultant_displayed_at_pc_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-checkboxfield-desktop-\''}, element_length = {'type':'id', 'length':6}, debug = debug, time_out = time_out)
		if element_definition == 'consultant_displayed_at_phone_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-checkboxfield-mobile-\''}, element_length = {'type':'id', 'length':6}, debug = debug, time_out = time_out)
		if element_definition == 'consultant_displayed_at_tablet_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-checkboxfield-tablet-\''}, element_length = {'type':'id', 'length':6}, debug = debug, time_out = time_out)
		# Оператор - Оценивать оператора
		if element_definition == 'consultant_operator_evaluation_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-checkboxfield-is_operator_rating-\''}, additional_parameter = {'type':'data-ref', 'value': 'inputEl'}, debug = debug, time_out = time_out)
		# Оператор - Ограничить количество активных чатов...
		if element_definition == 'consultant_operator_limit_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-checkboxfield-is_active_operator_chat_limit_enabled-\''}, additional_parameter = {'type':'data-ref', 'value': 'inputEl'}, debug = debug, time_out = time_out)
		# Оператор - Разрешить передачу файлов между участниками чата
		if element_definition == 'consultant_allow_operator_invite_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-checkboxfield-is_file_transfer-\''}, additional_parameter = {'type':'data-ref', 'value': 'inputEl'}, debug = debug, time_out = time_out)
		# Оператор - Разрешить приглашение от оператора 
		if element_definition == 'consultant_files_transfer_allow_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-checkboxfield-is_invite-\''}, additional_parameter = {'type':'data-ref', 'value': 'inputEl'}, debug = debug, time_out = time_out)




	def LABEL(self, element_definition = None, mask = {}, debug = False, time_out = 0.2):
	# Консультант - Чат - Оснавные настройки
		# Тектс группы: показывать на устройствах
		if element_definition == 'consultant_displayed_at_devices_group_name_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-cm-enumfield-visibility-\''}, element_length = {'type':'id', 'length':7}, debug = debug, time_out = time_out)
		# текст: Показывать на сайте
		if element_definition == 'consultant_displayed_at_site_text_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-cm-switchbox-is_visible-\''}, element_length = {'type':'id', 'length':7}, debug = debug, time_out = time_out)
		# подсказка к кнопке: Показывать на сайте
		if element_definition == 'consultant_displayed_at_site_help_text_main_settings':
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'id, \'chat-page-ul-statictip-switchboxLabel-\''}, element_length = {'type':'id', 'length':6}, debug = debug, time_out = time_out)
		# текст: Текст на баннере		
		if element_definition == 'consultant_banner_text_text_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-textfield-title-\''}, element_length = {'type':'id', 'length':6}, debug = debug, time_out = time_out)	
		# подсказка о количестве введенных символов в значении текст на баннере
		if element_definition == 'consultant_help_text_used_symbols_banner_text_text_main_settings':
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'id, \'chat-page-textfield-title-\''}, element_length = {'type':'id', 'length':6}, debug = debug, time_out = time_out)
		# Текст, группы: Запрос анкетных данных
		if element_definition == 'consultant_personal_data_request_header_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-fieldcontainer-\''}, element_length = {'type':'id', 'length':5}, debug = debug, time_out = time_out)	
		# Текст: ФИО, в блоке: Запрос анкетных данных
		if element_definition == 'consultant_personal_data_text_name_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-services-oc-chat-personalinfocombo-require_name-\''}, element_length = {'type':'id', 'length':9}, additional_parameter = {'type':'data-ref', 'value':'labelEl'}, debug = debug, time_out = time_out)
		# Текст: Телефон, в блоке: Запрос анкетных данных
		if element_definition == 'consultant_personal_data_text_phone_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-services-oc-chat-personalinfocombo-require_phone-\''}, element_length = {'type':'id', 'length':9}, additional_parameter = {'type':'data-ref', 'value':'labelEl'}, debug = debug, time_out = time_out)
		# Текст: E-mail, в блоке: Запрос анкетных данных
		if element_definition == 'consultant_personal_data_text_email_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-services-oc-chat-personalinfocombo-require_email-\''}, element_length = {'type':'id', 'length':9}, additional_parameter = {'type':'data-ref', 'value':'labelEl'}, debug = debug, time_out = time_out)
		# Текст, группы: Оператор
		if element_definition == 'consultant_personal_data_operator_header_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-label-\''}, element_length = {'type':'id', 'length':4}, debug = debug, time_out = time_out)
		# Текст: Оценка оператора, в секции: Оператор
		if element_definition == 'consultant_operator_evaluation_text_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-checkboxfield-is_operator_rating-\''}, additional_parameter = {'type': 'data-ref', 'value': 'boxLabelEl'}, debug = debug, time_out = time_out)	
		# Оператор - Ограничить количество активных чатов...
		if element_definition == 'consultant_operator_limit_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-checkboxfield-is_active_operator_chat_limit_enabled-\''}, additional_parameter = {'type': 'data-ref', 'value': 'boxLabelEl'}, debug = debug, time_out = time_out)
		# Оператор - Разрешить передачу файлов между участниками чата, текст на странице
		if element_definition == 'consultant_allow_operator_invite_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-checkboxfield-is_file_transfer-\''}, additional_parameter = {'type': 'data-ref', 'value': 'boxLabelEl'}, debug = debug, time_out = time_out)
		# Оператор - Разрешить приглашение от оператора 
		if element_definition == 'consultant_files_transfer_allow_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-checkboxfield-is_invite-\''}, additional_parameter = {'type': 'data-ref', 'value': 'boxLabelEl'}, debug = debug, time_out = time_out)
		# Оператор - Минимальное время нахождения посетителя на сайте (сек.): 
		if element_definition == 'consultant_files_min_time_at_site_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-numberfield-min_duration_for_invite-\''}, additional_parameter = {'type': 'data-ref', 'value': 'labelEl'}, debug = debug, time_out = time_out)




	# global ________________________________________________________________________________________________________________________________________
		# текст на подсказке (появляется после наведения курсора на иконку)	
		if element_definition == 'consultant_personal_data_help_text_from_icon_main_settings':
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'id, \'ext-quicktips-tip-body\''}, element_length = {'type':'id', 'length':4}, debug = debug, time_out = time_out)
		



	def INPUT(self, element_definition = None, mask = {}, debug = False, time_out = 0.2):
	# Консультант - Чат - Оснавные настройки
		# Поле ввода: Текст на баннере, само поле ввода
		if element_definition == 'consultant_input_for_banner_text_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-textfield-title-\''}, element_length = {'type':'id', 'length':6}, debug = debug, time_out = time_out)
		# Оператор - Ограничить количество активных чатов...
		if element_definition == 'consultant_operator_limit_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-numberfield-active_operator_chat_limit-\''}, additional_parameter = {'type': 'data-ref', 'value': 'inputEl'}, debug = debug, time_out = time_out)
		# Оператор - Минимальное время нахождения посетителя на сайте (сек.): 
		if element_definition == 'consultant_files_min_time_at_site_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-numberfield-min_duration_for_invite-\''}, additional_parameter = {'type': 'data-ref', 'value': 'inputEl'}, debug = debug, time_out = time_out)




	def ICONS(self, element_definition = None, mask = {}, debug = False, time_out = 0.2):
	# Консультант - Чат - Оснавные настройки
		# Иконка подсказки рядом с текстом: Запрос анкетных данных
		if element_definition == 'consultant_personal_data_request_icon_main_settings':
			curent_parent = self.LABEL(element_definition = 'consultant_personal_data_request_header_main_settings', debug = debug)
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'class, \'ul-helpiconizer-labelable\''}, parent = {'state_type':True, 'parent_object':curent_parent}, debug = debug, time_out = time_out)
		# Иконка подсказки рядом с текстом: Запрос анкетных данных
		if element_definition == 'consultant_operator_evaluation_icon_main_settings':
			curent_parent = self.LABEL(element_definition = 'consultant_operator_evaluation_text_main_settings', debug = debug)
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'class, \'ul-helpiconizer ul-helpiconizer-labelable\''}, parent = {'state_type':True, 'parent_object':curent_parent}, debug = debug, time_out = time_out)
		# Иконка подсказки рядом с текстом: Разрешить приглашение от оператора
		if element_definition == 'consultant_files_transfer_allow_icon_main_settings':
			curent_parent = self.LABEL(element_definition = 'consultant_files_transfer_allow_main_settings', debug = debug)
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'class, \'ul-helpiconizer ul-helpiconizer-labelable\''}, parent = {'state_type':True, 'parent_object':curent_parent}, debug = debug, time_out = time_out)










	def DROP_DOWN_FIELD(self, element_definition = None, mask = {}, debug = False, time_out = 0.2):
	# Консультант - Чат - Оснавные настройки
		# Поле поле выпадающего списка: ФИО
		if element_definition == 'consultant_field_dd_name_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-services-oc-chat-personalinfocombo-require_name-\''}, element_length = {'type':'id', 'length':9}, additional_parameter = {'type':'data-ref', 'value': 'inputEl'},debug = debug, time_out = time_out)
		# Поле поле выпадающего списка: Телефон
		if element_definition == 'consultant_field_dd_phone_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-services-oc-chat-personalinfocombo-require_phone-\''}, element_length = {'type':'id', 'length':9}, additional_parameter = {'type':'data-ref', 'value': 'inputEl'},debug = debug, time_out = time_out)
		# Поле поле выпадающего списка: E-mail
		if element_definition == 'consultant_field_dd_email_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-services-oc-chat-personalinfocombo-require_email-\''}, element_length = {'type':'id', 'length':9}, additional_parameter = {'type':'data-ref', 'value': 'inputEl'},debug = debug, time_out = time_out)