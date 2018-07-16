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



import autoRmbclib1
from tkinter import*
from tkinter import ttk
from tkinter import filedialog
import os
import time
import datetime
import threading
import tkcalendar
import locale

root=Tk()
#configurações iniciais
y_text_canvas=10
x_text_canvas=70
bases_escolhidas=[]
tags_bases=0
tags_vetor=[]
version="versão 2.0"
i1=autoRmbclib1.RbmcLib()
now1 = i1.now1
year=str(now1.year)
month=str(now1.month)
day=str(now1.day)
local_folders=StringVar()
local_folders.set("")


def update():
    while True:
        time.sleep(30)# tempo de atualização
        l6.config(text="%s/%s/%s" %(day,month,year))
        l7.config(text=i1.today_gnss)
        # l8.config(text=i)
        # i=i+1

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

    bb1=True
    aa1=c1.get()

    i=0
    for j in bases_escolhidas:
        if aa1==bases_escolhidas[i]:
            bb1=False
        i=i+1
    if bb1:
        bases_escolhidas.append(c1.get())
        tags_vetor.append(canvas.create_text(x_text_canvas,y_text_canvas,font="Times 12 italic bold",text=bases_escolhidas[-1],tag=str(tags_bases)))
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
    print(str(tags_bases))
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
    except IndexError:
        pass
    canvas.delete(tags_vetor[tags_bases-1])
    tags_bases=tags_bases-1
    print(str(tags_vetor))


def download_button():

    lista=[]
    global bases_escolhidas
    global local_folders
    cal1=calButtonMouse()
    cal2_converted=i1.convert_to_doy(cal1)
    # verificação se foi seleciando pelo menos uma data
    string_data_corrente="%s%s%s" %(day,month,year)
    string_cal1=str(cal1.day)+str(cal1.month)+str(cal1.year)
    if string_cal1==string_data_corrente:
        print("Aqui vai uma mensagem de alerta, favor selecionar a data de levantamento")

    if cal2_converted>10 and cal2_converted<100:
        cal2_converted="0"+str(cal2)
    elif cal2_converted<10:
        cal2_converted="00"+str(cal2_converted)
    else:
        cal2_converted=str(cal2_converted)

    file_target=i1.names_file_target(cal2_converted,bases_escolhidas)
    print(file_target)
    # download_ftp("geoftp.ibge.gov.br",paths_local_destino,folderYear,id_target,file_target,i)
    # i1.download_ftp(geoftp.ibge.gov.br,local_folders.get(),cal1.year)



#


#Threading de update
clock = threading.Timer(30, update)
clock.start()

# root.geometry('250x150+0+0')
root.resizable(width=False, height=False)
root.title("AutoRbmcIbge2")

os1=os.name;
if os.name=="nt":
    root.iconbitmap("alvo.ico")
else:
    # root.iconbitmap("@alvo2.xbm") // desisto, não esta funcionando no linux
    pass

# frames
frame1=Frame() #superior
frame2=Frame() # inferior
frame3=Frame()# canvas
frame5=Frame()
frame6=Frame()
# separador
separator = ttk.Separator(orient='horizontal')
separator.grid(row=1,sticky="we")
separator1 = ttk.Separator(orient='horizontal')
separator1.grid(row=1,column=1,sticky="we")
separator2 = ttk.Separator(orient='horizontal')
separator2.grid(row=1,column=2,sticky="we")

#frames
frame1.grid(row=0,column=0)# ComboBox e botoes
frame2.grid(row=2,column=0,sticky="nw")# Calendarios e Labels
frame3.grid(row=2,column=1,sticky="s")# Canvas
frame5.grid(row=0,column=1)# labels de hoje
frame6.grid(row=2,column=2,sticky="n")# botões
#Canvas
canvas = Canvas(frame3, bg='white', width=260, height=300)
canvas.grid(row=1,column=0)


# Botões

b1=Button(frame1,text="Adicionar base",command=add_button_text)
b2=Button(frame1,text="Salvar em:",command=browse_button)
# b3=Button(frame1,text="Extrair em:")

b4=Button(frame6,text="Remover",command=revomer_button)
b5=Button(frame6,text="Remover todos",command=revomer_button_todos)
b6=Button(frame6,text="Download",font=("Helvetica", 10),fg="red",command=download_button)

#frame1
b1.grid(row=2,column=4,pady=5)#Adicionar
b2.grid(row=4,column=4,pady=5)#Salvar em:,
# b3.grid(row=6,column=4,pady=5)#Extrair em:

#frame6
b4.grid(row=0,column=0,sticky="wn")#Remover
b5.grid(row=3,column=0,sticky="n",pady=20)#Remover todos
l55=Label(frame6)
l56=Label(frame6)
l57=Label(frame6)
l55.grid(row=2,column=0)#branco
#l56.grid(row=3,column=0)#branco
l57.grid(row=4,column=0,pady=20)#branco
l57.grid(row=4,column=0,pady=50)#branco
b6.grid(row=5,column=0,pady=10)

b6.grid(row=5,column=0,sticky="S",pady=10)
# ComboBox
c1=ttk.Combobox(frame1,width=30)
c1.grid(row=2,column=2,sticky="w")
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
l14=Label(frame3,text='Base para download')

l1.grid(row=0,column=5)
l2.grid(row=1,column=2,sticky="w")
l3.grid(row=0,column=10,sticky="e")
l4.grid(row=2,column=5,sticky="w") #Data atual
l6.grid(row=2,column=6)#Data
l5.grid(row=3,column=5)# dia de ano hoje
l7.grid(row=3,column=6,sticky="e")# dia de ano
# l8.grid(row=4,column=9) # testando update
l9.grid(row=4,column=5,sticky="e")
#frame 2
l10.grid(row=0,column=0,sticky="w")# data do levantamento
l11.grid(row=0,column=1,sticky="w")# data do levantamento
l12.grid(row=1,column=0,sticky="w")# dia do ano do levantamento
l13.grid(row=1,column=1,sticky="w")#dia do ano do levantamento
l14.grid(row=0,column=0,)




root.mainloop()
