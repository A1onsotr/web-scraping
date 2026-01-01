from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page1.html')
#print(html.read())


print()



html = urlopen('http://www.pythonscraping.com/pages/page1.html')
bs = BeautifulSoup(html.read(), 'html.parser')
#print(bs.h1)
#print(bs.title)
#print(bs.body)
#print(bs.html)


print()

print('ver todos los tags que hay')

#print(bs.find_all())

tags = set(tag.name for tag in bs.find_all())
print(tags)


