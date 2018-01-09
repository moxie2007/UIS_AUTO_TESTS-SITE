import  random, sys, time
from time import gmtime, strftime
from datetime import datetime

# import tools, pageElements, widgets_tools, vats_tools, start_uis_test
import tools, pageElements, start_uis_test
from loger import Loger as loger

configLK = tools.User_config()
configLK.set_lk_parametrs(source_name = 'ADMIN_LK')

# метод авторизации через админку
def login_to_the_LK(tools = None, driver = None, my_user_id = '1103', breakONerror = True):
	method_status = False
	method_result = {}
	timeOut = 120
	method_result['client_credential'] = tools.login_toLK_by_admin(adm_login = configLK.get_user_name, adm_pass = configLK.get_pass, user_id = my_user_id, stend_url = configLK.get_login_url)
	time_index = 0
	while True:
		# ждем появление основного меню (самое левое, общий блок)
		left_menu = tools.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'cm-westpanel-\'')
		# продолжаем если меню вообще нашлось
		if type(left_menu.get('count')) == int:
			# ищем родительский объект - весь блок меню
			for each_object in left_menu.get('elements'):
				current_object_id = each_object.get_attribute('id').split('-')
				if len(current_object_id) == 3:
					parent_object = each_object		
					break
			# ищем все пункты менюшек
			all_menu_items = tools.elements_list(object_type = 'span', search_type = 'contains', mask = 'class, \'x-tree-node-text\'')
			if type(all_menu_items.get('count')) == int:
				# перебираем все найденные объекты и если находим пункт меню, который называется Дашборды, то считаем, что пермишены е сть и работают
				elements_list = all_menu_items.get('elements')
				while len(elements_list) != 0:
					current_menu = elements_list.pop()
					try:# если меню такое есть, то идем дальше
						if current_menu.text == 'Дашборды':
							if tools.identity_of_the_child_to_the_parent(parent = parent_object, child = current_menu):
								method_result['existing_menu'] = True
								method_status = True
								break
						# если в списке последний элемент и это не Дашборды, то задаем условие выхода из поиска 
						if len(elements_list) <= 1:
							method_result['existing_menu'] = False
							method_status = True
					except:
						pass
			# выход из общего цикла если меню найдено
			if method_status:
				break
		if time_index >= timeOut:
			print('time out: ERROR')
			loger.file_log(text = 'Can\'t find west menu at all', text_type = 'ERROR  ')
			break
			if breakONerror is True:
				self.close_browser
				loger.file_log(text = 'Finish vats_sanity test with Error', text_type = 'SUCCESS')
				sys.exit()
		time.sleep(1)
		time_index += 1
	return method_result

# тест по проверке доступности Дашбордов
if __name__ == '__main__':
	index_testing = 0
	for tt in range(3000):
		print('START:\t{}\t:\t{}'.format(str(datetime.utcnow()),'vats_sanity 24 000 user\'s'))
		users_ids = ['1103', '2153', '4735', '10145', '11128', '33247', '51522', '51523']
		# users_ids = ['1103', '2153']#, '4735', '10145', '11128', '33247', '51522', '51523']
		for test_step in users_ids:
			# модуль инициализации (открываем браузер)
			main_unit = start_uis_test.Global_unit()
			driver = main_unit.init_browser(product_type = 'ch')
			tools_test = tools.Uis_tools(driver) # (инициализация модуля с таким именем из-за того что внутри происходит переопределение такого имени: tools)
			client_data = login_to_the_LK(tools = tools_test, my_user_id = test_step)
			# client_data = login_to_the_LK(tools = tools_test, driver = None, my_user_id = test_step)
			print('Клиетн с id:{}\tи типом пользователя:\t{}\tу которого пункт меню Дашборды:\t{}.'.format(client_data.get('client_credential').get('client_id'),client_data.get('client_credential').get('client_type'),client_data.get('existing_menu')))
			# закрываем браузер
			main_unit.close_browser
		print('OVER:\t{}\t:\t{}\ttesting index = {}'.format(str(datetime.utcnow()),'vats_sanity', index_testing))
		index_testing += 1

