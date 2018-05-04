from pygame.draw import line
from sqlalchemy import create_engine, Column, Integer, String, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.request import urlopen, Request
from urllib.error import HTTPError,URLError
import threading

import re
import html as htmlMod


engine = create_engine('sqlite:///webs.db', echo=False, connect_args={'check_same_thread':False})
Base = declarative_base()
Session = sessionmaker(bind = engine)
session =Session()
all=chr(116)+chr(111)+chr(100)+chr(111)
stry = chr(114)+chr(101)+chr(108)+chr(97)+chr(116)+chr(111)
CANTIDAD_MAX_HILOS = 2
cantidad_hilos = 0
CANTIDAD_PAGINAS_PROCESAR = 5

lista_autores = []
lista_categorias = []


def recreateTablesAll(directorioBase=None):
    Base.metadata.create_all(engine)

class Pagina(Base):
    __tablename__ = 'Paginas'

    id_pagina = Column(Integer, primary_key=True)
    texto = Column(String,nullable=False,default='')
    titulo = Column(String,nullable=False,default='')
    id_autor = Column(String,nullable=False,default='')
    valoracionMedia = Column(String,nullable=False,default='')
    id_categoria = Column(String,nullable=False,default='')
    tamanio = Column(Integer, nullable=False,default=0)

class Autor(Base):
    __tablename__ = 'Autores'
    id_autor = Column(String, primary_key=True)
    nombre_autor = Column(String)

class Categoria(Base):
    __tablename__ = 'Categorias'
    id_categoria = Column(String, primary_key=True)
    nombre_categoria = Column(String)


def procesar_pagina(id):
    global  lista_categorias, lista_autores
    while True:
        try:
            # id=570
            print(str(id))
            req = Request('https://www.' + all + stry + chr(115) + '.com/' + stry + '/' + str(id),
                          headers={'User-Agent': 'Mozilla/5.0'})
            site = urlopen(req)
            html = site.read().decode('cp1252')

            # f = open('file2.txt','r')
            # line = f.readline()
            # while line:
            #     print(line)
            #     line = f.readline()

            # html= f.read()
            p = re.compile('class=titulo>([^<]*)', re.DOTALL)
            m = p.search(html)
            titulo = m.group(1)
            # print(m.group(1))
            p = re.compile('class=autor><b><a href=/perfil/(\d+)/>([^<]*)', re.DOTALL)
            m = p.search(html)
            if m:
                id_autor = m.group(1)
                nombre_autor = m.group(2)
            else:
                id_autor = 0
                nombre_autor = 'Anonimo'

            # print(m.group(1))
            # print(m.group(2))
            p = re.compile('<a href=/categorias/(\d+)/>([^<]*)', re.DOTALL)
            m = p.search(html)
            id_categoria = m.group(1)
            nombre_categoria = m.group(2)
            # print(m.group(1))
            # print(m.group(2))
            # p = re.compile('<p style="text-align: justify;">([^<]*)', re.DOTALL)
            p = re.compile('<p align=\"*justify\"*>([^<]*)', re.DOTALL + re.IGNORECASE)
            # print(html)
            m = p.findall(html)
            texto = ''
            for i in m:
                s = htmlMod.unescape(i)
                # Sacamos nuevas lineas por si existen
                s = s.replace("\r", " ")
                s = s.replace("\t", " ")
                s = s.replace("\n", " ")
                texto = texto + '\n' + s
            # print("texto")
            # print(texto)
            # help(Session)
            pagina = session.query(Pagina).get(id)
            if not pagina:

                autor = session.query(Autor).get(id_autor)
                if not autor:
                    for autor_lista in lista_autores:
                        if autor_lista.id_autor!=id_autor:
                            autor = Autor(id_autor=id_autor, nombre_autor=nombre_autor)
                            lista_autores.append(autor)
                            session.add(autor)
                categoria = session.query(Categoria).get(id_categoria)
                if not categoria:
                    for categoria_lista in lista_categorias:
                        if categoria_lista!=id_categoria:
                            categoria = Categoria(id_categoria=id_categoria, nombre_categoria=nombre_categoria)
                            lista_categorias.append(categoria)
                            session.add(categoria)
                pagina = Pagina(id_pagina=id, id_autor=id_autor, id_categoria=id_categoria, texto=texto, titulo=titulo,
                                tamanio=str(len(html)))
                session.add(pagina)
                session.commit()
                # '''select sum(tamanio)/(1024*1024) from Paginas'''

        except HTTPError:
            continue
        except URLError:
            break
        break
    global cantidad_hilos
    cantidad_hilos -= 1


if __name__ == "__main__":

    recreateTablesAll()
    ultima_pagina = session.query(Pagina).order_by(desc(Pagina.id_pagina)).first()
    if not ultima_pagina:
        ultima_pagina = Pagina(id_pagina = 1)


    for id in range(0,CANTIDAD_PAGINAS_PROCESAR):
        while id<=CANTIDAD_PAGINAS_PROCESAR:
            if cantidad_hilos<CANTIDAD_MAX_HILOS:
                cantidad_hilos+=1
                print('lanzando hilo '+str(cantidad_hilos))
                t = threading.Thread(target=procesar_pagina, args=(ultima_pagina.id_pagina + id,))
                t.start()
                break
                # procesar_pagina(ultima_pagina.id_pagina + id)
                #lanzamos un nuevo hilo
            #sino seguimos iterando hasta que algun hilo termine y baje el contador
    while  cantidad_hilos>0:
        print("esperando para cerrar")
    # session.commit()