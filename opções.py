#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import alternativa
from tkinter import * 
from tkinter import messagebox
from pyanalise import compare
from definicoes import musica
from processamento import analise

global precisao_minima
precisao_minima = 80

global save_music_object_position
save_music_object_position = []

global music_itens
music_itens = musica.ler()

tela = Tk() 
tela.resizable(width=False, height=False)
tela.configure(background="white",border=0)
tela.grid_columnconfigure(1, weight=1)
tela.rowconfigure(1, weight=1)
tela.title('Diana chatbot - Combratec Inova')
tela.geometry("446x546+100+100")

fr_options = Frame(tela)
fr_options.grid_columnconfigure(1, weight=1)
fr_options.rowconfigure(1, weight=1)
fr_options.grid(row=1,column=1,sticky=NSEW)

def abrir_site(link):
    import webbrowser
    webbrowser.open(link)

def troca_tela(carregar):
	if carregar=='opca_hist':
		fr_options.grid_forget()
		fr_historic.grid(row=1,column=1,sticky=NSEW)

	elif carregar=='hist_opca':
		fr_options.grid(row=1,column=1,sticky=NSEW)
		fr_historic.grid_forget()

	elif carregar=='opca_pyan':
		fr_options.grid_forget()
		fr_pyanalise.grid(row=1,column=1,sticky=NSEW)

	elif carregar=='pyan_opca':
		fr_pyanalise.grid_forget()
		fr_options.grid(row=1,column=1,sticky=NSEW)

	elif carregar=='opca_musi':
		fr_options.grid_forget()
		fr_music.grid(row=1,column=1,sticky=NSEW)

	elif carregar=='musi_opca':
		fr_options.grid(row=1,column=1,sticky=NSEW)
		fr_music.grid_forget()

def resize(event=None):
	global precisao_minima
	precisao_minima = scale_py.get()
	print(precisao_minima)

def test_pyanalise(event):
	global precisao_minima

	ent_py_test_1.update()
	busca_semelhanca = compare.frase(ent_py_test_1.get(),ent_py_test_2.get())
	result_py_test['text'] = str(busca_semelhanca)+str('%')
	if busca_semelhanca < precisao_minima:
		result_py_test['fg'] = 'red'
	else:
		result_py_test['fg'] = 'blue'


def load_itens_musics():
    global save_music_object_position

    # remove all objects
    for list_objects in save_music_object_position:
        for especifc_objets in list_objects:
            especifc_objets.grid_forget()

    global music_itens
    music_itens = musica.ler()

    dic_load_entry = {'relief':GROOVE,'border':2}

    for x in range(len(music_itens)):
        ent_load_file_music = Entry(fr_music_3 , dic_load_entry)
        ent_load_comand_music = Entry(fr_music_3 , dic_load_entry)
        ent_load_file_music.grid(row=x,column=1,sticky=NSEW)
        ent_load_comand_music.grid(row=x,column=2,sticky=NSEW)

        ent_load_file_music.delete(0,END)
        ent_load_comand_music.delete(0,END)

        ent_load_file_music.insert(0,music_itens[x]['musica'])
        ent_load_comand_music.insert(0,music_itens[x]['comando'])

        btn_remove_item = Button(fr_music_3,config_btns_itens,image=img_remove)
        btn_remove_item['command'] = lambda btn_remove_item=btn_remove_item: remove_item_music(btn_remove_item)
        btn_remove_item.grid(row=x,column=3,sticky=NSEW)

        btn_load_test_music = Button(fr_music_3,config_btns_itens,text='TESTAR',relief=RAISED,border=1)
        btn_load_test_music.grid(row=x,column=4,sticky=NSEW)

        new_list_itens = [ ent_load_file_music , ent_load_comand_music , btn_remove_item , btn_load_test_music ]
    
        save_music_object_position = []
        save_music_object_position.append(new_list_itens) 

def remove_item_music(btn):
    global save_music_object_position
    for x in range(len(save_music_object_position)):
        if save_music_object_position[x][2] == btn:
            musica.remover(x)
            load_itens_musics()

def add_item_music():
    a = ent_new_file_music.get() 
    b = ent_new_comand_music.get()

    if (a == '') or (b == '') or a.isspace() or b.isspace() or (not ';' in b) or (':' in b) or (':' in a):
        messagebox.showinfo('erro','Dados inválidos detectado!')
    else:
        musica.adicionar({'musica': a, 'comando': b})
        load_itens_musics()
        ent_new_file_music.delete(0,END)
        ent_new_comand_music.delete(0,END)


fr_options_1 = Frame(fr_options,bg='blue')
fr_options_1.grid(row=0,column=1,sticky=NSEW)
fr_options_1.grid_columnconfigure(2,weight=1)

fr_options_2 = Frame(fr_options,bg='white')
fr_options_2.grid(row=1,column=1,sticky=NSEW)
fr_options_2.grid_columnconfigure((1,2),weight=1)
fr_options_2.grid_columnconfigure(2,weight=2)

conf_btns = {
	'relief':GROOVE,
	'highlightthickness':0,
	'border':0,
	'bg':'white'}

img_transparent  =  PhotoImage(file='Imagens/opcoes/transparent.png')
img_pyanalise    =  PhotoImage(file='Imagens/opcoes/pyanalise.png')
img_historic     =  PhotoImage(file='Imagens/opcoes/historico.png')
img_github_py    =  PhotoImage(file='Imagens/opcoes/github_branco.png')
img_continue     =  PhotoImage(file='Imagens/opcoes/avance.png')
img_music_2      =  PhotoImage(file='Imagens/opcoes/musica.png')
img_arduino      =  PhotoImage(file='Imagens/opcoes/arduino.png')
img_github       =  PhotoImage(file='Imagens/opcoes/github.png')
img_return       =  PhotoImage(file='Imagens/opcoes/return.png')
img_music        =  PhotoImage(file='Imagens/opcoes/musica.png')
img_about        =  PhotoImage(file='Imagens/opcoes/sobre.png')
img_remove       =  PhotoImage(file='Imagens/opcoes/remove.png')
img_add          =  PhotoImage(file='Imagens/opcoes/add.png')

img_transparent  =  img_transparent.subsample(3,3)
img_pyanalise    =  img_pyanalise.subsample(2,2)
img_historic     =  img_historic.subsample(2,2)
img_github_py    =  img_github_py.subsample(16,16)
img_continue     =  img_continue.subsample(2,2)
img_music_2      =  img_music_2.subsample(3,3)
img_arduino      =  img_arduino.subsample(2,2)
img_github       =  img_github.subsample(2,2)
img_return       =  img_return.subsample(3,3)
img_music        =  img_music.subsample(2,2)
img_about        =  img_about.subsample(2,2)
img_remove       =  img_remove.subsample(3,3)
img_add          =  img_add.subsample(3,3)

retornar = Button(fr_options_1,conf_btns,image=img_return,bg='blue',activebackground='blue')
retornar.grid(row=1,column=1)
lbl = Label(fr_options_1, text='OPÇÕES',font=("Sans",17,'bold'),bg='blue',fg='white')
lbl.grid(row=1,column=2,sticky=NSEW)

lbl = Label(fr_options_2,image=img_music,bg='white')
lbl.grid(row=1,column=1)
lbl = Label(fr_options_2,text='Tocar musica',font=("Sans",20,'bold'),bg='white')
lbl.grid(row=1,column=2,sticky=NSEW) 
btn_musica = Button(fr_options_2,conf_btns,image=img_continue)
btn_musica['command'] = lambda: troca_tela('opca_musi')
btn_musica.grid(row=1,column=3,sticky=NSEW) 

lbl = Label(fr_options_2,image=img_pyanalise,bg='white')
lbl.grid(row=2,column=1)
lbl = Label(fr_options_2,text='Pyanalise',font=("Sans",20,'bold'),bg='white')
lbl.grid(row=2,column=2,sticky=NSEW) 
btn_pyanalise = Button(fr_options_2,conf_btns,image=img_continue)
btn_pyanalise['command'] = lambda: troca_tela('opca_pyan')
btn_pyanalise.grid(row=2,column=3,sticky=NSEW) 

lbl = Label(fr_options_2,image=img_arduino,bg='white')
lbl.grid(row=3,column=1)
lbl = Label(fr_options_2,text='Comandos',font=("Sans",20,'bold'),bg='white')
lbl.grid(row=3,column=2,sticky=NSEW) 
btn_arduino = Button(fr_options_2,conf_btns,image=img_continue)
btn_arduino.grid(row=3,column=3,sticky=NSEW) 

lbl = Label(fr_options_2,image=img_historic,bg='white')
lbl.grid(row=4,column=1)
lbl = Label(fr_options_2,text='Histórico',font=("Sans",20,'bold'),bg='white')
lbl.grid(row=4,column=2,sticky=NSEW) 
btn_historico = Button(fr_options_2,conf_btns,image=img_continue)
btn_historico['command'] = lambda: troca_tela('opca_hist')
btn_historico.grid(row=4,column=3,sticky=NSEW) 

lbl = Label(fr_options_2,image=img_github,bg='white')
lbl.grid(row=5,column=1)
lbl = Label(fr_options_2,text='Nosso repositório!',font=("Sans",20,'bold'),bg='white')
lbl.grid(row=5,column=2,sticky=NSEW) 
btn_github = Button(fr_options_2,conf_btns,image=img_continue)
btn_github['comman'] = lambda: abrir_site('https://github.com/Combratec/Diana')
btn_github.grid(row=5,column=3,sticky=NSEW) 

lbl = Label(fr_options_2,image=img_about,bg='white')
lbl.grid(row=6,column=1)
lbl = Label(fr_options_2,text='Sobre este projeto!',font=("Sans",20,'bold'),bg='white')
lbl.grid(row=6,column=2,sticky=NSEW) 
btn_sobre = Button(fr_options_2,conf_btns,image=img_continue)
btn_sobre['comman'] = lambda: abrir_site('https://dianachatbot.blogspot.com/2019/02/dianachatbotcombratec.html')
btn_sobre.grid(row=6,column=3,sticky=NSEW) 

# ---- TELA DO HISTÓRICO ----
fr_historic = Frame(tela,background='white')
fr_historic.grid_columnconfigure(1,weight=1)
fr_historic.rowconfigure(3,weight=1)

fr_historic_1 = Frame(fr_historic,background="red")
fr_historic_1.grid_columnconfigure((1,2), weight=1)
fr_historic_1.grid(row=2,column=1,sticky=NSEW)

fr_historic_2 = Frame(fr_historic)
fr_historic_2.grid_columnconfigure(1,weight=1)
fr_historic_2.rowconfigure(1,weight=1)
fr_historic_2.grid(row=3,column=1,sticky=NSEW)

fr_historic_3 = Frame(fr_historic,background="black")
fr_historic_3.grid_columnconfigure((1,2),weight=1) 
fr_historic_3.grid(row=4,column=1,sticky=NSEW)

lbl_dic_config = {
	'background':'#00cccb',
    'highlightbackground':'#00cccb',
    'foreground':'#222',
    'font':("",14)}

# frame superior
lbl = Label(fr_historic,text="Histórico",background='#1976d3',font=("Sans",17,'bold'),highlightbackground="#1976d3", foreground='#fff')
lbl.grid(row=1,column=1,sticky=EW)

lbl = Label(fr_historic_1,lbl_dic_config,text="historico")
lbl.grid(row=1,column=1,sticky=NSEW)

lbl= Label(fr_historic_1,lbl_dic_config,text="Aprendizados")
lbl.grid(row=1,column=2,sticky=NSEW)

# frame central
text_h = Text(fr_historic_2,background='white', highlightbackground='#fff', border=2,foreground='black',font=("consolas", 12), undo=True, wrap='word')
text_h.insert(1.0, 'Não há nada aqui!')
text_h.grid(row=1,column=1,sticky=NSEW)

scl_h = Scrollbar(fr_historic_2, command=text_h.yview,background='white', activebackground="#f9f9f9", highlightbackground="white", highlightcolor="white")
scl_h.grid(row=1,column=2,sticky=NS)
text_h['yscrollcommand'] = scl_h.set

# frame inferior
btn_historic_return_screem = Button(fr_historic_3,text="Voltar",background='#009899', foreground='white', activebackground='#009899', activeforeground="#fff", highlightbackground='#009899', relief=FLAT, font=("Arial",12))
btn_historic_return_screem['command'] = lambda: troca_tela('hist_opca')
btn_historic_return_screem.grid(row=1, column=1,sticky=EW)

btn_clear_historic = Button(fr_historic_3,text="Limpar histórico",background='#fe0000', foreground='white', activebackground="#fe0000", activeforeground="#fff", highlightbackground="#fe0000", relief=FLAT, font=("Arial",12))
btn_clear_historic.grid(row=1, column=2,sticky=EW)


# ---- TELA DO PYANALISE ----
fr_pyanalise = Frame(tela)
fr_pyanalise.grid_columnconfigure(1, weight=1)
fr_pyanalise.rowconfigure(3, weight=1)

# frames
fr_pyanalise_1 = Frame(fr_pyanalise,bg='DarkGreen')
fr_pyanalise_1.grid_columnconfigure(2,weight=1)
fr_pyanalise_1.grid(row=0,column=1,sticky=NSEW)

fr_pyanalise_2 = Frame(fr_pyanalise,bg='white')
fr_pyanalise_2.grid_columnconfigure(1,weight=1)
fr_pyanalise_2.grid(row=1,column=1,sticky=NSEW)

fr_pyanalise_3 = Frame(fr_pyanalise,bg='white',pady=10)
fr_pyanalise_3.grid_columnconfigure((1,2),weight=1)
fr_pyanalise_3.grid(row=2,column=1,sticky=NSEW)

fr_pyanalise_4 = Frame(fr_pyanalise,bg='white')
fr_pyanalise_4.grid_columnconfigure(1,weight=1)
fr_pyanalise_4.rowconfigure(1,weight=1)
fr_pyanalise_4.grid(row=3,column=1,sticky=NSEW)

# configs
conf_btns = {
	'relief':GROOVE,
	'highlightthickness':0,
	'border':0,
	'bg':'white'}

config_description_pyan = {
	'font':("Sans",10,'bold'),
	'bg':'white',
	'fg':'black'}

# top
btn_py_return = Button(fr_pyanalise_1,conf_btns,image=img_return,bg='DarkGreen',activebackground='DarkGreen')
btn_py_return['command'] = lambda: troca_tela('pyan_opca')
btn_py_return.grid(row=1,column=1)

lbl_title = Label(fr_pyanalise_1, text='pyanalise',font=("Sans",17,'bold'),bg='DarkGreen',fg='white')
lbl_title.grid(row=1,column=2,sticky=NSEW)

btn_github_py = Button(fr_pyanalise_1,conf_btns,image=img_github_py,bg='DarkGreen',activebackground='DarkGreen')
btn_github_py['comman'] = lambda: abrir_site('https://github.com/gabrielogregorio/pyanalise')
btn_github_py.grid(row=1,column=3,sticky=NSEW)

# description function
lbl_description = Label(fr_pyanalise_2,text='Taxa de variação do PyAnalise',font=("Sans",12,'bold'),bg='green',fg='white')
lbl_description.grid(row=1,column=1,sticky=NSEW)

# control
scale_py = Scale(fr_pyanalise_2,from_=1, to=100, orient=HORIZONTAL,command=resize,highlightbackground='white',troughcolor='green',bd=1,bg='green',fg='white',highlightthickness=0)
scale_py.set(precisao_minima)
scale_py.grid(row=2,column=1,sticky=NSEW)

# desciption
lbl_frase_1 = Label(fr_pyanalise_3,config_description_pyan,text='frase 1')
lbl_frase_1.grid(row=1,column=1)

lbl_frase_2 = Label(fr_pyanalise_3,config_description_pyan,text='frase 2')
lbl_frase_2.grid(row=1,column=2)

# entry and testing
ent_py_test_1 = Entry(fr_pyanalise_3,relief=GROOVE,border=3,font=('Sans',15,'bold'))
ent_py_test_1.bind('<KeyRelease>',test_pyanalise)
ent_py_test_1.grid(row=2,column=1)

ent_py_test_2 = Entry(fr_pyanalise_3,relief=GROOVE,border=3,font=('Sans',15,'bold'))
ent_py_test_2.bind('<KeyRelease>',test_pyanalise)
ent_py_test_2.grid(row=2,column=2)

# value testing
result_py_test = Label(fr_pyanalise_4, text='0%',font=('Sans',40,'bold'),fg='blue',bg='#eee')
result_py_test.grid(row=1,column=1,sticky=NSEW)

# ---- TELA DE MUSICA ----
fr_music = Frame(tela,bg='white')
fr_music.grid_columnconfigure(1, weight=1)

fr_music_1 = Frame(fr_music,bg='blue',padx=6)
fr_music_1.grid(row=0,column=1,sticky=NSEW)
fr_music_1.grid_columnconfigure(2,weight=1)

fr_music_2 = Frame(fr_music,bg='white',padx=6)
fr_music_2.grid(row=1,column=1,sticky=NSEW)
fr_music_2.grid_columnconfigure((1,2),weight=1)

fr_music_3 = Frame(fr_music,bg='white',padx=6)
fr_music_3.grid(row=2,column=1,sticky=NSEW)
fr_music_3.grid_columnconfigure((1,2),weight=1)

fr_music_4 = Frame(fr_music,bg='white',padx=6)
fr_music_4.grid(row=3,column=1,sticky=NSEW)
fr_music_4.grid_columnconfigure((1,2),weight=1)

config_btns = {
    'relief':GROOVE,
    'highlightthickness':0,
    'border':0,
    'bg':'blue',
    'activebackground':'blue'}

config_btns_itens = {
    'relief':GROOVE,
    'highlightthickness':0,
    'border':0,
    'bg':'white',
    'activebackground':'white'}

config_btn_description = {
    'font':("Sans",10,'bold'),
    'bg':'white',
    'fg':'#777'}

# main
btn_return_screem = Button(fr_music_1,config_btns,image=img_return)
btn_return_screem['command'] = lambda: troca_tela('musi_opca')
btn_return_screem.grid(row=1,column=1)

lbl_title = Label(fr_music_1, text='TOCAR MÚSICAS',font=("Sans",17,'bold'),bg='blue',fg='white')
lbl_title.grid(row=1,column=2,sticky=NSEW)

lbl_icon = Label(fr_music_1,image=img_music_2,font=("Sans",17,'bold'),bg='blue')
lbl_icon.grid(row=1,column=3)

# description
lbl_file = Label(fr_music_2, config_btn_description, text='musica.mp3')
lbl_file.grid(row=1,column=1,sticky=NSEW)

lbl_comand = Label(fr_music_2, config_btn_description, text='solta o som ; soltando')
lbl_comand.grid(row=1,column=2,sticky=NSEW)

lbl_space = Label(fr_music_2, image=img_transparent,bg='white')
lbl_space.grid(row=1,column=3,sticky=NSEW)

lbl_space = Label(fr_music_2, image=img_transparent,bg='white')
lbl_space.grid(row=1,column=4,sticky=NSEW)

load_itens_musics()

# add new item
ent_new_file_music = Entry(fr_music_4,relief=GROOVE,border=2)
ent_new_file_music.grid(row=1,column=1,sticky=NSEW)

ent_new_comand_music = Entry(fr_music_4,relief=GROOVE,border=2)
ent_new_comand_music.grid(row=1,column=2,sticky=NSEW)

btn_add_music = Button(fr_music_4,config_btns_itens,image=img_add,command=add_item_music)
btn_add_music.grid(row=1,column=3,sticky=NSEW)

btn_new_test_music = Button(fr_music_4,config_btns_itens,text='TESTAR',relief=RAISED,border=1)
btn_new_test_music.grid(row=1,column=4,sticky=NSEW)

tela.mainloop()