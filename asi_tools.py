import sys, time
import tools, start_uis_test, pageElements
import loger 
from loger import Loger as loger

# создаем объект, для использования модуля описывающего элементы на страницах
lk_elements  = pageElements.LK()

class Asi_tools(tools.Uis_tools):
	def __init__(self, driver):
		self.driver = driver

#!!! def login_to_system - перенесен в tools. 

# управление сайтами
	@property
	def sites_get_site_list(self):
	# поиск записай на странице выбирает формирует список объектов из элементов в таблице шаблонов ответа, в списке только отображенные на странице элементы
		return self.elements_list(object_type = 'table', search_type = 'contains', mask = 'id, \'sites-page-tableview-\'')

	def sites_edit_site(self, site_name = None, timeOut = 120):
		value_parametrs = []
		list_sites_elements = self.sites_get_site_list
		print(list_sites_elements)
		# находим соответствующий эллемент и получаем номер таблицы в которой он хранится и его собственный номер (реализовать проверки!!!)
		for element in list_sites_elements[1]:
			print(element.get_attribute('id'), element.text)
			if str(site_name) in element.text:
				value_parametrs.append(element.get_attribute('id').split('-')[3])
				value_parametrs.append(element.get_attribute('id').split('-')[5])
				break
		# print(value_parametrs)
		# 	# если на текущей странице ничего не нашлось, то переходим на следующую. Если нашлось, то выходим из цикла поиска выполняем удаление
		# 	# если страница последняя, а результат отрицательный то тоже выходим	
		# 	if len(value_parametrs) == 0:
		# 		# создаю список с номерами страниц (номера могут быть только int)
		# 		numbers = []
		# 		for number in pages_with_templates[0]:
		# 			try:
		# 				numbers.append(int(number))
		# 			except Exception as ex:
		# 				pass
		# 		# выполняю переход на след страницу для поиска элемента
		# 		if paging in numbers:
		# 			self.choose_paging_value(page_name = paging)
		# 			paging += 1
		# 			time.sleep(1)
		# 		else:
		# 			# обшли все доступные страницы, но шаблона не нашли
		# 			break
		# 	else:
		# 		# удаляемый шаблон найден, выходим из поиска
		# 		break		
		# if value_parametrs != []:
		self.click_element(element_definition = lk_elements.BUTTON('edit_site', mask = value_parametrs), timeOut = timeOut)
		# 	# подтверждение удаления (нажатие на кнопку: Да)
		# 	yes_button = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'ul-mainbutton-yes-\'')
		# 	for item in yes_button[1]:
		# 		if 'btnInnerEl' in item.get_attribute('id'):
		# 			self.click_element(element_definition = item, timeOut = timeOut)
		# 			break
		# 	# ожидание удаления, если количество элементов на странице изменилось, то объект удалён
		# 	time_index = 0
		# 	while True:
		# 		value_of_teamplates_after_chang = self.get_total_list_values_count()[0]
		# 		if int(before_deleting_template_values_count) - int(value_of_teamplates_after_chang) == 1:
		# 			loger.file_log(text = 'Template: ' + str(template_name) + ', was successfully deleted', text_type = 'SUCCESS')
		# 			break
				
		# 		if time_index >= timeOut:
		# 			loger.file_log(text = 'Counter of the Templates wasn\'t changed. Deleting of the ' + str(template_name) + ' failed', text_type = 'ERROR  ')
		# 			break			
		# 		time.sleep(1)
		# 		time_index += 1
		# else:
		# 	loger.file_log(text = 'Can\'t find such template name: ' + str(template_name), text_type = 'ERROR  ')


	def my_navigation(self, tab_name = None, timeOut = 120):
		mask = 'class, \'x-tab-inner\''
		tabs = self.elements_list(object_type = 'span', search_type = 'contains', mask = mask, timeOut = timeOut)[1]
		for item in tabs:
			if tab_name in item.text:
				self.click_element(element_definition = item)
		return tabs

	def navigation_int_ac_in_table(self, tab_name = None, timeOut = 120):
		mask = 'class, \'x-grid-cell-inner \''
		tabs = self.elements_list(object_type = 'div', search_type = 'contains', mask = mask, timeOut = timeOut)[1]
		for item in tabs:
			if tab_name == item.text:
				# print(item.text)
				try:
					self.click_element(element_definition = item)
					break
				except Exception as ex:
					print(ex)
		return tabs

	def navigation_int_ac_plashka(self, tab_name = None, timeOut = 120):
		# аналог top_menu_navigation но для плашки в интегрированных рк
		mask = 'class, \'x-tab-inner x-tab-inner-ul\''
		tabs = self.elements_list(object_type = 'span', search_type = 'contains', mask = mask, timeOut = timeOut)[1]
		for item in tabs:
			if tab_name in item.text:
				self.click_element(element_definition = item)
		return tabs


	def countAndShowElementsInTable(self, timeOut = 120):
		# выводит списоком значения из первого измерения
		count_list = []
		current_id = None
		mask = 'class, \'x-grid-view x-grid-with-row-lines x-fit-item x-grid-view-ul\''
		tabs = self.elements_list(object_type = 'div', search_type = 'contains', mask = mask, timeOut = timeOut)
		print(tabs[0])
		# if tabs[0] == 1:
			# current_id = tabs[1][0].get_attribute('id')#.split('-')[-1]
		# return current_id

		print('la-la-la!')
		for item in tabs[1]:
			current_id = [item.get_attribute('id'),item.is_displayed()]
		# 	print(item.text)
			count_list.append(current_id)

		print('1:')
		print(count_list)
