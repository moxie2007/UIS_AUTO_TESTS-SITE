import tools
import time
from loger import Loger as loger

class LK(tools.Uis_tools):
	def __init__(self, driver):
		self.driver = driver

	def get_object(self, time_out = 0.5, debug = False, search_type = 'one', **kwargs):
	# (С!)метод поиска типовых объектов на странице, выдергивает по умолчанию первое соответствие.
	# пример передаваемых параметров
	# search_type = 'one', - по умолчанию ищет первый элемент, варианты передаваемых значений: one, all.
	# search_mask = {'main_type':None, 'search_type': None, 'mask': None}, - обязательно
	# element_length = {'type':None, 'length':None}, 
	# additional_parameter = {'type':None, 'value': None, 'operation': None}, operation=None. это полное равенство. in=вхождение 
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
				looking_elements = []
				for item in elements.get('elements'):
					# обработка по условию: количество значений в свойстве
					if element_length != None:
						# print('TEST:  ',len(item.get_attribute(element_length.get('type')).split('-')), '  :  ', element_length.get('length'))
						if len(item.get_attribute(element_length.get('type')).split('-')) == int(element_length.get('length')):
							if debug:
								loger.file_log(text = 'Найден эллемент на странице, через: длинну свойства тега: {}'.format(search_mask.get('search_type')) , text_type = 'DEBUG  ')
							counter_index += 1
					# обработка по условию: соответствие наименование свойства (например класс)
					if additional_parameter != None:
						if additional_parameter.get('operation') == None:
							if item.get_attribute(str(additional_parameter.get('type'))) == additional_parameter.get('value'):
								if debug:
									loger.file_log(text = 'Найден эллемент на странице, по вторичному признаку: {}'.format(additional_parameter.get('type')) , text_type = 'DEBUG  ')
								counter_index += 1
						if str(additional_parameter.get('operation')).lower() == 'in':
							if str(additional_parameter.get('value')) in str(item.get_attribute(str(additional_parameter.get('type')))):
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
						if search_type == 'one':
							method_status = True
							break
						if search_type == 'all':
							method_status = True
							print(item)
							if item not in looking_elements:
								looking_elements.append(item)
					else:
						counter_index = 1 # единица - потому что первое условие: search_mask, всегда должно быть
			if method_status:
				if search_type == 'one':
					result['object'] = item
					break
				if search_type == 'all':
					result['objects_list'] = looking_elements
					break
			if self.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
				if debug:
					loger.file_log(text = 'Не нашли элемент/ты, условий соответствия ожидалось: {}, было найдено: {}!'.format(output_index, counter_index), text_type = 'DEBUG  ')
				break
		return result

# сопоставление технических объектов мнемоникам	
	def ONOFF_BUTTON(self, element_definition = None, mask = {}, debug = False, time_out = 0.2):
	# Консультант - Чат - Оснавные настройки
		# подсказка к кнопке: Показывать на сайте
		if element_definition == 'consultant_displayed_at_site_btn_main_settings':
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'id, \'chat-page-cm-switchbox-is_visible-\''}, element_length = {'type':'id', 'length':7}, debug = debug, time_out = time_out)
		# Настройка распределения чатов
		if element_definition == 'consultant_chat_distribution_btn_main_settings':
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'id, \'chat-page-cm-switchbox-is_chat_distribution_enabled-\''}, additional_parameter = {'type':'data-ref', 'value': 'bodyEl'}, debug = debug, time_out = time_out)
	# Консультант - Чат - Удерживающие сообщения
		# Показывать в чате
		if element_definition == 'consultant_show_in_chat_hold_messages':
			return self.get_object(search_mask = {'main_type':'a', 'search_type': 'contains', 'mask': 'id, \'chat-page-cm-switchbox-chat_retention_is_enabled-\''}, element_length = {'type':'id', 'length':7}, debug = debug, time_out = time_out)
		# Показывать форму
		if element_definition == 'consultant_show_form_hold_messages':
			return self.get_object(search_mask = {'main_type':'a', 'search_type': 'contains', 'mask': 'id, \'chat-page-cm-switchbox-chat_retention_is_alternate_communication_way_enabled-\''}, element_length = {'type':'id', 'length':7}, debug = debug, time_out = time_out)
		
	def BUTTON(self, element_definition = None, mask = {}, debug = False, time_out = 0.2):
	# Консультант - Чат - Оснавные настройки
		# кнопка редактирования распределения по сегментам
		if element_definition == 'consultant_segment_edit_btn_main_settings':
			return self.get_object(search_mask = {'main_type':'a', 'search_type': 'contains', 'mask': 'id, \'chat-page-ul-usualbutton-segmentEditBtn-\''}, element_length = {'type':'id', 'length':6}, debug = debug, time_out = time_out)
		# кнопка редактирования распределения по сегментам
		if element_definition == 'consultant_add_group_btn_main_settings':
			return self.get_object(search_mask = {'main_type':'span', 'search_type': 'contains', 'mask': 'id, \'chat-page-cm-commongrid-\''}, element_length = {'type':'id', 'length':7}, additional_parameter = {'type':'id', 'operation':'in', 'value':'btnEl'}, debug = debug, time_out = time_out)
		# кнопка: Отмена, всей формы
		if element_definition == 'consultant_cancel_btn_main_settings':
			return self.get_object(search_mask = {'main_type':'span', 'search_type': 'contains', 'mask': 'id, \'chat-page-ul-linklikebutton-cancel-\''}, additional_parameter = {'type':'data-ref', 'value':'btnInnerEl'}, debug = debug, time_out = time_out)
		# кнопка: Сохранить, всей формы
		if element_definition == 'consultant_save_btn_main_settings':
			return self.get_object(search_mask = {'main_type':'span', 'search_type': 'contains', 'mask': 'id, \'chat-page-ul-mainbutton-saveRecord-\''}, additional_parameter = {'type':'data-ref', 'value':'btnInnerEl'}, debug = debug, time_out = time_out)

	def RADIO_BUTTON(self, element_definition = None, mask = {}, debug = False, time_out = 0.2):
	# Консультант - Чат - Оснавные настройки
		# кнопка: По сегментам
		if element_definition == 'consultant_segment_edit_rbtn_main_settings':
			curent_parent = self.LABEL(element_definition = 'consultant_segment_edit_text_main_settings', debug = debug)
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-radiofield-chatprocessingConfig-\''}, additional_parameter = {'type':'data-ref', 'value': 'inputEl'},  parent = {'state_type':True, 'parent_object':curent_parent}, debug = debug, time_out = time_out)
				
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
		# Подсказка: Распределение чатов идет на всех операторов
		if element_definition == 'consultant_chat_distribution_help_text_main_settings':
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'id, \'chat-page-ul-statictip-textHelpIsChatDistributionEnabled-\''}, element_length = {'type':'id', 'length':6}, debug = debug, time_out = time_out)
		# Подсказка об использующихся в распределении по сегментам правил
		if element_definition == 'consultant_segment_edit_help_text_main_settings':
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'id, \'chat-page-ul-statictip-textHelpSegment-\''}, element_length = {'type':'id', 'length':6}, debug = debug, time_out = time_out)
		

		# тут нужно переопределить так как объекты не имеют уникального определения
		# # текст: По сегментам, при включенном меню: настройка распределения чаттов
		# if element_definition == 'consultant_segment_edit_text_main_settings':
		# 	return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'id, \'chat-page-radiofield-chatprocessingConfig-\''}, additional_parameter = {'type': 'data-ref', 'value': 'innerWrapEl'}, debug = debug, time_out = time_out)
		# # текст: По группе сотрудников, при включенном меню: настройка распределения чаттов
		# if element_definition == 'consultant_group_edit_text_main_settings':
		# 	return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'id, \'chat-page-radiofield-chatprocessingConfig-\''}, additional_parameter = {'type': 'data-ref', 'value': 'innerWrapEl'}, debug = debug, time_out = time_out)


		# Заголовок над наименование для групп: Название поля выбора группы:
		if element_definition == 'consultant_groups_name_text_main_settings':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-textfield-staff_group_title-\''},  additional_parameter = {'type': 'data-ref', 'value': 'labelEl'}, debug = debug, time_out = time_out)
		
	# Консультант - Чат - Удерживающие сообщения
		# Подсказка в заголовке страницы (на желтом фоне)
		if element_definition == 'consultant_top_help_text_hold_messages':
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'id, \'chat-page-component-infoText-\''}, element_length = {'type':'id', 'length':5}, debug = debug, time_out = time_out)
		# Подсказка перед кнопкой: Показывать в чате
		if element_definition == 'consultant_show_in_chat_hold_messages':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-cm-switchbox-chat_retention_is_enabled-\''}, additional_parameter = {'type': 'data-ref', 'value': 'labelEl'}, debug = debug, time_out = time_out)
		# лейбл показа формы перед ВКЛ\ВЫКЛ кнопкой
		if element_definition == 'consultant_show_form_hold_messages':
			return self.get_object(search_mask = {'main_type':'label', 'search_type': 'contains', 'mask': 'id, \'chat-page-cm-switchbox-chat_retention_is_alternate_communication_way_enabled-\''}, additional_parameter = {'type': 'data-ref', 'value': 'labelEl'}, debug = debug, time_out = time_out)
		

		# ----------------------------------------------------------------------------------------
		# груповые объекты
		# == Заголовок блока ==
		if element_definition == 'consultant_block_header_hold_messages':
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'id, \'chat-page-title-\''}, additional_parameter = {'type': 'data-ref', 'value': 'textEl'}, debug = debug, search_type = 'all', time_out = time_out)
		
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
		# поле ввода для групп: Название поля выбора группы:
		if element_definition == 'consultant_groups_name_text_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-textfield-staff_group_title-\''}, additional_parameter = {'type': 'data-ref', 'value': 'inputEl'}, debug = debug, time_out = time_out)
	# Консультант - Чат - Удерживающие сообщения
		# ----------------------------------------------------------------------------------------
		# груповые объекты
		# поле ввода текста удерживающего сообщения
		if element_definition == 'consultant_text_hold_messages':
			return self.get_object(search_mask = {'main_type':'textarea', 'search_type': 'contains', 'mask': 'id, \'chat-page-textareafield-message_text-\''}, search_type = 'all', debug = debug, time_out = time_out)
		

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
	# Консультант - Чат - Удерживающие сообщения
		# выбор группы (input, открывающий выпадающий список) 
		if element_definition == 'consultant_field_dd_form_type_hold_messages':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-ul-combobox-chat_retention_alternate_communication_way-\''}, element_length = {'type':'id', 'length':7}, additional_parameter = {'type':'data-ref', 'value': 'inputEl'},debug = debug, time_out = time_out)
		# Поле поле выпадающего списка: через
		if element_definition == 'consultant_field_dd_through_hold_messages':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-ul-combobox-chat_retention_alternate_communication_way_timeout-\''}, element_length = {'type':'id', 'length':7}, additional_parameter = {'type':'data-ref', 'value': 'inputEl'},debug = debug, time_out = time_out)
		



	def LINK(self, element_definition = None, mask = {}, debug = False, time_out = 0.2):
	# Консультант - Чат - Распределение обращений по сегментам
		# ссылка возвращающая из распределения по сегментам в настройку распределения обращений
		if element_definition == 'consultant_segment_distribution_main_settings':
			return self.get_object(search_mask = {'main_type':'a', 'search_type': 'contains', 'mask': 'id, \'chat-segmenthandlingdistribution-cm-backbutton-back-back-\''}, element_length = {'type':'id', 'length':7},debug = debug, time_out = time_out)
		
	def GLOBAL_BLOCK_SECTION(self, element_definition = None, mask = {}, debug = False, time_out = 0.2):
	# Консультант - Чат - Удерживающие сообщения
		# блок удерживающего сообщения, общий поиск, потому что разница блока только в динамическом id
		if element_definition == 'parent_for_consultant_block_hold_messages':
			return self.get_object(search_mask = {'main_type':'div', 'search_type': 'contains', 'mask': 'id, \'chat-page-services-oc-chat-chatretentionmessagepanel-\''}, element_length = {'type':'id', 'length':7}, search_type = 'all', debug = debug, time_out = time_out)
	