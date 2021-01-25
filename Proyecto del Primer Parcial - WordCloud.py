# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UvQtgyzF6Tu3_P5HobmXWmg1mMeOo6Cd
"""

import requests
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
from PIL import Image

v = 0
while v == 0:
  print("Ingrese el id del usuario:")
  id = input()

  r = requests.get('https://es.stackoverflow.com/users/'+ id +'?tab=tags')

  c = r.content #devuelve el contenido de la pag en bits
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(c)

  if not soup.find("h1", class_="fs-headline1 mb4"):
    v = 1
  if v == 0:
    print("----- INGRESE UN USUARIO VALIDO -----")

r = requests.get('https://es.stackoverflow.com/users/'+ id +'?tab=tags')

c = r.content
from bs4 import BeautifulSoup
soup = BeautifulSoup(c)

Pag = soup.find_all("a", class_="s-pagination--item js-pagination-item")

Etiquetas = list()
Frecuencias = list()

paginas=0
for i in Pag:
    paginas=paginas+1

y = 0
if soup.find_all("a", class_="s-pagination--item js-pagination-item"):
  while y < paginas:
    y = y + 1
    # Realizar la solicitud a una URL
    r = requests.get('https://es.stackoverflow.com/users/'+ id +'?tab=tags&sort=votes&page='+ str(y))

    # Crear soup a partir del contenido de la solicitud
    c = r.content
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(c)

    # Encontrar etiquetas y frecuencia de las mismas (Se obtubo el identificador mediante inspeccionar)
    Tags = soup.find_all("a", class_="post-tag")
    Points = soup.find_all("div", class_="answer-votes")

    x=0
    #Recorro las frecuencias y las guardo en Frecuencias
    
    for i in Points:
      frec = str(i.text)

      if frec.find('k'):
        frec = frec.replace("k", "000")
      
      if int(frec) > 0:
        x=x+1
        Frecuencias.append(int(frec))

    #Recorro las etiquetas y las guardo en Etiquetas
    
    for i in Tags:
      Etiquetas.append(i.text)

else: 
   # Realizar la solicitud a una URL
  r = requests.get('https://es.stackoverflow.com/users/'+ id +'?tab=tags&sort=votes&page='+ str(y))

  # Crear soup a partir del contenido de la solicitud
  c = r.content
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(c)

  # Encontrar etiquetas y frecuencia de las mismas (Se obtubo el identificador mediante inspeccionar)
  Tags = soup.find_all("a", class_="post-tag")
  Points = soup.find_all("div", class_="answer-votes")

  x=0
  #Recorro las frecuencias y las guardo en Frecuencias
  
  for i in Points:
    frec = str(i.text)

    if frec.find('k'):
      frec = frec.replace("k", "000")
    
    if int(frec) > 0:
      x=x+1
      
      Frecuencias.append(int(frec))

  #Recorro las etiquetas y las guardo en Etiquetas
  
  for i in Tags:
    Etiquetas.append(i.text)
    print(i.text)

# Creamos un diccionario formado por dos listas pares
from itertools import groupby
Etiquetas = list(lista for lista, _ in groupby(Etiquetas))

if len(Etiquetas) == 0:
  if len(Frecuencias) == 0:
    Etiquetas.append("NO HAY")
    Frecuencias.append(1)  

zip_iterator = zip(Etiquetas, Frecuencias)
diccionario = dict(zip_iterator)
print(Etiquetas)
print(Frecuencias)

# Generamos la WordCloud mediante un dicccionario de frecuencias

wordcloud = WordCloud()
wordcloud = WordCloud().generate_from_frequencies(diccionario)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
