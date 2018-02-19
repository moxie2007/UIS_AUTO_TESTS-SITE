import sys, time, datetime
# import datetime
import tools, start_uis_test, pageElements
import loger 
from loger import Loger as loger

# создаем объект, для использования модуля описывающего элементы на страницах
lk_elements  = pageElements.LK()

class Vats_tools(tools.Uis_tools):
	def __init__(self, driver):
		self.driver = driver

	def dash_define_existing_dashboards(self, time_out = 120, skip_error_message = False, DEBUG = False):
	# (C!G)определяем существующие дашборды, возвращаем название, объект, стату(выбран объект или нет)
	# тут надо добавить проверка на видимую кнопку добавить Даш, что б не ждать лишнего, когда нет дашбордов
		step_await = self.wait_for_results()
		method_status = False
		result = {}
		indexing_step = 0 #условие на случай если кнопка добавить будет появляться раньше вкладок
		while True:
			method_status = False
			# определяем есть ли иконка: Добавить дашюорд
			if self.displayed_element(element_definition = lk_elements.BUTTON('dash_top_menu_add_btn'),  timeOut = 3).get('state'):
				# ищем вкладки, вкладок может и не быть
				new_elems = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'data-boundview, \'dashboards-page-analytics-dashboards-tabbar-tabbar-mode-\'', timeOut = 1)
				# пытаемся получить для каждой вкладки данные
				if type(new_elems.get('count')) == int:
					for current_item_index in range(new_elems.get('count')):
						try:
							if 'active' in new_elems.get('elements')[current_item_index].get_attribute('class'):
								result[new_elems.get('elements')[current_item_index]] = {'name':new_elems.get('elements')[current_item_index].text,'status':True}
							else:
								result[new_elems.get('elements')[current_item_index]] = {'name':new_elems.get('elements')[current_item_index].text,'status':False}
						except Exception as ex:
							pass
					if len(result) == new_elems.get('count'):
						method_status = True
					else:
						result.clear()
			if method_status:
				break
			if self.wait_for_results (time_data = step_await, time_out = (time_out) + 1).get('result'):
				break
			time.sleep(0.1)
		return result
		
	def dash_create_new_dashboard(self, dash_board_name = None, timeOut = 120, breakONerror = False):
	# (С) создаем новый Дашборд. считаем, что вкладка\страница уже открыта и количество доступных меньше допустимого максимума
		method_status = False
		# получаем текущее состояние вкладки дашборды
		current_dashboards_state = self.dash_define_existing_dashboards(skip_error_message = True, time_out = 3)
		# находим иконку для добавления и нажимаем
		add_buttons = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'dashboards-page-button-\'', timeOut = 5)
		if type(add_buttons.get('count')) == int:
			for add_button in add_buttons.get('elements'):
				if add_button.get_attribute('data-ref') == 'btnIconEl':
					self.click_element(element_definition = add_button)
					method_status = True
					break
		# ожидаем открывания формы\окна и поля ввода имени Дашборда и вводи имя нового Дашборда
		if method_status:
			time_index = 0
			while True:
				method_status = False
				dashboard_name_fields = self.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'dashboards-page-textfield-name-\'', timeOut = 1)
				if type(dashboard_name_fields.get('count')) == int:
					for current_obj in dashboard_name_fields.get('elements'):
						if 'inputEl' in current_obj.get_attribute('id').split('-'):
							self.change_value(element_definition = current_obj, text = str(dash_board_name))
							method_status = True
				if method_status:
					break
				if time_index >= timeOut:
					loger.file_log(text = 'Can\'t change Dashboard name', text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						self.close_browser
						sys.exit()
					break
				time.sleep(1)
				time_index += 1
		# находим и нажимаем кнопку: Создать
		if method_status:
			time_index = 0
			while True:
				method_status = False
				dashboard_save_btns = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'id, \'dashboards-page-ul-mainbutton-save-\'', timeOut = 1)
				if type(dashboard_save_btns.get('count')) == int:
					for dashboard_save_btn in dashboard_save_btns.get('elements'):
						self.click_element(element_definition = dashboard_save_btn)
						method_status = True
				if method_status:
					break
				if time_index >= timeOut:
					loger.file_log(text = 'Can\'t click to the Create button', text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						self.close_browser
						sys.exit()
					break
				time.sleep(1)
				time_index += 1
		# ожидаем, что активная вкладка - это вновь созданная (логика работы системы)
		if method_status:
			# time_index = 0
			step_await = self.wait_for_results()
			while True:
				method_status = False
				# проверяем есть ли кнопка: Плюсик, на странице
				add_buttons = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'dashboards-page-button-\'', timeOut = 1)		
				if type(add_buttons.get('count')) == int:
				# if type(add_buttons.get('count')) == int and method_status == False:
				# получаем состояние дашбордов (все вкладки)
				# -----------------------------------------------------------------------------------------------------------------------
				# -----------------------------------------------------------------------------------------------------------------------
				# -----------------------------------------------------------------------------------------------------------------------
				# -----------------------------------------------------------------------------------------------------------------------
				# -----------------------------------------------------------------------------------------------------------------------
				# переписать появление результаов
					tabs_count = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'data-boundview, \'dashboards-page-analytics-dashboards-tabbar-tabbar-mode-\'').get('count')
					if type(tabs_count) == int:
						if tabs_count - len(current_dashboards_state) == 1:





							# try:
							end_method_state = self.dash_define_existing_dashboards(skip_error_message = True, time_out = 2)
							# print(len(end_method_state), len(current_dashboards_state))
							# if len(end_method_state) - len(current_dashboards_state) == 1:
							# ищем какая вкладка в статусу True
							for current_object in end_method_state:
								if end_method_state.get(current_object).get('status'):
									# проверяем если эта вкладка по имени совпадает с той которую хотели создать, то выходим
									if end_method_state.get(current_object).get('name') == dash_board_name:
										loger.file_log(text = 'New dashboard with name:{} was created'.format(dash_board_name), text_type = 'SUCCESS')
										method_status = True		
							# except Exception as ex:
							# 	print(ex)
				if method_status:
					break
				if self.wait_for_results (time_data = step_await, time_out = timeOut).get('result'):
					loger.file_log(text = 'Another dashboard should be active', text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						self.close_browser
						sys.exit()
					break
				# time.sleep(1)
				# time_index += 1

	def dash_delete_dashboard(self, dash_board_name = None, breakONerror = False, time_out = 120):
	# (С!)удаляем дашборд, для удаления используем название. Удаляем один из многих подходящий дашборд (переделать)
		method_status = False
		# получаем список всех имеющихся дашбордов (предполагаем что они есть)
		existing_dashboards = self.dash_define_existing_dashboards(time_out = 5)
		state_befor_deleting = existing_dashboards #фиксируем состояние до удаления, для сравнения с результатом по завершению метода
		# получаем список всех созданных дашбордов и если он не пустой то находим выбранный
		if len(existing_dashboards.keys()) > 0:
			# today = datetime.datetime.today()
			# start_method_time = today.timestamp()  Это возможно уже не надо
			step_await = self.wait_for_results()
			while True:
				method_status = False
				for dash_board in existing_dashboards.keys():
					if existing_dashboards.get(dash_board).get('status'):
						# проверяем, совпадает ли название удаляемого даша и если нет, то переключаемся на нужный
						if existing_dashboards.get(dash_board).get('name') == dash_board_name:
							# print(existing_dashboards.get(dash_board),existing_dashboards.get(dash_board).get('name'), type(dash_board), dash_board)
							# наводим курсор на объект
							self.move_cursor_to_the_object(current_object = dash_board)
							# если иконка редактирования появилась, то дальше иначе снова наводим курсор
							if type(self.elements_list(object_type = 'span', search_type = 'contains', mask = 'class, \'x-tab-edit-btn-inner\'', timeOut = 1).get('count')) == int:
								method_status = True
							break
				# если искомая вкладка не была найдена в статусе актив то смотрим, а есть ли нужная вкладка и если ДА то кликаем на нее
				# если вкладки нет вообще, то нужно прервать метод (выходим из if в статусе False)
				if dash_board_name in existing_dashboards.keys() and method_status == False:
					self.click_element(element_definition = existing_dashboards.get(dash_board_name).get('object'), scroll_to_element = False)
					existing_dashboards = self.dash_define_existing_dashboards()
				if dash_board_name not in existing_dashboards.keys() and method_status == False:
					loger.file_log(text = 'There is no dasboard with name: {}\t. Method: vats_tools.dash_delete_dashboard'.format(dash_board_name), text_type = 'ERROR  ')
					break
				if method_status:
					break
				# если время вышло, а результат ожидаемый не получен
				if self.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t click to the Create button', text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						self.close_browser
						sys.exit()
					break				
		# ищем иконку редактирования дашборда и нажимаем на нее	
		if method_status:
			step_await = self.wait_for_results()
			while True:
				method_status = False
				edit_tabs_btns = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'class, \'x-tab-edit-btn-inner\'', timeOut = 1)
				# перебираем все найденные и если есть тот, который является потомком вкладки, жмем\кликаем на него
				if type(edit_tabs_btns.get('count')) == int:
					for edit_btn in edit_tabs_btns.get('elements'):
				
						if self.identity_of_the_child_to_the_parent(parent = existing_dashboards.get(dash_board_name).get('object'), child = edit_btn).get('result'):
							self.click_element(element_definition = edit_btn)
							method_status = True
				
				if method_status:
					break
				if self.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t click to the Create button', text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						self.close_browser
						sys.exit()
		# ищем кнопки..\иконку удаления и их родительские объекты
		if method_status:
			delete_btns_list = {}
			step_await = self.wait_for_results()
			while True:
				method_status = False
				delete_tabs_btns = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'componentid, \'dashboards-page-ul-usualbutton-remove-\'', timeOut = 1)
				# перебираем все найденные и собираем в словарь (объект, родитель)
				if type(delete_tabs_btns.get('count')) == int:
					for delete_btn in delete_tabs_btns.get('elements'):
						delete_btns_list[delete_btn] = self.get_parent(current_object = delete_btn)
					method_status = True
				if method_status:
					break
				if self.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t find the Garbage\Delete icon button', text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						self.close_browser
						sys.exit()
		# ищем поле редактирования названия Дашборда
		if method_status:
			step_await = self.wait_for_results()
			while True:
				method_status = False
				edit_tabs_fields = self.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'dashboards-page-ul-editabledisplayfield-name-\'', timeOut = 1)
				# ищем перебором тот объект значение которого совпадает с dash_board_name
				if type(edit_tabs_fields.get('count')) == int:
					for edit_field in edit_tabs_fields.get('elements'):
						if edit_field.get_attribute('value') == dash_board_name:
							# проходим по всем кнопкам удаления и у которой родитель совпадает с текстом - название Дашборда удаляем (такая должна быть одна - потому что открыть одновременно можно только одну)
							for current_parent in delete_btns_list.keys():
								if self.identity_of_the_child_to_the_parent(parent = delete_btns_list.get(current_parent), child = edit_field).get('result'):
									self.click_element(element_definition = current_parent)
									method_status = True
									break
				if method_status:
					break
				if self.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t click to the delete button. Method: dash_delete_dashboard', text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						self.close_browser
						sys.exit()
		# проверяем, что осталось вкладок на одну меньше
		if method_status:
			step_await = self.wait_for_results()
			while True:
				# ищем кнопку добавления нового Дашборда, после удаления она однозначно должна быть
				add_buttons = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'dashboards-page-button-\'', timeOut = 1)
				if type(add_buttons.get('count')) == int:
					# если размер количества уменьшился на 1, то считаем что удаление прошло успешно
					if len(state_befor_deleting) - len (self.dash_define_existing_dashboards(time_out = 1, skip_error_message = True)) == 1:
						method_status = True
				if method_status:
					break	
				if self.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t delete dashboard (result check). Method: dash_delete_dashboard', text_type = 'ERROR  ')
					if breakONerror is True:
						loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
						self.close_browser
						sys.exit()
		
		if method_status:
			loger.file_log(text = 'Dashboard: {}, was deleted'.format(dash_board_name), text_type = 'SUCCESS')
			return True
		if method_status == False:
			loger.file_log(text = 'Can\'t delete dashboard: {}'.format(dash_board_name), text_type = 'ERROR  ')
			return False
			if breakONerror is True:
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				self.close_browser
				sys.exit()

	def dash_define_widgets_at_dashboard(self, time_out = 120):
	# (СG) метод определяющий общее количество виджетов на дашборде, возвращает созданные не пустые
		method_status = False
		dashboard_elements = {}
		dashboard_boxes = 0
		test_step_await = self.wait_for_results()
		while True:
			try:
				# пироги
				all_pies = []
				pie = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-analytics-dashboards-piedash-\'',timeOut = 1)
				for pie_widget in pie.get('elements'):
					if str(pie_widget.get_attribute('class')) == 'x-container analytics-dashboards-dash x-container-ul x-box-layout-ct':
						dashboard_boxes += 1
						all_pies.append(pie_widget)
			except:
				pass					
			try:
				# пустые блоки
				empty = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-container-emptydash-component-\'',timeOut = 1)
				for empty_widget in empty.get('elements'):
					if 'x-container analytics-dashboards-emptydash x-container-ul' in str(empty_widget.get_attribute('class')):
						dashboard_boxes += 1
			except:
				pass	
			try:
				all_histograms = []
				# гистограмма
				gisto = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-analytics-dashboards-columndash-\'',timeOut = 1)
				for gistogramma in gisto.get('elements'):
					if 'x-container analytics-dashboards-dash x-container-ul x-box-layout-ct' == str(gistogramma.get_attribute('class')):
						dashboard_boxes += 2
						all_histograms.append(gistogramma)
			except:
				pass	
			try:
				all_graphs = []
				# грфик
				graphs = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-analytics-dashboards-linedash-\'',timeOut = 1)
				for graph in graphs.get('elements'):
					if 'x-container analytics-dashboards-dash x-container-ul x-box-layout-ct' == str(graph.get_attribute('class')):
						dashboard_boxes += 4
						all_graphs.append(graph)
			except:
				pass
			try:
				all_stikers = []
				# стикер
				stikers = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-analytics-dashboards-stickerdash-\'',timeOut = 1)
				for stiker in stikers.get('elements'):
					if 'x-container analytics-dashboards-dash x-container-ul x-box-layout-ct' == str(stiker.get_attribute('class')):
						dashboard_boxes += 1
						all_stikers.append(stiker)
			except:
				pass
			# проверяем нашли ли мы все элементы на конкретном дашборде
			if dashboard_boxes == 12:
				method_status = True
			else:
				# если нет то количество найденых значений обнуляем
				dashboard_boxes = 0
			# условие выхода из цикла: или найдены все элементы или истекло время поиска
			if method_status == True:
				# dashboard_elements = {'existing_widgets':{'sticker':all_stikers, 'pie':all_pies, 'histogram':all_histograms, 'graph':all_graphs}} 
				dashboard_elements['existing_widgets'] = {'sticker':all_stikers, 'pie':all_pies, 'histogram':all_histograms, 'graph':all_graphs}
				break
			if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
				loger.file_log(text = 'Can\'t find dashboard, you should check current element at page by yourself', text_type = 'ERROR  ')
				method_status = False
				break	
		return dashboard_elements

	def dash_get_widget_name(self, widget = None):
	#(CG) определяем заголовок виджета, в метод нужно передать объект (квадрат самого виджета)
		result = None
		# ищем все заголовки с дашборда
		try:
			widget_headers = self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'dashboards-page-label-title-\'').get('elements')
			# проверяем относится ли конкретный заголовок к родительскому дашу и если Да, то возвращаем текст заголовка
			for header in widget_headers:
				if self.identity_of_the_child_to_the_parent(parent = widget, child = header).get('result'):
					result = header.text
					break
		except:
			loger.file_log(text = 'Can\'t find widget headers, method: va.dash_get_widget_name', text_type = 'ERROR  ')
		return result

	def dash_get_widget_legend(self, widget = None):
	#(CG) определяем легенду виджета, в метод нужно передать объект (квадрат самого виджета)
	# возвращает или легенду или None
		result = None
		# ищем все заголовки с дашборда
		try:
			widget_legend = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-component-description-\'').get('elements')
			# проверяем относится ли конкретный блок с легендой к родительскому дашу и если Да, то запоминаем этот объект
			for legend_section in widget_legend:
				if self.identity_of_the_child_to_the_parent(parent = widget, child = legend_section).get('result'):
					result = legend_section.text
					break
		except Exception as ex:
			loger.file_log(text = 'Can\'t find widget legend, method: va.dash_get_widget_legend', text_type = 'ERROR  ')
		return result

	def dash_get_widget_total(self, widget = None):
	#(CG) определяем значение Всего в виджете (справа внизу), в метод нужно передать объект (квадрат самого виджета)
	# возвращает или легенду или None
		result = None
		# ищем все заголовки с дашборда
		try:
			widget_total_value = self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'dashboards-page-label-totalValue-\'').get('elements')
			# проверяем относится ли конкретный блок с легендой к родительскому дашу и если Да, то запоминаем этот объект
			for total_value_section in widget_total_value:
				if self.identity_of_the_child_to_the_parent(parent = widget, child = total_value_section).get('result'):
					result = total_value_section.text
					break
		except Exception as ex:
			loger.file_log(text = 'Can\'t find widget total value, method: va.dash_get_widget_total', text_type = 'ERROR  ')
		return result

	def dash_define_abbility_for_creation_new_dash(self, widget_type = 'stiker'):
	# определяет доступность создания нового виджета на текущем дашборде. В метод передаем тип необходимого даша
		# размерности виджетов
		widget_settings = {'size':{1:'stiker', 1:'pie', 2:'columndash', 4:'linedash'}}
		# определяем все доступнве для создания блоки
		result = None
		avalible_blocks = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-component-emptydash-component-\'')
		# если есть пустые блоки, то получаем их id
		if avalible_blocks.get('count') >= 1:
			blocks = {}
			for empty_block in avalible_blocks.get('elements'):
				blocks[empty_block.get_attribute('id').split('-')[5]] = empty_block

			# ищем все доступные клетки для создания виджета заданного типа
			for key in blocks.keys():
				print(key)

			result = blocks

		return result

	def dash_create_new_dash(self, widget_type = 'stiker'):
	#(CG!) создание нового виджета/ необходимо определить доступновть к созданию

		pass







