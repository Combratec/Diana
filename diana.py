#!/usr/bin/python3
# -*- coding: utf-8 -*-
from arduino_code import comand_arduino
from processamento import analise
from processamento import analise_comandos
from definicoes import comandar
from tkinter import messagebox
from definicoes import musica
from pyanalise import compare
from definicoes import basic
from tkinter import *
import alternativa
import time
import os


global save_comand_object_position
global save_music_object_position
global control_thread_listen
global control_thread_espeak
global perguntado_antes
global tenho_que_falar
global precisao_minima
global nome_usuario
global link_serial
global nome_bot
global tocando
global fazer
global placa
global lista
global texto
global mixer

save_comand_object_position = []
save_music_object_position = []
control_thread_listen = False
control_thread_espeak = False
perguntado_antes = 'nada'
tenho_que_falar = basic.ler_tenho_que_falar()
precisao_minima = basic.ler_pyanalise()
nome_usuario = 'você_: '
link_serial =  basic.ler_link_serial()
nome_bot = 'diana: '
tocando = False
fazer = 'nada'
placa = None
lista = []
texto = '__'

tela = Tk() 
tela.resizable(width=False, height=False)
tela.configure(background="white",border=0)
tela.grid_columnconfigure(1, weight=1)
tela.rowconfigure(1, weight=1)
tela.title('Diana chatbot - Combratec Inova')
tela.geometry("446x546+100+100")

# LOGICA DO SISTEMA
def processamento(pergunta):
    global precisao_minima
    global lista
    global fazer

    if fazer == 'nada':
        lista = analise_comandos(pergunta,'arquivos/comandos/arduino.txt')
        if precisao_minima < lista[0]:
            lista.append('é_comando')
            return '__comando_responder__'

    if fazer == 'nada':
        lista = analise_comandos(pergunta,'arquivos/comandos/musica.txt')
        if precisao_minima < lista[0]:
            lista.append('é_musica')
            return '__comando_responder__'

    lista = analise(pergunta)
    if precisao_minima > lista[0]:
        return '__criar_assunto__'
    else:
        if lista[3] == 1:
            return '__responder__'
        else:
            return '__continuar_assunto__'

def responder():
    global lista
    global fazer
    resp = basic.abrir_arquivo("arquivos/conteudo/{}".format(lista[1]))
    resp = resp.split(';')
    resposta = str(resp[ lista[2] + 1])
    resposta = resposta.rstrip().lstrip()
    fazer = 'nada'
    return str(resposta  + '\n')

def continuar_assunto(digitado):
    global lista
    global nome_bot
    global nome_usuario
    global fazer
    global tenho_que_falar

    texto = ';' + digitado
    rota = 'arquivos/conteudo/' + digitado

    arquivo = open (rota,'a', encoding="utf8")
    arquivo.write(texto)
    arquivo.close()

    texto_add = str((nome_bot + "Aprendido\n"))
    add_item_historic(texto_add)
    txt_intera.insert(END, texto_add)
    if tenho_que_falar == 'sim':
        falar.rec_thread('Aprendido')
    fazer = 'nada'

def criar_assunto(perguntado,digitado):
    basic.log('_criar_assunto')
    global lista
    global nome_bot
    global nome_usuario
    global fazer
    global tenho_que_falar

    entrada_add = digitado

    texto_add = str((nome_bot + "Entendido\n"))
    add_item_historic(texto_add)
    txt_intera.insert(END, texto_add)

    if tenho_que_falar == 'sim':
        falar.rec_thread('Entendido')

    x = 0
    while True:
        try:
            arquivo = basic.abrir_arquivo('arquivos/conteudo/{}{}'.format(x,'.txt'))
        except:
            arquivo = open ('arquivos/conteudo/'+str(x)+'.txt','w', encoding="utf8")
            arquivo.write(str(perguntado)+';'+str(entrada_add))
            arquivo.close()
            break

        x = x + 1
    fazer = 'nada'

def controlador_de_partes(digitado):
    global fazer
    global lista
    global perguntado_antes
    global tenho_que_falar
    global nome_bot

    ent_intera.delete(0, 'end')
    tela.update()

    if digitado.isspace() == True or ';' in digitado:
        messagebox.showinfo('OPS','Dados inválidos foram enviados. Espaços e ; não são permitidos!')
    elif '[ERRO]' in digitado:
        messagebox.showinfo('Problema ',digitado)
    else:
        texto_add = 'VOCÊ: ' + digitado + '\n'
        add_item_historic(texto_add)
        txt_intera.insert(END, texto_add)

        tela.update()
        if fazer == 'nada':
            fazer = processamento(digitado)
            if fazer == '__responder__':
                resposta_diana = responder()
                
                texto_add = nome_bot + resposta_diana
                add_item_historic(texto_add)
                txt_intera.insert(END, texto_add)

                if tenho_que_falar == 'sim':
                    falar.rec_thread(resposta_diana)
            elif fazer == '__comando_responder__':
                texto_add = nome_bot + lista[1] + '\n'
                add_item_historic(texto_add)
                txt_intera.insert(END, texto_add)
                fazer = 'nada'

                o_que_responder = lista[1]
                o_que_era = lista[2]

                if lista[3] == 'é_musica':
                    file = basic.abrir_arquivo('musica/arquivo')
                    file = file.split('\n')
                    for x in file:
                        x = x.split(':')
                        if x[3] == o_que_era+';'+o_que_responder:
                            play_music(x[1])
                            break


                elif lista[3] == 'é_comando':
                    file = basic.abrir_arquivo('comandos/arquivo')
                    file = file.split('\n')
                    for x in file:
                        x = x.split(':')
                        if x[3] == o_que_era+';'+o_que_responder:
                            use_serial(x[1])
                            break
            else:
                alternativa_resposta = alternativa.pergunta(digitado)
                if tenho_que_falar == 'sim':
                    falar.rec_thread(alternativa_resposta)
                texto_add = str((nome_bot + alternativa_resposta + '\n'))
                add_item_historic(texto_add)
                txt_intera.insert(END, texto_add)

        elif fazer == '__continuar_assunto__':
            continuar_assunto(digitado)

        elif fazer == '__criar_assunto__':
            criar_assunto(perguntado_antes,digitado)
        perguntado_antes = digitado
    txt_intera.see("end")

# INTERFACE PRINCIPAL
def status_falar_ou_nao(parametro):
    global tenho_que_falar
    if parametro == 'ler':
        if tenho_que_falar == 'sim':
            imagem = PhotoImage(file='Imagens/reconhece_escreve/icon_speak.png')
        else:
            imagem = PhotoImage(file='Imagens/reconhece_escreve/icon_speak_rev.png')
    elif parametro == 'trocar':
        if tenho_que_falar == 'sim':
            tenho_que_falar = 'nao'
            imagem = PhotoImage(file='Imagens/reconhece_escreve/icon_speak_rev.png')
        else:
            tenho_que_falar = 'sim'
            imagem = PhotoImage(file='Imagens/reconhece_escreve/icon_speak.png')
    imagem = imagem.subsample(16,16)
    status_som['image'] = imagem
    status_som.image = imagem

    basic.atualizar_tenho_que_falar(tenho_que_falar)

# PROCESSAMENTO DA FALA
class falar ():
    def rec_thread(texto_fala):
        global control_thread_espeak
        import speech_recognition as sr

        if control_thread_espeak == True:
            basic.log('já existe um thread sendo usado para processar a fala')
        else:
            try:
                import threading
                tts_thread = threading.Thread(target = falar.resp_speak, args=[texto_fala])
                tts_thread.start()
            except Exception as e:
                basic.log('Erro ao criar thread para a fala.\n'+str(e))
            else:
                control_thread_espeak = True

    def resp_speak(texto_fala):
        global control_thread_espeak

        try:
            from gtts import gTTS
            from pygame import mixer
        except Exception as e:
            messagebox.showinfo('ERRO_1',e)
        else:
            try:
                tts = gTTS(text=texto_fala, lang='pt-br')
                tts.save('audio.mp3')
                mixer.init() 
                mixer.music.load('audio.mp3')
                mixer.music.play()

            except Exception as er:
                basic.log('erro ao carregar e reproduzir audio. \n'+str(er))
                messagebox.showinfo('ERRO_2',er)
            else:
                basic.log('fala finalizada')
        finally:
            control_thread_espeak = False

        try:
            basic.log('deletando arquivo residual')
            os.remove('audio.mp3')
        except Exception as er2:
            basic.log('impossivel deletar o arquivo residual. \n'+str(er2))

# RECONHECIMENTO DE VOZ
class ouvir():
    def agora():
        global texto
        global control_thread_listen

        if control_thread_listen == True:
            messagebox.showinfo('Já existe um Thread sendo usado para reconhecimento de fala!')
        else:
            btn_recogn['state'] = 'disabled'
            tela.update()

            m = sr.Microphone()
            r = sr.Recognizer()

            basic.log('diga alguma coisa: ')

            with m as source:
                r.adjust_for_ambient_noise(source,duration=0.5)

            stop_listening = r.listen_in_background(m, ouvir.callback)

            btn_recogn.update()
            tela.update()

            while control_thread_listen == False:
                tela.update()
                time.sleep(0.3)
            control_thread_listen = False

            stop_listening(wait_for_stop=False)
            print('Parei de ouvir!')

            btn_recogn['state'] = 'normal'
            btn_recogn.update()
            return texto

    def callback(recognizer, audio):
        global control_thread_listen
        global texto

        try:
            rec =  recognizer.recognize_google(audio,language='pt-BR')
            texto = str(rec)
        except sr.UnknownValueError as e1:
            texto = "[ERRO] Eu não consegui entender nada!"+str(e1)
        except sr.RequestError as e2:
            texto = "[ERRO] parece que você tem um Problema com a internet! {}"+str(e2)
        except Exception as e3:
            texto = '[ERRO] ERRO DESCONHECIDO: '+str(e3)
        else:
            basic.log('reconhecimento de fala finalizado com sucesso')
        finally:
            control_thread_listen = True
            basic.log(texto)

# INTERFACE HISTÓRICO
def limpar_historico():
    basic.clear_historic()
    atualizar_historico()

def atualizar_historico():
    text_historics.delete(1.0, END)
    text_historics.insert(1.0,basic.load_historic())
    text_historics.see("end")

def add_item_historic(interacao):
    basic.add_historic(interacao)

# INTERFACE PYANALISE
def resize(event=None):
    global precisao_minima
    basic.atualizar_pyanalise(scale_pyanalise.get())
    precisao_minima = basic.ler_pyanalise()

def testar_pyanalise(event):
    global precisao_minima

    ent_py_test_1.update()
    busca_semelhanca = compare.frase(ent_py_test_1.get(),ent_py_test_2.get())
    result_py_test['text'] = str(busca_semelhanca)+str('%')

    if busca_semelhanca < precisao_minima:
        result_py_test['fg'] = 'red'
    else:
        result_py_test['fg'] = 'blue'

# INTEFACE MUSICA
def load_itens_musics():
    global save_music_object_position
    global music_itens

    for list_objects in save_music_object_position:
        for especifc_objets in list_objects:
            especifc_objets.grid_forget()

    save_music_object_position = []
    music_itens = musica.read_musics_in_file()
    dic_load_entry = {'relief':GROOVE,'border':2}

    basic.make_file_responses_music()
    for x in range(len(music_itens)):
        ent_load_file_music = Entry(fr_music_3 , dic_load_entry)
        ent_load_comm_music = Entry(fr_music_3 , dic_load_entry)
        btn_remove_music_it = Button(fr_music_3,config_btns_itens,image=img_remove)
        btn_load_test_music = Button(fr_music_3,config_btns_itens,text='TESTAR',relief=RAISED,border=1)

        btn_remove_music_it['command'] = lambda btn_remove_music_it=btn_remove_music_it: remove_item_music(btn_remove_music_it)
        btn_load_test_music['command'] = lambda btn_load_test_music=btn_load_test_music: set_music_play(btn_load_test_music)

        delete_insert_entry(ent_load_file_music,music_itens[x]['musica'])
        delete_insert_entry(ent_load_comm_music,music_itens[x]['comando'])

        ent_load_file_music.grid(row=x,column=1,sticky=NSEW)
        ent_load_comm_music.grid(row=x,column=2,sticky=NSEW)
        btn_remove_music_it.grid(row=x,column=3,sticky=NSEW)
        btn_load_test_music.grid(row=x,column=4,sticky=NSEW)

        new_list_itens = [ ent_load_file_music , ent_load_comm_music , btn_remove_music_it , btn_load_test_music ]
        save_music_object_position.append(new_list_itens) 

def remove_item_music(btn):
    global save_music_object_position
    total = len(save_music_object_position)
    for x in range(total):
        if save_music_object_position[x][2] == btn:
            musica.remover(x)
            load_itens_musics()
            break

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

def set_music_play(btn):
    global save_music_object_position
    for y in save_music_object_position:
        if y[3] == btn:
            play_music(y[0].get())

def play_music(link):
    global tocando
    global mixer
    if tocando == False:
        try:
            from pygame import mixer
        except Exception as e:
            messagebox.showinfo('ERRO','Por favor, instale a biblioteca pygame com o comando: \npip install pygame\nerro: '+str(e))
        else:
            try:
                mixer.init() 
                mixer.music.load('musica/'+link)
                mixer.music.play()
            except Exception as er:
                messagebox.showinfo('ERRO',er)
            else:
                tocando = True
    else:
        try:
            mixer.music.pause()
            tocando = False
        except Exception as e:
            messagebox.showinfo('ERRP',e)

# INTERFACE COMANDO com arduino
def load_itens_comand():
    global save_comand_object_position
    global itens

    for y in save_comand_object_position:
        y[0].grid_forget()
        y[1].grid_forget()
        y[2].grid_forget()
        y[3].grid_forget()

    save_comand_object_position = []
    itens = comandar.read_comands_in_file()
    basic.make_file_responses_comands()

    for x in range(len(itens)):
        ent_send_comand = Entry(fr_comand_4,relief=GROOVE,border=2)
        ent_comand_resp = Entry(fr_comand_4,relief=GROOVE,border=2)
        btn_remove_item = Button(fr_comand_4,conf_btns_item,image=img_remove)
        btn_test_serial = Button(fr_comand_4,conf_btns_item,text='TESTAR',relief=RAISED,border=1,padx=1)

        btn_remove_item['command'] = lambda btn_remove_item=btn_remove_item: remove_comand_itens(btn_remove_item)
        btn_test_serial['command'] = lambda btn_test_serial=btn_test_serial: acess_serial(btn_test_serial)

        delete_insert_entry(ent_send_comand,itens[x]['enviar'])
        delete_insert_entry(ent_comand_resp,itens[x]['comando'])

        ent_send_comand.grid(row=x,column=1,sticky=NSEW)
        ent_comand_resp.grid(row=x,column=2,sticky=NSEW)
        btn_remove_item.grid(row=x,column=3,sticky=NSEW)
        btn_test_serial.grid(row=x,column=4,sticky=NSEW)

        save_comand_object_position.append([ent_send_comand,ent_comand_resp,btn_remove_item,btn_test_serial]) 

def remove_comand_itens(btn):
    global save_comand_object_position
    total = len(save_comand_object_position)
    for x in range(total):
        if save_comand_object_position[x][2] == btn:
            comandar.remover(x)
            load_itens_comand()
            break

def add_comand_itens():
    basic.log('_add_comand_itens')
    a = ent_comand_add_send.get() 
    b = ent_comand_add_comand.get()
    if  a == '' or  b =='' or a.isspace() or b.isspace() or not ';' in b or ':' in b or ':' in a:
        messagebox.showinfo('ops','Caracteres inválidos detectado!')
    else:
        global itens
        comandar.adicionar({'enviar': ent_comand_add_send.get(), 'comando': ent_comand_add_comand.get()})

        load_itens_comand()
        ent_comand_add_send.delete(0,END)
        ent_comand_add_comand.delete(0,END)

def acess_serial(btn_test_serial):
    global save_comand_object_position
    for y in save_comand_object_position:
        if y[3] == btn_test_serial:
            test_use_serial(y[0].get(),btn_test_serial)

def use_serial(send_message_for_serial):
    global placa
    if placa == None:
        try:
            placa = comand_arduino.start_connection(link_serial)
        except:
            messagebox.showinfo('ERRO','Por favor, defina uma serial válida!')
            return 0
    try:
        comand_arduino.message(placa,None,send_message_for_serial,'nao')
    except Exception as e:
        messagebox.showinfo('ERRO!','Problema com esta serial. \n[ERRO] {}'.format(e))

def test_use_serial(send_message_for_serial,btn_test_serial):
    global placa

    if send_message_for_serial != None:
        try:
            comand_arduino.message(placa,None,send_message_for_serial,'nao')
        except Exception as e:
            messagebox.showinfo('ERRO!','Problema com esta serial. \n[ERRO] {}'.format(e))
            btn_test_serial.configure(bg='red',fg='white') 
            ent_serial_for_test['fg'] = 'red'
        else:
            btn_test_serial.configure(bg='green',fg='white') 
            ent_serial_for_test['fg'] = 'green'
    else:
        try:
            placa = comand_arduino.start_connection(ent_serial_for_test.get())
        except Exception as e:
            basic.log('serial ignorada!')
            messagebox.showinfo('ERRO!','Problema com esta serial. \n[ERRO] {}'.format(e))
            btn_test_serial.configure(bg='red',fg='white') 
            ent_serial_for_test['fg'] = 'red'
        else:
            basic.atualizar_link_serial(ent_serial_for_test.get())
            basic.log('serial salva!')
            btn_test_serial.configure(bg='green',fg='white') 
            ent_serial_for_test['fg'] = 'green'

# GERAIS
def delete_insert_entry(entry_name,insert_entry_name):
    entry_name.delete(0,END)
    entry_name.insert(0,insert_entry_name)

# TROCA DE INTERFACES
def troca_tela(carregar):
    if carregar == 'conf_inte':
        tela_frame_configuracoes.grid_forget()
        interacao.grid(row=1,column=1,sticky=NSEW)

    elif carregar == 'inte_conf':
        interacao.grid_forget()
        tela_frame_configuracoes.grid(row=1,column=1,sticky=NSEW)

    elif carregar=='opca_hist':
        fr_options.grid_forget()
        fr_historic.grid(row=1,column=1,sticky=NSEW)
        atualizar_historico()

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

    elif carregar=='opca_coma':
        fr_options.grid_forget()
        fr_comand.grid(row=1,column=1,sticky=NSEW)

    elif carregar=='coma_opca':
        fr_comand.grid_forget()
        fr_options.grid(row=1,column=1,sticky=NSEW)

    elif carregar=='inte_opti':
        interacao.grid_forget()
        fr_options.grid(row=1,column=1,sticky=NSEW)

    elif carregar=='opti_inte':
        fr_options.grid_forget()
        interacao.grid(row=1,column=1,sticky=NSEW)

# CARREGAMENTO DE IMAGENS
img_transparent  =  PhotoImage(file='Imagens/opcoes/transparent.png')
img_pyanalise    =  PhotoImage(file='Imagens/opcoes/pyanalise.png')
img_arduino_2    =  PhotoImage(file='Imagens/opcoes/arduino.png')
img_historic     =  PhotoImage(file='Imagens/opcoes/historico.png')
img_github_py    =  PhotoImage(file='Imagens/opcoes/github_branco.png')
img_continue     =  PhotoImage(file='Imagens/opcoes/avance.png')
icon_config      =  PhotoImage(file="Imagens/reconhece_escreve/icon_config.png")
img_music_2      =  PhotoImage(file='Imagens/opcoes/musica.png')
img_arduino      =  PhotoImage(file='Imagens/opcoes/arduino.png')
img_github       =  PhotoImage(file='Imagens/opcoes/github.png')
img_return       =  PhotoImage(file='Imagens/opcoes/return.png')
icon_speak       =  PhotoImage(file="Imagens/reconhece_escreve/icon_speak.png")
img_music        =  PhotoImage(file='Imagens/opcoes/musica.png')
img_about        =  PhotoImage(file='Imagens/opcoes/sobre.png')
img_remove       =  PhotoImage(file='Imagens/opcoes/remove.png')
icon_git         =  PhotoImage(file="Imagens/reconhece_escreve/icon_return_b.png")
img_edit         =  PhotoImage(file='Imagens/opcoes/edit.png')
icon_mic         =  PhotoImage(file="Imagens/reconhece_escreve/icon_mic.png")    
img_add          =  PhotoImage(file='Imagens/opcoes/add.png')

# REDIMENSIONAMENTO DE IMAGENS
img_transparent  =  img_transparent.subsample(3,3)
img_pyanalise    =  img_pyanalise.subsample(2,2)
img_arduino_2    =  img_arduino_2.subsample(2,2)
img_historic     =  img_historic.subsample(2,2)
img_github_py    =  img_github_py.subsample(16,16)
img_continue     =  img_continue.subsample(2,2)
icon_config      =  icon_config.subsample(16,16)
img_music_2      =  img_music_2.subsample(3,3)
img_arduino      =  img_arduino.subsample(2,2)
img_github       =  img_github.subsample(2,2)
img_return       =  img_return.subsample(3,3)
icon_speak       =  icon_speak.subsample(16,16)
img_music        =  img_music.subsample(2,2)
img_about        =  img_about.subsample(2,2)
img_remove       =  img_remove.subsample(3,3)
icon_git         =  icon_git.subsample(16,16)
img_edit         =  img_edit.subsample(3,3)
icon_mic         =  icon_mic.subsample(16,16)
img_add          =  img_add.subsample(3,3)

# ---- TELA PRINCIAL ----
interacao = Frame(tela)
interacao.grid_columnconfigure(2,weight=1)
interacao.rowconfigure(2,weight=1)
interacao.grid(row=1,column=1,sticky=NSEW)

config_btn = {
    'highlightbackground':'blue',
    'border':0,
    'bg':'blue',
    'relief':SUNKEN,
    'activebackground':'blue'
    ,'highlightthickness':0}

config_entry = {
    'fg':'white',
    'bg':'blue',
    'highlightbackground':'white',
    'highlightcolor':'white',
    'font':("",14)}

btn_github = Button(interacao,config_btn,image = icon_git)
lbl_titulo = Label(interacao,text="DIANA 8",bg='blue',fg='white',font=("Arial",20,'bold'))
btn_config = Button(interacao , config_btn , image = icon_config)
txt_intera = Text(interacao,bg='white',fg='black',highlightthickness=0,border=0,font=("consolas", 12), undo=True, wrap='word')
status_som = Button(interacao , config_btn)
ent_intera = Entry(interacao,config_entry) 
btn_recogn = Button(interacao,config_btn,image = icon_mic)

status_falar_ou_nao('ler')

ent_intera.bind("<Return>", (lambda event: controlador_de_partes(ent_intera.get())))
status_som['command'] = lambda: status_falar_ou_nao('trocar')
btn_recogn['command'] = lambda: controlador_de_partes(ouvir.agora())
btn_github['command'] = lambda: basic.abrir_site('https://github.com/Combratec/Diana')
btn_config['command'] = lambda: troca_tela('inte_opti')

btn_github.grid(row=1,column=1,sticky=NSEW)
lbl_titulo.grid(row=1,column=2,sticky=NSEW)
btn_config.grid(row=1,column=3,sticky=NSEW)
txt_intera.grid(row=2,column=1,columnspan=3,sticky=NSEW)
status_som.grid(row=3,column=1)
ent_intera.grid(row=3,column=2,sticky=NSEW)
btn_recogn.grid(row=3,column=3)

# ---- TELA DE OPÇÕES ----
conf_btns = {
    'relief':GROOVE,
    'highlightthickness':0,
    'border':0,
    'bg':'white'}

fr_options = Frame(tela)
fr_options_1 = Frame(fr_options,bg='blue')
fr_options_2 = Frame(fr_options,bg='white')

fr_options.grid_columnconfigure(1, weight=1)
fr_options.rowconfigure(1, weight=1)
fr_options_1.grid_columnconfigure(2,weight=1)
fr_options_2.grid_columnconfigure((1,2),weight=1)
fr_options_2.grid_columnconfigure(2,weight=2)

fr_options_1.grid(row=0,column=1,sticky=NSEW)
fr_options_2.grid(row=1,column=1,sticky=NSEW)

retornar = Button(fr_options_1,conf_btns,image=img_return,bg='blue',activebackground='blue')
retornar['command'] = lambda: troca_tela('opti_inte')
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
btn_arduino['command'] = lambda: troca_tela('opca_coma')
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
btn_github['comman'] = lambda: basic.abrir_site('https://github.com/Combratec/Diana')
btn_github.grid(row=5,column=3,sticky=NSEW) 

lbl = Label(fr_options_2,image=img_about,bg='white')
lbl.grid(row=6,column=1)
lbl = Label(fr_options_2,text='Sobre este projeto!',font=("Sans",20,'bold'),bg='white')
lbl.grid(row=6,column=2,sticky=NSEW) 
btn_sobre = Button(fr_options_2,conf_btns,image=img_continue)
btn_sobre['comman'] = lambda: basic.abrir_site('https://dianachatbot.blogspot.com/2019/02/dianachatbotcombratec.html')
btn_sobre.grid(row=6,column=3,sticky=NSEW) 

# ---- TELA DO HISTÓRICO ----
lbl_dic_config = {
    'background':'#00cccb',
    'highlightbackground':'#00cccb',
    'foreground':'#222',
    'font':("",14)}

fr_historic = Frame(tela,background='white')
fra_historic_1 = Frame(fr_historic,background="red")
fra_historic_2 = Frame(fr_historic)
fra_historic_3 = Frame(fr_historic,background="black")

fr_historic.rowconfigure(3,weight=1)
fr_historic.grid_columnconfigure(1,weight=1)
fra_historic_1.grid_columnconfigure((1,2), weight=1)
fra_historic_2.grid_columnconfigure(1,weight=1)
fra_historic_3.grid_columnconfigure((1,2),weight=1) 
fra_historic_2.rowconfigure(1,weight=1)

lbl_title_hist = Label(fr_historic,text="Histórico",background='#1976d3',font=("Sans",17,'bold'),highlightbackground="#1976d3", foreground='#fff')
lbl_text_histo = Label(fra_historic_1,lbl_dic_config,text="historico")
lbl_text_apren = Label(fra_historic_1,lbl_dic_config,text="Aprendizados")
text_historics = Text(fra_historic_2,background='white', highlightbackground='#fff', border=2,foreground='black',font=("consolas", 12), undo=True, wrap='word')
scrl_historics = Scrollbar(fra_historic_2, command=text_historics.yview,background='white', activebackground="#f9f9f9", highlightbackground="white", highlightcolor="white")
btn_histo_back = Button(fra_historic_3,text="Voltar",background='#009899', foreground='white', activebackground='#009899', activeforeground="#fff", highlightbackground='#009899', relief=FLAT, font=("Arial",12))
btn_clear_hist = Button(fra_historic_3,text="Limpar histórico",background='#fe0000', foreground='white', activebackground="#fe0000", activeforeground="#fff", highlightbackground="#fe0000", relief=FLAT, font=("Arial",12),command=limpar_historico)

btn_histo_back['command'] = lambda: troca_tela('hist_opca')
text_historics['yscrollcommand'] = scrl_historics.set

fra_historic_1.grid(row=2,column=1,sticky=NSEW)
fra_historic_2.grid(row=3,column=1,sticky=NSEW)
fra_historic_3.grid(row=4,column=1,sticky=NSEW)
lbl_title_hist.grid(row=1,column=1,sticky=EW)
lbl_text_histo.grid(row=1,column=1,sticky=NSEW)
lbl_text_apren.grid(row=1,column=2,sticky=NSEW)
text_historics.grid(row=1,column=1,sticky=NSEW)
scrl_historics.grid(row=1,column=2,sticky=NS)
btn_histo_back.grid(row=1, column=1,sticky=EW)
btn_clear_hist.grid(row=1, column=2,sticky=EW)

# ---- TELA DO PYANALISE ----
conf_btns = {
    'relief':GROOVE,
    'highlightthickness':0,
    'border':0,
    'bg':'white'}

config_description_pyan = {
    'font':("Sans",10,'bold'),
    'bg':'white',
    'fg':'black'}

fr_pyanalise = Frame(tela)
fr_pyanalise.grid_columnconfigure(1, weight=1)
fr_pyanalise.rowconfigure(3, weight=1)

fr_pyanalise_1 = Frame(fr_pyanalise,bg='DarkGreen')
fr_pyanalise_2 = Frame(fr_pyanalise,bg='white')
fr_pyanalise_3 = Frame(fr_pyanalise,bg='white',pady=10)
fr_pyanalise_4 = Frame(fr_pyanalise,bg='white')

fr_pyanalise_1.grid_columnconfigure(2,weight=1)
fr_pyanalise_2.grid_columnconfigure(1,weight=1)
fr_pyanalise_3.grid_columnconfigure((1,2),weight=1)
fr_pyanalise_4.grid_columnconfigure(1,weight=1)
fr_pyanalise_4.rowconfigure(1,weight=1)

btn_return = Button(fr_pyanalise_1,conf_btns,image=img_return,bg='DarkGreen',activebackground='DarkGreen')
lbl_title = Label(fr_pyanalise_1, text='pyanalise',font=("Sans",17,'bold'),bg='DarkGreen',fg='white')
btn_github = Button(fr_pyanalise_1,conf_btns,image=img_github_py,bg='DarkGreen',activebackground='DarkGreen')
lbl_descri = Label(fr_pyanalise_2,text='Taxa de variação do PyAnalise',font=("Sans",12,'bold'),bg='green',fg='white')
lbl_frase_1 = Label(fr_pyanalise_3,config_description_pyan,text='frase 1')
lbl_frase_2 = Label(fr_pyanalise_3,config_description_pyan,text='frase 2')
ent_py_test_1 = Entry(fr_pyanalise_3,relief=GROOVE,border=3,font=('Sans',15,'bold'))
scale_pyanalise = Scale(fr_pyanalise_2,from_=1, to=100, orient=HORIZONTAL,command=resize,highlightbackground='white',troughcolor='green',bd=1,bg='green',fg='white',highlightthickness=0)
ent_py_test_2 = Entry(fr_pyanalise_3,relief=GROOVE,border=3,font=('Sans',15,'bold'))
result_py_test = Label(fr_pyanalise_4, text='0%',font=('Sans',40,'bold'),fg='blue',bg='#eee')

btn_return['command'] = lambda: troca_tela('pyan_opca')
btn_github['comman'] = lambda: basic.abrir_site('https://github.com/gabrielogregorio/pyanalise')

scale_pyanalise.set(precisao_minima)
ent_py_test_1.bind('<KeyRelease>',testar_pyanalise)
ent_py_test_2.bind('<KeyRelease>',testar_pyanalise)

fr_pyanalise_1.grid(row=0,column=1,sticky=NSEW)
fr_pyanalise_2.grid(row=1,column=1,sticky=NSEW)
fr_pyanalise_3.grid(row=2,column=1,sticky=NSEW)
fr_pyanalise_4.grid(row=3,column=1,sticky=NSEW)
btn_return.grid(row=1,column=1)
lbl_title.grid(row=1,column=2,sticky=NSEW)
btn_github.grid(row=1,column=3,sticky=NSEW)
lbl_descri.grid(row=1,column=1,sticky=NSEW)
scale_pyanalise.grid(row=2,column=1,sticky=NSEW)
lbl_frase_1.grid(row=1,column=1)
lbl_frase_2.grid(row=1,column=2)
ent_py_test_1.grid(row=2,column=1)
ent_py_test_2.grid(row=2,column=2)
result_py_test.grid(row=1,column=1,sticky=NSEW)

# ---- TELA DE MUSICA ----
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

fr_music = Frame(tela,bg='white')
fr_music_1 = Frame(fr_music,bg='blue',padx=6)
fr_music_2 = Frame(fr_music,bg='white',padx=6)
fr_music_3 = Frame(fr_music,bg='white',padx=6)
fr_music_4 = Frame(fr_music,bg='white',padx=6)

fr_music.grid_columnconfigure(1, weight=1)
fr_music_1.grid_columnconfigure(2,weight=1)
fr_music_2.grid_columnconfigure((1,2),weight=1)
fr_music_3.grid_columnconfigure((1,2),weight=1)
fr_music_4.grid_columnconfigure((1,2),weight=1)

btn_return_screem = Button(fr_music_1,config_btns,image=img_return)
lbl_title = Label(fr_music_1, text='TOCAR MÚSICAS',font=("Sans",17,'bold'),bg='blue',fg='white')
lbl_icon = Label(fr_music_1,image=img_music_2,font=("Sans",17,'bold'),bg='blue')
lbl_file = Label(fr_music_2, config_btn_description, text='musica.mp3')
lbl_comand = Label(fr_music_2, config_btn_description, text='solta o som ; soltando')
lbl_space_1 = Label(fr_music_2, image=img_transparent,bg='white')
lbl_space_2 = Label(fr_music_2, image=img_transparent,bg='white')
ent_new_file_music = Entry(fr_music_4,relief=GROOVE,border=2)
ent_new_comand_music = Entry(fr_music_4,relief=GROOVE,border=2)
btn_add_music = Button(fr_music_4,config_btns_itens,image=img_add,command=add_item_music)
btn_new_test_music = Button(fr_music_4,config_btns_itens,text='TESTAR',relief=RAISED,border=1)

btn_return_screem['command'] = lambda: troca_tela('musi_opca')
btn_new_test_music['command'] = lambda: play_music(ent_new_file_music.get())
load_itens_musics()

fr_music_1.grid(row=0,column=1,sticky=NSEW)
fr_music_2.grid(row=1,column=1,sticky=NSEW)
fr_music_3.grid(row=2,column=1,sticky=NSEW)
fr_music_4.grid(row=3,column=1,sticky=NSEW)
lbl_icon.grid(row=1,column=3)
lbl_file.grid(row=1,column=1,sticky=NSEW)
lbl_comand.grid(row=1,column=2,sticky=NSEW)
lbl_space_1.grid(row=1,column=3,sticky=NSEW)
lbl_space_2.grid(row=1,column=4,sticky=NSEW)
lbl_title.grid(row=1,column=2,sticky=NSEW)
btn_return_screem.grid(row=1,column=1)
ent_new_file_music.grid(row=1,column=1,sticky=NSEW)
ent_new_comand_music.grid(row=1,column=2,sticky=NSEW)
btn_add_music.grid(row=1,column=3,sticky=NSEW)
btn_new_test_music.grid(row=1,column=4,sticky=NSEW)

# ---- TELA DE COMANDO ----
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

fr_comand = Frame(tela,bg='white')
fr_comand_1 = Frame(fr_comand,bg='blue',padx=6)
fr_comand_2 = Frame(fr_comand,bg='white',padx=6)
fr_comand_3 = Frame(fr_comand,bg='white',padx=6)
fr_comand_4 = Frame(fr_comand,bg='white',padx=6)
fr_comand_5 = Frame(fr_comand,bg='white',padx=6)
fr_comand_6 = Frame(fr_comand,bg='white',padx=6)

fr_comand.grid_columnconfigure(1, weight=1)
fr_comand_1.grid_columnconfigure(2,weight=1)
fr_comand_2.grid_columnconfigure((1),weight=1)
fr_comand_3.grid_columnconfigure((1,2),weight=1)
fr_comand_4.grid_columnconfigure((1,2),weight=1)
fr_comand_5.grid_columnconfigure((1,2),weight=1)
fr_comand_6.grid_columnconfigure((1),weight=1)

btn_comand_return_screem = Button(fr_comand_1,conf_btns,image=img_return)
lbl_title = Label(fr_comand_1, text='COMANDE',font=("Sans",17,'bold'),bg='blue',fg='white')
lbl_icon = Label(fr_comand_1,image=img_arduino_2,font=("Sans",17,'bold'),bg='blue')
lbl_descri = Label(fr_comand_2, text='Digite a serial: com4',font=("Sans",10,'bold'),bg='white',fg='black')
ent_serial_for_test = Entry(fr_comand_2,state='normal',relief=GROOVE,border=2)
btn_test_serial_new = Button(fr_comand_2,conf_btns_item,text='TESTAR',relief=RAISED,width=6,border=1,padx=1)
lbl_arduino_1 = Label(fr_comand_3,text='ENVIAR',font=("Sans",10,'bold'),bg='white',fg='black')
lbl_arduino_2 = Label(fr_comand_3,text='COMANDO ; RESPOSTA',font=("Sans",10,'bold'),bg='white',fg='black')
ent_comand_add_send = Entry(fr_comand_5,relief=GROOVE,border=2)
ent_comand_add_comand = Entry(fr_comand_5,relief=GROOVE,border=2)
btn_add = Button(fr_comand_5,conf_btns_item,image=img_add,command=add_comand_itens)
btn_add_test_serial = Button(fr_comand_5,conf_btns_item,text='TESTAR',relief=RAISED,border=1,padx=1)
btn_comand_help = Button(fr_comand_6,text='AJUDA',relief=RAISED,border=4,padx=5,pady=5,bg='purple',fg='white',font=('Sans',13,'bold'),activebackground='purple',activeforeground='white')

load_itens_comand()

ent_serial_for_test.insert(END,link_serial)
btn_test_serial_new['command'] = lambda btn_test_serial_new=btn_test_serial_new:  test_use_serial(None,btn_test_serial_new)
btn_add_test_serial['command'] = lambda btn_add_test_serial=btn_add_test_serial: test_use_serial(ent_comand_add_send.get(),btn_add_test_serial)
btn_comand_help['command'] = lambda: basic.abrir_site('https://dianachatbot.blogspot.com/2019/02/dianachatbotcombratec.html')
btn_comand_return_screem['command'] = lambda: troca_tela('coma_opca')

fr_comand_1.grid(row=0,column=1,sticky=NSEW)
fr_comand_2.grid(row=1,column=1,sticky=NSEW)
fr_comand_3.grid(row=2,column=1,sticky=NSEW)
fr_comand_4.grid(row=3,column=1,sticky=NSEW)
fr_comand_5.grid(row=4,column=1,sticky=NSEW)
fr_comand_6.grid(row=5,column=1,sticky=NSEW)
btn_comand_return_screem.grid(row=1,column=1)
lbl_title.grid(row=1,column=2,sticky=NSEW)
lbl_icon.grid(row=1,column=3)
lbl_descri.grid(row=1,column=1,columnspan=2,sticky=W)
ent_serial_for_test.grid(row=2,column=1,sticky=NSEW)
btn_test_serial_new.grid(row=2,column=2,sticky=NSEW)
lbl_arduino_1.grid(row=1,column=1)
lbl_arduino_2.grid(row=1,column=2)
ent_comand_add_send.grid(row=1,column=1,sticky=NSEW)
ent_comand_add_comand.grid(row=1,column=2,sticky=NSEW)
btn_add.grid(row=1,column=3,sticky=NSEW)
btn_add_test_serial.grid(row=1,column=4,sticky=NSEW)
btn_comand_help.grid(row=2,column=1,sticky=NSEW)

tela.mainloop() 

