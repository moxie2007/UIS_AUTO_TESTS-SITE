import os, sys, codecs, re
import time
from time import gmtime, strftime
import datetime
from datetime import datetime

from testrail import *

class Loger(object):
	def console_log(text, text_type):
		# тут должен преобразователь из технических имён в названия элементов 
		return text
	@staticmethod
	# старый простой логер
	def file_log(text, text_type, test_case_id = None, comment = None):
		with open('testFile.log', 'a+', encoding='utf-8') as f:
			f.write(str(datetime.utcnow()) + ' : ' + str(text_type) + ' : ' + str(text) + '.' + '\n')
			f.close()

	