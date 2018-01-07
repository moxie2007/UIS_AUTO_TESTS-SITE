from selenium import webdriver
from loger import Loger as loger
import time, asyncio

class Global_unit(object):
	def __init__(self):
		self.driver = None

	def init_browser(self, product_type = 'ch'):
	# открывает объект Браузера, доделать выбор браузера и добавить настройку полноэкранности
		env = {'ch': webdriver.Chrome, 'ff': webdriver.Firefox}
		try:
			self.driver = env.get(product_type)()
			try:
				self.driver.maximize_window()
			except Exception as ex:
				loger.file_log(text = 'Can\'t resize Browser window' , text_type = 'WARNING')
			return self.driver
		except Exception as ex:
			loger.file_log(text = 'Did not initialization Browser' , text_type = 'ERROR  ')
			return False
	
	@property
	def close_browser(self):
	# закрывает открытый объект Браузера 
		if self.driver:
			self.driver.quit()
			self.driver = None

	async def wait_for_timeout(self, time_out = 120):
	#(СG) функция для ожидания бу
		await asyncio.sleep(int(time_out))
		return {"time_out":time_out}

	def function_waiter(self, func):
		def inner(self, *args, **kwargs):
			function_waiter(*args, **kwargs)
		return inner
