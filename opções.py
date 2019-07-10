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
global precisao_minima
precisao_minima = 80
# Definições básicas da tela
tela = Tk() 
# tela.resizable(width=False, height=False)
tela.configure(background="white",border=0)
tela.grid_columnconfigure(1, weight=1)
tela.rowconfigure(1, weight=1)
tela.title('Diana chatbot - Combratec Inova')
tela.geometry("446x546+100+100")

fr_opcoes = Frame(tela)
fr_opcoes.grid_columnconfigure(1, weight=1)
fr_opcoes.rowconfigure(1, weight=1)
fr_opcoes.grid(row=1,column=1,sticky=NSEW)

# Abrir um site
def abrir_site(link):
    import webbrowser
    webbrowser.open(link)

def troca_tela(carregar):
	if carregar=='opca_hist':
		fr_opcoes.grid_forget()
		fr_h.grid(row=1,column=1,sticky=NSEW)

	elif carregar=='hist_opca':
		fr_opcoes.grid(row=1,column=1,sticky=NSEW)
		fr_h.grid_forget()

	elif carregar=='opca_pyan':
		fr_opcoes.grid_forget()
		fr_pyanalise.grid(row=1,column=1,sticky=NSEW)

	elif carregar=='pyan_opca':
		fr_pyanalise.grid_forget()
		fr_opcoes.grid(row=1,column=1,sticky=NSEW)



fr1 = Frame(fr_opcoes,bg='blue')
fr1.grid(row=0,column=1,sticky=NSEW)
fr1.grid_columnconfigure(2,weight=1)

fr2 = Frame(fr_opcoes,bg='white')
fr2.grid(row=1,column=1,sticky=NSEW)
fr2.grid_columnconfigure(1,weight=1)
fr2.grid_columnconfigure(2,weight=2)
fr2.grid_columnconfigure(3,weight=1)

conf_btns = {'relief':GROOVE,'highlightthickness':0,'border':0,'bg':'white'}

imagem = PhotoImage(file='Imagens/opcoes/return.png')
imagem = imagem.subsample(3,3)
retornar = Button(fr1,conf_btns,image=imagem,bg='blue',activebackground='blue')
retornar.grid(row=1,column=1)
lbl = Label(fr1, text='OPÇÕES',font=("Sans",17,'bold'),bg='blue',fg='white')
lbl.grid(row=1,column=2,sticky=NSEW)

avance = PhotoImage(file='Imagens/opcoes/avance.png')
avance = avance.subsample(3,3)
musica = PhotoImage(file='Imagens/opcoes/musica.png')
musica = musica.subsample(3,3)
lbl = Label(fr2,image=musica,bg='white')
lbl.grid(row=1,column=1)
lbl = Label(fr2,text='Tocar musica',font=("Sans",17,'bold'),bg='white')
lbl.grid(row=1,column=2,sticky=NSEW) 
btn_musica = Button(fr2,conf_btns,image=avance)
btn_musica.grid(row=1,column=3,sticky=NSEW) 

pyanalise_img = PhotoImage(file='Imagens/opcoes/pyanalise.png')
pyanalise_img = pyanalise_img.subsample(3,3)
lbl = Label(fr2,image=pyanalise_img,bg='white')
lbl.grid(row=2,column=1)
lbl = Label(fr2,text='Pyanalise',font=("Sans",17,'bold'),bg='white')
lbl.grid(row=2,column=2,sticky=NSEW) 
btn_pyanalise = Button(fr2,conf_btns,image=avance)
btn_pyanalise['command'] = lambda: troca_tela('opca_pyan')
btn_pyanalise.grid(row=2,column=3,sticky=NSEW) 

arduino = PhotoImage(file='Imagens/opcoes/arduino.png')
arduino = arduino.subsample(3,3)
lbl = Label(fr2,image=arduino,bg='white')
lbl.grid(row=3,column=1)
lbl = Label(fr2,text='Comandos',font=("Sans",17,'bold'),bg='white')
lbl.grid(row=3,column=2,sticky=NSEW) 
btn_arduino = Button(fr2,conf_btns,image=avance)
btn_arduino.grid(row=3,column=3,sticky=NSEW) 

historico = PhotoImage(file='Imagens/opcoes/historico.png')
historico = historico.subsample(3,3)
lbl = Label(fr2,image=historico,bg='white')
lbl.grid(row=4,column=1)
lbl = Label(fr2,text='Histórico',font=("Sans",17,'bold'),bg='white')
lbl.grid(row=4,column=2,sticky=NSEW) 
btn_historico = Button(fr2,conf_btns,image=avance)
btn_historico['command'] = lambda: troca_tela('opca_hist')
btn_historico.grid(row=4,column=3,sticky=NSEW) 

github = PhotoImage(file='Imagens/opcoes/github.png')
github = github.subsample(3,3)
lbl = Label(fr2,image=github,bg='white')
lbl.grid(row=5,column=1)
lbl = Label(fr2,text='Nosso repositório!',font=("Sans",17,'bold'),bg='white')
lbl.grid(row=5,column=2,sticky=NSEW) 
btn_github = Button(fr2,conf_btns,image=avance)
btn_github['comman'] = lambda: abrir_site('https://github.com/Combratec/Diana')
btn_github.grid(row=5,column=3,sticky=NSEW) 

sobre = PhotoImage(file='Imagens/opcoes/sobre.png')
sobre = sobre.subsample(3,3)
lbl = Label(fr2,image=sobre,bg='white')
lbl.grid(row=6,column=1)
lbl = Label(fr2,text='Sobre este projeto!',font=("Sans",17,'bold'),bg='white')
lbl.grid(row=6,column=2,sticky=NSEW) 
btn_sobre = Button(fr2,conf_btns,image=avance)
btn_sobre['comman'] = lambda: abrir_site('https://dianachatbot.blogspot.com/2019/02/dianachatbotcombratec.html')
btn_sobre.grid(row=6,column=3,sticky=NSEW) 

# ---- TELA DO HISTÓRICO ----
fr_h = Frame(tela,background='white')
fr_h.grid_columnconfigure(1,weight=1)
fr_h.rowconfigure(3,weight=1)

fr_s_h = Frame(fr_h,background="red")
fr_s_h.grid_columnconfigure((1,2), weight=1)
fr_s_h.grid(row=2,column=1,sticky=NSEW)

fr_c_h = Frame(fr_h)
fr_c_h.grid_columnconfigure(1,weight=1)
fr_c_h.rowconfigure(1,weight=1)
fr_c_h.grid(row=3,column=1,sticky=NSEW)

fr_i_h = Frame(fr_h,background="black")
fr_i_h.grid_columnconfigure((1,2),weight=1) 
fr_i_h.grid(row=4,column=1,sticky=NSEW)

cfg_hi = {'background':'#00cccb',
    'highlightbackground':'#00cccb',
    'foreground':'#222',
    'font':("",14)}

# ---- FRAME SUPERIOR ----
lbl = Label(fr_h,text="Histórico",background='#1976d3',font=("Sans",17,'bold'),highlightbackground="#1976d3", foreground='#fff')
lbl.grid(row=1,column=1,sticky=EW)

lbl = Label(fr_s_h,cfg_hi,text="historico")
lbl.grid(row=1,column=1,sticky=NSEW)

lbl= Label(fr_s_h,cfg_hi,text="Aprendizados")
lbl.grid(row=1,column=2,sticky=NSEW)

# ---- FRAME CENTRAL ----
text_h = Text(fr_c_h,background='white', highlightbackground='#fff', border=2,foreground='black',font=("consolas", 12), undo=True, wrap='word')
text_h.insert(1.0, 'Não há nada aqui!')
text_h.grid(row=1,column=1,sticky=NSEW)

scl_h = Scrollbar(fr_c_h, command=text_h.yview,background='white', activebackground="#f9f9f9", highlightbackground="white", highlightcolor="white")
scl_h.grid(row=1,column=2,sticky=NS)
text_h['yscrollcommand'] = scl_h.set

# ---- FRAME INFERIOR ----
btn_retorna_h = Button(fr_i_h,text="Voltar",background='#009899', foreground='white', activebackground='#009899', activeforeground="#fff", highlightbackground='#009899', relief=FLAT, font=("Arial",12))
btn_retorna_h['command'] = lambda: troca_tela('hist_opca')
btn_retorna_h.grid(row=1, column=1,sticky=EW)

btn_limpa_h = Button(fr_i_h,text="Limpar histórico",background='#fe0000', foreground='white', activebackground="#fe0000", activeforeground="#fff", highlightbackground="#fe0000", relief=FLAT, font=("Arial",12))
btn_limpa_h.grid(row=1, column=2,sticky=EW)






# ---- TELA DO PyANALISE ----
import time
from pyanalise import compare

# Abrir um site
def abrir_site(link):
    import webbrowser
    webbrowser.open(link)

def resize(event=None):
	global precisao_minima
	precisao_minima = scl_pyanalise.get()
	print(precisao_minima)

def chamar(event):
	global precisao_minima
	py_entry_1.update()
	busca_semelhanca = compare.frase(py_entry_1.get(),py_entry_2.get())
	resultado['text'] = str(busca_semelhanca)+str('%')
	if busca_semelhanca < precisao_minima:
		resultado['fg'] = 'red'
	else:
		resultado['fg'] = 'blue'

fr_pyanalise = Frame(tela)
fr_pyanalise.grid_columnconfigure(1, weight=1)
fr_pyanalise.rowconfigure(3, weight=1)

fr1_py = Frame(fr_pyanalise,bg='DarkGreen')
fr1_py.grid_columnconfigure(2,weight=1)
fr1_py.grid(row=0,column=1,sticky=NSEW)

fr2_py = Frame(fr_pyanalise,bg='green')
fr2_py.grid_columnconfigure(1,weight=1)
fr2_py.grid(row=1,column=1,sticky=NSEW)

fr3_py = Frame(fr_pyanalise,bg='white',pady=10)
fr3_py.grid_columnconfigure((1,2),weight=1)
fr3_py.grid(row=2,column=1,sticky=NSEW)

fr4_py = Frame(fr_pyanalise,bg='white')
fr4_py.grid_columnconfigure(1,weight=1)
fr4_py.rowconfigure(1,weight=1)
fr4_py.grid(row=3,column=1,sticky=NSEW)

conf_btns = {'relief':GROOVE,'highlightthickness':0,'border':0,'bg':'white'}

pyanalise = PhotoImage(file='Imagens/opcoes/github_branco.png')
pyanalise = pyanalise.subsample(16,16)

# ---- PARTE SUPERIOR ----
retornar = Button(fr1_py,conf_btns,image=imagem,bg='DarkGreen',activebackground='DarkGreen')
retornar['command'] = lambda: troca_tela('pyan_opca')
retornar.grid(row=1,column=1)

lbl = Label(fr1_py, text='pyanalise',font=("Sans",17,'bold'),bg='DarkGreen',fg='white')
lbl.grid(row=1,column=2,sticky=NSEW)

btn_pya = Button(fr1_py,conf_btns,image=pyanalise,bg='DarkGreen',activebackground='DarkGreen')
btn_pya['comman'] = lambda: abrir_site('https://github.com/gabrielogregorio/pyanalise')
btn_pya.grid(row=1,column=3,sticky=NSEW)

# ---- DESCRIÇÃO E VARIAÇÃO ----
lbl = Label(fr2_py,text='Taxa de variação do PyAnalise',font=("Sans",10,'bold'),bg='green',fg='white')
lbl.grid(row=1,column=1,sticky=NSEW)

scl_pyanalise = Scale(fr2_py,from_=1, to=100, orient=HORIZONTAL,command=resize,highlightbackground='white',troughcolor='green',bd=1,bg='green',fg='white',highlightthickness=0)
scl_pyanalise.set(precisao_minima)
scl_pyanalise.grid(row=2,column=1,sticky=NSEW)

# ---- TESTE ----
lbl = Label(fr3_py,text='frase 1',font=("Sans",10,'bold'),bg='white',fg='black')
lbl.grid(row=1,column=1)

lbl = Label(fr3_py,text='frase 2',font=("Sans",10,'bold'),bg='white',fg='black')
lbl.grid(row=1,column=2)

py_entry_1 = Entry(fr3_py,relief=GROOVE,border=3,font=('Sans',15,'bold'))
py_entry_1.bind('<KeyRelease>',chamar)
py_entry_1.grid(row=2,column=1)

py_entry_2 = Entry(fr3_py,relief=GROOVE,border=3,font=('Sans',15,'bold'))
py_entry_2.bind('<KeyRelease>',chamar)
py_entry_2.grid(row=2,column=2)

# ---- RESULTADO ----
resultado = Label(fr4_py, text='0%',font=('Sans',40,'bold'),fg='blue',bg='#eee')
resultado.grid(row=1,column=1,sticky=NSEW)


tela.mainloop()