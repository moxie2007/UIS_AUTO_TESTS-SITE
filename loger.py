# -*- coding: utf-8 -*-

import os, sys, codecs, re
import time
from time import gmtime, strftime
import datetime
from datetime import datetime

from testrail import *

class Loger(object):
	maxlenAction = 10
	maxlenResult = 7
	@staticmethod

	# def testrait_login(self, ):

	def console_log(text, text_type):
		# тут должен преобразователь из технических имён в названия элементов 
		return text
	@staticmethod
	# старый простой логер
	def file_log(text, text_type, test_case_id = None, comment = None):
		f = open("testFile.log",'a+')
		f.write(str(datetime.utcnow()) + ' : ' + str(text_type) + ' : ' + str(text) + '.' + '\n')
		f.close()

		# if test_case_id != None:
		# 	client = APIClient('http://testrail.uiscom.ru/')
		# 	# client.user = None
		# 	# client.password = None
		# 	start_run = client.send_post('add_result/' + str(test_case_id),{"status_id" : 5,"comment" : str(comment)})
	

	# это несколькоуровневый логер. Масив будет содержать тип действия соблюдая вложенность по индексам (от глобального к частному)
	

	def file_logExt(text, ActionType = [None]):
		# открываем файл лога
		f = open(u"testFile.log",'a+b')
		# перебираем значения действий и результатов и дописываем к ним пробелы если необходимо
		# for step in range(len(ActionType)):
		if len(ActionType[0]) < maxlenAction:
			maxlenAction - len(ActionType[0])


		for step in range(len(ActionType)):
			text_type = 1
		
		f.write(str(str(datetime.utcnow()).encode('utf-8') + ' : ' + str(text_type) + ' : ' + str(text) + '.' + '\n'))
		f.close()

# ACTION    
# PREPARE   
# VALIDATION