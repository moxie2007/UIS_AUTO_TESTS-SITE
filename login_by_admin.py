import  random, sys, time
from time import gmtime, strftime
from datetime import datetime

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

import tools, pageElements, widgets_tools, vats_tools, start_uis_test
from loger import Loger as loger

from testrail import *


lk_elements  = pageElements.LK()
# импортируем настройки из предварительно подготовленного файла
configLK = tools.User_config()
configLK.set_lk_parametrs()

loger.file_log(text = 'Start sanity (NEW mode) test', text_type = 'SUCCESS')

# модуль инициализации
main_unit = start_uis_test.Global_unit()
driver = main_unit.init_browser(product_type = 'ch')

tools = tools.Uis_tools(driver)
wg = widgets_tools.Wg_tools(driver)
va = vats_tools.Vats_tools(driver)

print('START:\t{}\t:\t{}'.format(str(datetime.utcnow()),'vats_sanity'))

tools.login_toLK_by_admin(adm_login = 'kuznetsov', adm_pass = 'Ikuznetsov159', user_id = '1103', stend_url = 'http://admin.test2.webdev.uiscom.ru/')

print('\nOVER:\t{}\t:\t{}'.format(str(datetime.utcnow()),'vats_sanity'))

time.sleep(5)
main_unit.close_browser