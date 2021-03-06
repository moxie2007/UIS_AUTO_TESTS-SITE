class LK(object):
	def INPUT(self,element, mask = None):
	# форма логина
		# окно ввода почты
		if element == 'login_e-mail':
			return ["/html/body/div/div/form/input[1]", None]
		# окно ввода пароля
		if element == 'login_password':
			return ["/html/body/div/div/form/input[2]", None]
	# ЛК-СЕРВИСЫ-Консультант
		# Общие настройки-Черный список- поле ввода ip	
		if element == 'konsultant_black_list_add_ip':
			return ['//*[@id="commonsettings-page-textfield-ip-' + str(mask) + '-inputEl"]', None]
		# Общие настройки-Черный список- поле ввода комментарий	
		if element == 'konsultant_black_list_add_comment':
			return ['//*[@id="commonsettings-page-textfield-description-' + str(mask) + '-inputEl"]', None]
	# ЛК-САЙТФОН
	# поле ввода: Текст на баннере
		if element == 'sitephone_banner_text_field':
			return ['//*[@id="sitephone-page-textfield-title-' + str(mask) + '-inputEl"]', None]
	# иконка рядом с полем ввода: Текст на баннере
		if element == 'sitephone_banner_text_error_icon':
			return ['//*[@id="sitephone-page-textfield-title-' + str(mask) + '-errorEl"]', None]

	# Яндекс
		if element == 'login_yandex':
			return ['//*[@id="root"]/div/div[2]/div/div[2]/div/div[2]/div/div/form/div[1]/label/input', None]
			# //*[@id="root"]/div/div[2]/div/div[2]/div/div[2]/div/div/form/div[1]/label/input
		if element == 'password_yandex':
			return ['//*[@id="root"]/div/div[2]/div[1]/div[2]/div/div[2]/div/div/form/div[2]/label/input', None]
	# Google
		if element == 'login_google':
			return ['//*[@id="identifierId"]', None]
		# if element == 'login_google2':
		# 	return ['//*[@id="view_container"]/form/div[2]/div/div[1]/div[1]/div/div[1]/div/div[3]', None]
		if element == 'password_google':
			return ['//*[@id="password"]/div[1]/div/div[1]/input', None]

	# Comagic
		if element == 'login_comagic':
			return ['/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/form/div[1]/input', None]
		if element == 'password_comagic':
			return ['/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/form/div[2]/input', None]







	
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
	# Дашборды - меню дашбордов - кнопка добавления нового дашборда
		if element == 'dash_top_menu_add_btn':
			return['div > div > div > div > a > span > span > span', None]
	# Яндекс
		if element == 'btn_login_yandex':
			return ['//*[@id="root"]/div/div[2]/div[1]/div[2]/div/div[2]/div/div/form/div[4]/button[1]/span/span', None]
	# Google
		if element == 'btn_next_login_google':
			return ['//*[@id="identifierNext"]/content/span', None]
		if element == 'btn_next_pwd_google':
			return ['//*[@id="passwordNext"]/content/span', None]
		if element == 'btn_select_account_google':
			return ['//*[@id="view_container"]/form/div[2]/div/div/div/ul/li[1]/div/div[2]/p[2]', None]
		if element == 'btn_change_google':
			return ['//*[@id="identifierLink"]/div[2]/p', None]
		if element == 'btn_submit_google':
			return ['//*[@id="submit_approve_access"]/content/span', None]
	# Comagic
		if element == 'btn_login_comagic':
			return ['/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/form/div[4]/button', None]



# Сайты - редактирование сайта
		if element == 'sites_edit_site':
			return ['//*[@id="sites-page-tableview-' + str(mask[0]) + '-record-' + str(mask[1]) + '"]/tbody/tr/td[5]/div/a[1]/img', None]



	# Дашборды создание\редактирование даша
		# кнопка выподающего списка в фильтрах: Параметр
		if element == 'dash_filters_parametr_drop_down_btn':
			return['dashboards-page-ul-combobox-filterField-' + str(mask) + '-trigger-picker', None]
		# кнопка выподающего списка в фильтрах: Условие
		if element == 'dash_filters_condition_drop_down_btn':
			return['dashboards-page-ul-combobox-filterComparison-' + str(mask) + '-trigger-picker', None]





	def SELECT(self,element, mask = None, userType = None):
	# Личный кабинет настройки консультант - Внешний вид
		# выпадающий список для пункта меню: Положение
		if element == 'lk_kons_view_dd':
			return['//*[@id="uisettings-page-cm-widgetpositioncombo-banner_place-' + str(mask) + '-inputEl"]', None] 	

	def COMBOBOX(self,element, mask = None, userType = None):
		# ВОТ это непонятно накой, тем более что возврат странный
		if element == 'test_site':
			return('//*[@id="ul-boundlist-1034"]',None)

		# СЕРВИСЫ - Cайтфон
		# чек-бокс: ПК
		if element == 'sitephone_checkbox_desktop':
			return['//*[@id="sitephone-page-checkboxfield-desktop-' + str(mask) + '-inputEl"]',None]		
		# чек-бокс: Смартфон
		if element == 'sitephone_checkbox_mobile':
			return['//*[@id="sitephone-page-checkboxfield-mobile-' + str(mask) + '-inputEl"]',None]			

	def LABELE(self,element, mask = None, userType = None):
		# СЕРВИСЫ - Консультант
		# Внешний вид
		# кнопка-лебл: Анимация
		if element == 'cons_view_animation_lable':
			return['//*[@id="uisettings-page-cm-switchbox-is_animation_enabled-' + str(mask) + '-inputEl"]',None]
		
		# СЕРВИСЫ - Cайтфон
		# кнопка-лейбл: Капча
		if element == 'sitephone_kaptcha_lable':
			return['//*[@id="sitephone-page-cm-switchbox-is_captcha_enabled-' + str(mask) + '-inputEl"]',None]
		# кнопка-лейбл: Показывать на сайте	
		if element == 'sitephone_display_at_site_lable':
			return['//*[@id="sitephone-page-cm-switchbox-is_visible-' + str(mask) + '-inputEl"]',None]
		# кнопка-лейбл: Анимация	
		if element == 'sitephone_animation_lable':
			return['//*[@id="sitephone-page-cm-switchbox-is_animation_enabled-' + str(mask) + '-inputEl"]',None]
		# кнопка-лейбл: Отложенный звонок: 	
		if element == 'sitephone_delayed_call_lable':
			return['//*[@id="sitephone-page-cm-switchbox-is_delayed_call_enabled-' + str(mask) + '-inputEl"]',None]
