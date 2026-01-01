from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os



ruta_html = '../lab-p/tabla.html'


with open(ruta_html, "r", encoding="utf-8") as f:
    html = f.read()

bs = BeautifulSoup(html, "html.parser")


#


vegetal_basket =  bs.find_all('img')[1]

parent_vegetal_basket = vegetal_basket.parent



def output(titulo,salida):
    print()
    print(titulo)
    print('-' * len(titulo))
    print()
    print(salida)


output('imagen cesta de vegetales', vegetal_basket)
output('pariente', parent_vegetal_basket)

# el hermano previo son los costos

costo = parent_vegetal_basket.previous_sibling

output('costo', costo)


# obtener todos los costos de la tabla

imgs = bs.find_all('img')

for f in range(len(imgs)):
    a = imgs[f].parent.previous_sibling.get_text()
    print(a)





# con expresiones regulares




row_table = bs.find_all('tr', {'class': 'gift'})


for f in range(len(row_table)):
    product = row_table[f]

    #print(f'iteracion {f}')

   # print(product)
    

first = row_table[0]

count = 1

name = []
values = []
for filas in row_table:
    children = filas.children

    name.append(filas.find('td').get_text(strip=True))

       
    for f in children:

        if re.search(r"\$(\d{1,3}(,\d{3})*)\.\d{2}",f.get_text()):
            values.append(f.get_text(strip=True))
            

print(name)
print(values)

