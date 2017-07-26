import tools as tools 
import loger 
from loger import Loger as loger
import pageElements
from selenium.webdriver.support.ui import Select
import time
from time import gmtime, strftime
import random
import datetime
from datetime import datetime
from testrail import *

lk_elements  = pageElements.LK()
# driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)

# импортируем настройки из предварительно подготовленного файла
configLK = tools.Use_config()
configLK.set_lk_parametrs()

# это надо еще сделать!!!!!!
# configTR = tools.Use_config()
# configTR.set_tr_parametrs()

tools = tools.Uis_tools()

# user = 23
# timeOut = 30

loger.file_log(text = 'Start sanity (NEW mode) test', text_type = 'SUCCESS')
# ------------------------------------------------------------------------------------
# алгоритм теста: авторизуемся в личном кабинете
# ------------------------------------------------------------------------------------
for test_step in range(1):
	# авторизуемся в личном кабинете
	step = tools.login_to(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass)
	
	time.sleep(2)
	tools.switch_env(selected_element = 'lk_env_select', server_name = 'siteow1.webdev.uiscom.ru')
	time.sleep(1)
	tools.lk_sidemenu_navigation (item_menu = ['Консультант', "Общие настройки"],  timeOut = 120)
	tools.top_menu_navigation(tab_name = 'Черный список')
	time.sleep(2)
	tools.top_menu_navigation(tab_name = 'Удерживающие сообщения')
	time.sleep(2)
	tools.top_menu_navigation(tab_name = 'Обратный звонок')
	time.sleep(2)
	tools.top_menu_navigation(tab_name = 'Системные сообщения')
	time.sleep(2)
	tools.lk_sidemenu_navigation (item_menu = ['Служебные','Уведомления'],  timeOut = 120)
	tools.switch_env(selected_element = 'lk_env_select', server_name = 'analyti.ga')
	tools.lk_sidemenu_navigation (item_menu = ['Сайтфон'],  timeOut = 120)
	time.sleep(2)
	tools.top_menu_navigation(tab_name = 'Обратный звонок')
	time.sleep(2)
	print('OVER!')
	time.sleep(2)
	tools.close_browser()
loger.file_log(text = 'Finish sanity test', text_type = 'SUCCESS', test_case_id = 45440, comment = 'Finish sanity test. at ' + str(datetime.utcnow()))