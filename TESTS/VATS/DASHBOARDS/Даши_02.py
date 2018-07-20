'''
Время выполнения: 45 минут.
Тест: перебор всех основных комбинаций по созданию нового дашборда.
поля: Что считаем, Как считаем, В разрезе чего.
требования: 
- тест заточен под пользователя 1103 на ПредПродакшене
- предварительно должна быть создана вкладка для: list_test
- первая ячейка Дашборда, должна быть занята стикером или пирогом
обработка ошибок: в случае возникновения ошибки и невозможности продолжить тест, выполнение остановится на экране с ошибкой
'''
import sys
sys.path.append('C:\\UIS_AUTO_TESTS\\UIS_AUTO_TESTS-SITE')
sys.path.append('d:\\Work\AUTOMATION\\SELENIUM_SCREEPTS')

import  random, sys, time
from time import gmtime, strftime
from datetime import datetime
import tools, pageElements, start_uis_test, vats_tools
from loger import Loger as loger

configLK = tools.User_config()
configLK.set_lk_parametrs(source_name = 'US')

time_out = 10
test_dashboard_tab = 'list_test'
# метод авторизации через админку

# тело теста
if __name__ == '__main__':
	index_testing = 1
	for tt in range(1):
		print('START:\t{}\t:\t{}'.format(str(datetime.utcnow()),'vats_sanity'))
		# модуль инициализации (открываем браузер)
		main_unit = start_uis_test.Global_unit()
		driver = main_unit.init_browser(product_type = 'ch')
		va = vats_tools.Vats_tools(driver)
		tools_test = tools.Uis_tools(driver) # (инициализация модуля с таким именем из-за того что внутри происходит переопределение такого имени: tools)
		# логинимся в ЛК
		tools_test.login_to(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass, breakONerror = True)
		# переходим в меню даши
		tools_test.lk_sidemenu_navigation(item_menu = ['Дашборды'], breakONerror = True)
		# переходим на предварительно подготовленную вкладку
		tools_test.top_menu_navigation(tab_name = test_dashboard_tab, timeOut = time_out, new_elemets_status = False)
		# находим объект для создания даша (желательно определить по объекту, какие типы дашей доступны для создания)
		# в результате мы дожидаемся открытой менюшки для создания дашей
		test_step_await = tools_test.wait_for_results()
		while True:
			test_status = False
			plus_buttoms = tools_test.elements_list(object_type = 'a', search_type = 'contains', mask = 'id, \'dashboards-page-button-\'')
			for button in plus_buttoms.get('elements'):
				if 'cm-editable-tabbar-add-btn' not in button .get_attribute('class'):
					tools_test.click_element(element_definition = button, breakONerror = False, scroll_to_element = False, timeOut = time_out)
					break
			get_text_object = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-title-\'')
			for text_object in get_text_object.get('elements'):
				if text_object.text == 'ДОБАВИТЬ ВИДЖЕТ':
					test_status = True
			if test_status:
				break				
			if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
				print('Выпадающее меню: Добавить виджет не появилось. строка теста {}'.format(57))
				break
		if test_status:
			test_step_await = tools_test.wait_for_results()
			while True:
				test_status = False
				dd_menu_items = tools_test.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'dashboards-page-menuitem-new-\'')
				if type(dd_menu_items.get('count')) == int:
					for new_btn in dd_menu_items.get('elements'):
						if 'Новый' in new_btn.text:
							tools_test.click_element(element_definition = new_btn, breakONerror = False, scroll_to_element = False, timeOut = time_out)
							# test_status = True
							break
				# ожидаем появление формы: Добавление нового виджета
				if type(dd_menu_items.get('count')) == int:
					form_headers = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-title-\'')
					if type(form_headers.get('count')) == int:
						for header_text in form_headers.get('elements'):
							if 'Добавление нового виджета' in header_text.text:
								test_status = True
								break
				if test_status:
					break						
				if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					print('Меню: Новый, не нашли и переход на форму Добавления нового виджета не произошло. строка теста {}'.format(81))
					break
		# получаем список всех доступных параметров: Что считаем (пустым он быть не может)
		if test_status:
			test_step_await = tools_test.wait_for_results()
			while True:
				test_status = False
				# ищем кнопку для открытия списка и жмем её
				what_calculate_dd_btns = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-cm-treecombo2-metric_id-\'')
				if type(what_calculate_dd_btns.get('count')) == int:
					for metric_dd_btn in what_calculate_dd_btns.get('elements'):
						if 'trigger-picker' in metric_dd_btn.get_attribute('id'):
							tools_test.click_element(element_definition = metric_dd_btn, breakONerror = False, scroll_to_element = False, timeOut = time_out)
				# ищем открывшийся список
				items_list = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-ul-treeview-\'')
				if type(items_list.get('count')) == int:
					test_status = True
				if test_status:
					break						
				if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					print('Не удалось найти и нажать кнопку для открытия списка: Что считаем. строка теста{}'.format(105))
					break
		# получаем список всех значений: Что считаем
		metrics_list = {}
		if test_status:
			test_step_await = tools_test.wait_for_results()
			while True:
				test_status = False
				metric_values = tools_test.elements_list(object_type = 'table', search_type = 'contains', mask = 'id, \'dashboards-page-ul-treeview-\'')				
				if type(metric_values.get('count')) == int:
					# ищем все объекты родительского типа (вкладки в меню)
					folders_items = {}
					parent_icons_objects = tools_test.elements_list(object_type = 'img', search_type = 'contains', mask = 'class, \' x-tree-elbow-img x-tree-elbow-end-plus x-tree-expander\'')
					if type(parent_icons_objects.get('count')) == int:
						for folder_object in parent_icons_objects.get('elements'):
							# по каждому объектиу поднимаеися на 4 значения вверх (потом завязать на родитель потомок)
							for iteration in range(4):
								folder_obj = tools_test.get_parent(current_object = folder_object)
								folder_object = folder_obj
								folders_items[folder_obj.text] = folder_obj
				# исключаем из списка пункты - папки
				for menu_item in metric_values.get('elements'):
					if type(folders_items.get(menu_item.text)) == type(None):
						metrics_list[menu_item.text] = menu_item
				# если список не пуст то считаем, что все ОК и идем дальше
				if len(metrics_list) != 0:	
					test_status = True
				if test_status:
					break						
				if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					print('Не удалось получить список Что считаем. строка теста{}'.format(131))
					break
		# закрываем список что считаем
		if test_status:
			tools_test.click_element(element_definition = metric_dd_btn, breakONerror = False, scroll_to_element = False, timeOut = time_out)
# ________________________________________________________________________________________
		# задаем название виджета
		test_step_await = tools_test.wait_for_results()
		while True:
			test_status = False	
			widget_names = tools_test.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'dashboards-page-textfield-name-\'')
			if type(widget_names.get('count')) == int:
				for widget_name in widget_names.get('elements'):
					if len(widget_name.get_attribute('id').split('-')) == 6:
						tools_test.change_value(element_definition = widget_name, text = 'test')
						test_status = True
			if test_status:
				break						
			if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
				print('Значение для: Что считаем, выставить не удалось. строка теста{}'.format(155))
				break
		# открываю список и в цикле перебираю объекты: что считаем
		# метрики
		for current_metric_key in metrics_list.keys():
			tools_test.click_element(element_definition = metric_dd_btn, breakONerror = False, scroll_to_element = False, timeOut = time_out)
			tools_test.click_element(element_definition = metrics_list.get(current_metric_key), breakONerror = False, scroll_to_element = True, timeOut = time_out)
			# необходимо проверяем что значение установилось
			test_step_await = tools_test.wait_for_results()
			while True:
				test_status = False
				fildes_value = tools_test.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'dashboards-page-cm-treecombo2-metric_id-\'')
				if type(fildes_value.get('count')) == int:
					for current_value in fildes_value.get('elements'):
						if current_value.get_attribute('value') == current_metric_key:
							test_status = True
							break
				if test_status:
					break						
				if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					print('Значение для: Что считаем, выставить не удалось. строка теста{}'.format(155))
					break
		# получаем список для всех значений: Как считаем.
			# нажимаем на кнопку выпадающего списка: как считаем
			if test_status:
				test_step_await = tools_test.wait_for_results()
				while True:
					test_status = False
					# ищем кнопку для открытия списка и жмем её
					how_calculate_dd_btns = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-cm-directorycombo-agg-\'')
					if type(how_calculate_dd_btns.get('count')) == int:
						for agg_dd_btn in how_calculate_dd_btns.get('elements'):
							if 'trigger-picker' in agg_dd_btn.get_attribute('id'):
								tools_test.click_element(element_definition = agg_dd_btn, breakONerror = False, scroll_to_element = False, timeOut = time_out)
								break
					# ищем открывшийся список
					items_list = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-ul-boundlist-\'')
					if type(items_list.get('count')) == int:
						test_status = True
					if test_status:
						break						
					if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
						print('Не удалось найти и нажать кнопку для открытия списка: Как считаем. строка теста{}'.format(177))
						break
			# считываем все значения открывшегося списка
			if test_status:
				agg_list = {}
				test_step_await = tools_test.wait_for_results()
				while True:
					test_status = False
					agg_values = tools_test.elements_list(object_type = 'li', search_type = 'contains', mask = 'data-boundview, \'dashboards-page-ul-boundlist-\'')
					if type(agg_values.get('count')) == int:
						for agg_value in agg_values.get('elements'):
							agg_list[agg_value.text] = agg_value
					if len(agg_list) != 0:
						test_status = True
					if test_status:
						break						
					if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
						print('Не удалось получить список значений из: Как считаем. строка теста{}'.format(194))
						break
			# закрываем список
			if test_status:
				tools_test.click_element(element_definition = agg_dd_btn, breakONerror = False, scroll_to_element = False, timeOut = time_out)
# ________________________________________________________________________________________
			# открываю список и в цикле перебираю объекты: как считаем
			# агрегаторы
			if test_status:
				for current_agg_key in agg_list.keys():
					tools_test.click_element(element_definition = agg_dd_btn, breakONerror = False, scroll_to_element = False, timeOut = time_out)
					
					# получаем список всех отображенных значений 
					list_list = tools_test.elements_list(object_type = 'li', search_type = 'contains', mask = 'data-boundview, \'dashboards-page-ul-boundlist-\'').get('elements')
					for elem_curent in list_list:
						if elem_curent.text == current_agg_key:
							tools_test.click_element(element_definition = elem_curent, breakONerror = False, scroll_to_element = True, timeOut = time_out)
							break
					# проверяем, что значение установилось
					test_step_await = tools_test.wait_for_results()
					while True:
						test_status = False
						fildes_value = tools_test.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'dashboards-page-cm-directorycombo-agg-\'')
						if type(fildes_value.get('count')) == int:
							for current_value in fildes_value.get('elements'):
								if current_value.get_attribute('value') == current_agg_key:
									test_status = True
									break
						if test_status:
							break						
						if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
							print('Не удалось получить выставленное значений из: Как считаем. строка теста{}'.format(238))
							break
					# получаем список для всех значений: В разрезе чего.
					# нажимаем на кнопку выпадающего списка: В разрезе чего
					if test_status:
						test_step_await = tools_test.wait_for_results()
						while True:
							test_status = False
							# ищем кнопку для открытия списка и жмем её
							dimension_dd_btns = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-cm-treecombo2-dimension_id-\'')
							if type(dimension_dd_btns.get('count')) == int:
								for dimension_dd_btn in dimension_dd_btns.get('elements'):
									if 'trigger-picker' in dimension_dd_btn.get_attribute('id'):
										tools_test.click_element(element_definition = dimension_dd_btn, breakONerror = False, scroll_to_element = False, timeOut = time_out)
										break
							# ищем открывшийся список
							dem_items_list = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-ul-treeview-\'')
							if type(dem_items_list.get('count')) == int:
								test_status = True
							if test_status:
								break						
							if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
								print('Не удалось открыть список значений : В разрезе чего. строка теста{}'.format(241))
								break
						# считываем все значения открывшегося списка
						if test_status:
							dimension_list = {}
							test_step_await = tools_test.wait_for_results()
							while True:
								test_status = False
								dimension_values = tools_test.elements_list(object_type = 'table', search_type = 'contains', mask = 'id, \'dashboards-page-ul-treeview-\'')
								if type(dimension_values.get('count')) == int:
									# ищем все объекты родительского типа (вкладки в меню)
									dimension_folders_items = {}
									# так как однотипный объект: иконка ПЛЮС, в зависимости от нахождения определяется разными классами определяем её как: 'class, \' x-tree-elbow-img x-tree-elbow-end-plus x-tree-expander\'')
									parent_dimension_icons_objects = tools_test.elements_list(object_type = 'img', search_type = 'contains', mask = 'class, \'-plus x-tree-expander\'')
									if type(parent_dimension_icons_objects.get('count')) == int:
										for folder_object in parent_dimension_icons_objects.get('elements'):
											# по каждому объектиу поднимаеися на 4 значения вверх (потом завязать на родитель потомок)
											for iteration in range(4):
												folder_obj = tools_test.get_parent(current_object = folder_object)
												folder_object = folder_obj
												dimension_folders_items[folder_obj.text] = folder_obj
								# исключаем из списка пункты - папки
								for dem_menu_item in dimension_values.get('elements'):
									if type(dimension_folders_items.get(dem_menu_item.text)) == type(None):
										dimension_list[dem_menu_item.text] = dem_menu_item
								# если список не пуст то считаем, что все ОК и идем дальше
								if len(dimension_list) != 0:
									test_status = True
								if test_status:
									break						
								if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
									print('Не удалось открыть список значений: В разрезе чего, и получить значения для перебора. строка теста{}'.format(271))
									break
					# закрываю открытое меню 
					if test_status:
						tools_test.click_element(element_definition = dimension_dd_btn, breakONerror = False, scroll_to_element = False, timeOut = time_out)
# ________________________________________________________________________________________
			# открываю список и в цикле перебираю объекты: в разрезе чего
			# агрегаторы
					if test_status:
						for current_dimension_key in dimension_list.keys():
							tools_test.click_element(element_definition = dimension_dd_btn, breakONerror = False, scroll_to_element = False, timeOut = time_out)
							tools_test.click_element(element_definition = dimension_list.get(current_dimension_key), breakONerror = False, scroll_to_element = True, timeOut = time_out)
							# проверяем, что значение установилось
							test_step_await = tools_test.wait_for_results()
							while True:
								test_status = False
								dimension_fildes_value = tools_test.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'dashboards-page-cm-treecombo2-dimension_id-\'')
								if type(dimension_fildes_value.get('count')) == int:
									for current_value in dimension_fildes_value.get('elements'):
										if current_value.get_attribute('value') == current_dimension_key:
											test_status = True
											time.sleep(0.2) # системное ожидание что бы  Selenium не забивал сокет
											break
								if test_status:
									break						
								if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
									print('Не удалось получить выставленное значений из: В разрезе чего. строка теста: {} искомое значение {}'.format(300, current_dimension_key))
									break
			# проверяем, что на превью отображено искомок значение. Варианта может быть два: совпадение и 0 - в случае если данных на такой агрегатор нет
							time.sleep(3)
							# if test_status:
							# 	test_step_await = tools_test.wait_for_results()
							# 	while True:
							# 		test_status = False
							# 		displayed_widget_text = va.dash_get_widget_dimension_from_creation_preview().get('dimension_text').lower()
							# 		if displayed_widget_text in ['0', 'не в разрезе', current_dimension_key.lower()]:
							# 			if displayed_widget_text in ['0','не в разрезе']:
							# 				loger.file_log(text = 'Widget without data. You should chek it by hands. Demension: {}'.format(current_dimension_key), text_type = 'WARNING')
							# 			test_status = True
							# 		if test_status:
							# 			break						
							# 		if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
							# 			print('Не удалось получить выставленное значений из: В разрезе чего. ожидаемое значение:{}, полученное значение: {}'.format(current_dimension_key, displayed_widget_text))
							# 			break
		# закрываем браузер
		if test_status:
			main_unit.close_browser
	print('OVER:\t{}\t:\t{}\ttesting index = {}'.format(str(datetime.utcnow()),'vats_sanity', index_testing))
	index_testing += 1

