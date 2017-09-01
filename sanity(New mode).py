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
configLK = tools.User_config()
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
	
	# time.sleep(2) siteapp2.webdev.uiscom.ru  siteow1.webdev.uiscom.ru
	tools.switch_env(selected_element = 'lk_env_select', server_name = 'sitecw2.webdev.uiscom.ru')
	# time.sleep(1)
	tools.lk_sidemenu_navigation (item_menu = ['Консультант', "Общие настройки"],  timeOut = 120)

	tools.general_settings_edit_template(template_name = 'test_1', new_name = 'test_1_1', timeOut = 120)
	# //*[@id="commonsettings-page-displayfield-id-1170-inputEl"]/a[1]/img
	# time.sleep(2)

	tools.general_settings_edit_template(template_name = 'test_1_1', new_name = 'test_1', timeOut = 120)
	# print(tools.get_total_list_values_count()[0])



	
	# tools.lk_sidemenu_navigation (item_menu = ['Лидогенератор'],  timeOut = 120)

	# # print(tools.get_total_list_values_count()[0])
	
	# tools.lk_sidemenu_navigation (item_menu = ['Консультант', "Общие настройки"],  timeOut = 120)
	
	# создание новых шаблонов	
	for i in range(1):
		tools.general_settings_add_template(template_name = 'txbwe_' + str(i+1))

	# time.sleep(1)

	# while True:
	# 	if int(tools.get_total_list_values_count()[0]) < 10:
	# 		break
	# 	tools.general_settings_delete_templates(template_name = tools.general_settings_get_templates_list[1][0].text )
	


			# tools.general_settings_delete_templates(template_name = 'txbest_IIIz_Kv_5qwe_2', timeOut = 5 )
			
			# time.sleep(2)
			# try:
			# 	print(tools.get_total_list_values_count()[0])
			# except Exception as ex:
			# 	print('--: ', ex)

			# time.sleep(1)
			# tools.general_settings_delete_templates(template_name = 'txbest_IIIz_Kv_5qwe_10', timeOut = 5  )

			# time.sleep(1)
			# try:
			# 	print(tools.get_total_list_values_count()[0])
			# except Exception as ex:
			# 	print('--: ', ex)

	# time.sleep(2)
	# tools.general_settings_delete_templates(template_name = 'test_Kziv_5qwe_1', timeOut = 5  )


	# try:
	# 	tools.choose_paging_value('дальше', timeOut = 1, breakONerror = False)
	# except:
	# 	pass

	# tools.get_active_page_in_list


	# tools.lk_sidemenu_navigation (item_menu = ['Аналитика', "Рекламные кампании"],  timeOut = 120)

	# time.sleep(5)

	# for i in range (5):
	# 	tools.general_settings_delete_templates(template_name = 'test_IIIz_Kv_5qwe_' + str(4 + i))








	# while tools.displayed_element(element_definition = tools.get_paging_templates_list[1].get('дальше')):
	# 	# print(tools.get_active_page_in_list)
	# 	if '5' in tools.get_active_page_in_list[0]:
	# 		break
	# 	# print(tools.get_active_page_in_list[1].keys())
	# 	tools.choose_paging_value('дальше', timeOut = 1, breakONerror = False)
	# 	print('-'*100)






		# time.sleep(2)

	# items = tools.general_settings_get_templates_list
	# for item in items[1]:
	# 	print(item.text)
	
	# тут
		# navi = tools.general_settings_get_paging_templates_list
		# # print(navi[0])
		# # print(navi[1])

		# # for i in range(2):
		# # 	index = 0 + i
		# # 	try:
		# # 		tools.general_settings_delete_templates(template_name = 'test_3y_' + str(index))
		# # 	except Exception as ex:
		# # 		print(ex)

		# for i in range(5):
		# 	tools.general_settings_add_template(template_name = 'test_01_' + str(i))
		# 	time.sleep(3)


		# print(tools.general_settings_get_templates_list)

	# # тут
		# 	# time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Теги'],  timeOut = 120)
		# 	# time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Уведомления'],  timeOut = 120)
		# 	# time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Графики активности'],  timeOut = 120)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Адресная книга'],  timeOut = 120)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Сотрудники'],  timeOut = 120)	
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Сайты'],  timeOut = 120)	
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Сайтфон'],  timeOut = 10)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Лидогенератор'],  timeOut = 10)
			
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Аналитика', "Сегменты"],  timeOut = 120)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Аналитика', "События"],  timeOut = 120)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Аналитика', "Рекламные кампании"],  timeOut = 120)
			
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Виртуальная АТС', "Факсы"],  timeOut = 10)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Виртуальная АТС', "База файлов"],  timeOut = 10)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Виртуальная АТС', "Опции разговора"],  timeOut = 10)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Виртуальная АТС', "Сценарии"],  timeOut = 120)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Виртуальная АТС', "Виртуальные номера и правила"],  timeOut = 120)

		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Консультант','Распределение обращений'],  timeOut = 10)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Консультант','Внешний вид'],  timeOut = 10)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Консультант','Каналы'],  timeOut = 10)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Консультант','Общие настройки'],  timeOut = 120)

		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Служебные', "Уведомления"],  timeOut = 10)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Служебные', "Запросы к API"],  timeOut = 10)

		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Лидогенерация'],  timeOut = 120)

		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Список обращений', "Звонки"],  timeOut = 10)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Список обращений', "Чаты"],  timeOut = 120)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Список обращений', "Заявки"],  timeOut = 120)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Список обращений', "Цели"],  timeOut = 10)

		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Общие отчёты', "Распределение входящих звонков"],  timeOut = 10)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Общие отчёты', "Обращения по сотрудникам"],  timeOut = 10)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Общие отчёты', "Качество обращений"],  timeOut = 120)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Общие отчёты', "Динамика обращений"],  timeOut = 120)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Общие отчёты', "Аудитория"],  timeOut = 120)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Общие отчёты', "Анализ трафика"],  timeOut = 120)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Общие отчёты', "Сквозная аналитика"],  timeOut = 120)
		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Общие отчёты', "Содержание"],  timeOut = 120)

		# 	time.sleep(2)
		# 	tools.lk_sidemenu_navigation (item_menu = ['Обзор'],  timeOut = 10)

		# 		# time.sleep(2)
		# 		# tools.lk_sidemenu_navigation (item_menu = ['Сайтфон'],  timeOut = 120)

		# 		# time.sleep(2)
		# 		# tools.lk_sidemenu_navigation (item_menu = ['Сайтфон'],  timeOut = 120)

		# 		# time.sleep(2)
		# 		# tools.lk_sidemenu_navigation (item_menu = ['Сайтфон'],  timeOut = 120)

		# 		# time.sleep(2)
		# 		# tools.lk_sidemenu_navigation (item_menu = ['Сайтфон'],  timeOut = 120)

		# 		# time.sleep(2)
		# 		# tools.lk_sidemenu_navigation (item_menu = ['Сайтфон'],  timeOut = 120)

		# 		# time.sleep(2)
		# 		# tools.lk_sidemenu_navigation (item_menu = ['Виртуальная АТС', "Сценарии"],  timeOut = 120)
		# 		# time.sleep(2)
		# 		# tools.lk_sidemenu_navigation (item_menu = ['Служебные', "Уведомления"],  timeOut = 120)
		# 		# time.sleep(2)
		# 		# tools.lk_sidemenu_navigation (item_menu = ["Уведомления"],  timeOut = 120)
		# 		# time.sleep(2)
		# 		# tools.lk_sidemenu_navigation (item_menu = ['Служебные', "Уведомления"],  timeOut = 120)
		# 		# time.sleep(2)
		# 		# tools.lk_sidemenu_navigation (item_menu = ['Список обращений', "Звонки"],  timeOut = 120)
		# 		# time.sleep(2)
		# 		# tools.lk_sidemenu_navigation (item_menu = ['Список обращений', "Чаты"],  timeOut = 120)
		# 		# time.sleep(2)
		# 		# tools.lk_sidemenu_navigation (item_menu = ['Список обращений', "Цели"],  timeOut = 120)
	# 		# time.sleep(10)


	# tools.top_menu_navigation(tab_name = 'Черный список')
	# time.sleep(2)
	# print(tools.general_settings_get_templates_list[0])
	# new_name = 'test_3bu_'
	# for index in range(250):
	# 	text = str(new_name) + str(index)
	# 	tools.general_settings_add_template(template_name = str(text))
	


	# tools.get_total_list_values_count()
	# # print(tools.get_total_list_values_count())
	# time.sleep(5)

		# tools.lk_sidemenu_navigation (item_menu = ['Виртуальная АТС', "Виртуальные номера и правила"],  timeOut = 120)
		# # time.sleep(1)
		# tools.get_total_list_values_count()
		# # print(tools.get_total_list_values_count())
		

		# tools.lk_sidemenu_navigation (item_menu = ['Служебные', "Уведомления"],  timeOut = 120)
		# # time.sleep(1)
		# tools.get_total_list_values_count()

		# tools.lk_sidemenu_navigation (item_menu = ['Уведомления'],  timeOut = 120)
		# # time.sleep(1)
		# tools.get_total_list_values_count()

		# # tools.lk_sidemenu_navigation (item_menu = ['Служебные', "Уведомления"],  timeOut = 120)
		# # time.sleep(1)
		# tools.get_total_list_values_count()


	print('OVER!')
	# time.sleep(2)
	tools.close_browser()
loger.file_log(text = 'Finish sanity test', text_type = 'SUCCESS', test_case_id = 45440, comment = 'Finish sanity test. at ' + str(datetime.utcnow()))
