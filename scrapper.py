from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.request import urlopen, Request
import re


engine = create_engine('sqlite:///webs.db', echo=True, connect_args={'check_same_thread':False})
Base = declarative_base()
Session = sessionmaker(bind = engine)
all=chr(116)+chr(111)+chr(100)+chr(111)
stry = chr(114)+chr(101)+chr(108)+chr(97)+chr(116)+chr(111)

def recreateTablesAll(directorioBase=None):
    Base.metadata.create_all(engine)

class Pagina(Base):
    __tablename__ = 'Paginas'

    id_pagina = Column(String, primary_key=True)
    texto = Column(String,unique=True)
    titulo = Column(String,nullable=False,default='')
    id_autor = Column(String,nullable=False,default='')
    valoracionMedia = Column(String,nullable=False,default='')
    id_categoria = Column(String,nullable=False,default='')

class Autor(Base):
    __tablename__ = 'Autores'
    id_autor = Column(String, primary_key=True)
    nombre_autor = Column(String, unique=True)

class Categoria(Base):
    __tablename__ = 'Categorias'
    id_categoria = Column(String, primary_key=True)
    nombre_categoria = Column(String, unique=True)

if __name__ == "__main__":
    # recreateTablesAll()
    # 136379
    req = Request('https://www.'+all+stry+chr(115)+'.com/'+stry+'/690',
        headers={'User-Agent': 'Mozilla/5.0'})
    htmlb = urlopen(req)
    html = htmlb.read().decode('cp1252')
    # html = '''t </tr>
    # <tr>
    #   <td bgColor=#fdfdfd width="100%" align="center" class="bordedown">
    #   <span class=autor><b><a href=/perfil/2/>Ernesto</a></b><SCRIPT TYPE="text/javascript">
    # <!-- '''
#     print(html)
    p = re.compile('class\=titulo>([a-zA-Z0-9_ \(\):]*)', re.DOTALL)
    m = p.search(html)
    print(m.group(1))
    p = re.compile('class\=autor><b><a href=/perfil/(\d+)/>([a-zA-Z0-9_ \(\):]*)', re.DOTALL)
    m = p.search(html)
    print(m.group(1))
    print(m.group(2))
    p = re.compile('<a href=/categorias/(\d+)/>([a-zA-Z0-9_ \(\):]*)', re.DOTALL)
    m = p.search(html)
    print(m.group(1))
    print(m.group(2))
    p = re.compile('<p align=justify>([a-zA-Z0-9_ \(\):\.\,\n\t\r\&;]*)', re.DOTALL)
    m = p.findall(html)
    # print(m)
    for i in m:
        s = i.
        print(i)
