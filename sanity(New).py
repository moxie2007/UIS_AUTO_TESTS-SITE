import tools, pageElements, random, widgets_tools, start_uis_test
from loger import Loger as loger
from selenium.webdriver.support.ui import Select
import time
from time import gmtime, strftime
from datetime import datetime
from testrail import *


lk_elements  = pageElements.LK()
# импортируем настройки из предварительно подготовленного файла
configLK = tools.User_config()
configLK.set_lk_parametrs()

loger.file_log(text = 'Start sanity (NEW mode) test', text_type = 'SUCCESS')

# модуль инициализации
main_unit = start_uis_test.Global_unit()
driver = main_unit.init_browser()
tools = tools.Uis_tools(driver)
wg = widgets_tools.Wg_tools(driver)

# тест консультант -- Каналы --  Сайтфон
		# tools.login_to(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass)
		# tools.switch_env(selected_element = 'lk_env_select', server_name = 'siteow1.webdev.uiscom.ru')
		# tools.lk_sidemenu_navigation (item_menu = ['Консультант', "Каналы"],  timeOut = 120)
		# tools.top_menu_navigation(tab_name = 'Сайтфон')
		# time.sleep(2)
		# print('Статус капчи:  ', wg.define_kapcha_status)
		# time.sleep(5)
		# wg.switch_kapcha_status()
		# time.sleep(5)
		# main_unit.close_browser
		# print('OVER!')
		# loger.file_log(text = 'Finish sanity test', text_type = 'SUCCESS', test_case_id = 45440, comment = 'Finish sanity test. at ' + str(datetime.utcnow()))

# тест в консультант -- общие настройки -- шаблоны сообщений
	# tools.login_to(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass)
	# tools.switch_env(selected_element = 'lk_env_select', server_name = 'siteow1.webdev.uiscom.ru')
	# tools.lk_sidemenu_navigation (item_menu = ['Консультант', "Общие настройки"],  timeOut = 120)

	# wg.general_settings_add_template(template_name = 'кузнецов_тест', timeOut = 120)
	# wg.general_settings_edit_template(template_name = 'кузнецов_тест', new_name = 'my test', timeOut = 120)
	# wg.general_settings_delete_templates(template_name = 'my test')

	# main_unit.close_browser
	# time.sleep(2)

	# print('OVER!')
	# loger.file_log(text = 'Finish sanity test', text_type = 'SUCCESS', test_case_id = 45440, comment = 'Finish sanity test. at ' + str(datetime.utcnow()))

# тест в консультант -- общие настройки -- шаблоны сообщений
tools.login_to(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass)
tools.switch_env(selected_element = 'lk_env_select', server_name = 'siteow1.webdev.uiscom.ru')
tools.lk_sidemenu_navigation (item_menu = ['Консультант', "Общие настройки"],  timeOut = 120)

tools.top_menu_navigation(tab_name = 'Черный список')
# wg.general_settings_add_template(template_name = 'кузнецов_тест', timeOut = 120)
# wg.general_settings_edit_template(template_name = 'кузнецов_тест', new_name = 'my test', timeOut = 120)
# wg.general_settings_delete_templates(template_name = 'my test')

print(wg.black_list_add_new_address(1,2))
main_unit.close_browser
time.sleep(2)

print('OVER!')
loger.file_log(text = 'Finish sanity test', text_type = 'SUCCESS', test_case_id = 45440, comment = 'Finish sanity test. at ' + str(datetime.utcnow()))