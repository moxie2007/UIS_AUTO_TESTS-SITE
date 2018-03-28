import sys, time, datetime, json
from datetime import datetime
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
				pie = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-analytics-dashboards-piedash-\'',timeOut = 0.2)
				for pie_widget in pie.get('elements'):
					if len(pie_widget.get_attribute('id').split('-')) == 6:
						dashboard_boxes += 1
						all_pies.append(pie_widget)
			except:
				pass					
			try:
				# пустые блоки (пока идентификацию оставляем по классу, потому что классы для пользователей UIS и Сomagic совпадают)
				empty = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-container-emptydash-component-\'',timeOut = 0.2)
				for empty_widget in empty.get('elements'):
					if 'x-container analytics-dashboards-emptydash x-container-ul' in str(empty_widget.get_attribute('class')):
						dashboard_boxes += 1
			except:
				pass	
			try:
				all_histograms = []
				# гистограмма
				gisto = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-analytics-dashboards-columndash-\'',timeOut = 0.2)
				for gistogramma in gisto.get('elements'):
					if len(gistogramma.get_attribute('id').split('-')) == 6:
						dashboard_boxes += 2
						all_histograms.append(gistogramma)
			except:
				pass	
			try:
				all_graphs = []
				# грфик
				graphs = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-analytics-dashboards-linedash-\'',timeOut = 0.2)
				for graph in graphs.get('elements'):
					if len(graph.get_attribute('id').split('-')) == 6:
						dashboard_boxes += 4
						all_graphs.append(graph)
			except:
				pass
			try:
				all_stikers = []
				# стикер
				stikers = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-analytics-dashboards-stickerdash-\'',timeOut = 0.2)
				for stiker in stikers.get('elements'):
					if len(stiker.get_attribute('id').split('-')) == 6:
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

	def dash_get_widget_type_from_creation_preview(self, time_out = 120):
	# (C)определяем какой тип виджета выбран
		result = {}
		definition_obj = None # объект по которому будем определять выделение кнопки (выбрана или нет)
		test_step_await = self.wait_for_results()
		test_status = False
		# ищем выделеный объект в секции типа виджета
		while True:
			if test_status == False:
				all_type_btns = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'id, \'dashboards-page-button-\'', timeOut = 0.2)
				# в цикле, по всем объектиам, ищем признак выделения объекта в его классе
				if type(all_type_btns.get('count')) == int:
					for btn in all_type_btns.get('elements'):
						if 'x-btn-pressed' in btn.get_attribute('class'):
							definition_obj = btn
							btn_id_mask = btn.get_attribute('id').split('dashboards-page-button-')[1]
							test_status = True
			if test_status:
				break		
			if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
				loger.file_log(text = 'Can\'t find type definition object for widget. Method: {}'.format('dash_get_widget_type_from_creation_preview'), text_type = 'ERROR  ')
				break
		if test_status:
			# ищем все объекты определяющие ТИП кнопки виджета и проверяем связь потомок-предок. для кого совпадет, тот и есть искомый тип активного виджета
			test_step_await = self.wait_for_results()
			while True:
				test_status = False
				all_type_definition_btns = self.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'dashboards-page-button-' + str(btn_id_mask) + '-btnIconEl\'', timeOut = 0.2)
				if type(all_type_definition_btns.get('count')) == int:
					for type_btn in all_type_definition_btns.get('elements'):
						if self.identity_of_the_child_to_the_parent(parent = definition_obj, child = type_btn).get('result'):
							result['widget_type_name'] = str(type_btn.get_attribute('class')).split('x-btn-icon-el x-btn-icon-el-default-medium ul-btn-icon-chart-')[1].replace(' ','')
							test_status = True
							break
				if test_status:
					break		
				if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t find type name object for widget. Method: {}'.format('dash_get_widget_type_from_creation_preview'), text_type = 'ERROR  ')
					break
		return result

	def dash_get_widget_dimension_from_creation_preview(self, time_out = 120):
	# (C)определяем в каком разрезе отображен виджета, пока работает только с пирагом и гистограммой
		result = {}
		test_status = False
		# определяем родительский объект открытой формы создания\редактирования виджета
		creation_windows = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-ext-comp-\'', timeOut = time_out)
		if type(creation_windows.get('count')) == int:
			for main_item in creation_windows.get('elements'):
				if main_item.get_attribute('class') == 'x-window ul-window-no-body-paddings x-layer x-window-ul x-closable x-window-closable x-window-ul-closable x-border-box ul-floating':
					creation_window = main_item
					break
		# определяем какой перед нами тип виджета
		widget_current_name = self.dash_get_widget_type_from_creation_preview().get('widget_type_name')
		if widget_current_name in ['pie','column']:
			test_status = True
		else:
			loger.file_log(text = 'This widget type: {}, hasn\'t got a demention. Method: {}'.format(self.dash_get_widget_type_from_creation_preview().get('widget_type_name'), 'dash_get_widget_dimension_from_creation_preview'), text_type = 'ERROR  ')
		# определяем какое стоит значение: в разрезе чего, значение берем как текст с предпросмотра.
		if test_status:
			test_step_await = self.wait_for_results()
			while True:
				test_status = False
				widget_priview_texts = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-cm-highchart-\'', timeOut = 1)	
				if type(widget_priview_texts.get('count')) == int:
					for item_text in widget_priview_texts.get('elements'):
						try: # тут при многократной смене значений быват так, что объект не успевает быть загружен
							if self.identity_of_the_child_to_the_parent(parent = creation_window, child = item_text).get('result'):
								if item_text.get_attribute('class') == 'x-component x-box-item x-component-ul':
									if widget_current_name == 'column':
										if len(item_text.get_attribute('id').split('-')) == 5:
											result['dimension_text'] = str(item_text.text.split('\n')[1])		
									if widget_current_name == 'pie':
										if len(item_text.get_attribute('id').split('-')) == 12:
											if item_text.text.lower() in ['не в разрезе']: # возможные варианты пустых данных
												result['dimension_text'] = str(item_text.text)
											else:
												result['dimension_text'] = str(item_text.text.split('\n')[0])
									test_status = True
									break
						except Exception as ex:
							pass
				if test_status:
					break		
				if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t define dimension text at preview. Method: {}'.format('dash_get_widget_dimension_from_creation_preview'), text_type = 'ERROR  ')
					break
		return result

	def dash_create_new_dash(self, widget_type = 'stiker'):
	#(CG!) создание нового виджета/ необходимо определить доступновть к созданию
		pass

	def dash_creation_form_get_list_of_preview_tabs(self, time_out = 120):
	#(С) возвращает количество и список вкладок 
		result = {}
		# получаем родительский объект колонки
		test_step_await = self.wait_for_results()
		while True:
			test_status = False	
			parent_objects = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-cm-singlecolumngrid-presetGroupsList-\'')	
			if type(parent_objects.get('count')) == int:
				for item in parent_objects.get('elements'):
					if len(item.get_attribute('id').split('-')) == 6:
						parrent_of_the_list = item
						test_status = True
						break
			if test_status:
				break						
			if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
				loger.file_log(text = 'Can\'t define parent column object from creation widget form. Method: {}'.format('dash_creation_form_get_list_of_preview_tabs'), text_type = 'ERROR  ')
				break			
		test_step_await = self.wait_for_results()
		while True:
			test_status = False
			tabs = self.elements_list(object_type = 'table', search_type = 'contains', mask = 'id, \'tableview\'', timeOut = 0.2)
			if type(tabs.get('count')) == int:
				# проверяем в том ли столбце найденые значения и если да, то записываем
				current_result = []
				for group_tab in tabs.get('elements'):
					if self.identity_of_the_child_to_the_parent(parent = parrent_of_the_list, child = group_tab).get('result'):
						current_result.append(group_tab)
				if len(current_result) != 0:
					result['count'] = len(current_result)
					result['elements'] = current_result
				if type(result.get('count')) == int:
					for tab in result.get('elements'):
						if '-item-selected' in tab.get_attribute('class'):
							result['active_tab'] = {tab:tab.text}
							test_status = True
							break
			if test_status:
				break						
			if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
				loger.file_log(text = 'Can\'t define tab\'s from creation widget form. Method: {}'.format('dash_creation_form_get_list_of_preview_tabs'), text_type = 'ERROR  ')
				break	
		return result

	def dash_creation_form_get_presets_items_from_list(self, time_out = 120):
	#(С) возвращает список конкретных пресетов с открытой вкладки 
		result = {}
		# получаем родительский объект колонки
		test_step_await = self.wait_for_results()
		while True:
			test_status = False	
			parent_objects = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-cm-singlecolumngrid-presetsList-\'')	
			if type(parent_objects.get('count')) == int:
				for item in parent_objects.get('elements'):
					if len(item.get_attribute('id').split('-')) == 6:
						parrent_of_the_items = item
						test_status = True
						break
			if test_status:
				break						
			if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
				loger.file_log(text = 'Can\'t define parent column object from creation widget form. Method: {}'.format('dash_creation_form_get_list_of_preview_tabs'), text_type = 'ERROR  ')
				break
		# получаем список всех всех значений			
		test_step_await = self.wait_for_results()
		while True:
			test_status = False
			items = self.elements_list(object_type = 'table', search_type = 'contains', mask = 'id, \'tableview\'')
			if type(items.get('count')) == int:
				# проверяем в том ли столбце найденые значения и если да, то записываем
				current_result = []
				for new_item in items.get('elements'):
					if self.identity_of_the_child_to_the_parent(parent = parrent_of_the_items, child = new_item).get('result'):
						current_result.append(new_item)
				if len(current_result) != 0:
					result['count'] = len(current_result)
					result['elements'] = current_result
				if type(result.get('count')) == int:
					for tab in result.get('elements'):
						if '-item-selected' in tab.get_attribute('class'):
							result['active_tab'] = {tab:tab.text}
							break
					test_status = True
			if test_status:
				break						
			if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
				loger.file_log(text = 'Can\'t define item\'s from creation widget form. Method: {}'.format('dash_creation_form_get_list_of_preview_tabs'), text_type = 'ERROR  ')
				break	
		return result

	def dash_creation_form_change_presets_folder(self, new_folder_name = None, time_out = 120):
	#(С) переключаемся на определенную папку с пресетами в случае успеха переключения статус метода: True
		result = {}
		# получаем текущее имя активной папки
		test_step_await = self.wait_for_results()
		while True:
			test_status = False
			active_tab = self.dash_creation_form_get_list_of_preview_tabs(time_out = time_out).get('active_tab')
			try:
				values = active_tab.keys()
				if len(values) == 1:
					for value in values:
						active_tab_name = active_tab.get(value)
					test_status = True
				else:
					loger.file_log(text = 'Can\'t define active folder at form for creation widget. Method: {}'.format('dash_creation_form_change_presets_folder'), text_type = 'ERROR  ')
			except Exception as ex:
				loger.file_log(text = 'System-logic ERROR in method: {}'.format('dash_creation_form_change_presets_folder'), text_type = 'ERROR  ')
			if test_status:
				break						
			if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
				loger.file_log(text = 'Can\'t define item\'s from creation widget form. Method: {}'.format('dash_creation_form_change_presets_folder'), text_type = 'ERROR  ')
				break
		# сравниваем с необходимой
		if test_status:
			test_step_await = self.wait_for_results()
			test_status = False
			while True:
				if str(active_tab_name) == str(new_folder_name):
					loger.file_log(text = 'The folder: {}, already chosen'.format(new_folder_name) , text_type = 'SUCCESS')
					break
			# если не совпало, то пытаемся переключиться
				else:
				# ищем объект которому соотносится new_folder_name
					folders = self.dash_creation_form_get_list_of_preview_tabs(time_out = time_out)
					for folder in folders.get('elements'):
						if str(folder.text) == str(new_folder_name):
							self.click_element(element_definition = folder)
							test_status = True
				if test_status:
					break						
				if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t choose new folder. Method: {}'.format('dash_creation_form_change_presets_folder'), text_type = 'ERROR  ')
					break
		# дожидаемся пока активной не станет необходимая папка
		if test_status:
			test_step_await = self.wait_for_results()
			while True:
				test_status = False
				for item_index in self.dash_creation_form_get_list_of_preview_tabs(time_out = time_out).get('active_tab').values():
					if item_index == new_folder_name:
						test_status = True
						loger.file_log(text = 'The folder was choosen from: {}, to {}'.format(active_tab_name, new_folder_name) , text_type = 'SUCCESS')
				if test_status:
					result = True
					break						
				if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					loger.file_log(text = '{} can\'t be choosen. Method: {}'.format(new_folder_name, 'dash_creation_form_change_presets_folder'), text_type = 'ERROR  ')
					break
		return result

	def dash_creation_form_choose_preset_item(self, new_preset_name = None, time_out = 120):
	#(!С) переключаемся на определенные пресет в случае успеха переключения статус метода: True
		result = {}
		# проверяем что форма создания редактирования виджета есть
		test_step_await = self.wait_for_results()
		while True:
			test_status = False
			main_forms = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-ext-comp-\'', timeOut = 0.2)
			if type(main_forms.get('count')) == int:
				for form in main_forms.get('elements'):
					if len(form.get_attribute('id').split('-')) == 5:
						parent_form_is = form
						test_status = True
						break
			if test_status:
				break						
			if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
				loger.file_log(text = 'Can\'t find widget creation form. Method: {}'.format('dash_creation_widget_from_preset'), text_type = 'ERROR  ')
				break
		# получаем список доступных виджетов
		if test_status:
			items = self.dash_creation_form_get_presets_items_from_list(time_out = time_out)
			if type(items.get('count')) == int:
				for item in items.get('elements'):
					if str(item.text) == str(new_preset_name):
						self.click_element(element_definition = item)
						break
		# проверяем, что название на пресете сменилось (название в превью)
		if test_status:
			while True:
				test_status = False
				widget_previe_names = self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'dashboards-page-label-title-\'', timeOut = 0.2)
				if type(widget_previe_names.get('count')) == int:
					for lable_name in widget_previe_names.get('elements'):
						if len(lable_name.get_attribute('id').split('-')) == 5:
							if str(lable_name.text) == str(new_preset_name):
								test_status = True
								result = True
								break
				if test_status:
					break						
				if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t find widget creation form. Method: {}'.format('dash_creation_widget_from_preset'), text_type = 'ERROR  ')
					break			
		return result

	def dash_creation_widget_from_preset(self, widget_folder = None, widget_name = None, time_out = 120):
	# (CG)создание виджета через пресеты
		# проверяем что форма создания редактирования виджета есть
		test_step_await = self.wait_for_results()
		while True:
			test_status = False
			main_forms = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-ext-comp-\'', timeOut = 0.1)
			if type(main_forms.get('count')) == int:
				for form in main_forms.get('elements'):
					if len(form.get_attribute('id').split('-')) == 5:
						parent_form_is = form
						test_status = True
						# получаем количество созданных виджетов
						current_dashboard = self.dash_define_widgets_at_dashboard(time_out = 1)
						break
			if test_status:
				break						
			if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
				loger.file_log(text = 'Can\'t find widget creation form. Method: {}'.format('dash_creation_widget_from_preset'), text_type = 'ERROR  ')
				break
		# выбираю нужную вкладку
		if test_status:
			self.dash_creation_form_change_presets_folder(new_folder_name = widget_folder, time_out = time_out)
		# выбираю нужный виджет
			self.dash_creation_form_choose_preset_item(new_preset_name = widget_name, time_out = time_out)
		# нажимаем кнопку Создать
		if test_status:
			test_step_await = self.wait_for_results()
			while True:
				test_status = False
				creation_btns = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'id, \'dashboards-page-ul-mainbutton-save-\'')
				if type(creation_btns.get('count')) == int:
					for btn_item in creation_btns.get('elements'):
						if len(btn_item.get_attribute('id').split('-')) == 6:
							self.click_element(element_definition = btn_item)
							test_status = True
				if test_status:
					break						
				if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t find creation form. Method: {}'.format('dash_creation_widget_from_preset'), text_type = 'ERROR  ')
					break
		# проверяем, что созданный виджет появился (по количеству виджетов на dashboard)
		if test_status:
			test_step_await = self.wait_for_results()
			while True:
				test_status = False
				dashboard_state = self.dash_define_widgets_at_dashboard(time_out = 1)
				try:
					for widget_item in dashboard_state.get('existing_widgets'):
						if len(current_dashboard.get('existing_widgets').get(widget_item)) != dashboard_state.get('existing_widgets').get(widget_item):
							test_status = True
							break
				except:
					pass
				if test_status:
					break						
				if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'New widget:{} {} wasn\'t created. Method: {}'.format(widget_folder, widget_name,'dash_creation_widget_from_preset'), text_type = 'ERROR  ')
					break

	def dash_delete_widget(self, widget = {None:{None:None}}, time_out = 120):
	# (CG)удаление виджета с дашборда, в метод нужно передать {тип виджета:[{имя виджета:легенда\данные с виджета}]}
	# если не все данные указаны то удаляем первый встреченный (тип и имя обязательны для указания)
		# получаем список всех виджетов со страницы, страница дашборда должна быть открыта и все виджеты уже есть
		result = {}
		widgets_list = self.dash_define_widgets_at_dashboard(time_out = 1)
		# ищем группу виджетов по ТИПУ
		test_status = False
		for group_list in widgets_list.get('existing_widgets'):
			if str(group_list) == str(list(widget.keys())[0]):
				# перебираем все виджеты и выбираем те, которые нужны (первичный ключь: ИМЯ)
				compared_widgets = []
				items_counter = 0
				for next_widget in widgets_list.get('existing_widgets').get(group_list):		
					if self.dash_get_widget_name(widget = next_widget) == list(widget.get(list(widget.keys())[0]).keys())[0]:
						compared_widgets.append(next_widget)
						items_counter = len(compared_widgets)
						# тут может быть ошибка логики, в том случае если виджет не найден 
				if items_counter == 0:
					loger.file_log(text = 'Widget wasn\'t found. Method: {}'.format('dash_delete_widget'), text_type = 'ERROR  ')
					# test_status = True # это хрень надо проверять почему не работает.!!!!!!!!!!!!!!!!!!!
				elif items_counter > 1:
					if list(widget.values())[0].get(list(list(widget.values())[0].keys())[0]) == None: 
						loger.file_log(text = 'Was found more than one widget. Without legend will be used first item', text_type = 'WARNING')
						result['widget'] = compared_widgets[0]
						test_status = True
					else:
						result['widget_name'] = self.dash_get_widget_name(widget = next_widget)
						test_status = True # пропускаем, далее в цикле перебираем легенды и ищем нужную. Тут одно значение, так и должно быть.
				else:
					result['widget_name'] = self.dash_get_widget_name(widget = next_widget)
					result['widget'] = next_widget
					test_status = True
				break # выход из перебора типов виджета
		# получаем весь текст с виджета
		test_status = True
		if test_status:
			# находим первое совпадение и считаем что найденный объект искомый
			for legend in compared_widgets:
				displayd_data = legend.text
				if list(widget.values())[0].get(list(list(widget.values())[0].keys())[0]) != None:
					# сравниваем легенду и полученную с виджета легенду
					if str(list(widget.values())[0].get(list(list(widget.values())[0].keys())[0])) in str(displayd_data): # тут возможно нужно преобразовать в строку без пробелов и перевода строки 
						test_status = True
						result['widget'] = legend
						result['widget_name'] = self.dash_get_widget_name(widget = next_widget)
						break		
		# ___________________________________________________________________
		# наводим курсор на название виджета (до появления икогки редактирования виджета)
		if test_status:
			test_step_await = self.wait_for_results()
			while True:
				test_status = False
				self.move_cursor_to_the_object(current_object = result.get('widget'))
				edit_icons = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'id, \'dashboards-page-ul-usualbutton-edit-\'')
				if type(edit_icons.get('count')) == int:
					for icon in edit_icons.get('elements'):
						if len(icon.get_attribute('id').split('-')) == 6:
							if self.displayed_element(element_definition = icon, timeOut = 0.2).get('state'):
								edit_icon = icon
								test_status = True
								break
				if test_status:
					break						
				if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t . Method: {}'.format('dash_delete_widget'), text_type = 'ERROR  ')
					break	
		# нажимаем на иконку редактирования виджета (ожидаем открытия формы редактирования виджета + родительский объект)
		if test_status:
			test_step_await = self.wait_for_results()
			self.click_element(element_definition = edit_icon)
			while True:
				test_status = False
				opened_forms = edit_icons = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-ext-comp-\'')
				if type(opened_forms.get('count')) == int:
					for opened_form in opened_forms.get('elements'):
						if len(opened_form.get_attribute('id').split('-')) == 5:
							parent_object = opened_form
							test_status = True
				if test_status:
					break						
				if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t . Method: {}'.format('dash_delete_widget'), text_type = 'ERROR  ')
					break	
		# находим кнопку удаления (от родителя) и нажимаем (ожидаем пока виджет пропадет с дашборда)
		if test_status:
			test_step_await = self.wait_for_results()
			while True:
				test_status = False
				delete_btns = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'id, \'dashboards-page-ul-usualbutton-remove-\'')
				if type(delete_btns.get('count')) == int:
					for del_btn in delete_btns.get('elements'):
						if len(del_btn.get_attribute('id').split('-')) == 6:
							test_status = True # значение кнопки del_btn будем использовать дальше в тесте
							break				
				if test_status:
					break						
				if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t . Method: {}'.format('dash_delete_widget'), text_type = 'ERROR  ')
					break			
		if test_status:
			test_step_await = self.wait_for_results()
			self.click_element(element_definition = del_btn)
			while True:
				test_status = False
				if widgets_list != self.dash_define_widgets_at_dashboard(time_out = 1):
					test_status = True
					loger.file_log(text = "Widget: {}, was deleted".format(result.get('widget_name')), text_type = 'SUCCESS')	
				if test_status:
					break						
				if self.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'Can\'t . Method: {}'.format('dash_delete_widget'), text_type = 'ERROR  ')
					break	
		return result