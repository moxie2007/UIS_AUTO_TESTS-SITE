import sys, time
import tools, start_uis_test, pageElements
import loger 
from loger import Loger as loger

# создаем объект, для использования модуля описывающего элементы на страницах
lk_elements  = pageElements.LK()

class Vats_tools(tools.Uis_tools):
	def __init__(self, driver):
		self.driver = driver

	def dash_define_existing_dashboards(self, time_out = 120):
	# (C!G)определяем существующие дашборды, возвращаем название, объект, стату(выбран объект или нет)
		time_index = 0
		method_status = None
		result = {}
		while True:
			# ищем вкладки
			try:
				new_elems = self.elements_list(object_type = 'a', search_type = 'contains', mask = 'data-boundview, \'-tabbar-tabbar-mode-\'')
				# проверяем нашлись ли элементы и если да, то выходим из цикла с полученным результатом
				if new_elems.get('count') != None:
					method_status = True
					break
			except:
				pass
			if time_index >= time_out:
				loger.file_log(text = 'Can\'t find dashboard, you should check current element at page by yourself', text_type = 'ERROR  ')
				method_status = False
				break
			time_index += 1
		# если элементы есть, то  выбираем нужные значения: текст, объект, состояние
		if method_status:
			for current_dashboard in new_elems.get('elements'):
				dashboard_select_status = False
				if 'x-tab-active' in str(current_dashboard.get_attribute('class')):
					dashboard_select_status = True
				result[current_dashboard.text] = {'object':current_dashboard, 'status':dashboard_select_status}
		return result

	def dash_define_widgets_at_dashboard(self, time_out = 120):
	# (СG) метод определяющий общее количество виджетов на дашборде, возвращает созданные не пустые
		method_status = False
		time_index = 0
		dashboard_boxes = 0
		while True:
			try:
				# пироги
				all_pies = []
				pie = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-analytics-dashboards-piedash-\'',timeOut = 1)
				for pie_widget in pie.get('elements'):
					if str(pie_widget.get_attribute('class')) == 'x-container analytics-dashboards-dash x-container-ul x-box-layout-ct':
						dashboard_boxes += 1
						all_pies.append(pie_widget)
			except:
				pass					
			try:
				# пустые блоки
				empty = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-component-emptydash-component-\'',timeOut = 1)
				for empty_widget in empty.get('elements'):
					if 'x-component analytics-dashboards-emptydash x-component-ul' in str(empty_widget.get_attribute('class')):
						dashboard_boxes += 1
			except:
				pass	
			try:
				all_histograms = []
				# гистограмма
				gisto = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-analytics-dashboards-columndash-\'',timeOut = 1)
				for gistogramma in gisto.get('elements'):
					if 'x-container analytics-dashboards-dash x-container-ul x-box-layout-ct' == str(gistogramma.get_attribute('class')):
						dashboard_boxes += 2
						all_histograms.append(gistogramma)
			except:
				pass	
			try:
				all_graphs = []
				# грфик
				graphs = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-analytics-dashboards-linedash-\'',timeOut = 1)
				for graph in graphs.get('elements'):
					if 'x-container analytics-dashboards-dash x-container-ul x-box-layout-ct' == str(graph.get_attribute('class')):
						dashboard_boxes += 4
						all_graphs.append(graph)
			except:
				pass
			try:
				all_stikers = []
				# стикер
				stikers = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-analytics-dashboards-stickerdash-\'',timeOut = 1)
				for stiker in stikers.get('elements'):
					if 'x-container analytics-dashboards-dash x-container-ul x-box-layout-ct' == str(stiker.get_attribute('class')):
						dashboard_boxes += 1
						all_stikers.append(stiker)
			except:
				pass
			# проверяем нашли ли мы все элементы на конкретном дашборде
			if dashboard_boxes == 12:
				method_status = True
			else:
				# если нет то количество найденых значений обнуляем
				dashboard_boxes = 0
			# условие выхода из цикла: или найдены все элементы или истекло время поиска
			if method_status == True:
				dashboard_elements = {'existing_widgets':{'sticker':all_stikers, 'pie':all_pies, 'histogram':all_histograms, 'graph':all_graphs}} 
				break
			if time_index >= time_out:
				loger.file_log(text = 'Can\'t find dashboard, you should check current element at page by yourself', text_type = 'ERROR  ')
				method_status = False
				break
			time.sleep(1)
			time_index += 1	
		return dashboard_elements

	def dash_get_widget_name(self, widget = None):
	#(CG) определяем заголовок виджета, в метод нужно передать объект (квадрат самого виджета)
		result = None
		# ищем все заголовки с дашборда
		try:
			widget_headers = self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'dashboards-page-label-title-\'').get('elements')
			# проверяем относится ли конкретный заголовок к родительскому дашу и если Да, то возвращаем текст заголовка
			for header in widget_headers:
				if self.identity_of_the_child_to_the_parent(parent = widget, child = header).get('result'):
					result = header.text
					break
		except:
			loger.file_log(text = 'Can\'t find widget headers, method: va.dash_get_widget_name', text_type = 'ERROR  ')
		return result

	def dash_get_widget_legend(self, widget = None):
	#(CG) определяем легенду виджета, в метод нужно передать объект (квадрат самого виджета)
	# возвращает или легенду или None
		result = None
		# ищем все заголовки с дашборда
		try:
			widget_legend = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-component-description-\'').get('elements')
			# проверяем относится ли конкретный блок с легендой к родительскому дашу и если Да, то запоминаем этот объект
			for legend_section in widget_legend:
				if self.identity_of_the_child_to_the_parent(parent = widget, child = legend_section).get('result'):
					result = legend_section.text
					break
		except Exception as ex:
			loger.file_log(text = 'Can\'t find widget legend, method: va.dash_get_widget_legend', text_type = 'ERROR  ')
		return result

	def dash_get_widget_total(self, widget = None):
	#(CG) определяем значение Всего в виджете (справа внизу), в метод нужно передать объект (квадрат самого виджета)
	# возвращает или легенду или None
		result = None
		# ищем все заголовки с дашборда
		try:
			widget_total_value = self.elements_list(object_type = 'label', search_type = 'contains', mask = 'id, \'dashboards-page-label-totalValue-\'').get('elements')
			# проверяем относится ли конкретный блок с легендой к родительскому дашу и если Да, то запоминаем этот объект
			for total_value_section in widget_total_value:
				if self.identity_of_the_child_to_the_parent(parent = widget, child = total_value_section).get('result'):
					result = total_value_section.text
					break
		except Exception as ex:
			loger.file_log(text = 'Can\'t find widget total value, method: va.dash_get_widget_total', text_type = 'ERROR  ')
		return result

	def dash_define_abbility_for_creation_new_dash(self, widget_type = 'stiker'):
	# определяет доступность создания нового виджета на текущем дашборде. В метод передаем тип необходимого даша
		# размерности виджетов
		widget_settings = {'size':{1:'stiker', 1:'pie', 2:'columndash', 4:'linedash'}}
		# определяем все доступнве для создания блоки
		result = None
		avalible_blocks = self.elements_list(object_type = 'div', search_type = 'contains', mask = 'id, \'dashboards-page-component-emptydash-component-\'')
		# если есть пустые блоки, то получаем их id
		if avalible_blocks.get('count') >= 1:
			blocks = {}
			for empty_block in avalible_blocks.get('elements'):
				blocks[empty_block.get_attribute('id').split('-')[5]] = empty_block

			# ищем все доступные клетки для создания виджета заданного типа
			for key in blocks.keys():
				print(key)

			result = blocks

		return result



	def dash_create_new_dash(self, widget_type = 'stiker'):
	#(CG!) создание нового виджета/ необходимо определить доступновть к созданию

		pass







