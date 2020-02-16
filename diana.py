#!/usr/bin/python3
# -*- coding: utf-8 -*-
from design  import design_principal
from design  import design_historico
from design  import design_pyanalise
from design  import design_comando
from design  import design_opcoes
from design  import design_musica
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import HORIZONTAL
from tkinter import Scrollbar
from tkinter import GROOVE
from tkinter import RAISED
from tkinter import Button
from tkinter import Entry
from tkinter import Label
from tkinter import Frame
from tkinter import Scale
from tkinter import Text
from tkinter import NSEW
from tkinter import END
from tkinter import Tk
from tkinter import EW
from tkinter import NS
from tkinter import W
from definicoes    import comandar
from definicoes    import musica
from definicoes    import basic
from arduino_code  import comand_arduino
from alternativa   import pergunta
from pyanalise     import compare
from processamento import analise_comandos
from processamento import analise
from time import sleep
from os   import remove

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

# A Diana irá falar a resposta
tenho_que_falar = basic.ler_tenho_que_falar()

# Precisão para saber se a Diana entendeu algo ou não.
precisao_minima = basic.ler_pyanalise()

# Endereço usado pela serial
link_serial =  basic.ler_link_serial()

# Salva a posição dos objetos de comando (Arduino)
save_comand_object_position = []

# Salva a posição dos objetos música
save_music_object_position = []

# Impede que o reconhecimento de voz seja ativado mais de uma vez por vez.
control_thread_listen = False

# impede que o sistema de fala seja ativadao mais de uma vez por vez.
control_thread_espeak = False

# O que foi perguntado anteriormente
perguntado_antes = 'nada'

# Usuario
nome_usuario = 'você_: '

# chatbot
nome_bot = 'Diana: '

# Indica se uma música está tocando
tocando = False

# O que fazer agora?
fazer = 'nada'

# Placa do arduino
placa = None

# Lista com os resultados do processamento
lista = []

def processamento(pergunta):
    ''' Recebe uma pergunta e retorna uma resposta '''

    global precisao_minima
    global lista
    global fazer
    dic_opcoes = [{'acao':'é_horas', 'diretorio':'arquivos/comandos/horas.txt'},
                  {'acao':'é_comando', 'diretorio':'arquivos/comandos/arduino.txt'},
                  {'acao':'é_musica', 'diretorio':'arquivos/comandos/musica.txt'}]

    # É para responder a uma pergunta do usuário
    if fazer == 'nada':

        # Loop por todas as opções
        for dic in dic_opcoes:

            # Manda a pergunta para as opções
            lista = analise_comandos(pergunta, dic['diretorio'])

            # Se obteve uma precisão melhor
            if precisao_minima <= lista[0]:

                # Adicione a opção
                lista.append(dic['acao'])

                # Retorna a resposta
                return '__comando_responder__'

    # Analisa a pergunta do usuário
    lista = analise(pergunta)

    # Analisa o comportamento para gerar uma resposta
    if precisao_minima > lista[0]:
        return '__criar_assunto__'
    else:
        if lista[3] == 1:
            return '__responder__'
        else:
            return '__continuar_assunto__'

def responder():
    ''' Gera a resposta '''
    global lista
    global fazer

    # Acessa a frase com a resposta
    resp = basic.abrir_arquivo('arquivos/conteudo/{}'.format(lista[1]))

    # Obtém a lista de frases
    resp = resp.split(';')

    # Acessa a resposta
    resposta = str(resp[ lista[2] + 1])

    # Limpa a resposta
    resposta = resposta.strip()

    # Marca que ja foi respondido
    fazer = 'nada'

    # Retorna a resposta formatada
    return str(resposta  + '\n')

def continuar_assunto(digitado):
    global lista
    global nome_bot
    global nome_usuario
    global fazer
    global tenho_que_falar

    # Adicionar a resposta no arquivo
    texto = ';' + digitado
    rota = 'arquivos/conteudo/' + lista[1]

    arquivo = open (rota, 'a', encoding='utf8')
    arquivo.write(texto)
    arquivo.close()

    # Texto padrão
    texto_add = str((nome_bot + 'Aprendido\n'))

    # Adicionar no histórico
    basic.add_historic(texto_add)

    # Adicionar no Text principal
    txt_main_inte_0.insert(END, texto_add)

    # Iniciar a resposta da fala
    if tenho_que_falar == 'sim':
        falar.ThreadDeFala('Aprendido')

    # liberar para outros comandos
    fazer = 'nada'

def criar_assunto(perguntado, digitado):
    global nome_bot
    global fazer
    global tenho_que_falar

    # Texto padrão
    texto_add = nome_bot + 'Entendido\n'

    # Adicionar no histórico
    basic.add_historic(texto_add)

    # Adicionar no Text principal
    txt_main_inte_0.insert(END, texto_add)

    # Verifica se a Diana vai falar alguma coisa
    if tenho_que_falar == 'sim':
        falar.ThreadDeFala('Entendido')

    # Cria um arquivo inexistente
    x = 0
    while True:
        # tente abrir esse arquivo
        try:
            arquivo = basic.abrir_arquivo('arquivos/conteudo/{}{}'.format(x, '.txt'))

        # Se não conseguir, ele não deve existir!
        except:
            arquivo = open ('arquivos/conteudo/'+str(x)+'.txt', 'w', encoding='utf8')
            arquivo.write(str(perguntado)+';'+str(digitado))
            arquivo.close()
            break

        x = x + 1

    # Libera o fazer.
    fazer = 'nada'

def responderHoras():
    global fazer
    global lista
    global tenho_que_falar
    global nome_bot

    dt = basic.retornar_time()

    if lista[1] == 'São {} horas e {} minutos':
        msg_resposta = lista[1].format(dt['hour'], dt['minute'])

    elif lista[1] == 'Hoje é dia {}':
        msg_resposta = lista[1].format(dt['day'])

    elif lista[1] == 'Estamos no mês {} de {}':
        msg_resposta = lista[1].format(dt['month'], dt['year'])

    elif lista[1] == 'Estamos em {}':
        msg_resposta = lista[1].format(dt['year'])

    texto_add = nome_bot + msg_resposta + '\n'

    if tenho_que_falar == 'sim':
        falar.ThreadDeFala(msg_resposta)

    return texto_add

def abrirArquivoEReproduzirMusica(o_que_era, o_que_responder):
    file = basic.abrir_arquivo('musica/arquivo')
    file = file.split('\n')

    for x in file:
        x = x.split(':')

        if x[3] == o_que_era + ';' + o_que_responder:
            play_music(x[1])
            break

def abrirArquivoExecutarComando(o_que_era, o_que_responder):
    file = basic.abrir_arquivo('comandos/arquivo')
    file = file.split('\n')

    for x in file:
        x = x.split(':')

        if x[3] == o_que_era + ';' + o_que_responder:
            send_serial_message(x[1], None)
            break

def controlador_de_partes(digitado):
    global fazer
    global lista
    global perguntado_antes
    global tenho_que_falar
    global nome_bot

    # Deletar a entrada
    ent_main_writ_0.delete(0, 'end')

    # Atualizar a tela
    tela.update()

    # Digitos inválidos
    if (digitado.isspace() == True or (';' in digitado) or (digitado == '')):
        messagebox.showinfo('Não faça isso', 'Espaços e ; não são tem poder aqui!')

    # Erro no que foi digitado ou falado.
    elif '[ERRO]' in digitado:
        messagebox.showinfo('Eita!', digitado)

    # Sem erros
    else:
        # texto padrão
        texto_add = 'você: ' + digitado + '\n'   

        # adiciona no histórico
        basic.add_historic(texto_add)

        # adiciona na tela principal
        txt_main_inte_0.insert(END, texto_add)

        # atualiza a tela
        tela.update()

        # Nenhuma ação especial a fazer
        if fazer == 'nada':

            # Verifica se será necessário ativar uma ação especial
            fazer = processamento(digitado)

            # A Diana pode responder a essa pergunta.            
            if fazer == '__responder__':

                # A Diana vai buscar uma resposta
                resposta_diana = responder()

                # Texto padrão
                texto_add = nome_bot + resposta_diana  

                # Adicionar no histórico
                basic.add_historic(texto_add)

                # Adicionar no Text principal
                txt_main_inte_0.insert(END, texto_add)

                # A opção de fala está ativa?
                if tenho_que_falar == 'sim':

                    # A Diana vai falar
                    falar.ThreadDeFala(resposta_diana)

            # Um comando foi acionado
            elif fazer == '__comando_responder__':

                # O usuário fez uma pergunta sobre horas
                if lista[3] == 'é_horas':
                    texto_add = responderHoras()
                else:
                    texto_add = nome_bot + lista[1] + '\n'

                # adiciona ao histórico
                basic.add_historic(texto_add)

                # insere no Text principal
                txt_main_inte_0.insert(END, texto_add)

                # libera o fazer
                fazer = 'nada'

                # Resposta que a diana vai dar
                o_que_responder = lista[1]

                # O que o usuário perguntou
                o_que_era = lista[2]

                # O usuário pediu para tocar uma música
                if lista[3] == 'é_musica':
                    abrirArquivoEReproduzirMusica(o_que_era, o_que_responder)

                # O usuário deu um comando programado para o Arduino
                elif lista[3] == 'é_comando':
                    abrirArquivoExecutarComando(o_que_era, o_que_responder)

            # Futuramente a Diana vai continuar ou criar um assunto
            else:

                if fazer != 'nada':
                    # Respostas alteranativas
                    alternativa_resposta = pergunta(digitado)

                    # Executar a fala
                    if tenho_que_falar == 'sim':
                        falar.ThreadDeFala(alternativa_resposta)

                    # texto padrão
                    texto_add = nome_bot + alternativa_resposta + '\n'

                    # Adicionar ao histórioc
                    basic.add_historic(texto_add)

                    # Adicionar na tela principal
                    txt_main_inte_0.insert(END, texto_add)

        # continuar uma conversa
        elif fazer == '__continuar_assunto__':
            continuar_assunto(digitado)

        # Criar um novo assunto
        elif fazer == '__criar_assunto__':
            criar_assunto(perguntado_antes, digitado)

        # pergunta anterior do usuário
        perguntado_antes = digitado

    # Atualiza o Text
    txt_main_inte_0.see('end')

def status_falar_ou_nao(parametro):
    '''Atualiza os dados de falar a resposta ou não '''
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

    imagem = imagem.subsample(16, 16)
    btn_main_audi_0['image'] = imagem
    btn_main_audi_0.image = imagem

    basic.atualizar_tenho_que_falar(tenho_que_falar)

class falar ():
    def ThreadDeFala(texto_fala):
        # impede que seja criados multiplos Threads
        global control_thread_espeak

        # Se Alguém já estiver usando o Thread
        if control_thread_espeak == True:
            basic.log('já existe um thread sendo usado para processar a fala')

        else:

            # Tenta deletar o áudio
            try:
                remove('audio.mp3')
            except Exception as er2:
                basic.log('impossivel deletar o arquivo residual de audio. \n'+str(er2))

            # Tenta criar um Thread
            try:
                import threading
                tts_thread = threading.Thread(target = falar.orquestraAFala, args=[texto_fala])
                tts_thread.start()
            except Exception as e:
                basic.log('Erro ao criar thread para a fala.\n'+str(e))
            else:

                # Se o Thread foi criado, ele bloqueia a criação de novos Threads
                control_thread_espeak = True

    def reproduzir_som(link):
        # Tente importar a biblioteca do PyGame
        try:
            from pygame import mixer
        except Exception as e_1:
            messagebox.showinfo('erro', 'Instale o pygame para reproduzir o som!\n'+str(e_1))
            basic.abrir_site('https://github.com/Combratec/Diana/blob/master/README.md#Como-ativar-a-fala')
        else:

            # Inicialização do mixer
            try:
                mixer.init() 
            except Exception as e_2:
                messagebox.showinfo('erro', 'Erro ao iniciar o mixer\n'+str(e_2))
            else:

                # Tente carregar o link
                try:
                    mixer.music.load(link)
                except Exception as e_3:
                    messagebox.showinfo('erro', 'Erro ao carregar audio\n'+str(e_3))
                else:

                    # Tente tocar o áudio
                    try:
                        mixer.music.play()
                    except Exception as e_4:
                        messagebox.showinfo('erro', 'Erro ao iniciar audio\n'+str(e_4))
                    else:

                        try:
                            while mixer.music.get_busy():
                                sleep(0.5)
                        except:
                            messagebox.showinfo('erro', 'um erro improvável aconteceu!')
                        else:
                            basic.log('Reprodução de som filizada com sucesso')

                mixer.quit()

    def orquestraAFala(texto_fala):
        # Impede que novos threads sejam criados
        global control_thread_espeak

        # Gerar o som
        analise = falar.gerar_som(texto_fala)

        # O áudio foi gerado com sucesso
        if analise == 0:
            falar.reproduzir_som('audio.mp3')

        # Liberar a execução da fala
        control_thread_espeak = False

    def gerar_som(texto_fala):
        # Tentar importar a biblioteca
        try:
            from gtts import gTTS

        except Exception as e_1:
            messagebox.showinfo('Aviso', 'O módulo GTTS não está instalado, eu precido dele para falar, portanto, vou abrir o site para que você possa fazer a instalação do gtts: \nErro:' + str(e_1))
            basic.abrir_site('https://github.com/Combratec/Diana/blob/master/README.md#Como-ativar-a-fala')

        else:

            # Tentar buscar o audio
            try:
                tts = gTTS(text=texto_fala, lang='pt-br')
            except Exception as e_2:
                messagebox.showinfo('erro', 'Não consegui buscar o áudio na internet.\n Erro:'+str(e_2))
            else:

                # Tentar salvar o audio
                try:
                    tts.save('audio.mp3')
                except Exception as e_3:
                    messagebox.showinfo('erro', 'Erro ao salvar audio, tente me mover para a sua Desktop ou dar mais permissões para mim!\n'+str(e_3))
                else:
                    return 0
        return 1

# RECONHECIMENTO DE VOZ
class ouvir():
    def agora():
        global texto
        global control_thread_listen
        global sr

        # Tente importar a biblioteca
        try:
            import speech_recognition as sr
        except Exception as e_1:
            messagebox.showinfo('Erro', 'Por favor, instale a biblioteca speechrecognition\nErro:'+str(e_1))
            basic.abrir_site('https://github.com/Combratec/Diana/blob/master/README.md#Como-ativar-o-reconhecimento-de-voz')
        else:

            # O Thread está oculpado
            if control_thread_listen == True:
                messagebox.showinfo('Já existe um Thread sendo usado para reconhecimento de fala!')

            # O Thread está disponível
            else:
                # Desabilite o botão
                btn_main_reco_0['state'] = 'disabled'

                # Atualize a tela
                tela.update()

                # Tente fazer o reconhecimento
                try:
                    m = sr.Microphone()
                    r = sr.Recognizer()

                    with m as source:
                        r.adjust_for_ambient_noise(source, duration=0.3)
                    stop_listening = r.listen_in_background(m, ouvir.inicarLeituraDoMicrofone)

                    while control_thread_listen == False:
                        tela.update()
                        sleep(0.3)

                    control_thread_listen = False
                    stop_listening(wait_for_stop=False)

                except:
                    texto = '[ERRO] Erro desconhecido_fala:'
                    btn_main_reco_0.update()
                    tela.update()

                btn_main_reco_0['state'] = 'normal'
                btn_main_reco_0.update()

                return texto

    def inicarLeituraDoMicrofone(recognizer, audio):
        global control_thread_listen
        global texto
        global sr

        try:
            rec =  recognizer.recognize_google(audio, language='pt-BR')
            texto = str(rec)

        except sr.UnknownValueError as e1:
            texto = '[ERRO] Eu não consegui entender nada!' + e1

        except sr.RequestError as e2:
            texto = '[ERRO] Parece que você tem um Problema com a internet! {}' + e2

        except Exception as e3:
            texto = '[ERRO] Erro desconhecido: ' + e3

        else:
            basic.log('reconhecimento de fala finalizado com sucesso')

        finally:
            control_thread_listen = True

def limpar_historico():
    basic.clear_historic()
    atualizar_historico()

def atualizar_historico():
    txt_historic_data_0.delete(1.0, END)
    txt_historic_data_0.insert(1.0, basic.load_historic())
    txt_historic_data_0.see('end')

def resize(event=None):
    global precisao_minima

    basic.atualizar_pyanalise(scl_pyanalise_prec_0.get())
    precisao_minima = basic.ler_pyanalise()

def testar_pyanalise(event):
    global precisao_minima

    ent_pyanalise_fras_0.update()
    busca_semelhanca = compare.frase(ent_pyanalise_fras_0.get(), ent_pyanalise_fras_1.get())
    lbl_pyanalise_resu_0['text'] = str(busca_semelhanca)+str('%')

    if busca_semelhanca < precisao_minima:
        lbl_pyanalise_resu_0['fg'] = 'red'
    else:
        lbl_pyanalise_resu_0['fg'] = '#3399ff'

def load_songs():
    global save_music_object_position
    global music_itens

    for list_objects in save_music_object_position:
        for especifc_objets in list_objects:
            especifc_objets.grid_forget()

    save_music_object_position = []
    music_itens = musica.read_musics_in_file()
    config_music_load = {'relief':GROOVE, 'border':2}

    basic.make_file_responses_music()

    for x in range(len(music_itens)):
        ent_music_file_1 = Entry(fr_music_3 , config_music_load)
        ent_music_comm_1 = Entry(fr_music_3 , config_music_load)
        btn_music_dele_0 = Button(fr_music_3, config_music_btns, image=img_remove)
        btn_music_test_1 = Button(fr_music_3, config_music_btns, text='TESTAR')

        btn_music_dele_0['command'] = lambda btn_music_dele_0=btn_music_dele_0: remove_songs(btn_music_dele_0)
        btn_music_test_1['command'] = lambda btn_music_test_1=btn_music_test_1: select_music(btn_music_test_1)

        delete_and_insert(ent_music_file_1, music_itens[x]['musica'])
        delete_and_insert(ent_music_comm_1, music_itens[x]['comando'])

        ent_music_file_1.grid(row=x, column=1, sticky=NSEW)
        ent_music_comm_1.grid(row=x, column=2, sticky=NSEW)
        btn_music_dele_0.grid(row=x, column=3, sticky=NSEW)
        btn_music_test_1.grid(row=x, column=4, sticky=NSEW)

        new_list_itens = [ent_music_file_1, ent_music_comm_1, btn_music_dele_0, btn_music_test_1]
        save_music_object_position.append(new_list_itens) 

def remove_songs(btn):
    global save_music_object_position

    total = len(save_music_object_position)
    for x in range(total):
        if save_music_object_position[x][2] == btn:
            musica.remover(x)
            load_songs()
            break 

def add_songs():
    a = ent_music_file_0.get() 
    b = ent_music_comm_0.get()

    if (a == '') or (b == '') or a.isspace() or b.isspace() or (not ';' in b) or (':' in b) or (':' in a):
        messagebox.showinfo('erro', 'Dados inválidos! Por favor, siga o modelo indicado acima!')
    else:
        musica.adicionar({'musica': a, 'comando': b})
        load_songs()
        ent_music_file_0.delete(0, END)
        ent_music_comm_0.delete(0, END)

def select_music(btn):
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
            messagebox.showinfo('ERRO', 'Por favor, instale a biblioteca pygame com o comando: \npip install pygame\nerro: ' + str(e))
            basic.abrir_site('https://github.com/Combratec/Diana/blob/master/README.md#Como-tocar-uma-m%C3%BAsica')
        else:
            try:
                mixer.init() 
                mixer.music.load('musica/'+link)
                mixer.music.play()
            except Exception as er:
                print(er)
                if 'Couldn\'t open' in str(er):
                    messagebox.showinfo('ERRO', 'Está musica não existe!')
                else:
                    messagebox.showinfo('ERRO', er)
            else:
                tocando = True
    else:
        try:
            mixer.music.pause()
            tocando = False
        except Exception as e:
            messagebox.showinfo('ERRP', e)

def load_commands():
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
        ent_command_send_1 = Entry (fr_command_4, relief=GROOVE, border=2)
        ent_command_comm_0 = Entry (fr_command_4, relief=GROOVE, border=2)
        ent_command_dele_0 = Button(fr_command_4, config_command_addi, image=img_remove)
        btn_command_test_2 = Button(fr_command_4, config_command_addi, text='TESTAR', relief=RAISED, border=1, padx=1)

        ent_command_dele_0['command'] = lambda ent_command_dele_0=ent_command_dele_0: remove_commands(ent_command_dele_0)
        btn_command_test_2['command'] = lambda btn_command_test_2=btn_command_test_2: select_serial(btn_command_test_2)

        delete_and_insert(ent_command_send_1, itens[x]['enviar'])
        delete_and_insert(ent_command_comm_0, itens[x]['comando'])

        ent_command_send_1.grid(row=x, column=1, sticky=NSEW)
        ent_command_comm_0.grid(row=x, column=2, sticky=NSEW)
        ent_command_dele_0.grid(row=x, column=3, sticky=NSEW)
        btn_command_test_2.grid(row=x, column=4, sticky=NSEW)

        save_comand_object_position.append([ent_command_send_1, ent_command_comm_0, ent_command_dele_0, btn_command_test_2]) 

def remove_commands(btn):
    global save_comand_object_position

    total = len(save_comand_object_position)
    for x in range(total):
        if save_comand_object_position[x][2] == btn:
            comandar.remover(x)
            load_commands()
            break

def add_commands():
    a = ent_command_send_0.get() 
    b = ent_command_comm_0.get()
    if  a == '' or  b =='' or a.isspace() or b.isspace() or not ';' in b or ':' in b or ':' in a:
        messagebox.showinfo('ops', 'Caracteres inválidos detectado!')
    else:
        global itens
        comandar.adicionar({'enviar': ent_command_send_0.get(), 'comando': ent_command_comm_0.get()})

        load_commands()
        ent_command_send_0.delete(0, END)
        ent_command_comm_0.delete(0, END)

def select_serial(btn_command_test_2):
    global save_comand_object_position

    for y in save_comand_object_position:
        if y[3] == btn_command_test_2:
            send_serial_message(y[0].get(), btn_command_test_2)

def send_start_serial(send_message_for_serial):
    global placa

    if placa == None:
        try:
            placa = comand_arduino.start_connection(link_serial)

        except:
            messagebox.showinfo('ERRO', 'Por favor, defina uma serial válida!')
            return 0
    try:
        send_serial_message(None, None)

    except Exception as e:
        messagebox.showinfo('ERRO!', 'Problema com esta serial. \n[ERRO] {}'.format(e))

def send_serial_message(send_message_for_serial, btn_command_test_2):
    global placa
    if placa == None:

        try:
            placa = comand_arduino.start_connection(ent_command_seri_0.get())

        except Exception as e:
            messagebox.showinfo('ERRO!', 'Problema com esta serial. \n[ERRO] {}'.format(e))
            cor = 'red'

        else:
            basic.atualizar_link_serial(ent_command_seri_0.get())
            cor = 'green'

        finally:
            if btn_command_test_2 != None:
                btn_command_test_2.configure(bg=cor, fg='white') 
                ent_command_seri_0['fg'] = cor

    if send_message_for_serial != None and placa != None and (send_message_for_serial != ''):
        try:
            comand_arduino.message(placa, send_message_for_serial)

        except Exception as e:
            messagebox.showinfo('ERRO!', 'Problema com esta serial. \n[ERRO] {}'.format(e))
            cor = 'red'

        else:
            cor = 'green'

        finally:

            if btn_command_test_2 != None:
                btn_command_test_2.configure(bg=cor, fg='white') 
                ent_command_seri_0['fg'] = cor

def delete_and_insert(entry_name, insert_entry_name):
    entry_name.delete(0, END)
    entry_name.insert(0, insert_entry_name)

def trocar_interface(carregar):
    if carregar == 'config_to_interface':
        tela_frame_configuracoes.grid_forget()
        interacao.grid(row=1, column=1, sticky=NSEW)

    elif carregar == 'interface_to_config':
        interacao.grid_forget()
        tela_frame_configuracoes.grid(row=1, column=1, sticky=NSEW)

    elif carregar=='opcoes_to_historic':
        fr_options_0.grid_forget()
        fra_historic_0.grid(row=1, column=1, sticky=NSEW)
        atualizar_historico()

    elif carregar=='historic_to_opcoes':
        fr_options_0.grid(row=1, column=1, sticky=NSEW)
        fra_historic_0.grid_forget()

    elif carregar=='opcoes_to_pyananalise':
        fr_options_0.grid_forget()
        fr_pyanalise_0.grid(row=1, column=1, sticky=NSEW)

    elif carregar=='pyananlise_to_opcoes':
        fr_pyanalise_0.grid_forget()
        fr_options_0.grid(row=1, column=1, sticky=NSEW)

    elif carregar=='opcoes_to_music':
        fr_options_0.grid_forget()
        fr_music_0.grid(row=1, column=1, sticky=NSEW)

    elif carregar=='music_to_opcoes':
        fr_options_0.grid(row=1, column=1, sticky=NSEW)
        fr_music_0.grid_forget()

    elif carregar=='opcoes_to_comands':
        fr_options_0.grid_forget()
        fr_command_0.grid(row=1, column=1, sticky=NSEW)

    elif carregar=='comands_to_opcoes':
        fr_command_0.grid_forget()
        fr_options_0.grid(row=1, column=1, sticky=NSEW)

    elif carregar=='interface_to_opti':
        interacao.grid_forget()
        fr_options_0.grid(row=1, column=1, sticky=NSEW)

    elif carregar=='opti_to_interface':
        fr_options_0.grid_forget()
        interacao.grid(row=1, column=1, sticky=NSEW)

tela = Tk() 
tela.resizable(width=False, height=False)
tela.configure(background='white', border=0)
tela.grid_columnconfigure(1, weight=1)
tela.rowconfigure(1, weight=1)
tela.title('Diana chatbot - Combratec')
tela.geometry('446x546+100+100')

# CARREGAMENTO DE IMAGENS
img_transparent  =  PhotoImage(file='Imagens/opcoes/transparent.png')
img_pyanalise    =  PhotoImage(file='Imagens/opcoes/pyanalise.png')
img_arduino_2    =  PhotoImage(file='Imagens/opcoes/arduino.png')
img_historic     =  PhotoImage(file='Imagens/opcoes/historico.png')
img_github_py    =  PhotoImage(file='Imagens/opcoes/github_branco.png')
img_continue     =  PhotoImage(file='Imagens/opcoes/avance.png')
icon_config      =  PhotoImage(file='Imagens/reconhece_escreve/icon_config.png')
img_music_2      =  PhotoImage(file='Imagens/opcoes/musica.png')
img_arduino      =  PhotoImage(file='Imagens/opcoes/arduino.png')
img_github       =  PhotoImage(file='Imagens/opcoes/github.png')
img_return       =  PhotoImage(file='Imagens/opcoes/return.png')
icon_speak       =  PhotoImage(file='Imagens/reconhece_escreve/icon_speak.png')
img_music        =  PhotoImage(file='Imagens/opcoes/musica.png')
img_about        =  PhotoImage(file='Imagens/opcoes/sobre.png')
img_remove       =  PhotoImage(file='Imagens/opcoes/remove.png')
icon_git         =  PhotoImage(file='Imagens/reconhece_escreve/icon_return_b.png')
img_edit         =  PhotoImage(file='Imagens/opcoes/edit.png')
icon_mic         =  PhotoImage(file='Imagens/reconhece_escreve/icon_mic.png')    
img_add          =  PhotoImage(file='Imagens/opcoes/add.png')

# REDIMENSIONAMENTO DE IMAGENS
img_transparent  =  img_transparent.subsample(3, 3)
img_pyanalise    =  img_pyanalise.subsample(2, 2)
img_arduino_2    =  img_arduino_2.subsample(2, 2)
img_historic     =  img_historic.subsample(2, 2)
img_github_py    =  img_github_py.subsample(16, 16)
img_continue     =  img_continue.subsample(2, 2)
icon_config      =  icon_config.subsample(16, 16)
img_music_2      =  img_music_2.subsample(3, 3)
img_arduino      =  img_arduino.subsample(2, 2)
img_github       =  img_github.subsample(2, 2)
img_return       =  img_return.subsample(3, 3)
icon_speak       =  icon_speak.subsample(16, 16)
img_music        =  img_music.subsample(2, 2)
img_about        =  img_about.subsample(2, 2)
img_remove       =  img_remove.subsample(3, 3)
icon_git         =  icon_git.subsample(16, 16)
img_edit         =  img_edit.subsample(3, 3)
icon_mic         =  icon_mic.subsample(16, 16)
img_add          =  img_add.subsample(3, 3)

# ---- TELA PRINCIAL ----
config_main_btns = design_principal.config_main_btns()
config_main_entr = design_principal.config_main_entr()
config_main_text = design_principal.config_main_text() 
config_main_titl = design_principal.config_main_titl()

interacao = Frame(tela)
interacao.grid_columnconfigure(2, weight=1)
interacao.rowconfigure(2, weight=1)
interacao.grid(row=1, column=1, sticky=NSEW)

btn_main_gith_0 = Button(interacao, config_main_btns, image = icon_git)
lbl_main_titl_0 = Label (interacao, config_main_titl, text='DIANA')
lbl_main_conf_0 = Button(interacao, config_main_btns , image = icon_config)
txt_main_inte_0 = Text  (interacao, config_main_text)
btn_main_audi_0 = Button(interacao, config_main_btns)
ent_main_writ_0 = Entry (interacao, config_main_entr) 
btn_main_reco_0 = Button(interacao, config_main_btns, image = icon_mic)

status_falar_ou_nao('ler')

ent_main_writ_0.bind('<Return>', (lambda event: controlador_de_partes(ent_main_writ_0.get())))
btn_main_audi_0['command'] = lambda: status_falar_ou_nao('trocar')
btn_main_reco_0['command'] = lambda: controlador_de_partes(ouvir.agora())
btn_main_gith_0['command'] = lambda: basic.abrir_site('https://github.com/Combratec/Diana')
lbl_main_conf_0['command'] = lambda: trocar_interface('interface_to_opti')

btn_main_gith_0.grid(row=1, column=1, sticky=NSEW)
lbl_main_titl_0.grid(row=1, column=2, sticky=NSEW)
lbl_main_conf_0.grid(row=1, column=3, sticky=NSEW)
txt_main_inte_0.grid(row=2, column=1, columnspan=3, sticky=NSEW)
btn_main_audi_0.grid(row=3, column=1)
ent_main_writ_0.grid(row=3, column=2, sticky=NSEW)
btn_main_reco_0.grid(row=3, column=3)

# ---- TELA DE OPÇÕES ----
config_options_btns = design_opcoes.config_options_btns()
config_options_txts = design_opcoes.config_options_txts()
config_options_icon = design_opcoes.config_options_icon()
config_options_opti = design_opcoes.config_options_opti()
config_options_retu = design_opcoes.config_options_retu()

fr_options_0 = Frame(tela)
fr_options_1 = Frame(fr_options_0, bg='#3399ff')
fr_options_2 = Frame(fr_options_0, bg='white')

fr_options_0.grid_columnconfigure(1, weight=1)
fr_options_0.rowconfigure(1, weight=1)
fr_options_1.grid_columnconfigure(2, weight=1)
fr_options_2.grid_columnconfigure((1, 2), weight=1)
fr_options_2.grid_columnconfigure(2, weight=2)

btn_option_retu_0 = Button(fr_options_1, config_options_retu, image=img_return)
lbl_option_opco_0 = Label (fr_options_1, config_options_opti, text='OPÇÕES')

lbl_option_musi_0 = Label (fr_options_2, config_options_icon, image=img_music)
lbl_option_toca_0 = Label (fr_options_2, config_options_txts, text='Tocar música')
btn_option_musi_0 = Button(fr_options_2, config_options_btns, image=img_continue)

lbl_option_pyan_0 = Label (fr_options_2, config_options_icon, image=img_pyanalise)
lbl_option_pyan_1 = Label (fr_options_2, config_options_txts, text='Pyanalise')
btn_option_pyan_0 = Button(fr_options_2, config_options_btns, image=img_continue)

lbl_option_ardu_0 = Label (fr_options_2, config_options_icon, image=img_arduino)
lbl_option_comm_0 = Label (fr_options_2, config_options_txts, text='Comandos')
btn_option_comm_0 = Button(fr_options_2, config_options_btns, image=img_continue)

lbl_option_hist_0 = Label (fr_options_2, config_options_icon, image=img_historic)
lbl_option_hist_1 = Label (fr_options_2, config_options_txts, text='Histórico')
btn_option_hist_0 = Button(fr_options_2, config_options_btns, image=img_continue)

lbl_option_gith_0 = Label (fr_options_2, config_options_icon, image=img_github)
lbl_option_noss_0 = Label (fr_options_2, config_options_txts, text='Nosso repositório!')
btn_option_gith_0 = Button(fr_options_2, config_options_btns, image=img_continue)

lbl_option_abou_0 = Label (fr_options_2, config_options_icon, image=img_about)
lbl_option_abou_1 = Label (fr_options_2, config_options_txts, text='Sobre este projeto!')
btn_option_abou_0 = Button(fr_options_2, config_options_btns, image=img_continue)

btn_option_retu_0['command'] = lambda: trocar_interface('opti_to_interface')
btn_option_abou_0['command'] = lambda: basic.abrir_site('https://dianachatbot.blogspot.com/2019/02/dianachatbotcombratec.html')
btn_option_gith_0['command'] = lambda: basic.abrir_site('https://github.com/Combratec/Diana')
btn_option_musi_0['command'] = lambda: trocar_interface('opcoes_to_music')
btn_option_comm_0['command'] = lambda: trocar_interface('opcoes_to_comands')
btn_option_hist_0['command'] = lambda: trocar_interface('opcoes_to_historic')
btn_option_pyan_0['command'] = lambda: trocar_interface('opcoes_to_pyananalise')

fr_options_1.grid(row=0, column=1, sticky=NSEW)
fr_options_2.grid(row=1, column=1, sticky=NSEW)

btn_option_retu_0.grid(row=1, column=1)
lbl_option_opco_0.grid(row=1, column=2, sticky=NSEW)
lbl_option_musi_0.grid(row=1, column=1)
lbl_option_toca_0.grid(row=1, column=2, sticky=NSEW) 
btn_option_musi_0.grid(row=1, column=3, sticky=NSEW) 
lbl_option_pyan_0.grid(row=2, column=1)
lbl_option_pyan_1.grid(row=2, column=2, sticky=NSEW) 
btn_option_pyan_0.grid(row=2, column=3, sticky=NSEW) 
lbl_option_ardu_0.grid(row=3, column=1)
lbl_option_comm_0.grid(row=3, column=2, sticky=NSEW) 
btn_option_comm_0.grid(row=3, column=3, sticky=NSEW) 
lbl_option_hist_0.grid(row=4, column=1)
lbl_option_hist_1.grid(row=4, column=2, sticky=NSEW) 
btn_option_hist_0.grid(row=4, column=3, sticky=NSEW) 
lbl_option_gith_0.grid(row=5, column=1)
lbl_option_noss_0.grid(row=5, column=2, sticky=NSEW) 
btn_option_gith_0.grid(row=5, column=3, sticky=NSEW) 
lbl_option_abou_0.grid(row=6, column=1)
lbl_option_abou_1.grid(row=6, column=2, sticky=NSEW) 
btn_option_abou_0.grid(row=6, column=3, sticky=NSEW) 

# ---- TELA DO HISTÓRICO ----
config_historic_titl = design_historico.config_historic_titl()
config_historic_scrl = design_historico.config_historic_scrl()
config_historic_retu = design_historico.config_historic_retu()
config_historic_clea = design_historico.config_historic_clea()
config_historic_text = design_historico.config_historic_text()
config_historic_tops = design_historico.config_historic_tops()

fra_historic_0 = Frame(tela, bg='white')
fra_historic_1 = Frame(fra_historic_0)
fra_historic_2 = Frame(fra_historic_0)
fra_historic_3 = Frame(fra_historic_0)

fra_historic_0.rowconfigure(3, weight=1)
fra_historic_0.grid_columnconfigure(1, weight=1)
fra_historic_1.grid_columnconfigure((1, 2), weight=1)
fra_historic_2.grid_columnconfigure(1, weight=1)
fra_historic_3.grid_columnconfigure((1, 2), weight=1) 
fra_historic_2.rowconfigure(1, weight=1)

lbl_historic_titl_0 = Label    (fra_historic_0, config_historic_titl, text='Histórico')
lbl_historic_hist_0 = Label    (fra_historic_1, config_historic_tops, text='histórico')
lbl_historic_lear_0 = Label    (fra_historic_1, config_historic_tops, text='Aprendizados')
txt_historic_data_0 = Text     (fra_historic_2, config_historic_text)
scl_historic_data_0 = Scrollbar(fra_historic_2, config_historic_scrl)
btn_historic_retu_0 = Button   (fra_historic_3, config_historic_retu, text='Voltar')
btn_historic_clea_0 = Button   (fra_historic_3, config_historic_clea, text='Limpar histórico')

txt_historic_data_0['yscrollcommand'] = scl_historic_data_0.set
scl_historic_data_0['command'] = txt_historic_data_0.yview
btn_historic_retu_0['command'] = lambda: trocar_interface('historic_to_opcoes')
btn_historic_clea_0['command'] =limpar_historico 

fra_historic_1.grid(row=2, column=1, sticky=NSEW)
fra_historic_2.grid(row=3, column=1, sticky=NSEW)
fra_historic_3.grid(row=4, column=1, sticky=NSEW)

lbl_historic_titl_0.grid(row=1, column=1, sticky=EW)
lbl_historic_hist_0.grid(row=1, column=1, sticky=NSEW)
lbl_historic_lear_0.grid(row=1, column=2, sticky=NSEW)
txt_historic_data_0.grid(row=1, column=1, sticky=NSEW)
scl_historic_data_0.grid(row=1, column=2, sticky=NS)
btn_historic_retu_0.grid(row=1, column=1, sticky=EW)
btn_historic_clea_0.grid(row=1, column=2, sticky=EW)

# ---- TELA DO PYANALISE ----
config_pyanalise_icon = design_pyanalise.config_pyanalise_icon()
config_pyanalise_fras = design_pyanalise.config_pyanalise_fras()
config_pyanalise_titl = design_pyanalise.config_pyanalise_titl()
config_pyanalise_desc = design_pyanalise.config_pyanalise_desc()
config_pyanalise_scal = design_pyanalise.config_pyanalise_scal() 
config_pyanalise_comp = design_pyanalise.config_pyanalise_comp() 
config_pyanalise_resu = design_pyanalise.config_pyanalise_resu()

fr_pyanalise_0 = Frame(tela)
fr_pyanalise_0.grid_columnconfigure(1, weight=1)
fr_pyanalise_0.rowconfigure(3, weight=1)

fr_pyanalise_1 = Frame(fr_pyanalise_0, bg='DarkGreen')
fr_pyanalise_2 = Frame(fr_pyanalise_0, bg='white')
fr_pyanalise_3 = Frame(fr_pyanalise_0, bg='white', pady=10)
fr_pyanalise_4 = Frame(fr_pyanalise_0, bg='white')

fr_pyanalise_1.grid_columnconfigure(2, weight=1)
fr_pyanalise_2.grid_columnconfigure(1, weight=1)
fr_pyanalise_3.grid_columnconfigure((1, 2), weight=1)
fr_pyanalise_4.grid_columnconfigure(1, weight=1)
fr_pyanalise_4.rowconfigure(1, weight=1)

btn_pyanalise_retu_0 = Button(fr_pyanalise_1, config_pyanalise_icon, image=img_return)
lbl_pyanalise_pyan_0 = Label (fr_pyanalise_1, config_pyanalise_titl, text='pyanalise')
btn_pyanalise_gith_0 = Button(fr_pyanalise_1, config_pyanalise_icon, image=img_github_py)
lbl_pyanalise_desc_0 = Label (fr_pyanalise_2, config_pyanalise_desc, text='Taxa de variação do Pyanalise')
lbl_pyanalise_fras_0 = Label (fr_pyanalise_3, config_pyanalise_fras, text='frase 1')
lbl_pyanalise_fras_1 = Label (fr_pyanalise_3, config_pyanalise_fras, text='frase 2')
scl_pyanalise_prec_0 = Scale (fr_pyanalise_2, config_pyanalise_scal, from_=1, to=100, orient=HORIZONTAL, command=resize)
ent_pyanalise_fras_0 = Entry (fr_pyanalise_3, config_pyanalise_comp)
ent_pyanalise_fras_1 = Entry (fr_pyanalise_3, config_pyanalise_comp)
lbl_pyanalise_resu_0 = Label (fr_pyanalise_4, config_pyanalise_resu, text='0%')

scl_pyanalise_prec_0.set(precisao_minima)
btn_pyanalise_retu_0['command'] = lambda: trocar_interface('pyananlise_to_opcoes')
btn_pyanalise_gith_0['command'] = lambda: basic.abrir_site('https://github.com/gabrielogregorio/pyanalise')
ent_pyanalise_fras_0.bind('<KeyRelease>', testar_pyanalise)
ent_pyanalise_fras_1.bind('<KeyRelease>', testar_pyanalise)

fr_pyanalise_1.grid(row=0, column=1, sticky=NSEW)
fr_pyanalise_2.grid(row=1, column=1, sticky=NSEW)
fr_pyanalise_3.grid(row=2, column=1, sticky=NSEW)
fr_pyanalise_4.grid(row=3, column=1, sticky=NSEW)

btn_pyanalise_retu_0.grid(row=1, column=1)
lbl_pyanalise_pyan_0.grid(row=1, column=2, sticky=NSEW)
btn_pyanalise_gith_0.grid(row=1, column=3, sticky=NSEW)
lbl_pyanalise_desc_0.grid(row=1, column=1, sticky=NSEW)
scl_pyanalise_prec_0.grid(row=2, column=1, sticky=NSEW)
lbl_pyanalise_fras_0.grid(row=1, column=1)
lbl_pyanalise_fras_1.grid(row=1, column=2)
ent_pyanalise_fras_0.grid(row=2, column=1)
ent_pyanalise_fras_1.grid(row=2, column=2)
lbl_pyanalise_resu_0.grid(row=1, column=1, sticky=NSEW)

# ---- TELA DE MUSICA ----
config_music_retu = design_musica.config_music_retu()
config_music_btns = design_musica.config_music_btns()
config_music_desc = design_musica.config_music_desc()
config_music_toca = design_musica.config_music_toca()
config_music_spac = design_musica.config_music_spac()
config_music_entr = design_musica.config_music_entr()
config_music_fram = design_musica.config_music_fram()

fr_music_0 = Frame(tela, bg='white')
fr_music_1 = Frame(fr_music_0, bg='#3399ff', padx=6)
fr_music_2 = Frame(fr_music_0, bg='white', padx=6)
fr_music_3 = Frame(fr_music_0, bg='white', padx=6)
fr_music_4 = Frame(fr_music_0, bg='white', padx=6)

fr_music_0.grid_columnconfigure(1, weight=1)
fr_music_1.grid_columnconfigure(2, weight=1)
fr_music_2.grid_columnconfigure((1, 2), weight=1)
fr_music_3.grid_columnconfigure((1, 2), weight=1)
fr_music_4.grid_columnconfigure((1, 2), weight=1)

btn_music_retu_0 = Button(fr_music_1, config_music_retu, image=img_return)
lbl_music_toca_0 = Label (fr_music_1, config_music_toca, text='TOCAR MÚSICAS')
lbl_music_musi_0 = Label (fr_music_1, config_music_toca, image=img_music_2)
lbl_music_file_0 = Label (fr_music_2, config_music_desc, text='musica.mp3')
lbl_music_solt_0 = Label (fr_music_2, config_music_desc, text='solta o som ; soltando')
lbl_music_spac_0 = Label (fr_music_2, config_music_spac, image=img_transparent)
lbl_music_spac_1 = Label (fr_music_2, config_music_spac, image=img_transparent)
ent_music_file_0 = Entry (fr_music_4, config_music_entr)
ent_music_comm_0 = Entry (fr_music_4, config_music_entr)
btn_music_addi_0 = Button(fr_music_4, config_music_btns, image=img_add)
btn_music_test_0 = Button(fr_music_4, config_music_btns, text='TESTAR')

load_songs()

btn_music_addi_0['command'] = add_songs
btn_music_retu_0['command'] = lambda: trocar_interface('music_to_opcoes')
btn_music_test_0['command'] = lambda: play_music(ent_music_file_0.get())

fr_music_1.grid(row=0, column=1, sticky=NSEW)
fr_music_2.grid(row=1, column=1, sticky=NSEW)
fr_music_3.grid(row=2, column=1, sticky=NSEW)
fr_music_4.grid(row=3, column=1, sticky=NSEW)

lbl_music_musi_0.grid(row=1, column=3)
lbl_music_file_0.grid(row=1, column=1, sticky=NSEW)
lbl_music_solt_0.grid(row=1, column=2, sticky=NSEW)
lbl_music_spac_0.grid(row=1, column=3, sticky=NSEW)
lbl_music_spac_1.grid(row=1, column=4, sticky=NSEW)
lbl_music_toca_0.grid(row=1, column=2, sticky=NSEW)
btn_music_retu_0.grid(row=1, column=1)
ent_music_file_0.grid(row=1, column=1, sticky=NSEW)
ent_music_comm_0.grid(row=1, column=2, sticky=NSEW)
btn_music_addi_0.grid(row=1, column=3, sticky=NSEW)
btn_music_test_0.grid(row=1, column=4, sticky=NSEW)

# ---- TELA DE COMANDO ----
config_command_retu = design_comando.config_command_retu()
config_command_addi = design_comando.config_command_addi()
config_command_expl = design_comando.config_command_expl()
config_command_titl = design_comando.config_command_titl() 
config_command_help = design_comando.config_command_help()
config_command_desc = design_comando.config_command_desc() 
config_command_seri = design_comando.config_command_seri() 
config_command_test = design_comando.config_command_test()
config_command_entr = design_comando.config_command_entr()

fr_command_0 = Frame(tela, bg='white')
fr_command_1 = Frame(fr_command_0, bg='#3399ff', padx=6)
fr_command_2 = Frame(fr_command_0, bg='white', padx=6)
fr_command_3 = Frame(fr_command_0, bg='white', padx=6)
fr_command_4 = Frame(fr_command_0, bg='white', padx=6)
fr_command_5 = Frame(fr_command_0, bg='white', padx=6)
fr_command_6 = Frame(fr_command_0, bg='white', padx=6)

fr_command_0.grid_columnconfigure(1, weight=1)
fr_command_1.grid_columnconfigure(2, weight=1)
fr_command_2.grid_columnconfigure(1, weight=1)
fr_command_3.grid_columnconfigure((1, 2), weight=1)
fr_command_4.grid_columnconfigure((1, 2), weight=1)
fr_command_5.grid_columnconfigure((1, 2), weight=1)
fr_command_6.grid_columnconfigure(1, weight=1)

btn_command_retu_0 = Button(fr_command_1, config_command_retu, image=img_return)
lbl_command_titl_0 = Label (fr_command_1, config_command_titl, text='COMANDOS')
lbl_command_icon_0 = Label (fr_command_1, config_command_titl, image=img_arduino_2)
lbl_command_desc_0 = Label (fr_command_2, config_command_desc, text='Digite a serial: com4 ou /dev/ttyACM0')
ent_command_seri_0 = Entry (fr_command_2, config_command_seri)
btn_command_test_0 = Button(fr_command_2, config_command_test, text='TESTAR')
lbl_command_envi_0 = Label (fr_command_3, config_command_expl, text='ENVIAR')
lbl_command_coma_0 = Label (fr_command_3, config_command_expl, text='COMANDO ; RESPOSTA')
ent_command_send_0 = Entry (fr_command_5, config_command_entr)
ent_command_comm_0 = Entry (fr_command_5, config_command_entr)
btn_command_addi_0 = Button(fr_command_5, config_command_addi, image=img_add)
btn_command_test_1 = Button(fr_command_5, config_command_test, text='TESTAR')
btn_command_help_0 = Button(fr_command_6, config_command_help, text='AJUDA')

load_commands()

ent_command_seri_0.insert(END, link_serial)
btn_command_addi_0['command'] = add_commands
btn_command_test_0['command'] = lambda: send_serial_message(None, btn_command_test_0)
btn_command_test_1['command'] = lambda: send_serial_message(ent_command_send_0.get(), btn_command_test_1)
btn_command_help_0['command'] = lambda: basic.abrir_site('https://github.com/Combratec/Diana/blob/master/README.md#Como-controlar-um-Ardu%C3%ADno')
btn_command_retu_0['command'] = lambda: trocar_interface('comands_to_opcoes')

fr_command_1.grid(row=0, column=1, sticky=NSEW)
fr_command_2.grid(row=1, column=1, sticky=NSEW)
fr_command_3.grid(row=2, column=1, sticky=NSEW)
fr_command_4.grid(row=3, column=1, sticky=NSEW)
fr_command_5.grid(row=4, column=1, sticky=NSEW)
fr_command_6.grid(row=5, column=1, sticky=NSEW)

btn_command_retu_0.grid(row=1, column=1)
lbl_command_titl_0.grid(row=1, column=2, sticky=NSEW)
lbl_command_icon_0.grid(row=1, column=3)
lbl_command_desc_0.grid(row=1, column=1, columnspan=2, sticky=W)
ent_command_seri_0.grid(row=2, column=1, sticky=NSEW)
btn_command_test_0.grid(row=2, column=2, sticky=NSEW)
lbl_command_envi_0.grid(row=1, column=1)
lbl_command_coma_0.grid(row=1, column=2)
ent_command_send_0.grid(row=1, column=1, sticky=NSEW)
ent_command_comm_0.grid(row=1, column=2, sticky=NSEW)
btn_command_addi_0.grid(row=1, column=3, sticky=NSEW)
btn_command_test_1.grid(row=1, column=4, sticky=NSEW)
btn_command_help_0.grid(row=2, column=1, sticky=NSEW)

tela.mainloop() 
