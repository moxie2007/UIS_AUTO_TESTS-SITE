'''
Тест: Создание всех пресетовских Виджетов.
виджеты: Динамика звонков, Потери звонков, Распределение звонков по сотрудникам, Среднее время ответа на звонок, Средняя длительность разговора, Регионы абонентов.
требования: 
- тест заточен под пользователя 1103 на ПредПродакшене
- предварительно должна быть создана вкладка для: test_dashboard_tab, вкладка должна быть пустая.
обработка ошибок: в случае возникновения ошибки и невозможности продолжить тест, выполнение остановится на экране с ошибкой
'''
import sys
sys.path.append('C:\\UIS_AUTO_TESTS\\UIS_AUTO_TESTS-SITE')

import  random, sys, time
from time import gmtime, strftime
from datetime import datetime
import tools, pageElements, start_uis_test, vats_tools
from loger import Loger as loger

configLK = tools.User_config()
configLK.set_lk_parametrs(source_name = 'LK')

time_out = 10
test_dashboard_tab = 'test_env_dont_touch'
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
		# получаем список уже имеющихся дашбордов (должен быть 0)
		widgets_list_before = []
		existing_widgets = va.dash_define_widgets_at_dashboard(time_out = time_out/5).get('existing_widgets')
		for widget_types in existing_widgets.keys():
			if len(existing_widgets.get(widget_types)) > 0:
				widgets_list_before += existing_widgets.get(widget_types)
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
				print('Выпадающее меню: Добавить виджет не появилось. строка теста {}'.format(62))
				break
		if test_status:
			test_step_await = tools_test.wait_for_results()
			while True:
				test_status = False
				dd_menu_items = tools_test.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'dashboards-page-menuitem-\'')
				if type(dd_menu_items.get('count')) == int:
					for new_btn in dd_menu_items.get('elements'):
						if 'Готовый' in new_btn.text:
							tools_test.click_element(element_definition = new_btn, breakONerror = False, scroll_to_element = False, timeOut = time_out)
							# test_status = True
							break
				# ожидаем появление формы: Добавление готового виджета
				if type(dd_menu_items.get('count')) == int:
					form_headers = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-title-\'')
					if type(form_headers.get('count')) == int:
						for header_text in form_headers.get('elements'):
							if 'Добавление готового виджета' in header_text.text:
								test_status = True
								break
				if test_status:
					break						
				if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					print('Меню: Готовый, не нашли и переход на форму Добавления готового виджета не произошло. строка теста {}'.format(86))
					break
		# получаем список всех доступных вкладок виджетов
		if test_status:
			test_step_await = tools_test.wait_for_results()
			while True:
				test_status = False	
			# Для того чтобы разделить группы виджетов и сами виджеты находим глобальные родительские объекты
				# получаем родительский объект группы
				groups_items =  tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-cm-singlecolumngrid-presetGroupsList-\'')
				if type(groups_items.get('count')) == int:
					for group in groups_items.get('elements'):
						if 'body' in group.get_attribute('id'):
							groups_parent_obgect = group
							break
				# получаем родительский объект готовых Виджетов
				values_items = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-cm-singlecolumngrid-presetsList-\'')
				if type(values_items.get('count')) == int:
					for item_value in values_items.get('elements'):
						if 'body' in item_value.get_attribute('id'):
							values_parent_obgect = item_value
							break
				# получаем список всех значений в группе
				presets_state = {}
				curent_folders = {} 
				curent_presets = {}
				all_items_list = tools_test.elements_list(object_type = 'table', search_type = 'contains', mask = 'id, \'dashboards-page-tableview-\'')
				if type(all_items_list.get('count')) == int:
					for item in all_items_list.get('elements'):
						if tools_test.identity_of_the_child_to_the_parent(parent = groups_parent_obgect, child = item).get('result'):
							# по этому параметру определяем выбранную папку
							if 'item-selected' in item.get_attribute('class'):
								curent_folders[item.text] = item
						if tools_test.identity_of_the_child_to_the_parent(parent = values_parent_obgect, child = item).get('result'):
							curent_presets[item.text] = item					
					presets_state['active_folder'] = curent_folders
					presets_state['presets'] = curent_presets
					if len(presets_state.get('presets')) != 0:
						test_status = True
				if test_status:
					break						
				if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					print('Не удалось получить список пресетов для группы: {}. строка теста {}'.format(curent_folders.keys(),128))
					break
# -------------------------------------------------------------
		# в цикле создаем все доступные виджеты	
		if test_status:
			creation_all_widgets_step_await = tools_test.wait_for_results()
			presets_names = []
			for preset_name in presets_state.get('presets').keys():
				presets_names.append(preset_name)
			while len(presets_names) != 0:
				# выбираем первый доступный пресет и если нет ошибки создаём его
				test_step_await = tools_test.wait_for_results()
				while True:
					test_status = False
					# получаем имя и по нему объект
					for current_name in presets_names:
						# берем следующее значение для создания виджета
						item_deletion = presets_state.get('presets').get(current_name)
						current_wiget_name = current_name
						break
					# выбираем пресет
					tools_test.click_element(element_definition = item_deletion, breakONerror = False, scroll_to_element = False, timeOut = time_out)		
					# находим объект самой формы
					form_objects = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-ext-comp-\'')
					if type(form_objects.get('count')) == int:
						for parent_form in form_objects.get('elements'):
							for id_item in parent_form.get_attribute('id').split('-'):
								try:
									id_item = int(id_item)
									break
								except: pass
							if type(id_item) == int:
								break
					# проверяем, что отображено название виджета = названию выбираемого меню.
					preview_headers_text = tools_test.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'dashboards-page-label-title-\'')
					if type(preview_headers_text.get('count')) == int:
						# проверяем, что конкретный заголовок принадлежит открытой форме создаваемого виджета
						for current_header_text in preview_headers_text.get('elements'):
							if tools_test.identity_of_the_child_to_the_parent(parent = parent_form , child = current_header_text).get('result'):
								# если название создаваемого даша совпадает с текстом предпросмотра
								if current_header_text.text == current_wiget_name:
								# if preview_headers_text.get('elements')[0].text == current_wiget_name:
									test_status = True
					if test_status:
						break						
					if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out*2).get('result'):
						print('Не удалось найти виджет. строка теста {}'.format(176))
						break
				# находим и жмем кнопку Создать
				if test_status:
					test_step_await = tools_test.wait_for_results()
					while True:
						test_status = False
						create_btn_objects = tools_test.elements_list(object_type = 'a', search_type = 'contains', mask = 'componentid, \'dashboards-page-ul-mainbutton-save-\'')
						if type(create_btn_objects.get('count')) == int:
							if create_btn_objects.get('count') == 1:
								tools_test.click_element(element_definition = create_btn_objects.get('elements')[0], breakONerror = False, scroll_to_element = False, timeOut = time_out)
								test_status = True
						if test_status:
							break						
						if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
							print('Не удалось нажать на кнопку:{}. строка теста {}'.format('Сохранить',189))
							break
				# проверяем что виджет создался
				if test_status:
					test_step_await = tools_test.wait_for_results()
					while True:
						test_status = False
						# собираем все вебъобекты имеющихся виджетовв один список
						widgets_list_after = []
						existing_widgets = va.dash_define_widgets_at_dashboard(time_out = time_out).get('existing_widgets')
						for widget_types in existing_widgets.keys():
							if len(existing_widgets.get(widget_types)) > 0:
								widgets_list_after += existing_widgets.get(widget_types)
						if len(widgets_list_after)-len(widgets_list_before) == 1:
							test_status = True
							widgets_list_before = widgets_list_after			
						if test_status:
							break						
						if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
							print('Не удалось найти созданный виджет. строка теста {}'.format(208))
							break
				# удаляем имя созданного виджета из списка создаваемых в тесте виджетов
				if test_status:
					presets_names.remove(current_name)
				# если список создаваемых виджетов пуст, то дальше открывать на создание форму не нужно
				if len(presets_names) > 0:
					# открываем следующую форму для создания готового виджета
					if test_status:
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
								print('Выпадающее меню: Добавить виджет не появилось. строка теста {}'.format('Сохранить',232))
								break
					if test_status:
						test_step_await = tools_test.wait_for_results()
						while True:
							test_status = False
							dd_menu_items = tools_test.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'dashboards-page-menuitem-\'')
							if type(dd_menu_items.get('count')) == int:
								for new_btn in dd_menu_items.get('elements'):
									if 'Готовый' in new_btn.text:
										tools_test.click_element(element_definition = new_btn, breakONerror = False, scroll_to_element = False, timeOut = time_out)
										# test_status = True
										break
							# ожидаем появление формы: Добавление готового виджета
							if type(dd_menu_items.get('count')) == int:
								form_headers = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-title-\'')
								if type(form_headers.get('count')) == int:
									for header_text in form_headers.get('elements'):
										if 'Добавление готового виджета' in header_text.text:
											test_status = True
											break
							if test_status:
								break						
							if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
								print('Меню: Готовый, не нашли и переход на форму Добавления готового виджета не произошло. строка теста {}'.format(256))
								break
					# получаем список всех доступных вкладок виджетов
					if test_status:
						test_step_await = tools_test.wait_for_results()
						while True:
							test_status = False	
						# Для того чтобы разделить группы виджетов и сами виджеты находим глобальные родительские объекты
							# получаем родительский объект группы
							groups_items =  tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-cm-singlecolumngrid-presetGroupsList-\'')
							if type(groups_items.get('count')) == int:
								for group in groups_items.get('elements'):
									if 'body' in group.get_attribute('id'):
										groups_parent_obgect = group
										break
							# получаем родительский объект готовых Виджетов
							values_items = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-cm-singlecolumngrid-presetsList-\'')
							if type(values_items.get('count')) == int:
								for item_value in values_items.get('elements'):
									if 'body' in item_value.get_attribute('id'):
										values_parent_obgect = item_value
										break
							# получаем список всех значений в группе
							presets_state = {}
							curent_folders = {} 
							curent_presets = {}
							all_items_list = tools_test.elements_list(object_type = 'table', search_type = 'contains', mask = 'id, \'dashboards-page-tableview-\'')
							if type(all_items_list.get('count')) == int:
								for item in all_items_list.get('elements'):
									if tools_test.identity_of_the_child_to_the_parent(parent = groups_parent_obgect, child = item).get('result'):
										# по этому параметру определяем выбранную папку
										if 'item-selected' in item.get_attribute('class'):
											curent_folders[item.text] = item
									if tools_test.identity_of_the_child_to_the_parent(parent = values_parent_obgect, child = item).get('result'):
										curent_presets[item.text] = item					
								presets_state['active_folder'] = curent_folders
								presets_state['presets'] = curent_presets
								if len(presets_state.get('presets')) != 0:
									test_status = True
							if test_status:
								break						
							if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
								print('Не удалось получить список пресетов для группы: {}. строка теста {}'.format(curent_folders.keys(),298))
								break					
				if tools_test.wait_for_results(time_data = creation_all_widgets_step_await, time_out = time_out*12).get('result'):
					print('Не удалось создать все Виджеты. строка теста {}'.format(301))
					break
		# закрываем браузер
		if test_status:
			main_unit.close_browser
	print('OVER:\t{}\t:\t{}\ttesting index = {}'.format(str(datetime.utcnow()),'vats_sanity', index_testing))
	index_testing += 1

