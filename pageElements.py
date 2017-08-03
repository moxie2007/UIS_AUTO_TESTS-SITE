class LK(object):
	def INPUT(self,element, mask = None):
	# форма логина
		# окно ввода почты
		if element == 'login_e-mail':
			return ["/html/body/div/div/form/input[1]",None]
		# окно ввода пароля
		if element == 'login_password':
			return ["/html/body/div/div/form/input[2]", None]
	def BUTTON(self,element, mask = None, userType = None):
	# кнопка логина
		if element == 'btn_login':
			return ["/html/body/div/div/form/input[3]", None]
	# Консультант - общие настройки, шаблон кнопки удаление 
		if element == 'remove_template':
			return['//*[@id="commonsettings-page-tableview-' + str(mask[0]) + '-record-' + str(mask[1]) + '"]/tbody/tr/td[2]/div/a[2]/img', None]

	def SELECT(self,element, mask = None, userType = None):
		if element == 'lk_env_select':
			return['//*[@id="cm-siteselector-1033-trigger-picker"]', None]
	# боковое меню личного кабинета, это не раьботает
		# if element == 'sm_cons':
		# 	return['//*[@id="ul-treeview-1025-record-12782"]/tbody/tr/td/div/span', None]
		# if element == 'sm_cons_general_settings':
		# 	return['//*[@id="ul-treeview-1025-record-12787"]/tbody/tr/td/div/a/span', None]
		# if element == 'sm_cons_channels':
		# 	return['//*[@id="ul-treeview-1025-record-12788"]/tbody/tr/td/div/a/span', None]
		# if element == 'sm_cons_view':
		# 	return['//*[@id="ul-treeview-1025-record-12789"]/tbody/tr/td/div/a/span', None]
		# if element == 'sm_cons_requests_distribution':
		# 	return['//*[@id="ul-treeview-1025-record-12790"]/tbody/tr/td/div/a/span', None]

	def COMBOBOX(self,element, mask = None, userType = None):
		if element == 'test_site':
			return('//*[@id="ul-boundlist-1034"]',None)


