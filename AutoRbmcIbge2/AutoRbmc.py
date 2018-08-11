# coding: utf-8
# version: 2.0
# python 3
# ftp://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados/

"""
version:2.0
author: Jose Ivan Silva Vegiani
Automacao de download e descompactação de dados do rbmc (IBGE)
rbmc: Rede Brasileira de Monitoramento Contínuo dos Sistemas GNSS
Script de código aberto e livre, cedido gratuitamente pelo autor.
"""

import modulo1
from tkinter import*
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
import os
import time
import datetime
import threading
import tkcalendar
import locale
import datetime
import ftplib
from pathlib import Path
import socket
from socket import gaierror



#configurações iniciais
root=Tk()


y_text_canvas=10
x_text_canvas=70
bases_escolhidas=[]
tags_bases=0
tags_vetor=[]
version="versão 2.0"
dataEscolhida=[]

os1=os.name
if os.name=="nt":
    root.iconbitmap("D:\Python\envAutoRmbcIbge2\AutoRbmcIbge2\source\\alvo.ico")
else:
    # root.iconbitmap("@alvo2.xbm") // desisto, não esta funcionando no linux
    pass





def calButtonMouse(*args):
    cal1=cal.selection_get()
    l11.config(text=str(cal1.day)+"/"+str(cal1.month)+'/'+str(cal1.year))
    l13.config(text=str(i1.convert_to_doy(cal1)))

    return cal1

#funcionalidades dos botões

def browse_button():
#     # Allow user to select a directory and store it in global var
#     # called folder_path
    global local_folders
    filename = filedialog.askdirectory()
    local_folders.set(filename)
    l9.config(text=local_folders.get())


def add_button_text():

    global x_text_canvas
    global y_text_canvas
    global bases_escolhidas
    global tags_bases
    global tags_vetor
    global dataEscolhida
    dataText=[]
    x_text_canvas=10


    bb1=True
    aa1=c1.get()
    bb1=cal.selection_get()
    i=0

    hoje="%s%s%s" %(day,month,year)
    inicio_cal1=str(cal.selection_get().day)+str(cal.selection_get().month)+str(cal.selection_get().year)
    if hoje==inicio_cal1:
        tkinter.messagebox.showerror("Falta de parâmetros",'FAVOR INFORMAR A DATA DO LEVANTAMENTO')
        return False

    for j in bases_escolhidas:
        if aa1==bases_escolhidas[i] and bb1==dataEscolhida[i]:
            bb1=False
        i=i+1
    if bb1:
        bases_escolhidas.append(c1.get())
        dataEscolhida.append(cal.selection_get())
        dataText.append(str(cal.selection_get().day)+"/"+str(cal.selection_get().month)+"/"+str(cal.selection_get().year))
        tags_vetor.append(canvas.create_text(x_text_canvas,y_text_canvas,anchor='w',justify='center', font="Times 12 italic bold",text=bases_escolhidas[-1]+"          "+str(dataText[-1]),tag=str(tags_bases)))
        tags_bases=tags_vetor[-1]
        y_text_canvas=y_text_canvas+20


def revomer_button_todos():

    global x_text_canvas
    global y_text_canvas
    global tags_vetor
    global tags_bases

    y_text_canvas=10
    x_text_canvas=70
    global bases_escolhidas
    dataEscolhida.clear()
    bases_escolhidas.clear()
    canvas.delete(ALL)
    canvas.update()

def revomer_button():
    global tags_bases
    global x_text_canvas
    global y_text_canvas
    global bases_escolhidas
    global tags_vetor
    y_text_canvas=y_text_canvas-20
    try:
        bases_escolhidas.pop(-1)
        dataEscolhida.pop(-1)
    except IndexError:
        pass
    canvas.delete(tags_vetor[tags_bases-1])
    tags_bases=tags_bases-1


def download_button():
    t1 = threading.Thread(target=threading_download, args=())
    t1.start()

# def progress_bar(bases_escolhidas_download_i):
#     t2 = threading.Thread(target=threading_progress_bar, args=(bases_escolhidas_download_i,))
#     t2.start()
#
# def threading_progress_bar(bases_escolhidas_download_i):
#


def threading_download():

    global dataText
    global bases_escolhidas
    global local_folders
    bases_escolhidas_download=[]
    global dataEscolhida


    # mensagens de falta de parâmetros
    hoje="%s%s%s" %(day,month,year)
    inicio_cal1=str(cal.selection_get().day)+str(cal.selection_get().month)+str(cal.selection_get().year)

    if hoje==inicio_cal1:
        tkinter.messagebox.showerror("Falta de parâmetros",'FAVOR INFORMAR A DATA DO LEVANTAMENTO')
        return False

    if local_folders.get()=='':
        tkinter.messagebox.showerror("Falta de parâmetros",'FAVOR INFORMAR O LOCAL ONDE O ARQUIVO SERÁ SALVO EM SEU COMPUTADOR')
        return False


    if len(bases_escolhidas)==0:
        tkinter.messagebox.showerror("Falta de parâmetros",'FAVOR INFORMAR UMA BASE PARA DOWNLOAD')
        return False

    cal2_converted=[]

    i=0
    for interage in dataEscolhida:
        cal2_converted.append(i1.convert_to_doy(dataEscolhida[i]))
        i=i+1

    i=0

    for interador in cal2_converted:

        if (cal2_converted[i]>=10) and (cal2_converted[i]<100):
            cal2_converted[i]="0"+str(cal2_converted[i])
            cal2_converted[i]=int(cal2_converted[i])
        elif cal2_converted[i]<10:
            cal2_converted[i]="00"+str(cal2_converted[i])
            cal2_converted[i]=int(cal2_converted[i])
        else:
            pass
        i=+1

    def threading_gui(bases_escolhidas_download,i):

        frame8=Frame(root)
        frame8.place(x=350,y=500)# progress bar
        text1=str(bases_escolhidas_download[i])
        pb = ttk.Progressbar(frame8, orient="horizontal", length=300, mode="determinate")
        try:
            pb["maximum"] =i1.fileSize(local_folders.get(),cal.selection_get().year,cal2_converted[i],bases_escolhidas_download,i)
        except ftplib.error_perm:
            pass
        pb["value"]=0
        l20=Label(frame8,text=text1,font=("Helvetica", 12))
        l20.config(text=text1)
        l20.update_idletasks()
        l20.grid(row=0,column=0,rowspan=1)
        pb.grid(row=1,column=0,rowspan=1)
        while pb["value"]<=pb["maximum"]:
            try:
                statinfo = os.stat(str(os.path.join(local_folders.get(),bases_escolhidas_download[i])))
            except FileNotFoundError:
                pass
            pb["value"]=statinfo.st_size
            pb.update_idletasks()
        pb["maximum"]=0
        pb["value"]=0
        frame8.destroy()


    bases_escolhidas_download=i1.names_file_target(cal2_converted,bases_escolhidas)

    i=0
    for j in bases_escolhidas:
        try:
            t2 = threading.Thread(target=threading_gui, args=(bases_escolhidas_download,i,))
            t2.start()
            i1.download_ftp(local_folders.get(),cal.selection_get().year,cal2_converted[i],bases_escolhidas_download,i)
            tkinter.messagebox.showinfo('Sucesso','Concluído download ' +str(bases_escolhidas_download[i]+' com sucesso!'))
        except ftplib.error_perm:
            tkinter.messagebox.showerror('ERRO','Arquivo '+str(bases_escolhidas_download[i]+' não encontrado no servidor'))
        except socket.gaierror:
            tkinter.messagebox.showerror('ERRO','Sem conexão com servidor')
        i=i+1


i1=modulo1.RbmcLib()
now1 = i1.now1
year=str(now1.year)
month=str(now1.month)
day=str(now1.day)
local_folders=StringVar()
local_folders.set("")


root.geometry('900x600')
root.resizable(width=True, height=True)
root.title("AutoRbmcIbge2")

frame1=Frame() #superior
frame2=Frame() # inferior
frame3=Frame()# canvas
frame5=Frame()
frame6=Frame()



#frames
frame1.place(x=0,y=40)# ComboBox e botoes
frame2.place(x=0,y=200)# Calendarios e Labels
frame3.place(x=350,y=200)# Canvas
frame5.place(x=0,y=30)# labels de hoje
frame6.place(x=610,y=220)# botões


#Canvas
canvas = Canvas(frame3, bg='white', width=260, height=250)
canvas.grid(row=2,column=0,rowspan=2,columnspan=2)

    # Botões

b1=Button(frame1,text="Adicionar base",command=add_button_text)
b2=Button(frame1,text="Salvar em:",command=browse_button)
    # b3=Button(frame1,text="Extrair em:")

b4=Button(frame6,text="Remover",command=revomer_button)
b5=Button(frame6,text="Remover todos",command=revomer_button_todos)
b6=Button(frame6,text="Download",font=("Helvetica", 12),fg="red",command=download_button)

#frame1
b1.grid(row=2,column=1,pady=5)#Adicionar
b2.grid(row=4,column=1,pady=5)#Salvar em:,


#frame6
b4.grid(row=2,column=1,sticky="w")#Remover
b5.grid(row=3,column=1,pady=15)#Remover todos
b6.grid(row=6,column=1,sticky="w",pady=135)

# ComboBox
c1=ttk.Combobox(frame1,width=30)
c1.grid(row=2,column=0,sticky="w")
c1['values']=i1.sigla
c1.current(2)
# Calendar
cal=tkcalendar.Calendar(frame2)
cal.bind('<<CalendarSelected>>',calButtonMouse)
cal.grid(row=2,column=0,sticky="w")

# Labels
l1=Label(frame1,text="AutoRbmcIbge",font=("Helvetica", 20))#fixo
l2=Label(frame1,text="Bases")#fixo
l3=Label(frame1,text=version)#fixo
l4=Label(frame5,text="Data atual:")#fixo
l5=Label(frame5,text="Dia do ano de hoje:")#fixo
l6=Label(frame5,text="%s/%s/%s" %(day,month,year))# alterar na execução
l7=Label(frame5,text=i1.today_gnss)# alterar na execução
#l8=Label(frame1,text="testar") #relógio para testar o update
l9=Label(frame1,text=local_folders.get())
#frame 2
l10=Label(frame2,text="Data do levantamento:")
l11=Label(frame2,text='0')# data do levantamento
l12=Label(frame2,text="Dia do ano do levantamento:")
l13=Label(frame2,text='0')
l14=Label(frame3,text='Base e data para download')


l1.grid(row=0,column=4,sticky="e")
l2.grid(row=1,column=0,sticky="w")
l3.grid(row=0,column=5,sticky="e")
l4.grid(row=2,column=5,sticky="w") #Data atual
l6.grid(row=2,column=6)#Data
l5.grid(row=3,column=5)# dia de ano hoje
l7.grid(row=3,column=6,sticky="e")# dia de ano
    # l8.grid(row=4,column=9) # testando update
l9.grid(row=4,column=2,sticky="w")
    #frame 2
l10.grid(row=0,column=0,sticky="w")# data do levantamento
l11.grid(row=0,column=1,sticky="w")# data do levantamento
l12.grid(row=1,column=0,sticky="w")# dia do ano do levantamento
l13.grid(row=1,column=1,sticky="w")#dia do ano do levantamento
l14.grid(row=0,column=0,sticky="w")
# l15.grid(row=0,column=0,sticky="e")
root.mainloop()
