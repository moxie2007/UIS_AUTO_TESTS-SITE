'''
Тест: .
требования: 
- 
'''
import sys
sys.path.append('C:\\UIS_AUTO_TESTS\\UIS_AUTO_TESTS-SITE')

import  random, sys, time
from time import gmtime, strftime
from datetime import datetime
import tools, pageElements, comagic_objects, start_uis_test, asi_tools
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
		obj_search = comagic_objects.LK(driver)
		# va = vats_tools.Vats_tools(driver)
		tools_test = tools.Uis_tools(driver) # (инициализация модуля с таким именем из-за того что внутри происходит переопределение такого имени: tools)
		asi = asi_tools.Asi_tools(driver)
		# логинимся в ЛК
		tools_test.login_to(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass, breakONerror = True)
		# переходим в меню даши
		tools_test.lk_sidemenu_navigation(item_menu = ['Сайты'], breakONerror = True)
		# переходим на предварительно подготовленную вкладку
		test_status = False
		print(asi.get_parent_obj_by_site_name(site_name = '123.ru'))
		test_status = True
		# закрываем браузер
		if test_status:
			main_unit.close_browser
	print('OVER:\t{}\t:\t{}\ttesting index = {}'.format(str(datetime.utcnow()),'vats_sanity', index_testing))
	index_testing += 1

