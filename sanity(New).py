import tools, pageElements, random, widgets_tools, start_uis_test, sys, comagic_objects
from loger import Loger as loger
from selenium.webdriver.support.ui import Select
import time
from time import gmtime, strftime
from datetime import datetime
from testrail import *


lk_elements  = pageElements.LK()

# импортируем настройки из предварительно подготовленного файла
configLK = tools.User_config()
configLK.set_lk_parametrs(source_name = 'WIDGETS_LK')

loger.file_log(text = 'Start sanity (NEW mode) test', text_type = 'SUCCESS')

# модуль инициализации
main_unit = start_uis_test.Global_unit()
driver = main_unit.init_browser(product_type = 'ch')

tools = tools.Uis_tools(driver)
wg = widgets_tools.Wg_tools(driver)
new_elements = comagic_objects.LK(driver)

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

debug = False

# тест в консультант -- общие настройки -- шаблоны сообщений
tools.login_to(url = configLK.get_login_url, user = configLK.get_user_name, password = configLK.get_pass)
tools.switch_env(selected_element = 'lk_env_select', server_name = 'sitecw2.webdev.uiscom.ru')
tools.lk_sidemenu_navigation (item_menu = ['Консультант', "Чат"],  timeOut = 120)

print(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_displayed_at_devices_group_name_main_settings',debug = debug).get('object')).get('element').text )
print(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_displayed_at_site_help_text_main_settings', debug = debug).get('object')).get('element').text )

for i in range(2):
	tools.displayed_element(element_definition = new_elements.ONOFF_BUTTON(element_definition = 'consultant_displayed_at_site_btn_main_settings', debug = debug).get('object')).get('element').click()
	time.sleep(0.5)


print(tools.displayed_element(element_definition = new_elements.CHECKBOX(element_definition = 'consultant_displayed_at_pc_main_settings', debug = debug).get('object')) )
print(tools.displayed_element(element_definition = new_elements.CHECKBOX(element_definition = 'consultant_displayed_at_phone_main_settings', debug = debug).get('object')) )
print(tools.displayed_element(element_definition = new_elements.CHECKBOX(element_definition = 'consultant_displayed_at_tablet_main_settings', debug = debug).get('object')) )

print(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_banner_text_text_main_settings', debug = debug).get('object')).get('element').text )


print(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_help_text_used_symbols_banner_text_text_main_settings', debug = debug).get('object')).get('element').text )

text_at_banner = tools.displayed_element(element_definition = new_elements.INPUT(element_definition = 'consultant_input_for_banner_text_main_settings', debug = debug).get('object'))
tools. change_value(element_definition = text_at_banner.get('element'), text = 'NWE_NAME')

print(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_help_text_used_symbols_banner_text_text_main_settings', debug = debug).get('object')).get('element').text )

print(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_personal_data_request_header_main_settings', debug = debug).get('object')).get('element').text )
its_icon = tools.displayed_element(element_definition = new_elements.ICONS(element_definition = 'consultant_personal_data_request_icon_main_settings', debug = debug).get('object')).get('element')
time.sleep(1)
tools.move_cursor_to_the_object(current_object = its_icon)
time.sleep(1)
print(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_personal_data_help_text_from_icon_main_settings', debug = debug).get('object')).get('element').text )

print('{}: {}'.format(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_personal_data_text_name_main_settings', debug = True).get('object')).get('element').text,	tools.displayed_element(element_definition = new_elements.DROP_DOWN_FIELD(element_definition = 'consultant_field_dd_name_main_settings', debug = True).get('object')).get('element').get_attribute('value') ))
print('{}: {}'.format(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_personal_data_text_phone_main_settings', debug = True).get('object')).get('element').text, tools.displayed_element(element_definition = new_elements.DROP_DOWN_FIELD(element_definition = 'consultant_field_dd_phone_main_settings', debug = True).get('object')).get('element').get_attribute('value') ))
print('{}: {}'.format(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_personal_data_text_email_main_settings', debug = True).get('object')).get('element').text, tools.displayed_element(element_definition = new_elements.DROP_DOWN_FIELD(element_definition = 'consultant_field_dd_email_main_settings', debug = True).get('object')).get('element').get_attribute('value') ))

print(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_personal_data_operator_header_main_settings', debug = debug).get('object')).get('element').text )

for i in range(3):
	tools.displayed_element(element_definition = new_elements.CHECKBOX(element_definition = 'consultant_operator_evaluation_main_settings', debug = debug).get('object')).get('element').click()
	time.sleep(0.3)
print(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_operator_evaluation_text_main_settings', debug = debug).get('object')).get('element').text )
its_icon = tools.displayed_element(element_definition = new_elements.ICONS(element_definition = 'consultant_operator_evaluation_icon_main_settings', debug = debug).get('object')).get('element')
time.sleep(1)
tools.move_cursor_to_the_object(current_object = its_icon)
time.sleep(1)
print(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_personal_data_help_text_from_icon_main_settings', debug = debug).get('object')).get('element').text )


for i in range(2):
	tools.displayed_element(element_definition = new_elements.CHECKBOX(element_definition = 'consultant_operator_limit_main_settings', debug = debug).get('object')).get('element').click()
	time.sleep(0.3)
print('{}: {}'.format(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_operator_limit_main_settings', debug = debug).get('object')).get('element').text,
tools.displayed_element(element_definition = new_elements.INPUT(element_definition = 'consultant_operator_limit_main_settings', debug = debug).get('object')).get('element').get_attribute('value') ))

for i in range(2):
	tools.displayed_element(element_definition = new_elements.CHECKBOX(element_definition = 'consultant_allow_operator_invite_main_settings', debug = debug).get('object')).get('element').click()
	time.sleep(0.3)
print('{}'.format(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_allow_operator_invite_main_settings', debug = debug).get('object')).get('element').text))


for i in range(2):
	tools.displayed_element(element_definition = new_elements.CHECKBOX(element_definition = 'consultant_files_transfer_allow_main_settings', debug = debug).get('object')).get('element').click()
	time.sleep(0.5)
print('{}'.format(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_files_transfer_allow_main_settings', debug = debug).get('object')).get('element').text))
time.sleep(0.5)
its_icon = tools.displayed_element(element_definition = new_elements.ICONS(element_definition = 'consultant_files_transfer_allow_icon_main_settings', debug = debug).get('object')).get('element')
time.sleep(1)
tools.move_cursor_to_the_object(current_object = its_icon)
time.sleep(1)
print(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_personal_data_help_text_from_icon_main_settings', debug = debug).get('object')).get('element').text )


input_field = tools.displayed_element(element_definition = new_elements.INPUT(element_definition = 'consultant_files_min_time_at_site_main_settings', debug = debug).get('object')).get('element')
print('{} {}'.format(tools.displayed_element(element_definition = new_elements.LABEL(element_definition = 'consultant_files_min_time_at_site_main_settings', debug = True).get('object')).get('element').text,
	input_field.get_attribute('value') ))
tools. change_value(element_definition = input_field, text = '20')





# print(wg.cons_view_change_widget_position(place = 'cl'))
# print(wg.cons_view_change_widget_position(place = 'ul'))
# print(wg.cons_view_change_widget_position(place = 'cr'))
# print(wg.cons_view_define_animation_state)
# print(wg.cons_view_define_color_number())
time.sleep(3)
main_unit.close_browser

print('OVER!')
loger.file_log(text = 'Finish sanity test', text_type = 'SUCCESS', test_case_id = 45440, comment = 'Finish sanity test. at ' + str(datetime.utcnow()))








