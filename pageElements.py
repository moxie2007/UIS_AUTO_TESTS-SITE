class LK(object):
	# """docstring for API"""
	# def __init__(self):
	# 	super(API, self).__init__()
	# # экран\форма логина
	def INPUT(self,element, mask = None):
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
	def SELECT(self,element, mask = None, userType = None):
		if element == 'lk_env_select':
			return['//*[@id="cm-siteselector-1033-trigger-picker"]', None]
	def COMBOBOX(self,element, mask = None, userType = None):
		if element == 'test_site':
			return('//*[@id="ul-boundlist-1034"]',None)
