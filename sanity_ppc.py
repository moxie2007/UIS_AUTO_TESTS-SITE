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
configLK.set_lk_parametrs(source_name = 'YA')

# lk_elements  = pageElements.LK()
# # импортируем настройки из предварительно подготовленного файла
# configLK = tools.User_config()
# configLK.set_lk_parametrs()

loger.file_log(text = 'Start asi test', text_type = 'SUCCESS')

# модуль инициализации
main_unit = start_uis_test.Global_unit()
driver = main_unit.init_browser(product_type = 'ch')

tools = tools.Uis_tools(driver)
asi = asi_tools.Asi_tools(driver)

# tools.login_to(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass)
# tools.switch_env(selected_element = 'lk_env_select', server_name = 'siteaasi1.webdev.uiscom.ru')
# tools.lk_sidemenu_navigation (item_menu = ['Сайты'],  timeOut = 120)

asi.login_to_yandex(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass)


