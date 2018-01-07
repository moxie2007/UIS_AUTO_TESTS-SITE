import  random, sys, time
from time import gmtime, strftime
from datetime import datetime

# import tools, pageElements, widgets_tools, vats_tools, start_uis_test
import tools, pageElements, start_uis_test
from loger import Loger as loger


def login_get_west_menu_items(tools = None, driver = None, my_user_id = '1103'):

	timeOut = 120
	tools.login_toLK_by_admin(adm_login = 'kuznetsov', adm_pass = 'Ikuznetsov159', user_id = my_user_id, stend_url = 'http://admin.test2.webdev.uiscom.ru/')
	time_index = 0
	while True:
		# ждем появление основного меню
		left_menu = tools.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'cm-mainmenu-\'')
		if type(left_menu.get('count')) == int:
			print('item: ', left_menu)
			break
		
		if time_index >= timeOut:
			print('time out: ERROR')
			loger.file_log(text = 'Can\'t find icon: Clients', text_type = 'ERROR  ')
			break
			if breakONerror is True:
				self.close_browser
				loger.file_log(text = 'Finish sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
		time.sleep(1)
		time_index += 1
	main_unit.close_browser


if __name__ == '__main__':
	print('START:\t{}\t:\t{}'.format(str(datetime.utcnow()),'vats_sanity'))
	users_ids = ['1103', '2153', '4735', '10145', '11128', '33247', '51522', '51523']
	for test_step in users_ids:
		# модуль инициализации (открываем браузер)
		main_unit = start_uis_test.Global_unit()
		driver = main_unit.init_browser(product_type = 'ch')
		tools_test = tools.Uis_tools(driver) # (инициализация модуля с таким именем из-за того что внутри происходит переопределение такого имени: tools)
		login_get_west_menu_items(tools = tools_test, driver = None, my_user_id = test_step)

	print('OVER:\t{}\t:\t{}'.format(str(datetime.utcnow()),'vats_sanity'))

