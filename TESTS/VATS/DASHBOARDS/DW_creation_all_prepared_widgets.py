'''
Тест: проверка создания всех виджетов из пресетов. Мы проверяем что виджет создается и удаляется и при этом,
система не падает. В случае ошибки выполнение остановится в том месте, где произошла ошибка.
виджеты: 
- тест заточен под пользователя 1103 на ПредПродакшене
- предварительно должна быть создана вкладка для: test_dashboard_tab, вкладка должна быть пустая.
обработка ошибок: в случае возникновения ошибки и невозможности продолжить тест, выполнение остановится на экране с ошибкой
'''
import sys
sys.path.append('C:\\UIS_AUTO_TESTS\\UIS_AUTO_TESTS-SITE')
# sys.path.append('D:\\Work\\AUTOMATION\\SELENIUM_SCREEPTS')

import  random, sys, time
from time import gmtime, strftime
from datetime import datetime
import tools, pageElements, start_uis_test, vats_tools
from loger import Loger as loger

configLK = tools.User_config()
configLK.set_lk_parametrs(source_name = 'NEW_LK')

test_name = 'Creation widgets by presets'
time_out = 20
test_dashboard_tab = 'list_test'
# метод авторизации через админку

# тело теста
if __name__ == '__main__':
	index_testing = 1
	for tt in range(4):
		print('START:\t{}\t:\t{}'.format(str(datetime.utcnow()),test_name))
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
		test_status = False		
		# переходим на тестовый дашборд
		dashboards = va.dash_define_existing_dashboards()
		for dashboard in dashboards.keys():
			if dashboards.get(dashboard).get('name') == test_dashboard_tab:
				tools_test.click_element(element_definition = dashboard)
				test_status = True
				break
		# ожидаем пока нужная вкладка станет активной
		if test_status:
			test_step_await = tools_test.wait_for_results()
			while True:
				test_status = False
				dashboards = va.dash_define_existing_dashboards()
				for dashboard in dashboards.keys():
					if dashboards.get(dashboard).get('status'):
						if dashboards.get(dashboard).get('name') == test_dashboard_tab:
							test_status = True
				if test_status:
					break				
				if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					print('Вкладка {} не стала активной'.format(test_dashboard_tab))
					break		
		# находим и нажимаем кнопку с плюсом для создания нового готового виджета
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
					print('Выпадающее меню: Добавить виджет не появилось. строка теста')
					break
		# выбираем пунк: Говый виджет
		if test_status:
			test_step_await = tools_test.wait_for_results()
			while True:
				test_status = False
				dd_menu_items = tools_test.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'dashboards-page-menuitem-\'')
				if type(dd_menu_items.get('count')) == int:
					for new_btn in dd_menu_items.get('elements'):
						if 'Готовый' in new_btn.text:
							tools_test.click_element(element_definition = new_btn, breakONerror = False, scroll_to_element = False, timeOut = time_out)
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
		# получаем список групп пресетов
		groups_list = va.dash_creation_form_get_list_of_preview_tabs()
		if type(groups_list.get('count')) == int:
			# print(groups_list)
			pass
		else:
			test_status = False
		# в цикле перебираем все вкладки и получаем все названия пресетов
		presets = {}
		if test_status:
			test_status = False
			for group in groups_list.get('elements'):
				va.dash_creation_form_change_presets_folder(new_folder_name = group.text, time_out = 10)
				new_list = []
				for item in va.dash_creation_form_get_presets_items_from_list(time_out = 120).get('elements'):
					new_list.append(item.text)
				presets[group.text] = new_list
			if len(presets) > 0:
				test_status = True
		# закрываем окно создания, что б не потерять значения в случае ошибок
		if test_status:
			test_step_await = tools_test.wait_for_results()
			action_status = True
			while True:
				test_status = False
				if action_status:
					cancel_btns =  tools_test.elements_list(object_type = 'a', search_type = 'contains', mask = 'id, \'dashboards-page-ul-linklikebutton-\'')
					if type(cancel_btns.get('count')) == int:
						for cancel_btn in cancel_btns.get('elements'):
							if len(cancel_btn.get_attribute('id').split('-')) == 5:
								tools_test.click_element(element_definition = cancel_btn)
								action_status = False
								break
				# ожидаем, когда пропадет форма создания\редактирования виджета
				add_form = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-ext-comp-\'', timeOut = 0.1)
				if type(add_form.get('count')) == int:
					if add_form.get('count') == 0:
						test_status = True
				if test_status:
					break				
				if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
					print('Не удалось закрыть окно создания виджета')
					break
# ----------------------------------------------------------------------------------------------------------------------------------------------------
# в  цикле, по списку виджетов последовательно создаем и удаляем виджеты
		# получаем список вкладок
		for folder in presets.keys():
			# перебираем в папке все значения\виджеты
			for preset in presets.get(folder):
				# находим и нажимаем кнопку с плюсом для создания нового готового виджета
				if test_status:
					test_step_await = tools_test.wait_for_results()
					while True:
						test_status = False
						plus_buttoms = tools_test.elements_list(object_type = 'a', search_type = 'contains', mask = 'id, \'dashboards-page-button-\'', timeOut = 0.2)
						for button in plus_buttoms.get('elements'):
							if 'cm-editable-tabbar-add-btn' not in button .get_attribute('class'):
								tools_test.click_element(element_definition = button, breakONerror = False, scroll_to_element = False, timeOut = 0.2)
								break
						get_text_object = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-title-\'', timeOut = 0.2)
						for text_object in get_text_object.get('elements'):
							if text_object.text == 'ДОБАВИТЬ ВИДЖЕТ':
								test_status = True
						if test_status:
							break				
						if tools_test.wait_for_results(time_data = test_step_await, time_out = time_out).get('result'):
							print('Выпадающее меню: Добавить виджет не появилось. строка теста')
							break
				# выбираем пунк: Говый виджет
				if test_status:
					test_step_await = tools_test.wait_for_results()
					while True:
						test_status = False
						dd_menu_items = tools_test.elements_list(object_type = 'span', search_type = 'contains', mask = 'id, \'dashboards-page-menuitem-\'')
						if type(dd_menu_items.get('count')) == int:
							for new_btn in dd_menu_items.get('elements'):
								if 'Готовый' in new_btn.text:
									tools_test.click_element(element_definition = new_btn, breakONerror = False, scroll_to_element = False, timeOut = 0.2)
									break
						# ожидаем появление формы: Добавление готового виджета
						if type(dd_menu_items.get('count')) == int:
							form_headers = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-title-\'', timeOut = 0.1)
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
				if test_status:
					# определяем текущие виджеты на странице 
					# создаем виджет
					va.dash_creation_widget_from_preset(widget_folder = folder, widget_name = preset)
					# определяем текущие виджеты на странице
					widgets = va.dash_define_widgets_at_dashboard(time_out = 0.5)
					for widget_type in list(widgets.get('existing_widgets').keys()):
						if len(widgets.get('existing_widgets').get(widget_type)) != 0:
							loking_type = widget_type
							break
					# удадяем созданный виджет
					va.dash_delete_widget(widget = {loking_type:{preset:None}}, time_out = 10)
					print('widget: {}, checked:\t{}\t:\t{}'.format(preset, str(datetime.utcnow()),test_name))
		# закрываем браузер
		if test_status:
			main_unit.close_browser
		print('OVER:\t{}\t:\t{}\ttesting index = {}'.format(str(datetime.utcnow()),test_name, index_testing))
		index_testing += 1

