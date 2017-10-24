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
		if element == 'edit_template':
			return['//*[@id="commonsettings-page-tableview-' + str(mask[0]) + '-record-' + str(mask[1]) + '"]/tbody/tr/td[2]/div/a[1]/img', None]
		# кнопка сохранения отредактированного шаблона
		if element == 'save_template_name_icon':
			return['//*[@id="commonsettings-page-displayfield-id-' + str(int(mask) + 1) + '-inputEl"]/a[1]/img', None]
		if element == 'cancel_template_name_icon':
			return['//*[@id="commonsettings-page-displayfield-id-' + str(int(mask) + 1) + '-inputEl"]/a[2]/img', None]
	# Консультант - каналы, обратный звонок
		# кнопка для открытия выпадающего списка: графиков показа
		if element == 'cons_back_call_schedule_drop_down_btn':
			# return['//*[@id="channels-page-cm-schedulecombo-schedule_id-' + str(mask) + '-trigger-picker"]', None]
			print(int(mask) + 1)
			return['channels-page-cm-schedulecombo-schedule_id-' + str(int(mask) + 1) + '-trigger-picker"]', None]
                             # channels-page-cm-schedulecombo-schedule_id-1138-trigger-picker


	def SELECT(self,element, mask = None, userType = None):
	# Личный кабинет настройки консультант обратный звонок 
		# включатель \ выключатель состояния капчи (предварительно определить динамическую часть id)
		if element == 'lk_kons_kapcha_select':
			return['//*[@id="channels-page-cm-switchbox-is_captcha_enabled-' + str(mask) + '-inputEl"]', None]
		# ВКЛ состояние выкючателя
		if element == 'state_on_kons_kapcha_select':
			return['//*[@id="channels-page-cm-switchbox-is_captcha_enabled-' + str(mask) + '-inputEl"]/span/span[1]', None]
		# ВЫКЛ состояние выкючателя
		if element == 'state_off_kons_kapcha_select':
			return['//*[@id="channels-page-cm-switchbox-is_captcha_enabled-' + str(mask) + '-inputEl"]/span/span[3]', None]
		if element == 'test':
			return['channels-page-cm-switchbox-is_captcha_enabled-' + str(mask), None]

	                # //*[@id="channels-page-cm-switchbox-is_captcha_enabled-1136-inputEl"]/span/span[1]
	# боковое меню личного кабинета, это не раьботает на ранней стадии разработки тестов не учтена динамика
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


