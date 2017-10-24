from selenium import webdriver
import loger

class Global_unit(object):
	def __init__(self):
		self.driver = None

	def init_browser(self, product_type = 'ch'):
	# открывает объект Браузера, доделать выбор браузера и добавить настройку полноэкранности
		env = {'ch': webdriver.Chrome, 'ff': webdriver.Firefox}
		try:
			self.driver = env.get(product_type)()
			self.driver.maximize_window()
			print(dir(webdriver))
			# инициализируем объекты модулей 
			return self.driver
		except Exception as ex:
			# print(ex)
			loger.file_log(text = 'Did not initialization Browser' , text_type = 'ERROR  ')
	
	@property
	def close_browser(self):
	# закрывает открытый объект Браузера 
		if self.driver:
			self.driver.quit()
			self.driver = None