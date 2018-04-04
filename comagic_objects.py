import tools
from loger import Loger as loger

class LK(tools.Uis_tools):
	def __init__(self, driver):
		self.driver = driver

	def get_object(self, search_mask = {'main_type':None, 'search_type': None, 'mask': None}, element_length = {'type':None, 'length':None}, 
		additional_parameter = {'type':None, 'value': None}, time_out = 0.5, debug = False):
	# метод поиска типовых объектов на странице, выдергивает первое соответствие.
		result = {}
		step_await = self.wait_for_results()
		elements = {}
		while True:
			method_status = False
			elements = self.elements_list(object_type = search_mask.get('main_type'), search_type = search_mask.get('search_type'), mask = search_mask.get('mask'), timeOut = 0.1)
			# проверяем нашлись ли объекты и если да то ищем конкретный
			if type(elements.get('count')) == int:
				for item in elements.get('elements'):
					# обработка по условию: количество значений в свойстве
					if element_length.get('type') != None:
						if len(item.get_attribute(element_length.get('type')).split('-')) == int(element_length.get('length')):
							if debug:
								loger.file_log(text = 'Найден эллемент на странице, через: длинну свойства тега: {}'.format(search_mask.get('search_type')) , text_type = 'DEBUG  ')
							method_status = True
							break
					# обработка по условию: соответствие наименование свойства (например класс)
					if additional_parameter.get('type') != None:
						if item.get_attribute(str(additional_parameter.get('type'))) == additional_parameter.get('value'):
							if debug:
								loger.file_log(text = 'Найден эллемент на странице, по вторичному признаку: {}'.format(additional_parameter.get('type')) , text_type = 'DEBUG  ')
							method_status = True
							break
			if method_status:
				result['object'] = item
				break
			if self.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
				break
		return result

# сопоставление технических объектов мнемоникам	

	def CHECKBOX(self, element_definition = None, mask = {}):
	# Консультант - Чат - Оснавные настройки
		# показывать на устройстве
		if element_definition == 'consultant_displayed_at_pc_main_settings':
			return self.get_object(search_mask = {'main_type':'input', 'search_type': 'contains', 'mask': 'id, \'chat-page-checkboxfield-desktop-\''}, element_length = {'type':'id', 'length':6})







	
	