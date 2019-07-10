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
tela.resizable(width=False, height=False)
tela.configure(background="white",border=0)
tela.grid_columnconfigure(1, weight=1)
tela.rowconfigure(1, weight=1)
tela.title('Diana chatbot - Combratec Inova')
tela.geometry("446x546+100+100")

# O que devo fazer: nada,'__responder__','__criar_assunto__','__continuar_assunto__'
global fazer
fazer = 'nada'

global tenho_que_falar
tenho_que_falar = 'sim'

# Precisão para responder.
global precisao_minima
precisao_minima = 80

global lista
lista = []

global perguntado_antes
perguntado_antes = 'nada'

# Nome do chatbot e do usuário
global nome_bot
global nome_usuario
nome_bot = 'TESS: '
nome_usuario = 'VOCÊ: '

# Faz teste em alguns módulos
def testes_modulos(): 
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

# Estado do Reconhecimento de voz e fala
def estado_sistemas(opcao):
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
    print('processamento')
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

# Controla se acontecerá uma resposta ou continuação de de conversa
def controlador_de_partes(digitado):
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


def troca_tela(mudar):
    # MENU
    if mudar == 'conf_inte':
        tela_frame_configuracoes.grid_forget()
        interacao.grid(row=1,column=1,sticky=NSEW)

    if mudar == 'inte_conf':
        interacao.grid_forget()
        tela_frame_configuracoes.grid(row=1,column=1,sticky=NSEW)

global inf_2
inf_2 = True

class falar ():
    def rec_thread(texto_fala):
        global inf_2

        import threading
        tts_thread = threading.Thread(target = falar.resp_speak, args=[texto_fala])
        tts_thread.start()
        while inf_2 == True:
            tela.update()
            time.sleep(0.3)
        inf_2= True

    def resp_speak(texto_fala):
        global inf_2
        try:
            from gtts import gTTS
            from playsound import playsound
        except Exception as e:
            erro = '[ERRO] '+str(e)
            messagebox.showinfo('ERRO',erro)
        else:
            try:
                tts = gTTS(text=texto_fala, lang='pt-br')
                tts.save('audio.mp3')
                playsound('audio.mp3')
            except Exception as er:
                erro = '[ERRO] '+str(er)
                messagebox.showinfo('ERRO',erro)
            else:
                print('Fala finalizada com sucesso!')
        finally:
            inf_2 = False

        # Remover audio, > Problema de permissão
        try:
            os.remove('audio.mp3')
        except:
            print('impossivel deletar o arquivo residual')



#!/usr/bin/env python3

import time
import speech_recognition as sr

global texto
texto = '__'

global inf
inf = True


class ouvir():
    def callback(recognizer, audio):
        global inf
        global texto

        # dados de áudio recebidos, agora vamos reconhecê-lo usando o Reconhecimento de fala do Google
        try:
            print('Processando...')
            rec =  recognizer.recognize_google(audio,language='pt-BR')
            texto = rec
        except sr.UnknownValueError:
            texto = "[ERRO] O Reconhecimento de fala não conseguiu entender o áudio"
        except sr.RequestError as e:
            texto = "[ERRO] Não foi possível solicitar os resultados: {0}".format(e)
        except:
            texto = '[ERRO] DESCONHECIDO'
        else:
            pass
        finally:
            inf = False
            print(texto)
    def agora():
        global texto
        global inf
        btn_rec['state'] = 'disabled'
        tela.update()

        # isto é chamado a partir do segmento de segundo plano
        m = sr.Microphone()
        r = sr.Recognizer()
        with m as source:
            r.adjust_for_ambient_noise(source,duration=0.5)

        # comece a escutar em segundo plano (note que não precisamos fazer isso dentro de uma instrução `with`)
        stop_listening = r.listen_in_background(m, ouvir.callback)
        print('Ouvindo...')

        imagem = PhotoImage(file='Imagens/reconhece_escreve/icon_mic_a.png')
        imagem = imagem.subsample(16,16)
        btn_rec['image'] = imagem
        btn_rec.image = imagem
        btn_rec.update()
        tela.update()

        while inf == True:
            tela.update()
            time.sleep(0.3)  # ainda estamos ouvindo, embora o segmento principal esteja fazendo outras coisas
        inf = True

        stop_listening(wait_for_stop=False)
        print('Parei de ouvir!')

        imagem = PhotoImage(file='Imagens/reconhece_escreve/icon_mic.png')
        imagem = imagem.subsample(16,16)
        btn_rec['image'] = imagem
        btn_rec.image = imagem
        btn_rec.update()
        btn_rec['state'] = 'normal'
        return texto

# Precisão do PyAnalise
def resize(event=None):
    global precisao_minima
    precisao_minima = scale_config.get()

# Abrir um site
def abrir_site(link):
    import webbrowser
    webbrowser.open(link)


# ------ Interacao --------- #

# CONFIGURAÇÕES BÁSICA
interacao = Frame(tela)
interacao.grid_columnconfigure(2,weight=1)
interacao.rowconfigure(2,weight=1)

# CONFIGURAÇÔES DOS WIDGETS
config_btn = {'highlightbackground':'blue','border':0,'bg':'blue','relief':SUNKEN,'activebackground':'blue','highlightthickness':0}
config_entry = {'fg':'white','bg':'blue','highlightbackground':'white','highlightcolor':'white','font':("",14)}

# CARREGAMENTO DE IMAGENS
icon_mic    = PhotoImage(file="Imagens/reconhece_escreve/icon_mic.png")    
icon_speak  = PhotoImage(file="Imagens/reconhece_escreve/icon_speak.png")
icon_git    = PhotoImage(file="Imagens/reconhece_escreve/icon_return_b.png")
icon_config = PhotoImage(file="Imagens/reconhece_escreve/icon_config.png")
icon_mic    = icon_mic.subsample(16,16)
icon_speak  = icon_speak.subsample(16,16)
icon_git    = icon_git.subsample(16,16)
icon_config = icon_config.subsample(16,16)

# VOLTAR
btn_git = Button(interacao,config_btn,image = icon_git)
btn_git['command'] = lambda: abrir_site('https://github.com/Combratec/Diana')
btn_git.grid(row=1,column=1,sticky=NSEW)

# TITULO
lbl_titulo = Label(interacao,text="DIANA 8",bg='blue',fg='white',font=("Arial",20,'bold'))
lbl_titulo.grid(row=1,column=2,sticky=NSEW)

# CONFIG
btn_config = Button(interacao , config_btn , image = icon_config)
btn_config['command'] = lambda: troca_tela('inte_conf')
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
interacao.grid(row=1,column=1,sticky=NSEW)

# ----||||---- TELA DO HISTÓRICO ----||||----


tela.mainloop() 
