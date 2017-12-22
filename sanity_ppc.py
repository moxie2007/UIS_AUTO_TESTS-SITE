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



'''логин в рс'''
# tools.login_to_system(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass, system_is = 'Yandex')
'''логин в лк комеджик'''
configLK.set_lk_parametrs(source_name = 'LK')
tools.login_to(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass)

'''переход в список сайтов
	переход в настройки сайта'''
tools.lk_sidemenu_navigation (item_menu = ['Сайты'],  timeOut = 120)
# переходим в редактирование сайта ns-studio.su или siteaasi1.webdev.uiscom.ru
asi.sites_edit_site(site_name = 'ns-studio.su', timeOut = 120)
time.sleep(5)
# переходим в режим Интеграция с сервисами
tools.top_menu_navigation (tab_name = 'Интеграция с сервисами', timeOut = 20)


'''подключение интеграции
	ввод логина
	клик по кнопке
	клик на выбор аккаунта (для гугла)'''


time.sleep(5)
main_unit.close_browser
print('FINISH!')
loger.file_log(text = 'Finish test', text_type = 'SUCCESS', test_case_id = 45440, comment = 'Finish test. at ' + str(datetime.utcnow()))
