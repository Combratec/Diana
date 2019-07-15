#!/usr/bin/python3
# -*- coding: utf-8 -*-
from tkinter import * 
from tkinter import messagebox
from definicoes import comandar
from definicoes import musica
from pyanalise import compare
from arduino_code import comand_arduino
from processamento import analise
import alternativa
import time
import speech_recognition as sr

tela = Tk() 
tela.resizable(width=False, height=False)
tela.configure(background="white",border=0)
tela.grid_columnconfigure(1, weight=1)
tela.rowconfigure(1, weight=1)
tela.title('Diana chatbot - Combratec Inova')
tela.geometry("446x546+100+100")

global fazer
global tenho_que_falar
global precisao_minima
global lista
global perguntado_antes
global save_comand_object_position
global save_music_object_position
global nome_bot
global nome_usuario
global texto
global control_thread_listen
global control_thread_espeak

fazer = 'nada'
tenho_que_falar = 'sim'
precisao_minima = 80
lista = []
perguntado_antes = 'nada'
save_comand_object_position = []
save_music_object_position = []
control_thread_listen = False
control_thread_espeak = False
nome_bot = 'diana: '
nome_usuario = 'você_: '
texto = '__'

def log(message):
    print(message)

def testes_modulos(): 
    log('_testes_modulos')
    lista_modulos = [1,1,1,1,1]
    try: 
        import speechrecognition # 1
    except:
        lista_modulos[0] = 0
    try: 
        import pyanalise # 2
    except:
        lista_modulos[1] = 0
    try: 
        import pyaudio # 3
    except:
        lista_modulos[2] = 0
    try: 
        import playsound # 4
    except:
        lista_modulos[3] = 0
    try: 
        import gtts # 5
    except:
        lista_modulos[4] = 0
    return lista_modulos

def estado_sistemas(opcao):
    log('_estado_sistemas')
    a = open('config.txt',encoding='utf8')
    file = a.read()
    a.close()

    lista = file.split('\n')
    lista_2 = []
    for x in lista:
        lista_2.append(x.split('='))

    if opcao == 'ler':
        return [ int(lista_2[0][1]) , int(lista_2[1][1]) ]

def processamento(pergunta):
    log('_processamento')
    global precisao_minima
    global lista

    # precisão | pos_file | pos_fras | p_frase+1 existe?
    lista = analise(pergunta)

    if precisao_minima > lista[0]:
        return '__criar_assunto__'
    else:
        if lista[3] == 1:
            return '__responder__'
        else:
            return '__continuar_assunto__'

def responder():
    log('_responder')
    global lista
    global fazer

    # precisão | pos_file | pos_fras | p_frase+1 existe?
    rota = "arquivos/conteudo/" + str(lista[1])

    arquivo = open (rota,'r', encoding="utf8")
    resp = str(arquivo.read())
    arquivo.close()

    resp = resp.split(';')
    resposta = str(resp[ lista[2] + 1])
    resposta = resposta.rstrip().lstrip()
    fazer = 'nada'
    return str(resposta  + '\n')

def continuar_assunto(digitado):
    log('__continuar_assunto')
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

    text_interacao.insert(END, str((nome_bot + "Aprendido\n")))
    if tenho_que_falar == 'sim':
        falar.rec_thread('Aprendido')
    fazer = 'nada'

def criar_assunto(perguntado,digitado):
    log('_criar_assunto')
    global lista
    global nome_bot
    global nome_usuario
    global fazer
    global tenho_que_falar

    entrada_add = digitado
    text_interacao.insert(END, str((nome_bot + "Entendido\n")))
    if tenho_que_falar == 'sim':
        falar.rec_thread('Entendido')

    x = 0
    while True:
        try:
            rota = 'arquivos/conteudo/' + str(x) +'.txt'
            arquivo = open (rota,'r')
            arquivo.close()
        except:
            # precisão | pos_file | pos_fras | p_frase+1 existe?
            arquivo = open ('arquivos/conteudo/'+str(x)+'.txt','w', encoding="utf8")
            arquivo.write(str(perguntado)+';'+str(entrada_add))
            arquivo.close()
            break

        x = x + 1

    fazer = 'nada'

def controlador_de_partes(digitado):
    log('_controlador_de_partes')
    global fazer
    global perguntado_antes
    global tenho_que_falar
    global nome_bot

    # limpar a entrada
    entry_interacao.delete(0, 'end')
    tela.update()

    # Testa entradas inválidas
    if digitado.isspace() == True or ';' in digitado:
        messagebox.showinfo('OPS','Dados inválidos foram enviados. Espaços e ; não são permitidos!')

    # Testa Condição de Erros
    elif '[ERRO]' in digitado:
        messagebox.showinfo('Problema ',digitado)

    # Se não houve erros
    else:
        text_interacao.insert(END, 'VOCÊ: ' + digitado + '\n')
        tela.update()

        # Não há nada para fazer ainda
        if fazer == 'nada':
            fazer = processamento(digitado)

            if fazer == '__responder__':
                resposta_diana = responder()
                text_interacao.insert(END, nome_bot + resposta_diana)

                if tenho_que_falar == 'sim':
                    falar.rec_thread(resposta_diana)

            else:
                alternativa_resposta = alternativa.pergunta(digitado)
                if tenho_que_falar == 'sim':
                    falar.rec_thread(alternativa_resposta)
                text_interacao.insert(END, str((nome_bot + alternativa_resposta + '\n')))

        elif fazer == '__continuar_assunto__':
            continuar_assunto(digitado)

        elif fazer == '__criar_assunto__':
            criar_assunto(perguntado_antes,digitado)

        # Salvar ultima entrada válida
        perguntado_antes = digitado

    text_interacao.see("end")

def def_tenho_que_falar():
    log('_def_tenho_que_falar')
    global tenho_que_falar
    if tenho_que_falar == 'sim':
        tenho_que_falar = 'nao'
        imagem = PhotoImage(file='Imagens/reconhece_escreve/icon_speak_rev.png')
    else:
        tenho_que_falar = 'sim'
        imagem = PhotoImage(file='Imagens/reconhece_escreve/icon_speak.png')

    imagem = imagem.subsample(16,16)
    status_audio['image'] = imagem
    status_audio.image = imagem

class falar ():
    log('_falar')
    def rec_thread(texto_fala):
        log('__rec_thread')
        global control_thread_espeak # naturalmente é False! 

        if control_thread_espeak == True:
            log('já existe um thread sendo usado para processar a fala')
        else:
            try:
                import threading
                tts_thread = threading.Thread(target = falar.resp_speak, args=[texto_fala])
                tts_thread.start()
            except Exception as e:
                log('erro ao criar thread para a fala.\n'+str(e))
            else:
                control_thread_espeak= True

    def resp_speak(texto_fala):
        log('__iniciar fala')
        global control_thread_espeak

        try:
            from gtts import gTTS
            from playsound import playsound
        except Exception as e:
            log('erro ai importar os módulos necessários. \n'+str(e))
            messagebox.showinfo('ERRO',e)
        else:
            try:
                tts = gTTS(text=texto_fala, lang='pt-br')
                tts.save('audio.mp3')
                playsound('audio.mp3')
            except Exception as er:
                log('erro ao carregar e reproduzir audio. \n'+str(e))
                messagebox.showinfo('ERRO',er)
            else:
                log('fala finalizada')
        finally:
            # Permite a geração de novas falas
            control_thread_espeak = False

        try:
            log('deletando arquivo residual')
            os.remove('audio.mp3')
        except Exception as er2:
            log('impossivel deletar o arquivo residual. \n'+str(er2))

class ouvir():
    log('_ouvir')
    def callback(recognizer, audio):
        log('__callback')
        global control_thread_listen
        global texto

        log('iniciar reconhecimento de fala')
        try:
            rec =  recognizer.recognize_google(audio,language='pt-BR')
            texto = rec
        except sr.UnknownValueError:
            texto = "[ERRO] O Reconhecimento de fala não conseguiu entender o áudio"
        except sr.RequestError as e:
            texto = "[ERRO] Não foi possível solicitar os resultados: {0}".format(e)
        except:
            texto = '[ERRO] DESCONHECIDO'
        else:
            log('reconhecimento de fala finalizado com sucesso')
        finally:
            control_thread_listen = False
            log(texto)

    def agora():
        log('__agora')
        global texto
        global control_thread_listen

        btn_rec['state'] = 'disabled'
        tela.update()

        m = sr.Microphone()
        r = sr.Recognizer()

        with m as source:
            r.adjust_for_ambient_noise(source,duration=0.5)

        stop_listening = r.listen_in_background(m, ouvir.callback)
        log('diga alguma coisa: ')

        btn_rec.update()
        tela.update()

        while control_thread_listen == True:
            tela.update()
            time.sleep(0.3)
        control_thread_listen = True

        stop_listening(wait_for_stop=False)
        print('Parei de ouvir!')

        btn_rec['state'] = 'normal'
        btn_rec.update()
        return texto

def resize(event=None):
    log('_resize')
    global precisao_minima
    precisao_minima = scale_config.get()

def abrir_site(link):
    log('_abrir_site')
    import webbrowser
    webbrowser.open(link)

def troca_tela(carregar):
    log('_troca_tela')
    if carregar == 'conf_inte':
        tela_frame_configuracoes.grid_forget()
        interacao.grid(row=1,column=1,sticky=NSEW)

    elif carregar == 'inte_conf':
        interacao.grid_forget()
        tela_frame_configuracoes.grid(row=1,column=1,sticky=NSEW)

    elif carregar=='opca_hist':
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

def resize(event=None):
    log('_precisao_minima')
    global precisao_minima
    precisao_minima = scale_py.get()

def test_pyanalise(event):
    log('_test_pyanalise')
    global precisao_minima

    ent_py_test_1.update()
    busca_semelhanca = compare.frase(ent_py_test_1.get(),ent_py_test_2.get())
    result_py_test['text'] = str(busca_semelhanca)+str('%')
    if busca_semelhanca < precisao_minima:
        result_py_test['fg'] = 'red'
    else:
        result_py_test['fg'] = 'blue'

def load_itens_musics():
    log('_load_itens_musics')
    global save_music_object_position
    global music_itens

    # remove all objects
    for list_objects in save_music_object_position:
        for especifc_objets in list_objects:
            especifc_objets.grid_forget()

    music_itens = musica.ler()

    dic_load_entry = {
        'relief':GROOVE,
        'border':2}

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
    log('_remove_item_music')
    global save_music_object_position
    for x in range(len(save_music_object_position)):
        if save_music_object_position[x][2] == btn:
            musica.remover(x)
            load_itens_musics()

def add_item_music():
    log('_add_item_music')
    a = ent_new_file_music.get() 
    b = ent_new_comand_music.get()

    if (a == '') or (b == '') or a.isspace() or b.isspace() or (not ';' in b) or (':' in b) or (':' in a):
        messagebox.showinfo('erro','Dados inválidos detectado!')
    else:
        musica.adicionar({'musica': a, 'comando': b})
        load_itens_musics()
        ent_new_file_music.delete(0,END)
        ent_new_comand_music.delete(0,END)

def load_itens_comand():
    log('_load_itens_comand')
    global save_comand_object_position
    for y in save_comand_object_position:
        y[0].grid_forget()
        y[1].grid_forget()
        y[2].grid_forget()
        y[3].grid_forget()

    save_comand_object_position = []
    global itens
    itens = comandar.ler()
    for x in range(len(itens)):
        ent_send_comand = Entry(fr_comand_4,relief=GROOVE,border=2)
        ent_send_comand.delete(0,END)
        ent_send_comand.insert(0,itens[x]['enviar'])
        ent_send_comand.grid(row=x,column=1,sticky=NSEW)

        ent_comand_respost = Entry(fr_comand_4,relief=GROOVE,border=2)
        ent_comand_respost.delete(0,END)
        ent_comand_respost.insert(0,itens[x]['comando'])
        ent_comand_respost.grid(row=x,column=2,sticky=NSEW)

        btn_remove_item = Button(fr_comand_4,conf_btns_item,image=img_remove)
        btn_remove_item['command'] = lambda btn_remove_item=btn_remove_item: remove_comand_itens(btn_remove_item)
        btn_remove_item.grid(row=x,column=3,sticky=NSEW)

        btn_test_serial = Button(fr_comand_4,conf_btns_item,text='TESTAR',relief=RAISED,border=1,padx=1)
        btn_test_serial['command'] = lambda btn_test_serial=btn_test_serial: acess_serial(btn_test_serial)
        btn_test_serial.grid(row=x,column=4,sticky=NSEW)
        save_comand_object_position.append([ent_send_comand,ent_comand_respost,btn_remove_item,btn_test_serial]) 

def acess_serial(btn_test_serial):
    log('_acess_serial')
    global save_comand_object_position
    for y in save_comand_object_position:
        if y[3] == btn_test_serial:
            test_use_serial(y[0].get(),btn_test_serial)
            return 0

def remove_comand_itens(btn):
    log('_remove_comand_itens')
    global save_comand_object_position
    for x in range(len(save_comand_object_position)):
        if save_comand_object_position[x][2] == btn:
            comandar.remover(x)
            load_itens_comand()
            return 0

def add_comand_itens():
    log('_add_comand_itens')
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

# Testa a porta serial
def test_use_serial(send_message_for_serial,btn_test_serial):
    try:
        comand_arduino.start_connection(ent_serial_for_test.get())
    except Exception as e:
        messagebox.showinfo('ERRO!','Problema com esta serial. \n[ERRO] {}'.format(e))
        btn_test_serial.configure(bg='red',fg='white') 
        ent_serial_for_test['fg'] = 'red'

    if send_message_for_serial != None:
        try:
            comand_arduino.message(send_message_for_serial)
        except:
            btn_test_serial.configure(bg='green',fg='white') 
            ent_serial_for_test['fg'] = 'green'
 
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

# ------ Interacao --------- #
interacao = Frame(tela)
interacao.grid_columnconfigure(2,weight=1)
interacao.rowconfigure(2,weight=1)
interacao.grid(row=1,column=1,sticky=NSEW)

# CONFIGURAÇÔES DOS WIDGETS
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

# VOLTAR
btn_git = Button(interacao,config_btn,image = icon_git)
btn_git['command'] = lambda: abrir_site('https://github.com/Combratec/Diana')
btn_git.grid(row=1,column=1,sticky=NSEW)

# TITULO
lbl_titulo = Label(interacao,text="DIANA 8",bg='blue',fg='white',font=("Arial",20,'bold'))
lbl_titulo.grid(row=1,column=2,sticky=NSEW)

# CONFIG
btn_config = Button(interacao , config_btn , image = icon_config)
btn_config['command'] = lambda: troca_tela('inte_opti')
btn_config.grid(row=1,column=3,sticky=NSEW)

# INTERACOES
text_interacao = Text(interacao,bg='white',fg='black',highlightthickness=0,border=0,font=("consolas", 12), undo=True, wrap='word')
text_interacao.grid(row=2,column=1,columnspan=3,sticky=NSEW)

# AUDIO
status_audio = Button(interacao , config_btn , image = icon_speak , command = def_tenho_que_falar)
status_audio.grid(row=3,column=1)

# ENTRADA
entry_interacao = Entry(interacao,config_entry) 
entry_interacao.bind("<Return>", (lambda event: controlador_de_partes(entry_interacao.get())))
entry_interacao.grid(row=3,column=2,sticky=NSEW)

# RECONHECIMENTO
btn_rec = Button(interacao,config_btn,image = icon_mic)
btn_rec['command'] = lambda: controlador_de_partes(ouvir.agora())
btn_rec.grid(row=3,column=3)

# ---- TELA DE OPÇÕES
conf_btns = {
    'relief':GROOVE,
    'highlightthickness':0,
    'border':0,
    'bg':'white'}

fr_options = Frame(tela)
fr_options.grid_columnconfigure(1, weight=1)
fr_options.rowconfigure(1, weight=1)

fr_options_1 = Frame(fr_options,bg='blue')
fr_options_1.grid(row=0,column=1,sticky=NSEW)
fr_options_1.grid_columnconfigure(2,weight=1)

fr_options_2 = Frame(fr_options,bg='white')
fr_options_2.grid(row=1,column=1,sticky=NSEW)
fr_options_2.grid_columnconfigure((1,2),weight=1)
fr_options_2.grid_columnconfigure(2,weight=2)

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
lbl_dic_config = {
    'background':'#00cccb',
    'highlightbackground':'#00cccb',
    'foreground':'#222',
    'font':("",14)}

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
fr_comand.grid_columnconfigure(1, weight=1)

fr_comand_1 = Frame(fr_comand,bg='blue',padx=6)
fr_comand_1.grid(row=0,column=1,sticky=NSEW)
fr_comand_1.grid_columnconfigure(2,weight=1)

fr_comand_2 = Frame(fr_comand,bg='white',padx=6)
fr_comand_2.grid(row=1,column=1,sticky=NSEW)
fr_comand_2.grid_columnconfigure((1),weight=1)

fr_comand_3 = Frame(fr_comand,bg='white',padx=6)
fr_comand_3.grid(row=2,column=1,sticky=NSEW)
fr_comand_3.grid_columnconfigure((1,2),weight=1)

fr_comand_4 = Frame(fr_comand,bg='white',padx=6)
fr_comand_4.grid(row=3,column=1,sticky=NSEW)
fr_comand_4.grid_columnconfigure((1,2),weight=1)

fr_comand_5 = Frame(fr_comand,bg='white',padx=6)
fr_comand_5.grid(row=4,column=1,sticky=NSEW)
fr_comand_5.grid_columnconfigure((1,2),weight=1)

fr_comand_6 = Frame(fr_comand,bg='white',padx=6)
fr_comand_6.grid_columnconfigure((1),weight=1)
fr_comand_6.grid(row=5,column=1,sticky=NSEW)

btn_comand_return_screem = Button(fr_comand_1,conf_btns,image=img_return)
btn_comand_return_screem['command'] = lambda: troca_tela('coma_opca')
btn_comand_return_screem.grid(row=1,column=1)

lbl_title = Label(fr_comand_1, text='COMANDE',font=("Sans",17,'bold'),bg='blue',fg='white')
lbl_title.grid(row=1,column=2,sticky=NSEW)

lbl_icon = Label(fr_comand_1,image=img_arduino_2,font=("Sans",17,'bold'),bg='blue')
lbl_icon.grid(row=1,column=3)

# verificação da serial
lbl_description = Label(fr_comand_2, text='Digite a serial: /com4',font=("Sans",10,'bold'),bg='white',fg='black')
lbl_description.grid(row=1,column=1,columnspan=2,sticky=W)

ent_serial_for_test = Entry(fr_comand_2,state='normal',relief=GROOVE,border=2)
ent_serial_for_test.insert(END,'/com5')
ent_serial_for_test.grid(row=2,column=1,sticky=NSEW)

btn_test_serial_new = Button(fr_comand_2,conf_btns_item,text='TESTAR',relief=RAISED,width=6,border=1,padx=1)
btn_test_serial_new['command'] = lambda btn_test_serial_new=btn_test_serial_new:  test_use_serial(None,btn_test_serial_new)
btn_test_serial_new.grid(row=2,column=2,sticky=NSEW)

lbl = Label(fr_comand_3,text='ENVIAR',font=("Sans",10,'bold'),bg='white',fg='black')
lbl.grid(row=1,column=1)
lbl = Label(fr_comand_3,text='COMANDO ; RESPOSTA',font=("Sans",10,'bold'),bg='white',fg='black')
lbl.grid(row=1,column=2)

load_itens_comand()

# add new item
ent_comand_add_send = Entry(fr_comand_5,relief=GROOVE,border=2)
ent_comand_add_send.grid(row=1,column=1,sticky=NSEW)

ent_comand_add_comand = Entry(fr_comand_5,relief=GROOVE,border=2)
ent_comand_add_comand.grid(row=1,column=2,sticky=NSEW)

btn_add = Button(fr_comand_5,conf_btns_item,image=img_add,command=add_comand_itens)
btn_add.grid(row=1,column=3,sticky=NSEW)

btn_add_test_serial = Button(fr_comand_5,conf_btns_item,text='TESTAR',relief=RAISED,border=1,padx=1)
btn_add_test_serial['command'] = lambda btn_add_test_serial=btn_add_test_serial: test_use_serial(ent_comand_add_send.get(),btn_add_test_serial)
btn_add_test_serial.grid(row=1,column=4,sticky=NSEW)

# btn help
btn_comand_help = Button(fr_comand_6,text='AJUDA',relief=RAISED,border=4,padx=5,pady=5,bg='purple',fg='white',font=('Sans',13,'bold'),activebackground='purple',activeforeground='white')
btn_comand_help['command'] = lambda: abrir_site('https://dianachatbot.blogspot.com/2019/02/dianachatbotcombratec.html')
btn_comand_help.grid(row=2,column=1,sticky=NSEW)

tela.mainloop() 
