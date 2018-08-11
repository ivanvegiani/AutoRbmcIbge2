# coding: utf-8



import datetime
import ftplib
from pathlib import Path
from socket import gaierror
import os
from tkinter import*
from tkinter import ttk
import threading



# Configurações iniciais



# delay_time=30 # tempo de espera para interação humana
# loop=15 # quantidade de dias recentes para download de base
# baseFolder = 'Cascavel', 'Maringá', 'Curitiba', 'Guarapuava' # bases a serem realizadas do download automático
# path_root = 'c:\IBGE' # pasta root das bases
# sigla = ['prcv', 'prma', 'ufpr', 'prgu'] # siglas das bases

# variaveis globais

# day = 0
# folderYear = 0
# path = []
# paths_local_destino = []
# folderYear = ''
# id_target = ''
#
# paths_extracts = []
# check = 0

# instanciando o tempo
now1 = datetime.datetime.now()
year=str(now1.year)
# configurando métodos dos logs
# format0='%(asctime)s - %(message)s'
# logging.basicConfig(filename=os.path.join(path_root,'log'+year+'.txt'), level=logging.INFO, format=format0, datefmt='%d/%m/%y %I:%M:%S %p')
#



def date2doy(date): # biblioteca de terceiros, créditos ao  https://github.com/purpleskyfall/gnsscal

    """Convert date to day of year, return int doy.
    Example:
    >>> from datetime import date
    >>> date2doy(date(2017, 5, 17))
    137
    """
    first_day = datetime.date(date.year, 1, 1)
    delta = date - first_day
    return delta.days + 1

def folder_year_function(day_delay):  # define a pasta local relativo ao ano
        """ day_delay é os dias subtraidos ao dia atual"""

        now = datetime.datetime.now()
        today_gnss = int(date2doy(datetime.date(now.year, now.month, now.day)))
        logs_bug('today_gnss', str(today_gnss))
        day_target = today_gnss-day_delay

        if day_target <= 0:
            folderYear = str(int(now.year)-1)
        else:
            folderYear = str(now.year)
        return folderYear





class RbmcLib():





    def __init__(self):
        self.sigla = ('Cascavel - prcv', 'Maringá - prma', 'Curitiba - ufpr', 'Guarapuava - prgu') # siglas das bases
        self.now1=now1
        self.today_gnss=date2doy(datetime.date(now1.year,now1.month,now1.day))


    def names_file_target(self,id_doy,bases): # define os nomes dos arquivos para busca
        # Cascavel: prcv , Maringá: prma, Curitiba:ufpr e Guarapuava:prgu
        file_target = []
        i=0
        for interador in bases:
            if bases[i]=='Cascavel - prcv':
                file_target.append('prcv'+str(id_doy[i])+"1"+".zip")
            elif  bases[i]=='Maringá - prma':
                file_target.append('prma'+str(id_doy[i])+"1"+".zip")
            elif  bases[i]=='Curitiba - ufpr':
                file_target.append('ufpr'+str(id_doy[i])+"1"+".zip")
            elif bases[i]=='Guarapuava - prgu':
                file_target.append('prgu'+str(id_doy[i])+"1"+".zip")
            else:
                pass
            i=i+1
        return file_target


    def convert_to_doy(self,date):
        first_day = datetime.date(date.year, 1, 1)
        delta = date - first_day
        return delta.days + 1


    def logs_info(mensagem): #log de informação
        logging.info(mensagem)

    def logs_bug(nome_variavel,variavel):  # log para debug, utilizado somente em desenvolvimento
        logging.debug('debug '+nome_variavel+': '+variavel)




    def bissexto(folderYear):  # verificação para ver se o ano é bissexto
        """ retorno booleano verdadeiro se o ano é bissexto"""
        year = int(folderYear)
        if (year % 100) != 0 and (year % 4) == 0 or (year % 400) == 0:
            return True
        else:
            return False


    def fileSize(self,paths_local_destino,folderYear,id_target,file_target,i):
        temp=0
        ftp=ftplib.FTP('geoftp.ibge.gov.br')
        ftp.login()
        dir_cwd = ("informacoes_sobre_posicionamento_geodesico/rbmc/dados"+'/'+str(folderYear)+"/"+str(id_target))
        ftp.cwd(str(dir_cwd))
        temp=ftp.size(file_target[i])
        ftp.quit()
        return temp



    def download_ftp(self,paths_local_destino,folderYear,id_target,file_target,i): # metodo para download da rbmc

        def call_back(block):
            #
            # print(statinfo.st_size)
            p.write(block)

        ftp=ftplib.FTP('geoftp.ibge.gov.br')
        ftp.login()
        dir_cwd = ("informacoes_sobre_posicionamento_geodesico/rbmc/dados"+'/'+str(folderYear)+"/"+str(id_target))
        ftp.cwd(str(dir_cwd))
        p = open(str(os.path.join(paths_local_destino,file_target[i])), "wb")
        ftp.retrbinary("RETR " + file_target[i],call_back)
        p.close()
        ftp.quit()
