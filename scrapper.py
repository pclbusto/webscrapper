from pygame.draw import line
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import re
import html as htmlMod


engine = create_engine('sqlite:///webs.db', echo=True, connect_args={'check_same_thread':False})
Base = declarative_base()
Session = sessionmaker(bind = engine)
session =Session()
all=chr(116)+chr(111)+chr(100)+chr(111)
stry = chr(114)+chr(101)+chr(108)+chr(97)+chr(116)+chr(111)

def recreateTablesAll(directorioBase=None):
    Base.metadata.create_all(engine)

class Pagina(Base):
    __tablename__ = 'Paginas'

    id_pagina = Column(Integer, primary_key=True)
    texto = Column(String, nullable=False)
    titulo = Column(String,nullable=False,default='')
    id_autor = Column(String,nullable=False,default='')
    valoracionMedia = Column(String,nullable=False,default='')
    id_categoria = Column(String,nullable=False,default='')

class Autor(Base):
    __tablename__ = 'Autores'
    id_autor = Column(String, primary_key=True)
    nombre_autor = Column(String)

class Categoria(Base):
    __tablename__ = 'Categorias'
    id_categoria = Column(String, primary_key=True)
    nombre_categoria = Column(String)

if __name__ == "__main__":

    recreateTablesAll()
    # print(Session)
    # 136379
    # id = 136379
    for id in range(40,50):
        print('https://www.'+all+stry+chr(115)+'.com/'+stry+'/'+str(id))
        req = Request('https://www.'+all+stry+chr(115)+'.com/'+stry+'/'+str(id),
            headers={'User-Agent': 'Mozilla/5.0'})
        try:
            htmlb = urlopen(req)
            html = htmlb.read().decode('cp1252')
        except HTTPError:
            continue

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
        p = re.compile('class=autor><b><a href=/perfil/(\d+)/>([a-zA-Z0-9_ \(\):]*)', re.DOTALL)
        m = p.search(html)
        if m:
            id_autor = m.group(1)
            nombre_autor = m.group(2)
        else:
            id_autor = 0
            nombre_autor = 'Anonimo'

        # print(m.group(1))
        # print(m.group(2))
        p = re.compile('<a href=/categorias/(\d+)/>([a-zA-Z0-9_ \(\):]*)', re.DOTALL)
        m = p.search(html)
        id_categoria = m.group(1)
        nombre_categoria = m.group(2)
        # print(m.group(1))
        # print(m.group(2))
        # p = re.compile('<p style="text-align: justify;">([^<]*)', re.DOTALL)
        p = re.compile('<p align=justify>([^<]*)', re.DOTALL)

        m = p.findall(html)
        texto = ''
        for i in m:
            s = htmlMod.unescape(i)
            texto = texto+'\n'+s
        print(texto)
        # help(Session)
        pagina = session.query(Pagina).get(id)
        if not pagina:

            autor = session.query(Autor).get(id_autor)
            if not autor:
                autor = Autor(id_autor = id_autor,nombre_autor = nombre_autor)
                session.add(autor)

            categoria = session.query(Categoria).get(id_categoria)
            if not categoria:
                categoria = Categoria(id_categoria = id_categoria, nombre_categoria = nombre_categoria)
                session.add(categoria)
            pagina = Pagina(id_pagina = id, id_autor = id_autor, id_categoria = id_categoria, texto = texto, titulo = titulo)
            session.add(pagina)
            session.commit()


