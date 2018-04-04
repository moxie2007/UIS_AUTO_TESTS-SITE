'''
Тест: нагрузочный тест загрузки отчета.
отчет: Общие отчеты - Анализ трафика
временной интервал: 01.12.2017-28.02.2018
- тест заточен под пользователя 74 на ПредПродакшене
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
configLK.set_lk_parametrs(source_name = 'ADMIN_LOAD')

time_out = 10

# в методе авторизация через админку

# тело теста
if __name__ == '__main__':
	index_testing = 1
	for tt in range(5):
		print('START:\t{}\t:\t{}'.format(str(datetime.utcnow()),'load_sanity'))
		# модуль инициализации (открываем браузер)
		main_unit = start_uis_test.Global_unit()
		driver = main_unit.init_browser(product_type = 'ch')
		va = vats_tools.Vats_tools(driver)
		tools_test = tools.Uis_tools(driver) # (инициализация модуля с таким именем из-за того что внутри происходит переопределение такого имени: tools)
		# логинимся в ЛК
		tools_test.login_toLK_by_admin(adm_login = configLK.get_user_name, adm_pass = configLK.get_pass, user_id = '74', stend_url = configLK.get_login_url, timeOut = 120, breakONerror = False)
		# tools_test.switch_env(server_name = 'siteapp2.webdev.uiscom.ru')
		tools_test.switch_env(server_name = 'comagic.ru')
		tools_test.lk_sidemenu_navigation(item_menu = ['Общие отчёты', 'Анализ трафика'])
		# ожидаем появление иконки календаря
		step_await = tools_test.wait_for_results()
		while True:
			test_status = False
			icons = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'visitorsource-page-cm-datecontrol-date_range-\'')
			if type(icons.get('count')) == int:
				for icon in icons.get('elements'):
					if len(icon.get_attribute('id').split('-')) == 8:
						calendar_icon = icon
						test_status = True
			if test_status:
				break
			if tools_test.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
				loger.file_log(text = 'немогу найти иконку открытия календаря', text_type = 'ERROR  ')		
		# находим значение количества записей на станице
		if test_status:
			while True:
				test_status = False
				counters_before = tools_test.get_total_list_values_count(timeOut = time_out)[0]
				test_status = True
				if test_status:
					break
				if tools_test.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'несмогли определить количество записей на странице', text_type = 'ERROR  ')
		# нажимаем на иконку и ожидаем открытия календаря, запоминаем родительскую форму календаря
		if test_status:
			tools_test.click_element(element_definition = calendar_icon, timeOut = time_out)
			while True:
				test_status = False
				calendar_forms = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'visitorsource-page-cm-daterange-popup-\'')
				if type(calendar_forms.get('count')) == int:
					for form in calendar_forms.get('elements'):
						if len(form.get_attribute('id').split('-')) == 6:
							parent_form = form
							test_status = True
				if test_status:
					break
				if tools_test.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'не определяется, открылся календарь или нет', text_type = 'ERROR  ')
		# находим input поля значения: С в календаре
		if test_status:
			while True:
				test_status = False
				dates_from = tools_test.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'visitorsource-page-ul-daterange-datefield-startDate-\'')
				if type(dates_from.get('count')) == int:
					for date_from in dates_from.get('elements'):
						if date_from.get_attribute('data-ref') == 'inputEl':
							tools_test.change_value(element_definition = date_from, text = '01.01.2017', breakONerror = False)
							test_status = True
				if test_status:
					break
				if tools_test.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'немогу найти поле ввода даты: Start date', text_type = 'ERROR  ')
		# находим input поля значения: ДО в календаре
		if test_status:
			while True:
				test_status = False
				dates_end = tools_test.elements_list(object_type = 'input', search_type = 'contains', mask = 'id, \'visitorsource-page-ul-daterange-datefield-endDate-\'')
				if type(dates_end.get('count')) == int:
					for date_end in dates_end.get('elements'):
						if date_end.get_attribute('data-ref') == 'inputEl':
							tools_test.change_value(element_definition = date_end, text = '28.02.2018', breakONerror = False)
							test_status = True
				if test_status:
					break
				if tools_test.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'немогу найти поле ввода даты: END date', text_type = 'ERROR  ')
		# находим кнопку: Применить и нажимаем
		if test_status:
			while True:
				test_status = False
				save_btns = tools_test.elements_list(object_type = 'a', search_type = 'contains', mask = 'id, \'visitorsource-page-ul-mainbutton-save-\'')
				if type(save_btns.get('count')) == int:
					for save_btn in save_btns.get('elements'):
						if len(save_btn.get_attribute('id').split('-')) == 6:
							tools_test.click_element(element_definition = save_btn)
							print('нажали кнопку: Применить:\t\t\t\t{}'.format(datetime.utcnow()))
							test_status = True
				if test_status:
					break
				if tools_test.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'кнопка: Применить, не найдена', text_type = 'ERROR  ')
		if test_status:
			while True:
				test_status = False
				counters_after = tools_test.get_total_list_values_count(timeOut = time_out)[0]
				try:
					if counters_before != counters_after:
						test_status = True
				except:
					pass
				if test_status:
					break
				if tools_test.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'кнопка: Применить, не найдена', text_type = 'ERROR  ')
		# закрываем браузер
		print('значение сменилось:\t\t\t\t\t\t{}'.format(datetime.utcnow()))
		if test_status:
			main_unit.close_browser
		print('OVER:\t{}\t:\t{}\ttesting index = {}'.format(str(datetime.utcnow()),'load_sanity', index_testing))
		index_testing += 1

