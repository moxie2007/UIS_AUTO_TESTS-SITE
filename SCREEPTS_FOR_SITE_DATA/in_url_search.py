from urllib.request import Request, urlopen

req = Request('http://siteca1.webdev.uiscom.ru')
webpage = urlopen(req)

data = (webpage.readlines())
for line in data:
	print(line.decode('UTF-8'))