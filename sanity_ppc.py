import tools, pageElements, random, asi_tools, start_uis_test, sys
from loger import Loger as loger
from selenium.webdriver.support.ui import Select
import time
from time import gmtime, strftime
from datetime import datetime
from testrail import *


lk_elements  = pageElements.LK()
# импортируем настройки из предварительно подготовленного файла
configLK = tools.User_config()
# configLK.set_lk_parametrs(source_name = 'LK')
configLK.set_lk_parametrs(source_name = 'YA')
# configLK.set_lk_parametrs(source_name = 'GG')

loger.file_log(text = 'Start asi test', text_type = 'SUCCESS')

# модуль инициализации
main_unit = start_uis_test.Global_unit()
driver = main_unit.init_browser(product_type = 'ff')
tools = tools.Uis_tools(driver)
asi = asi_tools.Asi_tools(driver)



# asi.login_to_yandex(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass)

'''логин в рс'''
# configLK.set_lk_parametrs(source_name = 'GG')
# asi.login_to_google(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass)
tools.login_to_system(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass, system_is = 'Yandex')
'''логин в лк комеджик'''
configLK.set_lk_parametrs(source_name = 'LK')
tools.login_to(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass)

'''переход в список сайтов
	переход в настройки сайта'''
tools.lk_sidemenu_navigation (item_menu = ['Сайты'],  timeOut = 120)

'''переход во вкладку интеграции'''

'''подключение интеграции
	ввод логина
	клик по кнопке
	клик на выбор аккаунта (для гугла)'''

''''''

''''''

