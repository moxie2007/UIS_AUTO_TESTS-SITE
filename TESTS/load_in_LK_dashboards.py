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
configLK.set_lk_parametrs(source_name = 'ADMIN_LK')

time_out = 10
# в методе авторизация через админку

def existing_await():
	result = False
	step_await = tools_test.wait_for_results()
	while True:
		test_status = False
		icons = tools_test.elements_list(object_type = 'div', search_type = 'contains', mask = 'id,\'dashboards-page-container-dash-info-\'', timeOut = 0.8)
		if type(icons.get('count')) == int:
			for icon in icons.get('elements'):
				if 'Звонки' in icon.text:
					test_status = True
					break
		if test_status:
			result = True
			break
		if tools_test.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
			loger.file_log(text = 'немогу найти легенду виджета', text_type = 'ERROR  ')
	return result	


# тело теста
if __name__ == '__main__':
	test_values  = []
	today = datetime.today()
	index_testing = 1
	for tt in range(11):
		# print('START:\t{}\t:\t{}'.format(str(datetime.utcnow()),'load_sanity'))
		# модуль инициализации (открываем браузер)
		main_unit = start_uis_test.Global_unit()
		driver = main_unit.init_browser(product_type = 'ch')
		va = vats_tools.Vats_tools(driver)
		tools_test = tools.Uis_tools(driver) # (инициализация модуля с таким именем из-за того что внутри происходит переопределение такого имени: tools)
		# логинимся в ЛК
		tools_test.login_toLK_by_admin(adm_login = configLK.get_user_name, adm_pass = configLK.get_pass, user_id = '4735', stend_url = configLK.get_login_url, timeOut = 120, breakONerror = False)
		# tools_test.login_to(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass, breakONerror = True)
		tools_test.switch_env(server_name = 'siteapp.webdev.uiscom.ru')
		tools_test.lk_sidemenu_navigation(item_menu = ['Дашборды'])
		test_status = True
		# получаем легенду
		if existing_await():
			see_legend = today.timestamp()
			step_await = tools_test.wait_for_results()
			tools_test.switch_env(server_name = 'siteapp1.webdev.uiscom.ru')
			St = datetime.utcnow()
			while True:
				test_status = False
				if existing_await():
					test_status = True
				if test_status:
					Sp = datetime.utcnow()
					break
				if tools_test.wait_for_results (time_data = step_await, time_out = time_out).get('result'):
					loger.file_log(text = 'немогу найти легенду виджета', text_type = 'ERROR  ')		
		if test_status:
			result_time = Sp-St
			test_values.append(float(str(result_time).split(':')[2]))
			# test_values.append(result_time.seconds*1000000 + result_time.microseconds)
			main_unit.close_browser
		index_testing += 1
	over_result = sorted(test_values)
	seredina = int(len(over_result)/2)

	print('Значение величины ожидания, по медиане = {}'.format(over_result[seredina]))


