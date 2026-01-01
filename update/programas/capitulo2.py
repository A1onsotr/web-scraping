from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen('https://www.pythonscraping.com/pages/warandpeace.html')

with open('warandpeace.html', 'wb') as archivo:
    archivo.write(html.read())
    
bs = BeautifulSoup(html.read(), 'html.parser')

#print(bs.prettify())


nameList = bs.find_all('span', {'class':'green'})

'''
for name in nameList:
    print(name.get_text())

'''

# Pagina 3


html = urlopen('https://www.pythonscraping.com/pages/page3.html')


bs = BeautifulSoup(html.read(), 'html.parser')

print(bs.prettify())


#print(bs.find('img',{'src':'../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())


#imprimimos la fila de la cesta de  vegetales.

print(bs.find_all('tr')[1])

# buscamos los hijos

print(bs.find_all('tr')[1])


a = bs.find_all('tr')[1]

print()
print('pico')
print(a.find_all('td')[2])



#imprimimos a los hijos

print('hijos de la primera fila')

print()

print(a.contents[2])

print()


# descendientes

# children considera al tag -> hijo directo. en este caso la fila, sus hijos son las celdas, pero dentro
# tiene otro descendiente, el string.

print('descendientes de la primera fila')

for child in a.descendants: # primera fila, la de la cesta de vegetales
    print(child)



'''
imprime dos tipo de descendiente, descendiente 1 que son las celdas y descendiente 2 que son el string
dentro de las celdas.


cada hijo tiene un pariente, por ello dentro de cada hijo se puede acceder al pariente
'''


# concepto : siblings = hermanos


sibling_soup = BeautifulSoup("<a><b>text1</b><c>text2</c></a>", 'html.parser')
print(sibling_soup.prettify())

# buscamos la estructura 'b'
print(sibling_soup.b)

# entrega <b>text1</b>, su proximo hermano deberia ser <b>text2</b>

print(sibling_soup.b.next_sibling)


'''
¿ Que hace bs.find('img',{'src':'../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())?

nos faltarìa por ver que es lo que hace .find vs find_all() y ver que es la clase scr.

para ello, veamos el prettify

okey podemos ver lo siguiente:

- tenemos el tag <img> cuyo atributo es src, al cual se asocia una imagen.

- podriamos buscar con text por ejemplo. no funciona pero sigamos


ahora que hace find vs find_all()

'''

print(bs.find_all('img'))
