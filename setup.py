# coding: utf-8
import os
import zipfile
from setuptools import setup

control=True
if os.path.exists('dist/'):
    control=False


setup(
   name='AutoRmbcIbge2',
   version='2.0',
   description='Software não oficial do IBGE destinado a executar download da rede de monitoramento contínuo',
   author='José Ivan Silva Vegiani',
   author_email='ivanvegiani@gmail.com',
   packages=['AutoRbmcIbge2'],  #same as name
   install_requires=['tkcalendar'], #external packages as dependencies
)
print(control)

if control:
    lista=os.listdir('dist/')
    egg_path=os.path.join('dist',str(lista[0]))
    print(egg_path)
    zip1 = zipfile.ZipFile(egg_path)
    zip1.extractall('../')