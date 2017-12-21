import sys, time
import tools, start_uis_test, pageElements
import loger 
from loger import Loger as loger

# создаем объект, для использования модуля описывающего элементы на страницах
lk_elements  = pageElements.LK()

class Asi_tools(tools.Uis_tools):
	def __init__(self, driver):
		self.driver = driver

#ШФБЛОН(! Этой опции больше нет все методы перенести и перепроверить) консультант -- Общие настройки -- Шаблоны сообщений
	@property
	def general_settings_get_templates_list(self):
	# (C) поиск записай на странице выбирает формирует список объектов из элементов в таблице шаблонов ответа, в списке только отображенные на странице элементы
		return self.elements_list(object_type = 'table', search_type = 'contains', mask = 'id, \'commonsettings-page-tableview-\'')

	#!!! def login_to_system - перенесен в tools. 