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
        falar('Aprendido')
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
        falar('Entendido')

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
    elif '[Erro]' in digitado:
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
                    falar(resposta_diana)

            else:
                alternativa_resposta = alternativa.pergunta(digitado)
                if tenho_que_falar == 'sim':
                    falar(alternativa_resposta)
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
    som_interacao['image'] = imagem
    som_interacao.image = imagem


def troca_tela(mudar):
    # MENU
    if mudar == 'conf_inte':
        tela_frame_configuracoes.grid_forget()
        interacao.grid(row=1,column=1,sticky=NSEW)

    if mudar == 'inte_conf':
        interacao.grid_forget()
        tela_frame_configuracoes.grid(row=1,column=1,sticky=NSEW)

def falar(mensagem):
   try:
      from gtts import gTTS             # Importação do gerador de fala
      from playsound import playsound   # Importação do reprodutor de áudio
      tts = gTTS(text=mensagem, lang='pt')
      tts.save("teste.mp3")
      playsound("teste.mp3")
   except Exception as erro:
      print('Fala cancelada!')
      return "[Erro] "+str(erro)
   else:
      print('Fala concluida!')
      return True

def ouvir():
   # https://pypi.org/project/SpeechRecognition/
   # RECOMENDA-SE o uso do Python 3.6
   try:
      import speech_recognition as sr
      import pyaudio
      microfone = sr.Recognizer()
   except Exception as e:
      return "[Erro] "+str(e)
   else:
      with sr.Microphone() as source:
         microfone.adjust_for_ambient_noise(source)
         print("Diga alguma coisa: ")
         audio = microfone.listen(source)
         try:
            frase = microfone.recognize_google(audio,language='pt-BR')
         except:
            return '[Erro] Diga alguma coisa!'
         else:
            return frase

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

# ESQUEMA DE CORES
rec_esc_fundo_geral = "black"   # Fundo azul dos frames e dos botões
fundo__titulo_geral = "black"   # Fundo do título principal
cor_titulo_geral = "white"      # Cor do título principal
cor_text_preto = "white"        # Cor do texto do Text
fundo_f3 = "black"              # Cor de fundo do Text
rec_esc_frente_geral = "white"  # Cor do texto do Entry
bordas_db = "black"             # Bordas do Entry

# CONFIGURAÇÔES DOS WIDGETS
config_btn = {'highlightbackground':rec_esc_fundo_geral,'border':0,'background':rec_esc_fundo_geral,'relief':FLAT,'activebackground':rec_esc_fundo_geral}
config_entry = {'foreground':rec_esc_frente_geral,'background':rec_esc_fundo_geral,'highlightbackground':bordas_db,'highlightcolor':bordas_db,'font':("",14)}

# CARREGAMENTO DE IMAGENS
inte_icon_mic    = PhotoImage(file="Imagens/reconhece_escreve/icon_mic.png")
inte_icon_voltar = PhotoImage(file="Imagens/reconhece_escreve/icon_speak.png")
inte_icon_return = PhotoImage(file="Imagens/reconhece_escreve/icon_return.png")
inte_icon_config = PhotoImage(file="Imagens/reconhece_escreve/icon_config.png")
inte_icon_mic    = inte_icon_mic.subsample(16,16)
inte_icon_voltar = inte_icon_voltar.subsample(16,16)
inte_icon_return = inte_icon_return.subsample(16,16)
inte_icon_config = inte_icon_config.subsample(16,16)

# VOLTAR
config_btn['image'] = inte_icon_return
btn_voltar_rec = Button(interacao,config_btn)
btn_voltar_rec['command'] = lambda btn_voltar_rec=btn_voltar_rec: messagebox.showinfo('Então','Esse botão não serve para nada!')
btn_voltar_rec.grid(row=1,column=1)

# TITULO
lbl_titulo = Label(interacao,text="DIANA 8",background=fundo__titulo_geral,foreground=cor_titulo_geral,font=("",17))
lbl_titulo.grid(row=1,column=2,sticky=NSEW)

# CONFIG
config_btn['image'] = inte_icon_config
btn_config_rec = Button(interacao,config_btn)
btn_config_rec['command'] = lambda btn_config_rec=btn_config_rec: troca_tela('inte_conf')
btn_config_rec.grid(row=1,column=3)

# INTERACOES
text_interacao = Text(interacao,background=fundo_f3,foreground=cor_text_preto,highlightthickness=0,border=0,font=("consolas", 12), undo=True, wrap='word')
text_interacao.grid(row=2,column=1,columnspan=3,sticky=NSEW)

# AUDIO
config_btn['image'] = inte_icon_voltar
config_btn['command'] = def_tenho_que_falar
som_interacao = Button(interacao,config_btn)
som_interacao.grid(row=3,column=1)

# ENTRADA
entry_interacao = Entry(interacao,config_entry) 
entry_interacao.bind("<Return>", (lambda event: controlador_de_partes(entry_interacao.get())))
entry_interacao.grid(row=3,column=2,sticky=NSEW)

# RECONHECIMENTO
config_btn['image'] = inte_icon_mic,
btn_rec = Button(interacao,config_btn)
btn_rec['command'] = lambda btn_rec=btn_rec: controlador_de_partes(ouvir())
btn_rec.grid(row=3,column=3)
interacao.grid(row=1,column=1,sticky=NSEW)

# ------------------ TELA DE CONFIGURAÇÃO ------------------ #

# Informações de estilo
letra_roxa = "purple"                # Cor de todas as letras roxas purple
fundo_verde = "green"                # Cor de fundo da escala taxa de variação
dois_titulos = "blue"                # Cor dos dos títulos "RECONHECIMENTO DE VOZ" e "FALA ONLINE PT-BR"
fundo_botao = "white"                # Cor de fundo dos botões ligado e desligado
letra_verde = "green"                # Cor de todas as letras verde green
letra_titulos = "white"              # Cor dos três principais títulos
letra_azul_site = "blue"             # Cor de todas as letras azul dos textos "site"
fundo_azul_titulo = "blue"           # Cor de fundo dos dois principais titulos azuis
fundo_modo_ativo = "white"           # Cor de fundo quando mouse estiver sobre o widget
texto_modo_ativo_ok = "#000"         # Texto no modo ativo "ok"(bibliotecas detectadas)
fundo_configuracoes = "white"        # Background geral de todos os fundos brancos
texto_modo_ativo_erro = "green"      # Texto no modo ativo "erro"(bibliotecas não detectadas)

configuracoes_voltar_imagem = PhotoImage(file="Imagens/configurações/volta_config.png")

# Atualização do estado do botão
status = estado_sistemas('ler')

# Condicionais de imagem para o botão de estado da fala
if status[0]==0:
    configuracoes_fala_imagem = PhotoImage(file="Imagens/configurações/desativado.png")
else:
    configuracoes_fala_imagem = PhotoImage(file="Imagens/configurações/ativado.png")

# Condicionais de imagem para o botão de estado do reconhecimento de voz
if status[1]==0:
    configuracoes_reconhecimento_imagem = PhotoImage(file="Imagens/configurações/desativado.png")
else:
    configuracoes_reconhecimento_imagem = PhotoImage(file="Imagens/configurações/ativado.png")

configuracoes_fala_imagem = configuracoes_fala_imagem.subsample(4,4)
configuracoes_voltar_imagem = configuracoes_voltar_imagem.subsample(3,3)
configuracoes_reconhecimento_imagem = configuracoes_reconhecimento_imagem.subsample(4,4)

# Definições do frame Configurações
tela_frame_configuracoes = Frame(tela,background=fundo_configuracoes)
tela_frame_configuracoes.grid_columnconfigure(1,weight=1)
tela_frame_configuracoes.rowconfigure(1,weight=1)

# Definições do frame Secundário
configuracoes_frame = Frame(tela_frame_configuracoes)
configuracoes_frame.configure(background=fundo_azul_titulo)

# Meteoro para voltar
configuracoes_voltar_texto = Button(configuracoes_frame,image=configuracoes_voltar_imagem,font=("",17),background=fundo_azul_titulo,foreground="white",highlightbackground=fundo_azul_titulo,activeforeground=fundo_azul_titulo,activebackground=fundo_azul_titulo,relief=FLAT)
configuracoes_voltar_texto['command'] = lambda configuracoes_voltar_texto=configuracoes_voltar_texto: troca_tela('conf_inte')
configuracoes_voltar_texto.grid(row=1,column=1,sticky=EW,pady=10)

# Texto configurações gerais
configuracoes_logo_texto = Label(configuracoes_frame,text="Configurações gerais   ",font=("",20),background=fundo_azul_titulo,foreground=letra_titulos)
configuracoes_logo_texto.grid(row=1,column=2,sticky=EW,pady=10)
configuracoes_frame.grid(row=0,column=1,sticky=EW)
configuracoes_frame.grid_columnconfigure(1,weight=1)

# Frame de testes do reconhecimento de voz
configuracoes_frame_1 = Frame(tela_frame_configuracoes,background=fundo_configuracoes,pady=5,padx=10)

# Titulo da primeira opção de teste
configuracoes_reconhecimento_texto = Label(configuracoes_frame_1,text="RECONHECIMENTO DE VOZ ",fg=dois_titulos,bg=fundo_configuracoes,font=("",15))
configuracoes_reconhecimento_texto.grid(row=1,column=1,sticky=W)

# Botão de status do reconhecimento de voz
configuracoes_reconhecimento_imagem_botao = Button(configuracoes_frame_1,image=configuracoes_reconhecimento_imagem,bg=fundo_configuracoes,highlightbackground=fundo_botao,relief=FLAT,bd=0,activebackground=fundo_botao)
configuracoes_reconhecimento_imagem_botao.grid(row=1,column=2)

# Texto avisando da função
configuracoes_reconhecimento_testar_label = Label(configuracoes_frame_1,text="Clique em testar, e diga alguma coisa!",bg=fundo_configuracoes,fg=letra_roxa,highlightbackground=letra_roxa,relief=FLAT,bd=0,activebackground="white",font=("Arial",12))
configuracoes_reconhecimento_testar_label.grid(row=2,column=1,columnspan=2,sticky=E)

# Botão para testes
configuracoes_reconhecimento_testar_botao = Button(configuracoes_frame_1,text="TESTAR",bg=fundo_configuracoes,fg=letra_roxa,highlightbackground=letra_roxa,relief=FLAT,bd=0,activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_ok,font=("Arial",12))
configuracoes_reconhecimento_testar_botao.grid(row=2,column=1,columnspan=2,sticky=W)

# Frame geral (solucionando problemas)
configuracoes_frame_1.grid(row=1,column=1,sticky=EW)
configuracoes_frame_1.grid_columnconfigure(1, weight=3)

# Frame do teste da fala
configuracoes_frame_2 = Frame(tela_frame_configuracoes,background=fundo_configuracoes,pady=5,padx=10)
configuracoes_fala_texto = Label(configuracoes_frame_2,text="FALA ONLINE PT-BR ",foreground=dois_titulos,background=fundo_configuracoes,font=("",13))
configuracoes_fala_texto.grid(row=1,column=1,sticky=W)

# Status do reconhecimento de voz
configuracoes_fala_imagem_botao = Button(configuracoes_frame_2,image=configuracoes_fala_imagem,background=fundo_configuracoes,highlightbackground=fundo_botao,relief=FLAT,bd=0,activebackground=fundo_botao)
configuracoes_fala_imagem_botao.grid(row=1,column=2,sticky=W)

# Botão para testar o modo
configuracoes_fala_testar_botao = Button(configuracoes_frame_2,text="TESTAR O MODO FALA",background=fundo_configuracoes,foreground=letra_roxa,highlightbackground=letra_roxa,relief=FLAT,bd=0,activeforeground=texto_modo_ativo_ok, activebackground=fundo_modo_ativo,font=("Arial",12))
configuracoes_fala_testar_botao.grid(row=2,column=1,columnspan=2,sticky=E+W)
configuracoes_frame_2.grid(row=2,column=1,sticky=EW)
configuracoes_frame_2.grid_columnconfigure(1, weight=3)

# Guia dos módulos necessários
configuracoes_modulo = Label(tela_frame_configuracoes,text="  Módulos necessários  ",background=fundo_azul_titulo,foreground=letra_titulos,pady=5,padx=10,font=("",15))
configuracoes_modulo.grid(row=3,column=1,sticky=EW)

teste_resultados = testes_modulos()

# Frame do pyanalise
configuracoes_frame_3 = Frame(tela_frame_configuracoes)
# Carregamento do botão de acordo com o status na inicialização

conf_certo = {'font':("",16),'background':fundo_configuracoes,'foreground':letra_verde,'highlightbackground':letra_verde,'activebackground':fundo_modo_ativo,'activeforeground':texto_modo_ativo_ok,'relief':FLAT}
conf_erro = {'font':("",16),'background':fundo_configuracoes,'foreground':"red",'highlightbackground':"red",'activebackground':fundo_modo_ativo,'activeforeground':texto_modo_ativo_erro,'relief':FLAT}
config_site = {'text':' SITE ','font':("",16),'background':fundo_configuracoes,'foreground':letra_azul_site,'highlightbackground':letra_azul_site,'activebackground':fundo_modo_ativo,'activeforeground':texto_modo_ativo_ok,'relief':FLAT}

if teste_resultados[1] == 1:
    configuracoes_pyanalise = Button(configuracoes_frame_3,conf_certo)
    configuracoes_pyanalise['text'] = "pyanalise"
else:
    configuracoes_pyanalise = Button(configuracoes_frame_3,conf_erro)
    configuracoes_pyanalise['text'] = "Preciso do pyanalise!"

configuracoes_pyanalise.grid(row=2,column=1,columnspan=2,sticky=EW)
# Carregamento com  o site do pyanalise
configuracoes_pyanalise_link = Button(configuracoes_frame_3,config_site)
configuracoes_pyanalise_link['command'] = lambda configuracoes_pyanalise_link=configuracoes_pyanalise_link: abrir_site('https://github.com/gabrielogregorio/pyanalise')
configuracoes_pyanalise_link.grid(row=2,column=1,columnspan=2,sticky=E)
configuracoes_frame_3.grid(row=4,column=1,sticky=EW)
configuracoes_frame_3.grid_columnconfigure(1, weight=3)

# Frame do reconhecimento de voz
configuracoes_frame_4 = Frame(tela_frame_configuracoes)
# Carregamento do botão de acordo com o status na inicialização
if teste_resultados[0]==1:
    configuracoes_speechrecognition = Button(configuracoes_frame_4,conf_certo)
    configuracoes_speechrecognition['text'] = "Speech Recognition"
else:
    configuracoes_speechrecognition = Button(configuracoes_frame_4,conf_erro)
    configuracoes_speechrecognition['text'] = "Instalar Speech Recognition"

configuracoes_speechrecognition.grid(row=2,column=1,columnspan=2,sticky=EW)
# Carregamento do botão com o site
configuracoes_speechrecognition_link = Button(configuracoes_frame_4,config_site)
configuracoes_speechrecognition_link['command'] = lambda configuracoes_speechrecognition_link=configuracoes_speechrecognition_link: abrir_site('https://pypi.org/project/SpeechRecognition/')
configuracoes_speechrecognition_link.grid(row=2,column=1,columnspan=2,sticky=E)
configuracoes_frame_4.grid(row=5,column=1,sticky=EW)
configuracoes_frame_4.grid_columnconfigure(1, weight=3)

# Frame do Pyaudio
configuracoes_frame_5 = Frame(tela_frame_configuracoes)

# Carregamento do botão com o status do pyaudio
if teste_resultados[2] == 1:
    configuracoes_pyaudio = Button(configuracoes_frame_5,conf_certo)
    configuracoes_pyaudio['text'] = "Pyaudio"
else:
    configuracoes_pyaudio = Button(configuracoes_frame_5, conf_erro)
    configuracoes_pyaudio['text'] = "Instalar pyaudio"
configuracoes_pyaudio.grid(row=2,column=1,columnspan=2,sticky=EW)
# Carregamento do botão com o site do pyaudio
configuracoes_pyaudio_link = Button(configuracoes_frame_5,config_site)
configuracoes_pyaudio_link['command'] = lambda configuracoes_pyaudio_link=configuracoes_pyaudio_link: abrir_site('https://pypi.org/project/PyAudio/')
configuracoes_pyaudio_link.grid(row=2,column=1,columnspan=2,sticky=E)
configuracoes_frame_5.grid(row=6,column=1,sticky=EW)
configuracoes_frame_5.grid_columnconfigure(1, weight=3)

# Frame do playsound
configuracoes_frame_6 = Frame(tela_frame_configuracoes)

# Carregamento do botão com o status do playsound
if teste_resultados[3] == 1:
    configuracoes_playsound = Button(configuracoes_frame_6, conf_certo)
    configuracoes_playsound['text'] ="Playsound"
else:
    configuracoes_playsound = Button(configuracoes_frame_6,conf_erro)
    configuracoes_playsound['text'] = "Instalar playsound"
configuracoes_playsound.grid(row=2,column=1,columnspan=2,sticky=EW)

# Carregamento do botão site
configuracoes_playsound_link = Button(configuracoes_frame_6,config_site)
configuracoes_playsound_link['command'] = lambda configuracoes_playsound_link=configuracoes_playsound_link: abrir_site('https://pypi.org/project/playsound/')
configuracoes_playsound_link.grid(row=2,column=1,columnspan=2,sticky=E)
configuracoes_frame_6.grid(row=7,column=1,sticky=EW)
configuracoes_frame_6.grid_columnconfigure(1, weight=3)

# Frame do GTTS
configuracoes_frame_7 = Frame(tela_frame_configuracoes)

# Carregamento do botão de acordo com o status na inicialização
if teste_resultados[4]==1:
    configuracoes_gtts = Button(configuracoes_frame_7,conf_certo)
    configuracoes_gtts['text'] = "GTTS"
else:
    configuracoes_gtts = Button(configuracoes_frame_7, conf_erro)
    configuracoes_gtts['text'] = "Instalar gtts"
configuracoes_gtts.grid(row=2,column=1,columnspan=2,sticky=EW)

# Carregamento do botão site
configuracoes_gtts_link = Button(configuracoes_frame_7,config_site)
configuracoes_gtts_link['command'] = lambda configuracoes_gtts_link=configuracoes_gtts_link: abrir_site('https://pypi.org/project/gTTS/')
configuracoes_gtts_link.grid(row=2,column=1,columnspan=2,sticky=E)
configuracoes_frame_7.grid(row=8,column=1,sticky=EW)
configuracoes_frame_7.grid_columnconfigure(1, weight=3)

# Frame de controle da taxa de variação do pyanalise
configuracoes_frame_8 = Frame(tela_frame_configuracoes)
configuracoes_frame_8.configure(background=fundo_verde,padx=9,pady=9)

# Texto sobre a função
taxa_variacao = Label(configuracoes_frame_8,text="Taxa de precisão do pyanalise")
taxa_variacao.configure(font=("",17),background=fundo_verde,foreground=letra_titulos)
taxa_variacao.grid(row=0,column=1,sticky=N+S+E+W)

# Escala da taxa de variação
scale_config = Scale(configuracoes_frame_8,from_=1, to=100, orient=HORIZONTAL,command=resize)
scale_config.configure(background=fundo_verde,foreground=letra_titulos,highlightbackground=fundo_verde,troughcolor=fundo_verde,bd=1)
scale_config.set(precisao_minima) # Aqui a escala é colocada na sua devida posição
scale_config.grid(row=1,column=1,sticky=NSEW)
configuracoes_frame_8.grid(row=10,column=1,sticky=N+S+E+W)
configuracoes_frame_8.grid_columnconfigure(1, weight=1)
configuracoes_frame_8.rowconfigure(1, weight=1)


tela.mainloop() 
