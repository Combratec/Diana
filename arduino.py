#!/usr/bin/python3
# -*- coding: utf-8 -*-
try:
    from tkinter import * 
    from tkinter import messagebox
except Exception as erro:
    print('Erro com o módulo Tkinter! \n Erro: '+str(erro))
    i = input('[Pressione enter]')
else:
    print('Iniciando Diana')

# Faz o processamento dos arquivos
from processamento import analise
import alternativa

# Definições básicas da tela
tela = Tk() 
# tela.resizable(width=False, height=False)
tela.configure(background="white",border=0)
tela.title('Diana chatbot - Combratec Inova')
tela.geometry("446x546+100+100")

tela.grid_columnconfigure(1, weight=1)

fr1 = Frame(tela,bg='blue')
fr1.grid(row=0,column=1,sticky=NSEW)
fr1.grid_columnconfigure(2,weight=1)

fr2 = Frame(tela,bg='white')
fr2.grid(row=1,column=1,sticky=NSEW)
fr2.grid_columnconfigure((1,2),weight=1)

fr3 = Frame(tela,bg='white')
fr3.grid(row=2,column=1,sticky=NSEW)
fr3.grid_columnconfigure((1,2),weight=1)

fr4 = Frame(tela,bg='white')
fr4.grid(row=3,column=1,sticky=NSEW)
fr4.grid_columnconfigure((1,2),weight=1)

fr5 = Frame(tela,bg='white')
fr5.grid(row=4,column=1,sticky=NSEW)
fr5.grid_columnconfigure((1,2),weight=1)

fr6 = Frame(tela,bg='white')
fr6.grid(row=5,column=1,sticky=NSEW)
fr6.grid_columnconfigure((1,2),weight=1)

conf_btns = {
	'relief':GROOVE,
	'highlightthickness':0,
	'border':0,
	'bg':'blue',
	'activebackground':'blue'}

conf_btns_item = {
	'relief':GROOVE,
	'highlightthickness':0,
	'border':0,
	'bg':'white',
	'activebackground':'white'}

imagem = PhotoImage(file='Imagens/opcoes/return.png')
imagem = imagem.subsample(3,3)
arduino = PhotoImage(file='Imagens/opcoes/arduino.png')
arduino = arduino.subsample(3,3)

retornar = Button(fr1,conf_btns,image=imagem)
retornar.grid(row=1,column=1)

lbl = Label(fr1, text='COMANDE',font=("Sans",17,'bold'),bg='blue',fg='white')
lbl.grid(row=1,column=2,sticky=NSEW)

lbl = Label(fr1,image=arduino,font=("Sans",17,'bold'),bg='blue')
lbl.grid(row=1,column=3)

# ---- Verificação da serial ----#
lbl = Label(fr2, text='Digite a serial: /dev/com4 ...',font=("Sans",10,'bold'),bg='white',fg='black')
lbl.grid(row=1,column=1,columnspan=2,sticky=NSEW)

entry = Entry(fr2,state='normal')
entry.grid(row=2,column=1,sticky=NSEW)

btn = Button(fr2,conf_btns_item,text='testar',relief=FLAT,width=7)
btn.grid(row=2,column=2,sticky=NSEW)

# ---- load ----
delete =  PhotoImage(file='Imagens/opcoes/delete.png')
code =  PhotoImage(file='Imagens/opcoes/code.png')
edit   =  PhotoImage(file='Imagens/opcoes/edit.png')
add    =  PhotoImage(file='Imagens/opcoes/add.png')
nad    =  PhotoImage(file='Imagens/opcoes/nada.png')
delete =  delete.subsample(3,3)
code   =  code.subsample(2,2)
edit   =  edit.subsample(3,3)
add    =  add.subsample(3,3)
nad    =  nad.subsample(3,3)

lbl = Label(fr3,text='enviar',font=("Sans",10,'bold'),bg='white',fg='black')
lbl.grid(row=1,column=1)
lbl = Label(fr3,text='comando;resposta',font=("Sans",10,'bold'),bg='white',fg='black')
lbl.grid(row=1,column=2)

# ---- Itens ativos ----#
entry = Entry(fr4,state='disable')
entry.grid(row=1,column=1,sticky=NSEW)

entry = Entry(fr4,state='disable')
entry.grid(row=1,column=2,sticky=NSEW)

btn = Button(fr4,conf_btns_item,image=delete)
btn.grid(row=1,column=3,sticky=NSEW)

btn = Button(fr4,conf_btns_item,image=edit)
btn.grid(row=1,column=4,sticky=NSEW)

# ---- ADICIONAR NOVO ----
entry = Entry(fr5)
entry.grid(row=1,column=1,sticky=NSEW)

entry = Entry(fr5)
entry.grid(row=1,column=2,sticky=NSEW)

btn = Button(fr5,conf_btns_item,image=add)
btn.grid(row=1,column=3,sticky=NSEW)

lbl = Button(fr5,conf_btns_item,image=nad)
lbl.grid(row=1,column=4,sticky=NSEW)

# ---- código mínino ----
lbl = Label(fr6,image=code,border=5)
lbl.grid(row=1,column=1)

tela.mainloop()