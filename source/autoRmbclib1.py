


import os
import time
import datetime
import zipfile
import ftplib
from pathlib import Path
from socket import gaierror
import logging
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
                file_target.append('prcv'+str(id_doy)+"1"+".zip")
            elif  bases[i]=='Maringá - prma':
                file_target.append('prma'+str(id_doy)+"1"+".zip")
            elif  bases[i]=='Curitiba - ufpr':
                file_target.append('ufpr'+str(id_doy)+"1"+".zip")
            elif bases[i]=='Guarapuava - prgu':
                file_target.append('prgu'+str(id_doy)+"1"+".zip")
            else:
                pass

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




    def download_ftp(address,paths_local_destino,folderYear,id_target,file_target,i,prin=True): # metodo para download da rbmc


        site_address=address
        ftp=ftplib.FTP(site_address)
        ftp.login()
        dir_cwd = str("informacoes_sobre_posicionamento_geodesico/rbmc/dados"+'/'+folderYear+"/"+id_target)
        if prin:
            print (str(dir_cwd))
            print('\nConectado em ftp://geoftp.ibge.gov.br \n')
        ftp.cwd(str(dir_cwd))
        p = open(str(os.path.join(paths_local_destino,file_target[i])), "wb")
        if prin:
            print('Downloading file '+file_target[i]+' para '+str(paths_local_destino))
        try:
            ftp.retrbinary("RETR " + file_target[i], p.write)
            p.close()
            if prin:
                print('Download file '+file_target[i]+' sucess\n')
        except ftplib.error_perm:
            if prin:
                print('Arquivo '+file_target[i]+' não encontrado no servidor\n')
            logs_info('Arquivo '+file_target[i]+' não encontrado no servidor\n')
            p.close()
            os.remove(os.path.join(paths_local_destino[i],file_target[i]))
            logs_bug("remove: path ",str(paths_local_destino[i]))

        except TimeoutError:
            print('tempo de conexao expirado')
            logs_info('tempo de conexao expirado')
        logs_info('Download file '+file_target[i]+' sucess')

        ftp.quit()




    def extracts(paths_extracts,paths_local_destino,file_target,prin=True): # define a descompactação do zip
        j=0
        for b in baseFolder:
            if not os.path.exists(os.path.join(str(paths_local_destino[j]),"extracts")):
                os.makedirs(os.path.join(str(paths_local_destino[j]),"extracts"))
            paths_extracts.append(os.path.join(str(paths_local_destino[j]),"extracts"))
            j=j+1
        i=0
        for z in baseFolder:

            try:
                zip1 = zipfile.ZipFile(str(os.path.join(paths_local_destino[i],file_target[i])))
                zip1.extractall(str(paths_extracts[i]))
                if prin:
                    print('Extraindo para '+str(paths_extracts[i]))
                logs_info('Extraido '+file_target[i]+' com sucesso')
                zip1.close()
            except:
                os.remove(os.path.join(paths_local_destino[i],file_target[i]))
                logs_info('Erro '+file_target[i]+' não encontrado')
            i=i+1


    def dia_de_hoje(): # retorna o dia atual em gnss calendar
        now = datetime.datetime.now()
        today_gnss=int(date2doy(datetime.date(now.year,now.month,now.day)))
        return today_gnss

    def conversao_dia(dia,mes,ano): # converte variáveis dia, mes e ano para gnss calendar

        var = datetime.date(ano, mes, dia)
        alvo=int(date2doy(datetime.date(var.year,var.month,var.day)))
        logs_bug('alvo', str(alvo))
        return alvo



    def reset_folders():

        global folderYear
        global id_target
        global file_target
        global paths_local_destino
        global path_root

        day = 0
        folderYear = 0
        path.clear()
        paths_local_destino.clear()
        file_target.clear()
        folderYear = ''
        id_target = ''
        check = 0


    def setup_folders_files(dia=0,mes=0,ano=0, manual=False):

        global folderYear
        global id_target
        global file_target
        global paths_local_destino
        global path_root

        reset_folders()

        if  manual:

            folderYear = str(ano)
            local_bases_folders(path_root, folderYear)
            id_target = id_target_function((conversao_dia(dia, mes, ano)), delay=False)
            file_target = names_file_target(id_target)
            logs_bug("file_target in rotina manual", str(file_target))
            paths_local_destino = paths_bases_globais(path_root, folderYear)

        else:

            folderYear=folder_year_function(day)
            local_bases_folders(path_root,folderYear)
            id_target=id_target_function(day)
            file_target=names_file_target(id_target)
            paths_local_destino=paths_bases_globais(path_root,folderYear)



    def rotina_auto(loop=31,prin=True,only_check=False,day=0,delay=True): # rotina principal automatica

        global paths_extracts
        global folderYear
        global id_target
        global file_target
        global paths_local_destino
        global path_root

        setup_folders_files()

        if  only_check:

            soma_files=0
            i=0

            for b1 in paths_local_destino:
                list_dir=paths_local_destino[i]
                try:
                    list_dir_file=os.listdir(list_dir)
                except FileNotFoundError:
                    pass
                try:
                    list_dir_file.remove('extracts')
                except ValueError:
                    pass
                number_files = len(list_dir_file)
                soma_files=number_files+soma_files
                logs_bug('path',str(paths_local_destino[i]))
                logs_bug('number_files',str(number_files))
                logs_bug('soma_files',str(soma_files))
                i=i+1
            return soma_files



        else:
            for a1 in range(loop): # variável bb determina quantos arquivos para trás podem ser baixados em modo automático

                reset_folders()
                folderYear = folder_year_function(day)
                local_bases_folders(path_root, folderYear)

                if delay:
                    id_target=id_target_function(day)

                else:
                    id_target=id_target_function(day,delay=False)   #delay False utilizado para testes
                file_target = names_file_target(id_target)
                paths_local_destino = paths_bases_globais(path_root, folderYear)
                i=-1

                for exist in baseFolder:
                    i=i+1
                    logs_bug("paths é arquivo?",os.path.join(paths_local_destino[i],file_target[i]))
                    logs_bug("is file",str(os.path.isfile(os.path.join(paths_local_destino[i],file_target[i]))))
                    if not os.path.isfile(os.path.join(paths_local_destino[i],file_target[i])):
                        logs_bug("fez download",str(os.path.isfile(os.path.join(paths_local_destino[i],file_target[i]))))
                        if not only_check:
                            try:
                                if prin:
                                    download_ftp("geoftp.ibge.gov.br",paths_local_destino,folderYear,id_target,file_target,i)
                                    extracts(paths_extracts,paths_local_destino,file_target)
                                else:
                                    download_ftp("geoftp.ibge.gov.br",paths_local_destino,folderYear,id_target,file_target,i,prin=False)
                                    extracts(paths_extracts,paths_local_destino,file_target,prin=False)
                                    paths_extracts.clear()
                            except gaierror:
                                if prin:
                                    print('Sem conexão com o servidor ftp://geoftp.ibge.gov.br')
                                logs_info('Sem conexão com servidor ftp://geoftp.ibge.gov.br')
                            except ftplib.error_perm:
                                logs_info('Arquivo '+str(file_target[i])+' não encontrado')
                                if prin:
                                    print('Arquivo '+str(file_target[i])+' não encontrado')
                            # try:)
                            #     if prin:
                            #         extracts(paths_extracts,paths_local_destino,file_target)
                            #     else:
                            #         extracts(paths_extracts,paths_local_destino,file_target,prin=False)

                            except FileNotFoundError:
                                pass
                            except zipfile.BadZipFile:
                                pass
                    else:
                        pass
                    logs_info('Arquivo da base '+str(file_target[i])+' existente em: '+str(paths_local_destino[i]))

                day=day+1

    def rotina_base_especifica(dia,mes,ano): # rotina principal manual

        global paths_extracts
        global folderYear
        global id_target
        global file_target
        global paths_local_destino
        global path_root

        setup_folders_files(dia,mes,ano,manual=True)
        i=-1

        for exist in baseFolder:
            i=i+1
            logs_bug('paths_local_destino[i]',str(paths_local_destino[i]))
            if not os.path.isfile(os.path.join(paths_local_destino[i],file_target[i])):
                try:
                    download_ftp("geoftp.ibge.gov.br",paths_local_destino,folderYear,id_target,file_target,i)
                except gaierror:
                    print('Sem conexão com o servidor ftp://geoftp.ibge.gov.br')
                    logs_info('Sem conexão com servidor ftp://geoftp.ibge.gov.br')
                except ftplib.error_perm:
                    logs_info('Arquivo '+file_target[i]+' não encontrado')
                    print('Arquivo '+file_target[i]+' não encontrado')
                try:
                    extracts(paths_extracts,paths_local_destino,file_target)
                    paths_extracts.clear()
                except FileNotFoundError:
                    pass
                except zipfile.BadZipFile:
                    logs_info('Arquivo '+file_target[i]+' não encontrado para extraçao')
                    print('Erro de extração de dados, FileNotFoundError')
            print('Arquivo da base '+file_target[i]+' existente em '+str(paths_local_destino[i]))

        reset_folders()

    # def thread2(name,th2):
    #     schedule.every().day.at(th2).do(rotina_auto)
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1*60)

    def thread3(name,th3):
        global check
        check=rotina_auto(prin=False,only_check=True)



    def interacao_user():

        print('Entrando em modo manual')
        time.sleep(1)
        l2=True
        while l2:
            try:
                dia=int(input('Qual dia da base para download? \n'))
                if dia >31 or dia<=0:
                    print('favor inserir valor entre 1 a 31')
                    l2=True
                    raise ValueError
                else:
                    l2=False
            except ValueError:
                print('Favor inserir apenas número correspondendo ao dia da base a ser baixada')
                l2=True
        l3=True
        while l3:
            try:
                mes=int(input('Qual mês? (mês da data da coleta)\n'))
                if mes >12 or mes<=0:
                    print('favor inserir um valor que corresponde ao mês entre 1 a 12')
                    raise ValueError
                else:
                    l3=False
            except ValueError:
                print('Favor inserir apenas número correspondendo o mês')
                l3=True
        l4=True
        while l4:
            try:
                ano=int(input('Qual ano ?(ano da data da coleta)\n'))
                conversao_dia(dia,mes,ano)
                if (ano >=2016) and (ano<=now1.year):
                    l4=False
                    rotina_base_especifica(dia,mes,ano)
                else:
                    raise TypeError  # eu sei que não é TypeError, mas serviu...
            except TypeError:
                print('Favor inserir apenas número correspondente ao ano entre 2016 e ano atual.')
                l4=True

            except ValueError:
                print('Data não existente, favor digitar uma data existente')
                interacao_user()
        lf=True
        while lf:
            print('Deseja fazer download de mais uma base?')
            resp0=input('y/n\n')
            try:
                if resp0=='y' or resp0=='n':
                    if resp0=='y':
                        interacao_user()
                    else:
                        lf=False
                        print('Deseja prosseguir para modo automático? ou finalizar?')
                        print('digite y para prossegui e n para finalizar?')
                        resp1 = input()
                        try:
                            if resp1=='y' or resp0=='n':
                                if resp1 == 'y':
                                    segunda_etapa()
                                if resp1=='n':
                                    print('Fim da aplicação')
                                    os._exit(1)
                                else:
                                    ValueError
                        except ValueError:
                            print('Favor responda somente y para sim ou n para não')
                else:
                    raise ValueError
            except ValueError:
                print('Favor responda somente y para sim ou n para não')

    def show_files():

        global path_root

        print('\nExibindo arquivos contidos em %s:\n' %path_root)
        time.sleep(2)
        setup_folders_files()
        i=-1
        for ai in paths_local_destino:
            i=i+1
            path.append(paths_local_destino[i])
            try:
                print('\nArquivos contidos em: '+str(path[i])+str(os.listdir(path[i])))
                logs_info('Arquivos contidos em: '+str(path[i])+str(os.listdir(path[i])))
            except FileNotFoundError:
                pass

# def interrupted(signum, frame): # funciona apenas no linux
#      "called when read times out"
#     print ('Aplicação finalizada')
#     sys.exit()

# def watchdog():
#     segunda_etapa()
# # time.sleep(10)
# #   os._exit(1)

# ----------------------------------------------------fluxo principal ---------------------------------------------------------#
#
#
# # Primeira etapa --------------------------------------------------------------------------------------------------------------#
#
# def primeira_etapa():
#
#     global delay_time
#
#     delay_time = 30   # delay time in seconds
#     alarm = threading.Timer(delay_time, watchdog)
#     alarm.start()
#     print('\nDigite enter  para iniciar\n')
#     print('Se %d segundos não houver intereção, a aplicação irá para modo automático'% delay_time)
#     # print('Digite enter para continuar e escolher uma base para download')
#     input()
#     # disable the alarm after success
#
#     l0=True
#     while l0:
#         print('\n\nDigite 1 para escolher uma base específica')
#         print('Digite 2 para iniciar modo automático')
#         r0=int(input())
#         try:
#             if r0==1 or r0==2:
#                 if r0==1:
#                     l0=False
#                     alarm.cancel()
#                     interacao_user()
#                 else:
#                     l0=False
#                     alarm.cancel()
#                     segunda_etapa()
#                     break
#             else:
#                 l0=True
#                 raise ValueError
#         except ValueError:
#             print('Por favor, responda somente 1 ou 2 para os opções')
#
#
#
#
#
#
# # Segunda etapa --------------------------------------------------------------------------------------------------------------#
# def segunda_etapa():
#
#
#     global check
#     global loop
#     global path_root
#
#     # verifica quantos arquivos de base há no em local
#     t3 = threading.Thread(target=thread3, args=('task13', 'none'))
#     t3.start()
#     print('As bases por este programa, serão baixadas e descompactadas automaticamente em %s\n' %path_root)
#     time.sleep(2)
#     print('\nEm %s' %path_root)
#     time.sleep(4)
#     print('\nAguarde enquanto faremos algumas verificações')
#     time.sleep(3)
#     t3.join()
#     if check < 0:
#         check = 0
#     print('\nFoi verificado que há ao todo há %d bases em C:\IBGE\n ' % check)
#     time.sleep(2)
#     print('Verificando se há arquivos recentes no servidor do IBGE para serem baixados\n')
#     time.sleep(2)
#     rotina_auto(loop, prin=True, only_check=False)
#     print('Foi verificado e atualizado os arquivos recentes com sucesso')
#     show_files()
#     time.sleep(6)
#     os._exit(1)
#
#
# # primeira_etapa()
