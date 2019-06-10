#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__      = 'Gabriel Gregório da Silva'
__email__       = 'gabriel.gregorio.1@outlook.com'

__diana__       = 'https://dianachatbot.blogspot.com/'
__description__ = 'Chatbot da Combratec com um método de Inteligência Artificial'
__copyright__   = 'Copyright 2018-2019, Combratec'
__status__      = 'Development'
__date__        = '09/02/2019'
__version__     = '7.2.7'

__project__     = 'https://combratecinova.blogspot.com'
__Social__      = 'https://www.facebook.com/combratec'


'''Passe para o final, você precisa ler os termos, a nota e os créditos dos módulos que foram usados antes de sair editando o código da Diana.
'''

# Carregamento imediato apenas dos módulos necessários
import time
import random
import delimitador
from definicoes import diana
from alternativa import alternativa
try:
 from tkinter import * 
except:
 from Tkinter import * 
try:
 from tkinter import messagebox
except:
 from Tkinter import messagebox

# Definições básicas da tela
tela = Tk() 
tela.resizable(width=False, height=False)
tela.configure(background="white",border=0)
tela.grid_columnconfigure(1, weight=1)
tela.rowconfigure(1, weight=1)
tela.title('Diana chatbot - Combratec Inova')
tela.geometry("446x546+100+100")

global acesso_em_modo_texto
acesso_em_modo_texto = "nao"

# Definição de segurança que analisa o arquivo configurações
# Caso o arquivo configurações não seja localizado é criado um automaticamente através da string "esperado"
def atualizar_dados_de_controle_rec_voz_arqler_total():
        print("...Atualizando dados de controle...")
        esperado = "reconhecimento=1\nfala=1\nmipand=0\nplaysound=0\ngtts=0\npyaudio=0\nspeechRecognition=0\nvariação=079\nproxima_ação=n"
        def criar_arquivo_config():
            try:
                arquivo = open("configurações","r", encoding="utf8")
            except: # O arquivo não foi localizado
                print("... Erro grave! - ARQUIVO NÃO CONFIGURAÇÕES NÃO LOCALIZADO")
                print("... O arquivo configurações não existe!")
                print("... Vou criar ter que criá-lo")
                arquivo = open("configurações","w", encoding="utf8")
                arquivo.write(esperado)
                arquivo.close()
            try:
                arquivo.close() # Fechar o arquivo caso não tenha acontecido erros!
            except:
                pass
        criar_arquivo_config() # Refazer os testes!

        # Agora vamos tentar acessar uma das últimas posições do arquivo
        arquivo = open("configurações","r", encoding="utf8")
        try: 
            status = str(arquivo.read())[108] 
        except:
            print(" ** ** ** ** Erro grave!, POSIÇÃO 108 INEXISTENTE")
            print(" ** ** ** ** A posição não existe")
            print(" ** ** ** ** Vou reescrever o arquivo configurações")
            arquivo = open("configurações","w", encoding="utf8")
            arquivo.write(esperado)
            arquivo.close()
        try:
            arquivo.close()
        except:
            pass
        # Quantidade de caracteres
        arquivo = open("configurações","r", encoding="utf8")
        arquivo_ler = str(arquivo.read())
        total = int(len(arquivo_ler)) 
        arquivo.close()

        # Leitura dos dados de fala
        arquivo = open("configurações","r", encoding="utf8")
        status = str(arquivo.read())[22]
        arquivo.close()
        if status=="0":
            print("fala desativada")
            controlar_voz  = "n"
        else:
            print("fala ativada")
            controlar_voz  = "s"

        # Leitura dos dados de reconhecimento de voz
        arquivo = open("configurações","r", encoding="utf8") # Abrir o arquivo
        status = str(arquivo.read())[15] # Ler o arquivo "0" significa desativado e "1" ativado.
        arquivo.close()
        if status=="0":
            print("Reconhecimento desativado")
            controlar_reconhecimento = "n"
        else:
            print("Reconhecimento ativado")
            controlar_reconhecimento = "s"

        # **** USO DO RETURN ****
        # arquivo = atualizar_dados_de_controle_rec_voz_arqler_total()
        # controlar_reconhecimento = arquivo[0]
        # controlar_voz = arquivo[1]
        # arquivo_ler = arquivo[2]
        # total = arquivo[3]
        return controlar_reconhecimento,controlar_voz,arquivo_ler,total
atualizar_dados_de_controle_rec_voz_arqler_total() # Executar a primeira definição de segurança

'''Pode ser que a diana esteja esperando uma resposta
de uma pergunta feita para ela no ultimo acesso,
isso garante que ao iniciar ela vai recomeçar.'''
# Abertura do arquivo configurações
arquivo = open("configurações","r", encoding="utf8")
acao_geral = str(arquivo.read()) # Leitura de todo o arquivo [IMPORTANTÍSSIMO]
arquivo.close()
# Reset das configurações de criar assunto ou continuar assunto
arquivo = open("configurações","w", encoding="utf8")
acao_modo_texto = acao_geral[0:108]+"n "+acao_geral[109:len(acao_geral)]
arquivo.write(acao_modo_texto)
arquivo.close()

# Análise de funcionalidade e disponibilidade dos módulos
resultados = diana.testa_modulos() # Análise da disponibilidade dos módulos recomendados
mipand = resultados[0]             # Módulo de processamento de dados
os = resultados[1]                 # Inútil até agora
speechrecognition = resultados[2]  # Módulo que de reconhecimento de voz
pyaudio = resultados[3]            # Em analise...
playsound = resultados[4]          # Módulo que executa arquivos de áudio
gtts = resultados[5]               # Módulo que cria arquivos mp3

# Definições em grupos
basico_status = "ok"               # Sistemas básicos
reconhecimento_status = "ok"       # Sistemas de reconhecimento
fala_status = "ok"                 # sistemas de fala

# Etapa de verificação dos módulos para a primeira inicialização
# Módulos básicos indisponíveis
if mipand == "0" or os == "0":
   basico_status = "erro"
   print("****** Módulos básicos não encontrados!") 
# Módulos de reconhecimento de voz
if speechrecognition == "0" or pyaudio == "0":
   reconhecimento_status = "erro"
   print("****** Módulos de reconhecimento de voz não encontrado!")
# Módulos de fala
if playsound == "0" or gtts == "0":
   fala_status = "erro"
   print("****** Módulos de fala não encontrado!")

# Abertura dos dados de precisão do mipand ( É tipo uma confiança para comparar palavras )
arquivo = open("configurações","r", encoding="utf8")       # Abrindo o arquivo configurações
atualizar_variacao = arquivo.read()  # Conversão para string
scale = int(atualizar_variacao[91:94])    # Variação do mipand (Precisão das respostas)
arquivo.close()                           # Fechando o arquivo
print("variação do mipand definida para {}".format(scale)) # Printando a "scale" apenas para confirmação

# Atualização do reconhecimento de voz (Ativado ou Desativado)
def atualiza_configuracoes_reconhecimento(): # Atualização do Reconhecimento de voz
    arquivo = atualizar_dados_de_controle_rec_voz_arqler_total()
    status = arquivo[0]
    arquivo_ler = arquivo[2]
    total = arquivo[3]
    # Se o reconhecimento estava desativado
    if status== "n": 
        print("Reconhecimento ativado")
        arquivo = open("configurações","w", encoding="utf8")
        # Ligando o reconhecimento de voz
        novo = arquivo_ler[0:15]+"1"+arquivo_ler[16:total] 
        arquivo.write(novo)
        arquivo.close()

        # Atualização da imagem da tela de configuração e da tela do menu
        configuracoes_reconhecimento_imagem = PhotoImage(file="Imagens/configurações/ativado.png")
        menu_reconhecimento_img = PhotoImage(file="Imagens/Menu/rec_ati.png")
        
        # redimensionamento de imagens
        configuracoes_reconhecimento_imagem = configuracoes_reconhecimento_imagem.subsample(4,4)

        # Atualização da tela configuração
        configuracoes_reconhecimento_imagem_botao["image"] =configuracoes_reconhecimento_imagem
        configuracoes_reconhecimento_imagem_botao.image = configuracoes_reconhecimento_imagem
        # Atualização da tela menu
        menu_reconhecimento_img_botao["image"] = menu_reconhecimento_img
        menu_reconhecimento_img_botao.image = menu_reconhecimento_img

    if status=="s": # Se o reconhecimento estava ativado
        print("Reconhecimento desativado")
        arquivo = open("configurações","w", encoding="utf8")
        # Desligando o reconhecimento de voz
        novo = arquivo_ler[0:15]+"0"+arquivo_ler[16:total] 
        arquivo.write(novo)
        arquivo.close()

        # Atualização de imagens
        menu_reconhecimento_img = PhotoImage(file="Imagens/Menu/rec_des.png")
        configuracoes_reconhecimento_imagem = PhotoImage(file="Imagens/configurações/desativado.png")

        # Redimensionamento de imagens
        configuracoes_reconhecimento_imagem = configuracoes_reconhecimento_imagem.subsample(4,4)

        # Atualização da tela de configuração
        configuracoes_reconhecimento_imagem_botao["image"] = configuracoes_reconhecimento_imagem
        configuracoes_reconhecimento_imagem_botao.image = configuracoes_reconhecimento_imagem
        # Atualização da tela Menu
        menu_reconhecimento_img_botao["image"] = menu_reconhecimento_img
        menu_reconhecimento_img_botao.image = menu_reconhecimento_img

def atualizar_historico():
   # Etapa de testes do arquivo ( O arquivo pode ter sido removido acidentalmente ) 
    analise_historico = "sim"
    try:
       historico_arquivo = open("Analise/histórico.txt","r", encoding="utf8")
    except:
       print(" **** Arquivo 'histórico.txt' na pasta 'Analise/' não foi encontrado!")
       print(" **** Vou cria-lo!")
       # Impedir a tentativa de fechar o arquivo que deu erro
       analise_historico = "não"
       # Acesso como modo criação < Existe a possibilidade da pessoa estar em uma pasta somente leitura e isso vai falhar! >
       historico_arquivo = open("Analise/histórico.txt","w", encoding="utf8")
       historico_arquivo.write(" ")
       historico_arquivo.close()

    # Caso não tenha acontecido erros
    if analise_historico == "sim":
        historico_arquivo_ler = historico_arquivo.read()
        historico_arquivo.close()

    # Acesso do arquivo histórico
    historico_arquivo = open("Analise/histórico.txt","r", encoding="utf8")
    historico_arquivo_ler = historico_arquivo.read()
    historico_arquivo.close()

    try:
        invalidade = str(historico_arquivo_ler[0]) 
    except:
        print("Histórico completamente vazio!")
        historico_arquivo_ler = " "
    return historico_arquivo_ler
# Correção de eventuais bugs
atualizar_historico()

# Atualização da voz (Ativado ou Desativado)
def atualiza_configuracoes_fala(): # Atualização da Fala
    # Acessar o arquivo e fazer leitura de dados
    arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() 
    status = arquivo[1]
    arquivo_ler = arquivo[2]
    total = arquivo[3]

    if status== "n": # Se a fala estava desativada
        print("fala ativado")
        arquivo = open("configurações","w", encoding="utf8")
        novo = arquivo_ler[0:22]+"1"+arquivo_ler[23:total] # Ativar a fala
        arquivo.write(novo)
        arquivo.close()

        # Atualização da imagem da tela de configuração e da tela do menu
        configuracoes_fala_imagem = PhotoImage(file="Imagens/configurações/ativado.png")
        menu_fala_img = PhotoImage(file="Imagens/Menu/fala_ati.png")

        # Redimensionamento das imagens
        configuracoes_fala_imagem = configuracoes_fala_imagem.subsample(4,4)

        # Atualização da tela de configurações
        configuracoes_fala_imagem_botao["image"] = configuracoes_fala_imagem
        configuracoes_fala_imagem_botao.image = configuracoes_fala_imagem
        # Atualização da tela do menu
        menu_menu_fala_img_botao["image"] = menu_fala_img
        menu_menu_fala_img_botao.image = menu_fala_img

    if status=="s": # Se a voz estava ativada
        print("fala desativado")
        arquivo = open("configurações","w", encoding="utf8")
        novo = arquivo_ler[0:22]+"0"+arquivo_ler[23:total] # desativar a fala
        arquivo.write(novo)
        arquivo.close()

        # Atualização da tela de configuração
        configuracoes_fala_imagem = PhotoImage(file="Imagens/configurações/desativado.png")
        menu_fala_img = PhotoImage(file="Imagens/Menu/fala_des.png")

        # Redimensionamento das imagens
        configuracoes_fala_imagem = configuracoes_fala_imagem.subsample(4,4)
        # Atualização da tela de configurações
        configuracoes_fala_imagem_botao["image"] = configuracoes_fala_imagem
        configuracoes_fala_imagem_botao.image = configuracoes_fala_imagem
        # Atualização da tela do menu
        menu_menu_fala_img_botao["image"] = menu_fala_img
        menu_menu_fala_img_botao.image = menu_fala_img

# Testar os sistemas de voz na tela de configurações
def testar_configuracoes_voz(): 
    print("[teste] - Configurações de voz")
    # Atualizar o Botão
    configuracoes_fala_testar_botao["text"] = "testando ..."
    configuracoes_fala_testar_botao.update()

    # Chamar as definições da diana para executar o processo de geração de fala
    res = diana.saidaAudio("Está tudo funcionando!")   

    # Se acontecer algum erro.
    if res =="ERRO!":
        print("[erro*] - Configurações de voz")
        # Atualizar botão
        configuracoes_fala_testar_botao["text"] = "Algo deu errado!" 
        configuracoes_fala_testar_botao.update()
    else: # Se não houver erros
        print("[teste] - Configurações de voz funcionando!")
        # Atualizar botão
        configuracoes_fala_testar_botao["text"] = "Você me ouviu?" 
        configuracoes_fala_testar_botao.update()

# Teste especial no reconhecimento de voz
def testar_configuracoes_reconhecimento_de_voz():  
    # Atualização de dados
    arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() 
    controlar_reconhecimento = arquivo[0]
    controlar_voz = arquivo[1]

    cancelar="não" # variável de continuidade
    mensagem="Diga alguma coisa: "
    print("[teste] - Reconhecimento de voz!")

    # tentar importar o módulo de reconhecimento
    try:
        import speech_recognition as sr 
    except: 
        # Atualização do label
        configuracoes_reconhecimento_testar_label["text"] = "Preciso do módulo Speechrecognition"
        configuracoes_reconhecimento_testar_label.update()
        print("[erro*] - Reconhecimento de voz!")
        cancelar="sim" # Cancelar a tentativa de escutar

    if cancelar=="não": # Se não aconteceram erros
        try:
            microfone = sr.Recognizer()
        except:
            microfone_nao_localizado()
        with sr.Microphone() as source:
            microfone.adjust_for_ambient_noise(source) # ajuste do ruido
            print("Diga alguma coisa!: ")
            # Atualização do label
            configuracoes_reconhecimento_testar_label["text"] = "Diga alguma coisa!"
            configuracoes_reconhecimento_testar_label.update()
            # Preparação para a esculta
            try:
                audio = microfone.listen(source) 
            except:
                microfone_nao_localizado()
            try:
                frase = microfone.recognize_google(audio,language='pt-BR') # Tentativa de escultar
            except PermissionError: # Erro de permissão
                # atualização do label
                configuracoes_reconhecimento_testar_label["text"] = "Erro de permissão 'PermissionError'" # Exibir mensagem de erro na Label
                configuracoes_reconhecimento_testar_label.update()
                dicas_permissao() # Chamar a definição, que é uma caixa de texto
                cancelar="sim" # Ativa o modo cancelar geral!
                repeticao_respostas = 10
                if controlar_voz == "s":
                    repeticao_respostas = gerar_resposta_repetir(repeticao_respostas)
                    repeticao_respostas = repeticao_respostas+1
            except: # Qualquer outro erro
                print("Erro")
                configuracoes_reconhecimento_testar_label["text"] = "Eu não sei o que esta errado!" # Exibir mensagem de erro na Label
                configuracoes_reconhecimento_testar_label.update()
                cancelar="sim"# Ativa o modo cancelar geral!
            # Se deu certo
            if cancelar=="não": 
                configuracoes_reconhecimento_testar_label["text"] = frase # Exibir a fala da pessoa
                configuracoes_reconhecimento_testar_label.update()

# Controle da precisão do mipand através barra móvel
def resize(event=None):

    arquivo = open("configurações","r", encoding="utf8")
    atualizar_variacao = str(arquivo.read()) # Ler todo o arquivo
    arquivo.close()

    posi_Analise=scale_config.get() # Dizer que essa variável recebe o valor da escala agora
    total_arquivo = int(len(atualizar_variacao)-1) # Atualizar posicionamento para escalas uma escala mais natural
    if posi_Analise==0: # Se o amigão conseguiu a proeza de colocar em zero    
        # Não fazer nada hahaha
        print("* ISSO NÂO PODIA TER ACONTECIDO!, mipand definido para zero!")
    else:  
        arquivo = open("configurações","w", encoding="utf8")
        # Se ele chegou a 100, temos 3 dígitos, portando é só escrever
        if posi_Analise==100: 
            # Povo perfeccionista
            print("...Nenhuma variação tolerada! {}".format(posi_Analise)) 
            # Preparar 3 espaços até o final
            atualizar_variacao = atualizar_variacao[0:91]+str(posi_Analise)+atualizar_variacao[94:total_arquivo+1]  
        # Se for abaixo de 100 e maior que 9, temos 2 dígitos, portanto adicionamos um zero
        elif posi_Analise<100 and posi_Analise>9: 
            print("...Atualizando variação {}".format(posi_Analise))
            # Preparando 1 espaço reserva
            atualizar_variacao = atualizar_variacao[0:91]+"0"+str(posi_Analise)+atualizar_variacao[94:total_arquivo+1] 
        # Se estava abaixo de 10 e maior que 0
        else: 
            # Um peido pode ser reconhecido como uma lâmpada de LED aqui!
            print("...Variação absurda demais! {}".format(posi_Analise)) 
            # reserve 2 casas com zero (O int consegue limpar esses zeros)
            atualizar_variacao = atualizar_variacao[0:91]+"00"+str(posi_Analise)+atualizar_variacao[94:total_arquivo+1] 
        arquivo.write(atualizar_variacao) # escrever a nova variação
        arquivo.close()

# Carregamento de sites em diversas telas - autoexplicativo...
def abrir_site_gtts():
    import webbrowser
    webbrowser.open('https://pypi.org/project/gTTS/')

def abrir_site_playsound():
    import webbrowser
    webbrowser.open('https://pypi.org/project/playsound/')

def abrir_site_mipand():
    import webbrowser
    webbrowser.open('https://github.com/Combratec/mipand/')

def abrir_site_PIP3():
    import webbrowser
    webbrowser.open('https://pypi.org/project/pip/')

def abrir_site_pyaudio():
    import webbrowser
    webbrowser.open('https://pypi.org/project/PyAudio/')

def abrir_site_SPEECHRECOGNITION():
    import webbrowser
    webbrowser.open('https://pypi.org/project/SpeechRecognition/')

def abrir_site_ajuda(): # Abertura de teste [ Efeitos especiais! ou quase... foi um teste ]
    # Escolha da imagem
    menu_ajuda_img = PhotoImage(file="Imagens/Menu/abrindo.png")

    # Atualização da imagem
    menu_ajuda_img_botao["image"] = menu_ajuda_img
    menu_ajuda_img_botao.update()

    # Acessando o site
    import webbrowser
    webbrowser.open('https://dianachatbot.blogspot.com')
    # Delay para volta automática
    time.sleep(2)

    # Escolha da imagem
    menu_ajuda_img = PhotoImage(file="Imagens/Menu/ajuda.png")

    # Atualização da imagem
    menu_ajuda_img_botao["image"] = menu_ajuda_img # Imagem normal voltando
    menu_ajuda_img_botao.image = menu_ajuda_img

class atualizacoes(): # Gerenciador de layouts e eventos
    # Atualização de dados
    arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() 
    controlar_reconhecimento = arquivo[0]
    controlar_voz = arquivo[1]
    arquivo_ler = arquivo[2]
    total = arquivo[3]

    # Sair da tela de load e carregar a tela de testes
    def tela_testes(): 
        print(" ********** Carregando tela de testes ********** ")
        tela_de_load.grid_forget()
        inicia_frame.grid(row=1,column=1,sticky=NSEW)

    # Sair da tela de testes e carregar a tela de menu
    def tela_testes_menu(): 
        print(" ********** Carregando tela do menu ********** ")
        inicia_frame.grid_forget() # Destruir frame testes
        ignorar="nao" # Variável de continuidade

        # Definições de quando vai aparecer a tela de avaliação
        try:
            arquivo = open("Analise/quantidade_acesso.txt","r",encoding="utf8")
        except: 
            ignorar="sim"     # Cancelar todo o tipo de tentativa de acesso ao arquivo
            arquivo_acessar=0 # Definir como 0 a quantidade de acesso.

        # Caso não tenha ocorrido erros
        if ignorar=="nao":
            # verificar se o arquivo é um número inteiro
            try:
                arquivo_acessar = int(arquivo.read())
            except:
                ignorar="sim"     # ignorar geral
                arquivo_acessar=0 # Definir como 0 a quantidade de aceso
            # Se não tiver acontecido erros
            if ignorar=="nao":
                arquivo.close() # fechar o arquivo
        
        # Se a quantidade de acessos na Diana for igual a 4 ou igual a 8, pedir uma avaliação!
        if arquivo_acessar==4 or arquivo_acessar==8:        
            menu_conversar.grid_forget()                 # Destruir o botão conversar 
            menu_avaliar.grid(row=1,column=1,sticky=EW)  # Construir o botão avaliar
   
        # Acessar o arquivo e somar mais um
        arquivo_acessar=str(arquivo_acessar+1)
        arquivo = open("Analise/quantidade_acesso.txt","w",encoding="utf8")
        arquivo.write(arquivo_acessar)
        arquivo.close()

        # Construir o Menu
        frameMenu.grid(row=1,column=1,sticky=NSEW)

    # Sair do menu e carregar o histórico
    def menu_historico(): 
        print(" ********** Carregando tela do histórico ********** ")
        frameMenu.grid_forget()
        # Leitura do histórico
        historico_arquivo = open("Analise/histórico.txt","r", encoding="utf8")
        historico_arquivo_ler = str(historico_arquivo.read())
        historico_arquivo.close()
        
        # Atualização do histórico
        historico_texto_text.delete(1.0, END)                   # Deletar o conteúdo do "Text" da tela histórico se tiver
        historico_texto_text.insert(1.0, historico_arquivo_ler) # Escrever a nova string, recentemente atualizada
        historico_texto_text.see("end")
        frame_historico.grid(row=1,column=1,stick=NSEW)         # Carregar a tela do histórico com as novas atualizações

    # Sair do histórico e volar para o menu
    def historico_menu(): 
        print(" ********** Carregando tela do menu ********** ")
        # Voltar o botão de limpeza ao modo normal
        historico_limpar_botao["text"] = "Limpar histórico" # Animação necessária
        historico_limpar_botao.text = "Limpar histórico"

        frame_historico.grid_forget()              # Destruir a tela do histórico
        frameMenu.grid(row=1,column=1,stick=NSEW)  # Construir a tela de menu

    def menu_interacao(): 
        # Limpeza de resíduos de texto
        # deletar dados de texto da tela escreve / escreve
        texto_tela_5.delete('1.0', END) 
        # Deletar dados da tela que reconhece e escreve
        tela_rec_text.delete('1.0', END)
        # Apenas para deixar claro a proposta da tela pra o usuário
        tela_rec_text.insert(1.0, "Iai, vamos conversar?") 
        # Atualizar dados da tela que você escreve e ela fala

        print(" ********** Carregando tela de interação ********** ")
        # atualização de dados 
        arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() 
        status = arquivo[0]
        controlar_reconhecimento = arquivo[0]
        controlar_voz = arquivo[1]
        arquivo_ler = arquivo[2]
        total = arquivo[3]
        print("Reconhecimento de voz: {}".format(controlar_reconhecimento))
        print("Sistemas de voz:       {}".format(controlar_voz))

        # reconhecimento de voz desativado e fala ativada!
        if controlar_reconhecimento=="n" and controlar_voz=="s": 
            frameMenu.grid_forget()
            # Atualização de cor
            tela.configure(background = "black")
            frame_escreve_fala.grid(row=1,column=1,sticky=NSEW)

        # reconhecimento de voz ativado e fala desativada!
        if controlar_reconhecimento=="s" and controlar_voz=="n": # Com reconhecimento, mas sem a voz
            frameMenu.grid_forget()

            tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/clique-me.png") # Atualizar a imagem (tinha um bug aqui)
            tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
            tela_rec_ouvir["image"] = tela_rec_img_mic
            tela_rec_ouvir.update()  # Imagem já atualizada
            tela_rec_ouvir.image = tela_rec_img_mic # Desnecessário, apenas para tirar todas as dúvidas da atualização de tela
            tela_rec_esc.grid(row=1,column=1,sticky=NSEW) # Tela de reconhecimento de voz e resposta por texto
            tela.configure(background = "black") # definir o fundo como preto

        # reconhecimento de voz ativado e fala ativada!
        if controlar_reconhecimento=="s" and controlar_voz=="s": # Se tudo está ok, partiu tela principal
            frameMenu.grid_forget()
            # Carregamento de imagens
            interacao_esperando_img = PhotoImage(file="Imagens/fala/esperando.png") # Carregando imagem novamente para solucionar outro bug
            # Atualização de imagem
            interacao_esperando_img_botao["image"] = interacao_esperando_img 
            interacao_esperando_img_botao.update()
            interacao_esperando_img_botao.image = interacao_esperando_img # Garantia outra vez
            # Atualização de cor
            tela.configure(background = "white") 
            frame_interacao.grid(row=1,column=1,sticky=NSEW) 

        # reconhecimento de voz desativado e fala desativada!
        if controlar_reconhecimento=="n" and controlar_voz=="n": # Nem um e nem outro pega
            frameMenu.grid_forget()
            # Atualização de cor
            tela.configure(background = "black") 
            tela_5.grid(row=1,column=1,sticky=NSEW) # Tela puramente texto, Ttkinter parece ser horrível nisso!

    # Saindo de uma interação de volta ao menu
    def interacao_menu(): 
        print(" ********** Carregando tela do menu ********** ")

        # Mais um reset para evitar que a tela rec/esc mantenha o acesso em modo texto ativado
        global acesso_em_modo_texto
        # Set de reconhecimento de voz se a tela rec_esc estiver habilitada
        if acesso_em_modo_texto=="sim":
            arquivo = open("configurações","w", encoding="utf8")
            novo = arquivo_ler[0:15]+"1"+arquivo_ler[16:total] 
            arquivo.write(novo)
            arquivo.close()
        acesso_em_modo_texto = "nao"


        tela.configure(background = "white") # Definir fundo de tela como branco
        # Atualização de dados
        arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() 
        status = arquivo[0]
        controlar_reconhecimento = arquivo[0] 
        controlar_voz = arquivo[1]
        arquivo_ler = arquivo[2]
        total = arquivo[3]

        # Abertura do arquivo configurações
        arquivo = open("configurações","r", encoding="utf8")
        acao_geral = str(arquivo.read()) # Leitura de todo o arquivo [IMPORTANTÍSSIMO]
        arquivo.close()
        # Reset das configurações de criar assunto ou continuar assunto
        arquivo = open("configurações","w", encoding="utf8")
        acao_modo_texto = acao_geral[0:108]+"n "+acao_geral[109:len(acao_geral)]
        arquivo.write(acao_modo_texto)
        arquivo.close()

        # Limpeza de resíduos de texto
        # deletar dados de texto da tela escreve / escreve
        texto_tela_5.delete('1.0', END) 
        # Deletar dados da tela que reconhece e escreve
        tela_rec_text.delete('1.0', END)
        # Apenas para deixar claro a proposta da tela pra o usuário
        tela_rec_text.insert(1.0, "Iai, vamos conversar?") 
        # Atualizar dados da tela que você escreve e ela fala

        base = delimitador.delimitar("Iai, vamos conversar!")
        escreve_fala_base = delimitador.delimitar("Olá, vamos conversar!")
        escreve_fala_resposta["text"] = escreve_fala_base 

        # reconhecimento de voz desativado e fala ativada!
        if controlar_reconhecimento=="n" and controlar_voz=="s": 
            frame_escreve_fala.grid_forget()
            frameMenu.grid(row=1,column=1,stick=NSEW)

        # reconhecimento de voz ativado e fala desativada!
        if controlar_reconhecimento=="s" and controlar_voz=="n": # Saindo da tela que reconhece sua voz e que responde escrevendo
            tela_rec_esc.grid_forget()# Tela reconhece e responde escrevendo
            frameMenu.grid(row=1,column=1,stick=NSEW)

        # reconhecimento de voz ativado e fala ativada!
        if controlar_reconhecimento=="s" and controlar_voz=="s": # Saindo da tela divina que está tudo funcionando
            frame_interacao.grid_forget()
            frameMenu.grid(row=1,column=1,stick=NSEW)

        # reconhecimento de voz desativado e fala desativada!
        if controlar_reconhecimento=="n" and controlar_voz=="n": # Saindo da tela "basicona", somente texto
            tela_5.grid_forget()
            frameMenu.grid(row=1,column=1,stick=NSEW)

    # Definição que você sai do menu e vai para as configurações
    def menu_config():
        print(" ********** Carregando tela de configurações ********** ")
        frameMenu.grid_forget()
        tela_frame_configuracoes.grid(row=1,column=1,columnspan=2,sticky=NSEW)

    # Definição que você sai das configurações e volta para o menu
    def config_menu(): 
        print(" ********** Carregando tela do menu ********** ")
        frameMenu.grid(row=1,column=1,stick=NSEW)
        tela_frame_configuracoes.grid_forget()

    # Saindo da tela que reconhece sua voz e responde escrevendo e indo para o histórico
    def reconhece_escreve_historico(): 
        print(" ********** Carregando tela do histórico ********** ")
        tela_rec_esc.grid_forget() # Destruindo a tela
        # Acessando o novo arquivo de histórico
        historico_arquivo = open("Analise/histórico.txt","r", encoding="utf8")
        historico_arquivo_ler = str(historico_arquivo.read()) 
        historico_arquivo.close()
        historico_texto_text.delete(1.0, END) # Destruindo tudo o que tem lá
        historico_texto_text.insert(1.0, historico_arquivo_ler) # Colocando o novo conteúdo, “atualizadão”!!!
        historico_texto_text.see("end")
        frame_historico.grid(row=1,column=1,stick=NSEW) # Exibir a tela

    # Saindo da tela que reconhece a sua voz e responde com texto e indo para o menu
    def reconhece_escreve_menu(): 
        print(" ********** Carregando tela de menu ********** ")
        tela_rec_esc.grid_forget()
        frameMenu.grid(row=1,column=1,stick=NSEW)

    # Saindo da tela que reconhece a sua voz e escreve na tela e indo para a tela de configurações
    def reconhece_escreve_configuracoes(): 
        print(" ********** Carregando tela de configurações ********** ")
        tela_rec_esc.grid_forget()
        tela_frame_configuracoes.grid()

    # Saindo da tela menu e indo para a tela avaliação!!!!
    def menu_avaliacao(): 
        print(" ********** Carregando tela de avaliação ********** ")
        frameMenu.grid_forget()
        frame_telas_de_avaliacao.grid(row=1,column=1,sticky=NSEW)

    # Saindo da tela de avaliação e indo para a tela do menu
    def avaliacao_menu(): 
        print(" ********** Carregando tela do menu ********** ")
        frame_telas_de_avaliacao.grid_forget()

        # Remover o botão avaliar
        menu_avaliar.grid_forget()
        menu_conversar.grid(row=1,column=1,sticky=EW)
        frameMenu.grid(row=1,column=1,stick=NSEW)

# Definição para limpar o histórico!
def limpar_historico(): 
    print("__ LIMPANDO HISTÓRICO __")
    historico_arquivo = open("Analise/histórico.txt","w", encoding="utf8") # Acessando o arquivo do histórico 
    historico_arquivo.write("") # Escrevendo tudo o que nós homens sabemos sobre vocês, mulheres!!!
    historico_arquivo.close()
    historico_limpar_botao["text"] = "Já era!" # Animação necessária
    historico_limpar_botao.text = "Já era!"
    historico_texto_text.delete('1.0', END) # Deletando os dados do "Text" no histórico

# Gerador de respostas criativas e retorna uma palavra
def gerar_res_criativa():

    # Atualização de dados
    arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() 
    controlar_voz = arquivo[1]

    # Sorteio aleatório
    registro_audio = int(random.randint(1,6))

    # Gerador de respostas criativas 
    resposta_padrao = "Entendido!"
    if registro_audio==1: 
        resposta_padrao = "aprendi!"
        link_rep = "Audios/aprendi.mp3"

    elif registro_audio==2: 
        resposta_padrao = "registrado"
        link_rep = "Audios/registrado.mp3"

    elif registro_audio==3:
        resposta_padrao = "salvo"
        link_rep = "Audios/salvo.mp3"

    elif registro_audio==4:
        resposta_padrao = "Saquei"
        link_rep = "Audios/Saquei.mp3"

    elif registro_audio==5:
        resposta_padrao = "Entendi!"
        link_rep = "Audios/Entendi.mp3"

    else:
        resposta_padrao = "Interessante"
        link_rep = "Audios/interessante.mp3"
        # Se temos a voz, execute ela com tudo!   

    if controlar_voz == "s": 
        from playsound import playsound
        playsound(link_rep) 
    return resposta_padrao

def respostas_para_entradas_criativas(entrada):
    print("respostas criativas")
    # Atualização de dados
    arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() 
    controlar_reconhecimento = arquivo[0]
    controlar_voz = arquivo[1]

    # Prepara respostas alternativas e criativas
    retorno = alternativa(entrada) 
                    
    # Definições gerais
    resposta_padrao = "O que você responderia?: "
    diretorio_local = "Audios/responderia.mp3"

    # Gerando respostas criativas
    if retorno =="Você conhece":
        resposta_padrao = "Acho que não, você conhece?: "
        diretorio_local = "Audios/Acho_que_não_você_conhece.mp3"

    elif retorno =="Você sabia":
        resposta_padrao = "Interessante, me diga mais!: "
        diretorio_local = "Audios/Interessante_me_diga_mais.mp3"

    elif retorno =="Você já":
        resposta_padrao = "Definitivamente não, e você?: "
        diretorio_local = "Audios/Definitivamente_não_e_voce.mp3"

    elif retorno =="Você gosta de":
        resposta_padrao = "Você gosta?: "
        diretorio_local = "Audios/voce_gosta.mp3"

    elif retorno =="O que é":
        resposta_padrao = "Não sei, me diga você!: "
        diretorio_local = "Audios/nao_sei_me_diga_voce.mp3"

    elif retorno =="Quando isso":
        resposta_padrao = "Me diga você!: "
        diretorio_local = "Audios/me_diga_voce.mp3"

    elif retorno =="Você pode me recomendar":
        resposta_padrao = "Me recomende primeiro!: "
        diretorio_local = "Audios/me_recomende_primeiro.mp3"

    elif retorno =="Como se diz":
        resposta_padrao = "Como você diria?: "
        diretorio_local = "Audios/como_voce_diria.mp3"

    elif retorno =="O que você recomenda":
        resposta_padrao = "Me recomende primeiro!: "
        diretorio_local = "Audios/me_recomende_primeiro.mp3"

    elif retorno =="Você estava":
        resposta_padrao = "Não, e você?: "
        diretorio_local = "Audios/nao_e_voce.mp3"

    else:
        if controlar_voz  == "s" and controlar_reconhecimento == "n":
            resposta_padrao = "O que você responderia?: "
            diretorio_local = "Audios/responderia.mp3"

    if controlar_voz  == "s":
        from playsound import playsound                      
        playsound(diretorio_local)

    print("Resposta criativa")
    resp_pula = resposta_padrao+"\n"
    escreve_fala_base = delimitador.delimitar(resp_pula)
    escreve_fala_resposta["text"] = escreve_fala_base
    return resposta_padrao

# Gerar respostas para erros excessivos em algumas telas
def gerar_resposta_repetir(repeticao_respostas):
    from playsound import playsound 
    repeticao_respostas_nova = repeticao_respostas
    # Eu não estou ouvindo nada!, você poderia repetir por favor? 
    if repeticao_respostas == 1:
        playsound("Audios/repetir_por_favor.mp3")

    # Eu não estou entendendo o que você está falando, repita!
    elif repeticao_respostas == 2:
        playsound("Audios/entendendo_repetir_por_favor.mp3")

    # Ei, você ativou a internet? Eu preciso dela para escutar!
    elif repeticao_respostas == 3:
        playsound("Audios/ei_internet_para_escultar.mp3")

     # Ei, da um clique no ícone de configurações na tela do menu e teste o reconhecimento de voz!
    elif repeticao_respostas == 4:
        playsound("Audios/ei_teste_reconhecimento.mp3")

       # Ei, Se você entrou aqui por engano, clica no x lá em cima! Pode ser que o seu microfone não esteja funcionando!
    elif repeticao_respostas == 5:
        playsound("Audios/ei_entrou_engano.mp3")

         # Deu por hoje né! Eu não estou ouvindo nada!
    elif repeticao_respostas == 6:
        playsound("Audios/deu_por_hoje.mp3")
        repeticao_respostas_nova = 0

        # Erro de permissão
    elif repeticao_respostas == 10: # Numero especial 
        playsound("Audios/permissao_atencao.mp3")
        tela.destroy()
    return repeticao_respostas_nova

# Processo geral de interação
class processo_rec(): 
    def ouvir_processar(): # Escuta de usuário
        print("\n___Escutar usuário") # Indicador de modo esculta
        # Atualizar dados
        arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() 
        controlar_reconhecimento = arquivo[0]
        controlar_voz = arquivo[1]
        arquivo_ler = arquivo[2]
        total = arquivo[3]

        # Se o reconhecimento de voz estiver ativado
        if controlar_reconhecimento == "s": 

            repeticao_respostas = 1
            manter = "sim" # Uma variável de selo, sabe, se tiver algum "bug" é para ficar aqui mesmo!
            while manter=="sim": 
                import speech_recognition as sr # Os testes já foram feitos! A qui não deve acontecer nenhum erro.
                microfone = sr.Recognizer()
                with sr.Microphone() as source:
                   microfone.adjust_for_ambient_noise(source) # Cuidando do ruido ambiente
                 
                   # Carregamento de imagem
                   interacao_esperando_img = PhotoImage(file="Imagens/fala/ouvindo.png")
                   tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/ouvindo.png")

                   # Atualização da imagem
                   interacao_esperando_img_botao["image"] = interacao_esperando_img 
                   interacao_esperando_img_botao.update()
                   # Carregamento de imagem
                   tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
                   # Atualização da imagem
                   tela_rec_ouvir["image"] = tela_rec_img_mic 
                   tela_rec_ouvir.update()

                   print("____Diga alguma coisa: ") 
                   audio = microfone.listen(source)
                   # Tratamento de erros no microfone
                   try:
                       frase = microfone.recognize_google(audio,language='pt-BR') # Ouvindo sua voz!
                   except PermissionError: # Erro de permissão
                       dicas_permissao()
                       entrada = "" 
                       frase = entrada
                       repeticao_respostas = 10
                   except: # Se a internet caiu, ou você não falou nada, ou deu algum outro bug
                       print("****Erro!") 
                       entrada = "" 
                       frase = entrada 
                entrada = frase 
                print("____",entrada) # Apenas exibir a entrada na tela

                # Tratamento de erros nos resultados
                if entrada == "" or entrada == "ERRO!":
                    print("____Erro")

                    # Carrega imagens da tela de interação
                    interacao_esperando_img = PhotoImage(file="Imagens/fala/falando.png")
                    tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/repita.png")

                    # Atualização da tela de interação
                    interacao_esperando_img_botao["image"] = interacao_esperando_img # Ative a tela de falando
                    interacao_esperando_img_botao.update()
                    # Carrega imagens da tela reconhece | escreve
                    tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
                    # Atualização da tela de reconhece | escreve
                    tela_rec_ouvir["image"] = tela_rec_img_mic 
                    tela_rec_ouvir.update()
                    tela_rec_text.insert(END, "\nDiana: Repita, por favor!") 
                    tela_rec_text.see("end")

                    # Tela com reconhecimento de voz e sem a fala
                    if controlar_voz  == "n" and controlar_reconhecimento == "s": 
                        time.sleep(1) # Espere 2 segundo, para o usuário ler a mensagem na tela

                    if controlar_voz == "s":
                        repeticao_respostas = gerar_resposta_repetir(repeticao_respostas)
                        repeticao_respostas = repeticao_respostas+1

                    manter="sim" # Se deu ruim, pergunte tudo novamente. Até a pessoa falar alguma coisa
                else:
                   tela_rec_text.insert(END, "\nVocê: {}".format(frase)) 
                   tela_rec_text.see("end")
                   manter = "cai fora kkkk"                        # Se deu certo, cai fora!
                   print("____Reconhecimento de voz bem sucedido!") # Apenas para análise de rotina!
        else: # Se o reconhecimento de voz estava desativado
            manter = "sim" # Variável de travamento
            while manter == "sim":
                print("___Entrada de texto via teclado") 

                # Se nós estivermos no modo mais básico
                if controlar_voz  == "n" and controlar_reconhecimento == "n": 
                    entrada = str(entrada_tela_5.get())                       # A 'entrada' vai receber o Entry da tela mais básica
                    entrada_tela_5.delete(0, 'end')                           # Ele vai ser destruído, ou melhor, seu texto vai ser apagado
                    texto_tela_5.insert(END, "\nVocê: {}".format(entrada))    # O Text dessa tela vai receber o que você acabou de digitar
                    texto_tela_5.see("end")
                    if acesso_em_modo_texto=="sim":
                        entrada = str(tela_rec_entry.get())                       # A 'entrada' vai receber o Entry da tela mais básica
                        tela_rec_entry.delete(0, 'end')                           # Ele vai ser destruído, ou melhor, seu texto vai ser apagado
                        tela_rec_text.insert(END, "\nVocê: {}".format(entrada))    # O Text dessa tela vai receber o que você acabou de digitar
                        tela_rec_text.see("end")

                # Se a voz está ativada e o reconhecimento não
                if controlar_voz  == "s" and controlar_reconhecimento == "n": 
                    entrada =str(escreve_fala_entrada.get())            # A entrada vai receber o  Entry dessa tela
                    escreve_fala_entrada.delete(0, 'end')               # Ele vai ser deletado!
                    string = "Você: {}".format(entrada)
                    escreve_fala_base = delimitador.delimitar(string)   # Essa tela está em alfa e o delimitador vão colocar dados no Label
                    escreve_fala_resposta["text"] = escreve_fala_base   # ATUALIZAÇÃO URGENTE

                # Improvável de acontecer! As entradas são tratadas anteriormente
                if entrada=="" or entrada.isspace() or (";" in entrada): # Se uma dessas condições acontecer, pergunte novamente
                    manter = "sim"
                    print("Isso não podia ter acontecido **#*")
                else:
                    manter = "cai fora"

        # Aqui deu tudo certo e o meu  digitado vale a minha entrada
        digitado = entrada 
        # Carregamento de imagem
        interacao_esperando_img = PhotoImage(file="Imagens/fala/pensando.png") # Já que a voz demora, vamos colocar um pensando na parada
        tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/pensando.png")
        # Atualização de imagem da tela interação
        interacao_esperando_img_botao["image"] = interacao_esperando_img
        interacao_esperando_img_botao.image = interacao_esperando_img
        interacao_esperando_img_botao.update()

        # Carregamento de imagem da tela que reconhece a voz e responde escrevendo
        tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
        # Atualização de imagem
        tela_rec_ouvir["image"] = tela_rec_img_mic 
        tela_rec_ouvir.image = tela_rec_img_mic
        tela_rec_ouvir.update()

        # Gerar resposta!
        resultados = diana.processamento(digitado)
        responder = "não"
        precisao_resp = resultados[0]
        assunto_resp = resultados[1]
        posicao_no_assunto_resp = resultados[2]

        # Atualizar variação do mipand!
        arquivo = open("configurações","r", encoding="utf8")
        atualizar_variacao = arquivo.read()
        precisao_esperada_resp = int(atualizar_variacao[91:94])
        arquivo.close()

        # Enviando dados para gerar resposta.
        resposta = diana.gerar_resposta(precisao_resp,assunto_resp,posicao_no_assunto_resp,precisao_esperada_resp) 

        # Se estivermos na tela instantânea com reconhecimento de voz!
        if controlar_voz  == "n" and controlar_reconhecimento == "s":
            time.sleep(1)

        print("____Finaliza escuta de usuário___")
        # Retorna dados básicos
        return digitado,entrada,resultados,responder,precisao_esperada_resp,resposta 

    # Nesse processo, a pessoa perguntou algo que está no final de uma lista, 
    def continuar_assunto(digitado,entrada,assunto_resp,resposta): # Situação de continuar um assunto
        print("\n___Continuar assunto___")
        # Atualização básica de dados
        arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() 
        status = arquivo[0]
        controlar_reconhecimento = arquivo[0]
        controlar_voz = arquivo[1]
        arquivo_ler = arquivo[2]

        resposta_padrao = "Me diga você!"

        # Carregamento de imagem 
        interacao_esperando_img = PhotoImage(file="Imagens/fala/falando.png")
        tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/falando.png")
        # Atualização da imagem
        interacao_esperando_img_botao["image"] = interacao_esperando_img 
        interacao_esperando_img_botao.update()
       
        # Carregamento da imagem        
        tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
        # Atualização da imagem
        tela_rec_ouvir["image"] = tela_rec_img_mic 
        tela_rec_ouvir.update()

        # Se a fala estiver ativada
        if controlar_voz == "s": 
            from playsound import playsound
            # Execute o áudio me diga você!
            playsound("Audios/me_diga_voce.mp3")

        # Atualização de texto da tela reconhece | escreve
        base = delimitador.delimitar("Me diga você!") 
        tela_rec_text.insert(END, "\nDiana: Me diga você!")
        tela_rec_text.see("end")
        

        # Se estamos na tela reconhece | escreve
        if controlar_voz  == "n" and controlar_reconhecimento == "s": 
            time.sleep(1) # Espere um pouquinho ai, para a pessoa conseguir ler né!

        # Se o reconhecimento estiver ativado
        if controlar_reconhecimento == "s": 
           repeticao_respostas = 1
           manter = "sim" 
           while manter=="sim":
              import speech_recognition as sr
              microfone = sr.Recognizer()
              with sr.Microphone() as source:
                 microfone.adjust_for_ambient_noise(source)
                 print("___Diga alguma coisa: ")

                 # Atualizar tela que reconhece | escreve
                 base = delimitador.delimitar("Diga alguma coisa!")
                 
                 # Carregamento de imagem
                 interacao_esperando_img = PhotoImage(file="Imagens/fala/ouvindo.png")
                 # Atualização da imagem central da tela de interação
                 interacao_esperando_img_botao["image"] = interacao_esperando_img
                 interacao_esperando_img_botao.update()

                 # Carregar imagem da tela reconhece | escreve
                 tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/ouvindo.png")
                 tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
                 # Atualizar imagem da tela reconhece | escreve
                 tela_rec_ouvir["image"] = tela_rec_img_mic 
                 tela_rec_ouvir.update()

                 # Inicia a esculta
                 audio = microfone.listen(source)
                 try:
                    frase = microfone.recognize_google(audio,language='pt-BR')
                 except PermissionError:
                    dicas_permissao()
                    entrada = ""
                    frase = entrada
                    repeticao_respostas = 10
                 except:
                    entrada = ""
                    frase = entrada
              entrada = frase
              if entrada == "":
                 # Carregar imagem
                 interacao_esperando_img = PhotoImage(file="Imagens/fala/falando.png")
                 # Atualizar imagem principal da tela de interação
                 interacao_esperando_img_botao["image"] = interacao_esperando_img 
                 interacao_esperando_img_botao.update()

                 # Carregar imagem da tela reconhece | escreve
                 tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/repita.png")
                 tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
                 # Atualizar imagem da tela reconhece escreve
                 tela_rec_ouvir["image"] = tela_rec_img_mic # Atualizar a telinha
                 tela_rec_ouvir.update()
    
                 tela_rec_text.insert(END, "\nDiana: Eu não entendi! Repita, por favor!") 
                 tela_rec_text.see("end")

                 if controlar_voz == "s":
                     repeticao_respostas = gerar_resposta_repetir(repeticao_respostas)
                     repeticao_respostas = repeticao_respostas+1
                 manter="sim"
              else:
                 tela_rec_text.insert(END, "\nVocê: {}".format(frase)) 
                 tela_rec_text.see("end")
                 manter = "cai fora kkkk" # Uffa, deu tudo certo!

        # Carregando tela imagem da tela de interação
        interacao_esperando_img = PhotoImage(file="Imagens/fala/falando.png")
        # Atualizando imagem da tela de interação
        interacao_esperando_img_botao["image"] = interacao_esperando_img
        interacao_esperando_img_botao.update()

        # Carrega a imagem
        tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/falando.png") 
        tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
        # Atualizar imagem da tela reconhece | escreve
        tela_rec_ouvir["image"] = tela_rec_img_mic
        tela_rec_ouvir.update()

        # Adaptação mais simples """ Apenas par enviar os dados para o autocompletar e para o histórico
        resposta = entrada
        pergunta = digitado

        # Enviando para a definições autocompletar da Diana
        diana.continuar_assunto(assunto_resp,resposta) 

        # Vamos salvar os dados no histórico!
        diana.salvaHistorico(pergunta,resposta)

        # Gera uma resposta criativa, executa o som e retorna a resposta | ÁREA SUJEITA A BUGS |
        resposta_alternativa = gerar_res_criativa()

        # Atualizar a tela reconhece | escreve
        base = delimitador.delimitar("Diana: {}".format(resposta_alternativa)) 
        tela_rec_text.insert(END, "\nDiana: {}\n".format(resposta_alternativa))
        tela_rec_text.see("end")
        
        # Atualização de resposta
        print("Diana: {}".format(resposta_alternativa))

        # Carregamento de imagem
        interacao_esperando_img = PhotoImage(file="Imagens/fala/esperando.png")
        tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/clique-me.png")
        # Atualização de imagem
        interacao_esperando_img_botao["image"] = interacao_esperando_img 
        interacao_esperando_img_botao.update()
        interacao_esperando_img_botao.image = interacao_esperando_img # Normalizando a tela de padrão

        # Carregamento de imagem da tela reconhece | escreve
        tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
        # Atualizando a imagem da tela reconhece | escreve
        tela_rec_ouvir["image"] = tela_rec_img_mic
        tela_rec_ouvir.update()
        tela_rec_ouvir.image = tela_rec_img_mic 

        # Modo continuar assunto finalizado
        print("___Finaliza continuar assunto___")

    # Modo criar assunto
    def criar_assunto(digitado,entrada,resposta):
        print("___Criar assunto___ especial")

        # Atualização de dados
        arquivo = atualizar_dados_de_controle_rec_voz_arqler_total()
        status = arquivo[0]
        controlar_reconhecimento = arquivo[0]
        controlar_voz = arquivo[1]
        arquivo_ler = arquivo[2]
        total = arquivo[3]

        # Carregamento de imagem
        interacao_esperando_img = PhotoImage(file="Imagens/fala/falando.png")
        tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/falando.png")
        # Atualização de imagem
        interacao_esperando_img_botao["image"] = interacao_esperando_img
        interacao_esperando_img_botao.update()

        tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
        # Atualização de imagem
        tela_rec_ouvir["image"] = tela_rec_img_mic
        tela_rec_ouvir.update()

        # Gerador de respostas criativas | ÁREA SUSCETÍVEL A BUGS |
        resposta_padrao = respostas_para_entradas_criativas(entrada)

        # Atualização da tela reconhece escreve
        base = delimitador.delimitar("Diana: {}".format(resposta_padrao))
        tela_rec_text.insert(END, "\nDiana: {}\n".format(resposta_padrao)) 
        tela_rec_text.see("end")
        
        # tempinho para a pessoa pensar...
        time.sleep(1.5) 

        # Variável para dar respostas diferentes quando a Diana não entender algo
        repeticao_respostas = 1

        # Se o reconhecimento de voz estiver ativo
        if controlar_reconhecimento == "s": 
            manter = "sim" # Selo de continuidade
            while manter=="sim":
                import speech_recognition as sr
                microfone = sr.Recognizer()
                with sr.Microphone() as source:
                   microfone.adjust_for_ambient_noise(source)

                   # Atualização da tela reconhece | escreve
                   base = delimitador.delimitar("Diana: Diga alguma coisa!")

                   # Carregamento de imagem
                   interacao_esperando_img = PhotoImage(file="Imagens/fala/ouvindo.png")
                   tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/ouvindo.png")
                   # Atualização de imagem
                   interacao_esperando_img_botao["image"] = interacao_esperando_img # Atualizar Imagem da melhor tela do mundo
                   interacao_esperando_img_botao.update()

                   # Carregamento de imagem
                   tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
                   # Atualização de imagem
                   tela_rec_ouvir["image"] = tela_rec_img_mic
                   tela_rec_ouvir.image = tela_rec_img_mic # Atualizar imagem da telinha
                   tela_rec_ouvir.update()

                   print("___Diga alguma coisa: ") 

                   # Esculta do usuário
                   audio = microfone.listen(source)
                   try:
                       frase = microfone.recognize_google(audio,language='pt-BR') 
                   except PermissionError: # Erro de permissão
                       dicas_permissao()
                       entrada = ""
                       frase = entrada
                       repeticao_respostas = 10
                   except:                 # Outros tipos de erros
                       entrada = ""
                       frase = entrada
                entrada = frase
                if entrada == "": # ERRO QUALQUER
                    print("nenhum conteudo encontrado")
                    # Carregamento de imagem
                    interacao_esperando_img = PhotoImage(file="Imagens/fala/falando.png")
                    tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/repita.png") 
                    # Atualização de imagem
                    interacao_esperando_img_botao["image"] = interacao_esperando_img
                    interacao_esperando_img_botao.update()

                    # Mensagem para o usuário repetir
                    tela_rec_text.insert(END, "\nDiana: Não consigo ouvir nada!") 
                    tela_rec_text.see("end")

                    tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
                    # Atualização de imagem
                    tela_rec_ouvir["image"] = tela_rec_img_mic
                    tela_rec_ouvir.update()

                    if controlar_voz == "s":
                        repeticao_respostas = gerar_resposta_repetir(repeticao_respostas)
                        repeticao_respostas = repeticao_respostas+1
                    manter="sim"
                else:
                    tela_rec_text.insert(END, "\nVocê: {}".format(frase)) 
                    tela_rec_text.see("end")
                    print("Você: {}".format(entrada))
                    manter = "cai fora kkkk"

        resposta = entrada # Deu tudo certo
        diana.criar_assunto(digitado,resposta) # Diana definições criando um novo assunto
        pergunta = digitado 

        # Salvando dados no histórico
        diana.salvaHistorico(pergunta,resposta) 
        interacao_esperando_img = PhotoImage(file="Imagens/fala/falando.png")
        interacao_esperando_img_botao["image"] = interacao_esperando_img # Atualizar a imagem da melhor tela do mundo
        interacao_esperando_img_botao.update()

        # Gera uma resposta criativa, executa o som e retorna a resposta
        segunda_resposta_padrao = gerar_res_criativa()

        # Atualizar a tela reconhece | escreve
        base = delimitador.delimitar("Diana: {}".format(segunda_resposta_padrao)) 
        tela_rec_text.insert(END, "\nDiana: {}".format(segunda_resposta_padrao))
        tela_rec_text.see("end")
        
        print("Diana: {}".format(segunda_resposta_padrao))
        # Carregamento de imagem
        interacao_esperando_img = PhotoImage(file="Imagens/fala/esperando.png")
        tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/clique-me.png")
        # Atualização de imagem
        interacao_esperando_img_botao["image"] = interacao_esperando_img # Normalizando a melhor tela do mundo
        interacao_esperando_img_botao.update()
        interacao_esperando_img_botao.image = interacao_esperando_img

        tela_rec_img_mic = tela_rec_img_mic.subsample(3,3) 
        # Atualização da imagem
        tela_rec_ouvir["image"] = tela_rec_img_mic
        tela_rec_ouvir.update()
        tela_rec_ouvir.image = tela_rec_img_mic 

        print("___Finaliza criar assunto___")

    def criar_assunto_modo_texto(digitado,entrada,resposta): # Modo criar assunto
        global acesso_em_modo_texto
        print("\n___Criar assunto no modo texto___")
        # Dentro da tolerância do mipand, caso não haja semelhança entre o que você
        # digitou e o os dados do banco de dados, vamos ter que criar uma lista
        # É aqui que á mágica acontece! Mas, esse é o modo texto
        arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() #Atualização de dados
        status = arquivo[0]
        controlar_reconhecimento = arquivo[0]
        controlar_voz = arquivo[1]
        arquivo_ler = arquivo[2]
        total = arquivo[3]

        # Se a tela que você digita e ela fala estiver ativa
        if controlar_voz  == "s" and controlar_reconhecimento == "n": 
            entrada =str(escreve_fala_entrada.get()) # A entrada já vai receber o conteúdo do Entrty
            escreve_fala_entrada.delete(0, 'end')    # Deletar sua fala, a Diana vai responder na fala
            string="Você: {}".format(entrada)
            base = delimitador.delimitar(string)     # Delimitar. Atualizar para Text por favor!
            escreve_fala_resposta["text"] =  base
        else: # Se não, ou seja, nossa telinha
            entrada = str(entrada_tela_5.get())      # Entry da telinha que você fala e ela escreve
            entrada_tela_5.delete(0, 'end')          # Deletar toda a bagaça!
            texto_tela_5.insert(END, "Você: {}".format(entrada)) # Colocar sua resposta no Text
            texto_tela_5.see("end")
            if acesso_em_modo_texto=="sim":
                entrada = str(tela_rec_entry.get())  # Entry da telinha que você fala e ela escreve
                tela_rec_entry.delete(0, 'end')      # Deletar toda a bagaça!
                tela_rec_text.insert(END, "Você: {}".format(entrada)) # Colocar sua resposta no Text
                tela_rec_text.see("end")

        # Criar assunto_no arquivo
        resposta = entrada # Aqui deu tudo certo!
        diana.criar_assunto (digitado,resposta) # Criar assunto, assunto criado!
        pergunta = digitado 

        diana.salvaHistorico(pergunta,resposta) # salvar dados no histórico

        # Esse trecho pode ser removido.
        escreve_fala_imagem = PhotoImage(file="Imagens/tela_fala_escreve/falando.png")
        escreve_fala_imagem_btn["image"] = escreve_fala_imagem
        escreve_fala_imagem_btn.update()

        # Gera uma resposta criativa, executa o som e retorna a resposta
        resposta_padrao = gerar_res_criativa()

        escreve_fala_imagem = PhotoImage(file="Imagens/tela_fala_escreve/esperando.png")
        escreve_fala_imagem_btn["image"] = escreve_fala_imagem
        escreve_fala_imagem_btn.image = escreve_fala_imagem

        string = "Diana: {}".format(resposta_padrao)
        base = delimitador.delimitar(string) # Delimitar, atualizar para text por favor!
        escreve_fala_resposta["text"] =  base

        tela_rec_text.insert(END, "\nDiana: {}\n".format(resposta_padrao))
        tela_rec_text.see("end")

        texto_tela_5.insert(END, "\nDiana: {}\n".format(resposta_padrao))
        texto_tela_5.see("end")
        print("___Finaliza criar assunto no modo texto___")

    def continuar_assunto_modo_texto(digitado, entrada, assunto_resp, resposta): # Modo continuar, mas no modo texto puro
        print("\n___Continuar assunto em modo texto___")
        global acesso_em_modo_texto
        arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() # Atualização de dados
        status = arquivo[0]
        controlar_reconhecimento = arquivo[0]
        controlar_voz = arquivo[1]
        arquivo_ler = arquivo[2]
        total = arquivo[3]

        if controlar_voz  == "s" and controlar_reconhecimento == "n": # Se eu estou no modo escrevo e recebo a fala
            entrada =str(escreve_fala_entrada.get()) # Pegar dados do Entry 
            escreve_fala_entrada.delete(0, 'end') # Deletar dados do Entry
            string = "Você: {}".format(entrada)
            base = delimitador.delimitar(string) # Delimitar, atualizar para text por favor!
            escreve_fala_resposta["text"] = base
        else:
            entrada = str(entrada_tela_5.get()) # Ler dados do modo mais básico
            entrada_tela_5.delete(0, 'end') # Deletar dados do modo mais básico
            texto_tela_5.insert(END, "Você: {}".format(entrada)) # Inserira sua resposta
            texto_tela_5.see("end")
            if acesso_em_modo_texto=="sim":
                entrada = str(tela_rec_entry.get()) # Ler dados do modo mais básico
                tela_rec_entry.delete(0, 'end') # Deletar dados do modo mais básico
                tela_rec_text.insert(END, "Você: {}".format(entrada)) # Inserira sua resposta
                tela_rec_text.see("end")

        resposta = entrada     
        diana.continuar_assunto(assunto_resp,resposta) # Continuando assunto!
        pergunta = digitado

        diana.salvaHistorico(pergunta,resposta) # Salvando dados no histórico!
    
        escreve_fala_imagem = PhotoImage(file="Imagens/tela_fala_escreve/falando.png")
        escreve_fala_imagem_btn["image"] = escreve_fala_imagem
        escreve_fala_imagem_btn.update()

        # Gera uma resposta criativa, executa o som e retorna a resposta
        resposta_padrao = gerar_res_criativa()

        escreve_fala_imagem = PhotoImage(file="Imagens/tela_fala_escreve/esperando.png")
        escreve_fala_imagem_btn["image"] = escreve_fala_imagem
        escreve_fala_imagem.image = escreve_fala_imagem

        string = "Diana: {}".format(resposta_padrao)
        base = delimitador.delimitar(string) # Delimitar, atualizar para text por favor!
        escreve_fala_resposta["text"] = base # Atualizar o texto do escreve ele fala

        tela_rec_text.insert(END, "\nDiana: {}\n".format(resposta_padrao))
        tela_rec_text.see("end")

        texto_tela_5.insert(END, "\nDiana: {}\n".format(resposta_padrao)) # Atualizar o texto do modo mais básico
        texto_tela_5.see("end")
        print("___Finaliza continuar assunto___")

    # Esse modo vai reproduzir a resposta encontrada
    def responder_apenas(resposta,entrada):
        print("Resposta direta")

        global acesso_em_modo_texto # Variável para o rec/esc se passar pelo esc/esc

        arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() # Atualizar dados
        status  = arquivo[0]
        controlar_reconhecimento = arquivo[0]
        controlar_voz = arquivo[1]
        arquivo_ler   = arquivo[2]
        total = arquivo[3]

        pergunta = entrada # Adaptação para os nomes dessa definição
        # Se a voz estiver ativada
        if controlar_voz == "s":
            from gtts import gTTS                # Módulo que gera arquivo de fala em mp3
            from playsound import playsound      # Módulo que executa arquivos em mp3
            tts = gTTS(text=resposta, lang='pt') # configuração do gerador
            tts.save("ultima_resposta.mp3")      # Gerando o som

            # Atualizar a parte visual das telas, principal, esc/voz e rec/esc
            interacao_esperando_img = PhotoImage(file="Imagens/fala/falando.png")
            escreve_fala_imagem = PhotoImage(file="Imagens/tela_fala_escreve/falando.png")
            tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/falando.png")

            # Redimensionamento de imagens
            tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)

            # Atualiza tela principal
            interacao_esperando_img_botao["image"] = interacao_esperando_img
            interacao_esperando_img_botao.update()
            # Atualiza tela escreve/fala
            escreve_fala_imagem_btn["image"] = escreve_fala_imagem
            escreve_fala_imagem_btn.update()
            # Atualiza tela rec/esc
            tela_rec_ouvir["image"] = tela_rec_img_mic 
            tela_rec_ouvir.update()
            
            # Modo antigo, esc/voz
            string = "Diana: "+resposta
            base = delimitador.delimitar(string) # reposta da Diana!
            escreve_fala_resposta["text"] = base # Modo escreve e ela fala

            # Modo reconhece a voz e escreve
            tela_rec_text.insert(END, "\nDiana: {} ".format(resposta))
            tela_rec_text.see("end")

            playsound("ultima_resposta.mp3") # Executar o arquivo
            print("___Diana disse: ",resposta)
            #diana.salvaHistorico(pergunta,resposta) # Salvar no histórico
        else: # Fala desativada, exibe apenas a resposta
            print("___",resposta)
            texto_tela_5.insert(END, "\nDiana: {}\n".format(resposta))
            texto_tela_5.see("end")
            tela_rec_text.insert(END, "\nDiana: {}\n".format(resposta))
            tela_rec_text.see("end")
            
        interacao_esperando_img = PhotoImage(file="Imagens/fala/esperando.png")
        interacao_esperando_img_botao["image"] = interacao_esperando_img # Atualiza melhor tela do mundo
        interacao_esperando_img_botao.image = interacao_esperando_img            

        escreve_fala_imagem = PhotoImage(file="Imagens/tela_fala_escreve/esperando.png")
        escreve_fala_imagem_btn["image"] = escreve_fala_imagem
        escreve_fala_imagem_btn.image = escreve_fala_imagem

        tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/clique-me.png")
        tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
        tela_rec_ouvir["image"] = tela_rec_img_mic # atualiza tela ouve e escreve
        tela_rec_ouvir.image = tela_rec_img_mic

        print("___atualizando histórico")
        diana.salvaHistorico(pergunta,resposta) # Salvo no histórico

        if resposta=="É diana chatbot, vou te mostrar !":
            import webbrowser
            webbrowser.open('https://dianachatbot.blogspot.com')
        print("___Finaliza resposta direta___")


    def controlador_partes(): # Controla a execução de tarefas
        print("_Controlador de etapas")
        
        global acesso_em_modo_texto

        arquivo = open("configurações","r", encoding="utf8")
        acao_geral = str(arquivo.read()) # Leitura de todo o arquivo [IMPORTANTÍSSIMO]
        acao_modo_texto = acao_geral[108] # c/d/n o que fazer, nada, criar assunto ou continuar assunto
        arquivo.close()

        arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() # Atualização básica
        status  = arquivo[0]
        controlar_reconhecimento = arquivo[0]
        controlar_voz = arquivo[1]
        arquivo_ler   = arquivo[2]
        total = arquivo[3]

        if acao_modo_texto=="c":
            print("__Continuar assunto")
            # Cancelamento das ações especiais
            arquivo = open("configurações","w", encoding="utf8")
            acao_modo_texto = acao_geral[0:108]+"n "+acao_geral[109:len(acao_geral)]
            arquivo.write(acao_modo_texto) # Normalizar para a próxima execução
            arquivo.close()

            import ast
            # Nesse arquivo fica salvo uma string na forma de tupla que contém dados da última interação em modo texto
            arquivo = open("analise_principal","r", encoding="utf8")
            arquivo_leitura = str(arquivo.read())
            arquivo.close()

            # Convertendo a string para tupla acessível
            var = arquivo_leitura
            analise  = ast.literal_eval(var)
            digitado = analise[0]
            entrada  = analise[1]
            resultados = analise[2]
            responder  = analise[3]
            resposta   = analise[5]
            precisao_resp = resultados[0]
            assunto_resp  = resultados[1]
            posicao_no_assunto_resp = resultados[2]

            # Atualização da variação
            arquivo = open("configurações","r", encoding="utf8")
            atualizar_variacao = arquivo.read()
            precisao_esperada_resp = int(atualizar_variacao[91:94])
            arquivo.close()

            # Acessar o modo criar assunto com os dados da tupla
            processo_rec.criar_assunto_modo_texto(digitado, entrada,resposta) # Executar processo de criar assunto

        elif acao_modo_texto=="d":
            print("__Continuar o assunto")
            # Normalização da ação modo texto
            arquivo = open("configurações","w", encoding="utf8")
            acao_modo_texto = acao_geral[0:108]+"n"+acao_geral[109:len(acao_geral)] 
            arquivo.write(acao_modo_texto)
            arquivo.close()

            import ast
            # Conversão da tupla para string com os dados da última interação
            arquivo = open("analise_principal","r", encoding="utf8")
            arquivo_leitura = str(arquivo.read())
            arquivo.close()

            var = arquivo_leitura
            analise    = ast.literal_eval(var)
            digitado   = analise[0]
            entrada    = analise[1]
            resultados = analise[2]
            responder  = analise[3]
            resposta   = analise[5]
            precisao_resp = resultados[0]
            assunto_resp  = resultados[1]
            posicao_no_assunto_resp = resultados[2]

            # Atualização da variação
            arquivo = open("configurações","r", encoding="utf8")
            atualizar_variacao = arquivo.read()
            precisao_esperada_resp = int(atualizar_variacao[91:94])
            arquivo.close()

            processo_rec.continuar_assunto_modo_texto(digitado, entrada, assunto_resp, resposta) # Processo de criar assunto
        else:
            print("__Modo ouvir e interpretar")
            # Processar e obter as informações da resposta
            analise = processo_rec.ouvir_processar() # resposta padrão > digitado,entrada,resultados,responder,precisao_esperada_resp,resposta 

            # conversão da tupla em string
            arquivo = open("analise_principal","w", encoding="utf8")
            arquivo.write(str(analise))
            arquivo.close()

            # obtenção de dados da tupla análise
            digitado = analise[0]
            entrada = analise[1]
            resultados = analise[2]
            responder = analise[3]
            resposta = analise[5]
            precisao_resp = resultados[0]
            assunto_resp = resultados[1]
            posicao_no_assunto_resp = resultados[2]

            # Atualização da variação
            arquivo = open("configurações","r", encoding="utf8")
            atualizar_variacao = arquivo.read()
            precisao_esperada_resp = int(atualizar_variacao[91:94])
            arquivo.close()

            if resposta =="__CRIAR NOVO ASSUNTO__": # C DE CRIAR ASSUNTO
                print("___Modo criar assunto")
                if controlar_reconhecimento == "n":
                    print("___Armazenar  o c para a próxima interação")
                    print("___Reconhecimento de voz desativado")
                    # Setar o arquivo como c
                    arquivo = open("configurações","w", encoding="utf8")
                    acao_modo_texto = acao_geral[0:108]+"c "+acao_geral[109:len(acao_geral)]
                    arquivo.write(acao_modo_texto)
                    arquivo.close()

                    # gerador de respostas criativas
                    resposta_padrao = respostas_para_entradas_criativas(entrada)                 
                    # Tela puramente escrita
                    texto_tela_5.insert(END, "\nDiana: {}\n".format(resposta_padrao))
                    texto_tela_5.see("end")
                    # Tela reconhece e responde escrevendo
                    tela_rec_text.insert(END, "\nDiana: {}\n".format(resposta_padrao))
                    tela_rec_text.see("end")
                else:
                    print("___Modo criar assunto direto")
                    processo_rec.criar_assunto(digitado,entrada,resposta)

            elif resposta =="__CONTINUAR LISTA__": #D DE CONTINUAR LISTA
                print("__Continuar assunto_")
                if controlar_reconhecimento == "n":
                    print("___Marcar o d para continuar assunto")
                    arquivo = open("configurações","w", encoding="utf8")
                    acao_modo_texto = acao_geral[0:108]+"d "+acao_geral[109:len(acao_geral)]
                    arquivo.write(acao_modo_texto)
                    arquivo.close()

                    # Gerador de repostas para entradas criativas
                    resposta_padrao = respostas_para_entradas_criativas(entrada)

                    # Tela voz/esc
                    if controlar_voz  == "s" and controlar_reconhecimento == "n":
                        variavel_limpa = "Diana: {}".format(resposta_padrao)
                        escreve_fala_base = delimitador.delimitar(variavel_limpa)
                        escreve_fala_resposta["text"] = escreve_fala_base

                    # Tela esc/esc
                    texto_tela_5.insert(END, "\nDiana: {}\n".format(resposta_padrao))
                    texto_tela_5.see("end")

                    # Tela rec/esc
                    tela_rec_text.insert(END, "\nDiana: {}\n".format(resposta_padrao))
                    tela_rec_text.see("end")
                else:
                    print("___Modo continuar assunto direto")
                    processo_rec.continuar_assunto(digitado,entrada,assunto_resp,resposta)
            else:
                print("__Resposta encontrada")

                # responder a pergunta
                processo_rec.responder_apenas(resposta,entrada)
            print("Finaliza controlador de partes\n")

    ''' Essa definição analisa a entrada de arquivos e decide se vai transferir 
     as perguntas para o gerador de respostas da Diana '''
    def transferir_controlador_partes():
        print("Tranferência do controlador de partes")
        arquivo = atualizar_dados_de_controle_rec_voz_arqler_total() # Atualizar dados
        status = arquivo[0]
        controlar_reconhecimento = arquivo[0]
        controlar_voz = arquivo[1]
        arquivo_ler = arquivo[2]
        total = arquivo[3]

        # Variável usada para fazer o modo: rec/esc se passar pelo esc/esc
        global acesso_em_modo_texto

        # Modo esc/esc e variável acesso em modo texto não funcionando
        if controlar_voz  == "n" and controlar_reconhecimento == "n" and acesso_em_modo_texto!="sim":
            print("Modo esc/esc g_amt!=sim")
            entrada = str(entrada_tela_5.get())
            if entrada=="" or entrada.isspace() or (";" in entrada): 
                print("***Eu não vou responder se você digitar '' ou ';' ou apenas espaços sem nada")
                texto_tela_5.insert(END, "\nSem caracteres malucos por favor!")
                texto_tela_5.see("end")
            else:
                print("Gerar resposta")
                processo_rec.controlador_partes() # Continuar
            entrada_tela_5.delete(0, 'end')

        # Modo esc/esc e variável acesso em modo texto funcionamento
        if controlar_voz  == "n" and controlar_reconhecimento == "n" and acesso_em_modo_texto=="sim":
            print("Modo esc/esc g_amt==sim")
            entrada = str(tela_rec_entry.get())
            if entrada=="" or entrada.isspace() or (";" in entrada): 
                print("***Eu não vou responder se você digitar '' ou ';' ou apenas espaços sem nada")
                tela_rec_text.insert(END, "\nSem caracteres malucos por favor!")
                tela_rec_text.see("end")
            else:
                print("Gerar resposta")
                processo_rec.controlador_partes() # Continuar
            tela_rec_entry.delete(0, 'end')

        if controlar_voz  == "s" and controlar_reconhecimento == "n":
            print("Modo voz/esc")
            entrada =str(escreve_fala_entrada.get()) 
            if entrada=="" or entrada.isspace() or (";" in entrada): # Se uma dessas condições acontecer, pergunte novamente
                print("***Eu não vou responder se você digitar '' ou ';' ou apenas espaços sem nada")
                escreve_fala_base = delimitador.delimitar("Sem caracteres malucos por favor!")
                escreve_fala_resposta["text"] =  escreve_fala_base 
            else:
                print("Gerar resposta")
                processo_rec.controlador_partes()
            escreve_fala_entrada.delete(0, 'end')

        if controlar_voz  == "n" and controlar_reconhecimento == "s" and acesso_em_modo_texto=="sim:":
            print("Modo esc/rec amt==sim")
            entrada = str(tela_rec_entry.get())
            if entrada=="" or entrada.isspace() or (";" in entrada): 
                print("***Eu não vou responder se você digitar '' ou ';' ou apenas espaços sem nada")
                tela_rec_text.insert(END, "\nSem caracteres malucos por favor!")
                tela_rec_text.see("end")
            else:
                print("Gerar resposta")
                processo_rec.controlador_partes() # Continuar
            tela_rec_entry.delete(0, 'end')

# Telas de avaliação
def microfone_nao_localizado():
    print("*** Não tem microfone ***")
    messagebox.showinfo("Temos um problema!", "Parece que você não tem microfone!")
    
def acao_primeira_tela():
    print("*** Oi? ***")
    messagebox.showinfo("Isso é um erro!", "Não posso deixar você cometer uma burrada dessas!")

def dicas_permissao():
    print("*** Mensagem - Permission ***")
    messagebox.showinfo("Erro de permissão","Se por acaso eu estiver sendo executada dentro de um pen drive, pode ser que ele esteja me bloqueando! Me transfira para a sua Desktop por favor! ")

def acao_segunda_estrela():
    print("___Clique na segunda estrela___")
    frame_inicial_avaliacao.grid_forget()
    frame_segunda_estrela.grid(row=1,column=1,sticky=NSEW)
    terceira_estrela_label.grid(row=1,column=1,sticky=NSEW)
    segunda_estrela_label.update()
    time.sleep(4)
    
    segunda_estrela_label["foreground"] = "orange"
    segunda_estrela_label["text"] = "Sabia que eu sou uma \nversão beta?"
    segunda_estrela_label.update()
    time.sleep(4)
    
    segunda_estrela_label["foreground"] = "red"
    segunda_estrela_label["text"] = "Sabia que essa é a minha\n primeira interface\n gráfica?"
    segunda_estrela_label.update()
    time.sleep(4)
    
    segunda_estrela_label["foreground"] = "black"
    segunda_estrela_label["text"] = "Você não tem coração?\n fica vendo então..."
    segunda_estrela_label.update()
    time.sleep(4)
    
    segunda_estrela_label["foreground"] = "purple"
    segunda_estrela_label["text"] = "Vou colocar um presentinho\n para você!"
    segunda_estrela_label.update()
    time.sleep(1)
    
    segunda_estrela_label["text"] = "Um bug nesse código!"
    segunda_estrela_label.update()

    arquivo = open("conversas/bug","r", encoding="utf8")
    bug = "\n"+arquivo.read()+"\n"
    arquivo.close()
    
    arquivo = open("conversas/bug_achou","r", encoding="utf8")
    bug_achou = "\n"+arquivo.read()+"\n"
    arquivo.close()
    
    arquivo = open("conversas/bug_outro","r", encoding="utf8")
    bug_outro = "\n"+arquivo.read()+"\n"
    arquivo.close()
    
    arquivo = open("conversas/bug_ultimo","r", encoding="utf8")
    bug_ultimo = "\n"+arquivo.read()+"\n"
    arquivo.close()
    
    arquivo = open("conversas/bug_mentira","r", encoding="utf8")
    bug_mentira = "\n"+arquivo.read()+"\n"
    arquivo.close()
    
    arquivo = open("diana.py","r", encoding="utf8")
    diana = arquivo.read()
    diana_total = len(diana)
    arquivo.close()
    
    arquivo = open("diana.py","w", encoding="utf8")
    instalar_bug = diana[0:8024]+bug+diana[8024:58619]+bug_achou+diana[58619:80056]+bug_outro+diana[80056:98432]+bug_ultimo+diana[98432:132576]+bug_mentira+diana[132576:diana_total]
    arquivo.write(instalar_bug)
    arquivo.close()

    time.sleep(1)
    segunda_estrela_label["foreground"] = "green"
    segunda_estrela_label["text"] = "Boa sorte programador(a)\n gênio!"
    segunda_estrela_label.update()
    time.sleep(2)
    
    print("___Destruindo tela!___")
    tela.destroy()

def acao_terceira_estrela():
    print("___Tela de clique na terceira estrela___")
    frame_inicial_avaliacao.grid_forget()
    frame_terceira_estrela.grid(row=1,column=1)
    terceira_estrela_label["foreground"] = "red"
    terceira_estrela_label["text"] = "Você acha que poderia \nfazer melhor?"
    terceira_estrela_label.update()
    time.sleep(3)

    terceira_estrela_label.grid_forget()
    frame_terceira_estrela_botoes.grid(row=1,column=2)

def acao_terceira_estrela_sim():
    print("___Clique no sim___")
    frame_terceira_estrela_botoes.grid_forget()
    terceira_estrela_label.grid(row=1,column=1)
    terceira_estrela_label["foreground"] = "orange"
    terceira_estrela_label["text"] = "Então tá nerd pica das \ngalaxias"
    terceira_estrela_label.update()
    time.sleep(4)
    
    terceira_estrela_label["foreground"] = "green"
    terceira_estrela_label["text"] = "Sabia que eu sou uma \nversão BETA?"
    terceira_estrela_label.update()
    time.sleep(3.6)
    
    terceira_estrela_label["foreground"] = "black"
    terceira_estrela_label["text"] = "Você sabe o que significa\n B E T A?"
    terceira_estrela_label.update()
    time.sleep(3.6)
    
    terceira_estrela_label["foreground"] = "purple"
    terceira_estrela_label["text"] = "Sabe?"
    terceira_estrela_label.update()
    time.sleep(2)
    
    terceira_estrela_label["foreground"] = "green"
    terceira_estrela_label["text"] = "Tem certeza que sabe \nmesmo?"
    terceira_estrela_label.update()
    time.sleep(3.6)
    
    terceira_estrela_label["foreground"] = "orange"
    terceira_estrela_label["text"] = "Eu estou aprendendo caramba,\n esto indignada com\n isso!"
    terceira_estrela_label.update()
    time.sleep(4.5)
    
    terceira_estrela_label["foreground"] = "red"
    terceira_estrela_label["text"] = "Mas já que você é assim,\n tchau!"
    terceira_estrela_label.update()
    time.sleep(3.6)
    tela.destroy()

def acao_terceira_estrela_nao():
    print("___Clique no não___")
    frame_terceira_estrela_botoes.grid_forget()
    terceira_estrela_label.grid(row=1,column=1)
    terceira_estrela_label.update()
    terceira_estrela_label["foreground"] = "red"
    terceira_estrela_label["text"] = "Então por que você me \n avaliou assim caramba?"
    terceira_estrela_label.update()
    time.sleep(3)
    
    terceira_estrela_label["foreground"] = "green"
    terceira_estrela_label["text"] = "Você já parou para pensar\n o tanto de coisa que\n você critica sem ter\n a menor capacidade \nde fazer melhor?"
    terceira_estrela_label.update()
    time.sleep(8)
    
    terceira_estrela_label["text"] = "já parou para pensar?"
    terceira_estrela_label.update()
    time.sleep(2)
    
    terceira_estrela_label["foreground"] = "red"
    terceira_estrela_label["text"] = "Já? Já parou Stark!"
    terceira_estrela_label.update()
    time.sleep(3.6)
    
    terceira_btn_desculpa.grid(row=2,column=1,sticky=W)
    terceira_btn_dane_se.grid(row=2,column=1,sticky=E)

def acao_terceira_estrela_desculpa():
    print("___Clique no desculpa___")
    terceira_btn_desculpa.grid_forget()
    terceira_btn_dane_se.grid_forget()
    terceira_estrela_label["foreground"] = "green"
    terceira_estrela_label["text"] = "Então vamos dialogar e \n fingir que você jamais\n pensou em me avaliar\n tão bosta assim!"
    terceira_estrela_label.update()
    time.sleep(6)
    
    frame_terceira_estrela.grid_forget() # Destruir essa tela
    frame_telas_de_avaliacao.grid_forget()

    menu_avaliar.grid_forget()                    # Remover o botão avaliar
    menu_conversar.grid(row=1,column=1,sticky=EW) # Construir o frame menu
    frameMenu.grid(row=1,column=1,stick=NSEW)     # Construir a tela do menu

def acao_terceira_estrela_dane_se():      
    print("___Clique no dane-se___")
    terceira_btn_desculpa.grid_forget()
    terceira_btn_dane_se.grid_forget()
    terceira_estrela_label["foreground"] = "red"
    terceira_estrela_label["text"] = "Igualmente !!!"
    terceira_estrela_label.update()
    time.sleep(2)
    tela.destroy()

def acao_quarta_estrela(): 
    print("___Clique na quarta ou quinta estrela___")
    frame_inicial_avaliacao.grid_forget()
    frame_quarto_quinto_estrela.grid(row=1,column=1) 
    quarta_quinta_estrela_label["text"] = "Você acha que poderia \nfazer melhor?"
    quarta_quinta_estrela_label.update()
    time.sleep(3.5)
    
    quarta_quinta_estrela_label.grid_forget()
    frame_quarta_quinta_estrela_btn.grid(row=1,column=2)

def acao_quarto_quinto_estrela_sim(): 
    print("___Clique no sim___")
    frame_quarta_quinta_estrela_btn.grid_forget()
    quarta_quinta_estrela_label.grid(row=1,column=1)
    quarta_quinta_estrela_label["foreground"] = "red"
    quarta_quinta_estrela_label["text"] = "Então tá programador(a) \n pica das galaxias!"
    quarta_quinta_estrela_label.update()
    time.sleep(4.2)
    
    quarta_quinta_estrela_label["text"] = "Sabia que eu sou uma \n versão B E T A?"
    quarta_quinta_estrela_label["foreground"] = "orange"
    quarta_quinta_estrela_label.update()
    time.sleep(3.7)
    
    quarta_quinta_estrela_label["foreground"] = "red"
    quarta_quinta_estrela_label["text"] = "Mas já que é assim,\n tchau!"
    quarta_quinta_estrela_label.update()
    time.sleep(2.6)
    tela.destroy()

def acao_quarto_quinto_estrela_nao():  
    print("___Clique no não___")
    frame_quarta_quinta_estrela_btn.grid_forget()
    quarta_quinta_estrela_label.grid(row=1,column=1)
    quarta_quinta_estrela_label["foreground"] = "red"
    quarta_quinta_estrela_label["text"] = "Então por que você me \n avaliou assim poh?"
    quarta_quinta_estrela_label.update()
    time.sleep(3)
    
    quarta_quinta_estrela_label["foreground"] = "orange"
    quarta_quinta_estrela_label["text"] = "Você já parou para pensar\n o tanto de coisa que você\n critica ser ter a menor\n capacidade de fazer\nmelhor?"
    quarta_quinta_estrela_label.update()
    time.sleep(8)
    
    quarta_quinta_estrela_btn_desculpa.configure(background="green",foreground="white",highlightbackground="white",activeforeground="white",activebackground="green",relief=FLAT,font=("",20))
    quarta_quinta_estrela_btn_dane_se.configure(background="red",foreground="white",highlightbackground="white",activeforeground="white",activebackground="red",relief=FLAT,font=("",20))
    quarta_quinta_estrela_btn_desculpa.grid(row=2,column=1,sticky=E)
    quarta_quinta_estrela_btn_dane_se.grid(row=2,column=1,sticky=W)

def acao_quarto_quinto_desculpa(): 
    print("___Clique no desculpa___")
    quarta_quinta_estrela_btn_desculpa.grid_forget()
    quarta_quinta_estrela_btn_dane_se.grid_forget()
    quarta_quinta_estrela_label["foreground"] = "orange"
    quarta_quinta_estrela_label["text"] = "Então vamos conversar \nfinge que você nunca\n pensou em me avaliar\n tão ruim assim!"
    quarta_quinta_estrela_label.update()
    time.sleep(5.2)
  
    frame_telas_de_avaliacao.grid_forget()

    menu_avaliar.grid_forget() # Remover o botão avaliar
    menu_conversar.grid(row=1,column=1,sticky=EW)
    frame_quarto_quinto_estrela.grid_forget() 
    frameMenu.grid(row=1,column=1,stick=NSEW) # Construir a tela do menu

def acao_quarto_quinto_dane_se():      
    print("___Clique no dane-se___")
    quarta_quinta_estrela_btn_desculpa.grid_forget()
    quarta_quinta_estrela_btn_dane_se.grid_forget()
    quarta_quinta_estrela_label["foreground"] = "red"
    quarta_quinta_estrela_label["text"] = "Igualmente!"
    quarta_quinta_estrela_label.update()
    time.sleep(2)
    tela.destroy()

def acao_seis():
    print("___Clique na sexta estrela___")
    frame_inicial_avaliacao.grid_forget()
    frame_sexta_estrela.grid(row=1,column=1) 
    frame_sexta_estrela.update()
    time.sleep(2)
    
    se_btn_enviar.configure(background="purple",foreground="white",activeforeground="purple",activebackground="white",highlightbackground="white",relief=FLAT,font=("",30))
    se_btn_enviar.grid(row=2,column=1)
    se_btn_enviar.update()

def acao_sexto_link():
    print("___Link da sexta estrela___")
    import webbrowser
    webbrowser.open('https://dianachatbot.blogspot.com')
    frame_sexta_estrela.grid_forget() 
    frame_telas_de_avaliacao.grid_forget()
    menu_avaliar.grid_forget() # Remover o botão avaliar
    menu_conversar.grid(row=1,column=1,sticky=EW)
    frameMenu.grid(row=1,column=1,stick=NSEW) # Construir a tela do menu

def acao_sete_oito():
    print("___Clique na setima ou oitava estrela___")
    frame_inicial_avaliacao.grid_forget()
    frame_sete_oito_estrela.grid(row=1,column=1) 
    frame_sete_oito_estrela.update()
    time.sleep(2)
    
    setima_oitava_estrela_label["foreground"] = "green" 
    setima_oitava_estrela_label["text"] = "Eu me sinto lisongeada!"
    setima_oitava_estrela_label.update()
    time.sleep(2.3)
    
    setima_oitava_estrela_label["text"] = "Sabe, estou muito feliz\n por receber essa avaliação,\n mesmo sendo uma versão\n beta!"
    setima_oitava_estrela_label.update()
    time.sleep(5.4)
    
    setima_oitava_estrela_label["text"] = "Isso me deixa muito \nfeliz! Deixa uma mensagem\n lá no site, eu vou adorar\n ler sua mensagem!"
    setima_oitava_estrela_label.update()
    time.sleep(6)
    
    setimo_oitava_estrela_btn_enviarenviar.grid(row=2,column=1)
    setimo_oitava_estrela_btn_enviarenviar.update()

def acao_sete_oito_link():
    print("___Link da sétima ou oitava estrela___")
    import webbrowser
    webbrowser.open('https://dianachatbot.blogspot.com')
    frame_sete_oito_estrela.grid_forget() 

    menu_avaliar.grid_forget()# Remover o botão avaliar
    frame_telas_de_avaliacao.grid_forget()
    menu_conversar.grid(row=1,column=1,sticky=EW)
    frameMenu.grid(row=1,column=1,stick=NSEW) # Construir a tela do menu

def acao_nove():
    print("___Clique na nona estrela___")
    frame_inicial_avaliacao.grid_forget()
    frame_nove_estrela.grid(row=1,column=1) 
    frame_nove_estrela.update()
    time.sleep(2)
    
    nona_estrela_label["text"] = "Como assim?"
    nona_estrela_label.update()
    time.sleep(2)
    
    nona_estrela_label["text"] = "Eu estou apaixonada por \nvocê mano, já pensou\n em acessar o site para\n deixar o seu comentário lá?"
    nona_estrela_label.update()
    time.sleep(6)
    
    nona_estrela_btn_enviar.configure(font=("",16),background="white",foreground="black",activeforeground="white",activebackground="black",relief=FLAT,highlightbackground="black")
    nona_estrela_btn_enviar.grid(row=2,column=1)
    nona_estrela_btn_enviar.update()

def acao_nove_link():
    print("___Clique no link da nona estrela___")
    import webbrowser
    webbrowser.open('https://dianachatbot.blogspot.com')
    frame_nove_estrela.grid_forget() 
    frame_telas_de_avaliacao.grid_forget()
    # Remover o botão avaliar
    menu_avaliar.grid_forget()
    menu_conversar.grid(row=1,column=1,sticky=EW)
    frameMenu.grid(row=1,column=1,stick=NSEW) 

def atualizar(): # Rotina de atualização da primeira tela (Tela de load estilo!)
    x=1
    tela.configure(background="#dcdcdc")
    tela.update()
    while True:

        link_arquivo = "Imagens/load/animação/"+str(x)+".png"
        imagem = PhotoImage(file=link_arquivo)
        image_botao["image"] = imagem
        image_botao.update()
        time.sleep(0.07)
        if x==20:
            time.sleep(1)
            tela.configure(background="#fff")
            tela.update()
            atualizacoes.tela_testes()
            break
        x=x+1

def fechar_tudo():
    tela.destroy()

# Definição usada para usar o modo escreve escreve sendo o modo reconhece escreve
'''
Temporariamente, a Diana no modo reconhece/escreve,
se passa pelo modo escreve/escreve, foi uma forma
de economizar código, e aproveitar uma estrutura já
existente, infelizmente isso está uma bela bagunça.
'''
def usar_modo_texto():
    print("acesso em modo texto")
    global acesso_em_modo_texto
    acesso_em_modo_texto = "sim"
    # Atualiza dados do arquivo ! IMPORTANTÍSSIMO))
    arquivo = atualizar_dados_de_controle_rec_voz_arqler_total()
    arquivo_ler = arquivo[2]
    total = arquivo[3]
    # Aqui a Diana se passa pelo modo escreve/escreve
    arquivo = open("configurações","w", encoding="utf8")
    novo = arquivo_ler[0:15]+"0"+arquivo_ler[16:total] 
    arquivo.write(novo)
    arquivo.close()
    # Envio de dados e processamento
    processo_rec.transferir_controlador_partes()
    # Atualiza dados do arquivo ! IMPORTANTÍSSIMO))
    arquivo = atualizar_dados_de_controle_rec_voz_arqler_total()
    arquivo_ler = arquivo[2]
    total = arquivo[3]
    # Aqui a Diana se coloca no seu lugar de origem!
    arquivo = open("configurações","w", encoding="utf8")
    novo = arquivo_ler[0:15]+"1"+arquivo_ler[16:total] 
    arquivo.write(novo)
    arquivo.close()
    # Cancelamento da execução do modo se ...passar...
    acesso_em_modo_texto = "nao"





# FIM DA TELA DE LOGIN
#===========================================================================
# TELA DE VALIDAÇÃO



#===========================================================================
# tela de interação puramente escrita
fundo_esc_esc = "#940092"
fundo_esc_esc_barrinha = "#940092"
frente_esc_texto_geral = "#fff"

fundo_esc_text = "white"
borda_esc_frente = "#555"

borda_esc_esc = "#940092"
texto_interacao_simples = "#940092"

tela_5 = Frame(tela,background=fundo_esc_esc) 
tela_5.grid_columnconfigure(1,weight=1)
tela_5.rowconfigure(2,weight=1)

label_tela_5 = Label(tela_5,text="chat de conversação",font=("",22),padx=8,pady=8,background=fundo_esc_esc,foreground=frente_esc_texto_geral)
label_tela_5.grid(row=1,column=1,sticky=NSEW)

frame_texto_tela_5 = Frame(tela_5,background=fundo_esc_esc)
frame_texto_tela_5.grid_columnconfigure(1,weight=1)

texto_tela_5 = Text(frame_texto_tela_5 ,background=fundo_esc_text,border=0,highlightcolor=borda_esc_esc,highlightthickness=1,highlightbackground=borda_esc_esc,foreground=texto_interacao_simples)
texto_tela_5.configure(border=0, pady=2)
texto_tela_5.config(font=("consolas", 12), undo=True, wrap='word')
texto_tela_5.insert(1.0, "")
texto_tela_5.grid(row=1, column=1, sticky=EW)

scrollb_texto_tela_5 = Scrollbar(frame_texto_tela_5,command=texto_tela_5.yview,background=fundo_esc_esc,activebackground=fundo_esc_esc_barrinha)
scrollb_texto_tela_5.grid(row=1, column=2, sticky=NS)
texto_tela_5['yscrollcommand'] = scrollb_texto_tela_5.set

frame_texto_tela_5.grid(row=2,column=1)

frame_botoes_tela_5 = Frame(tela_5,background=fundo_esc_esc)
frame_botoes_tela_5.grid_columnconfigure(2,weight=1)

botao_voltar_tela_5 = Button(frame_botoes_tela_5,text="voltar")
botao_voltar_tela_5["command"] = atualizacoes.interacao_menu
botao_voltar_tela_5["background"] = fundo_esc_esc
botao_voltar_tela_5["activebackground"] = fundo_esc_esc
botao_voltar_tela_5["foreground"] = frente_esc_texto_geral
botao_voltar_tela_5["activeforeground"] = "#e4ff00"
botao_voltar_tela_5["highlightthickness"] =0
botao_voltar_tela_5["relief"] = FLAT
botao_voltar_tela_5["border"] = 0
botao_voltar_tela_5["padx"] = 10
botao_voltar_tela_5["font"] = ("",13)
botao_voltar_tela_5.grid(row=1,column=1)

conteudo_texto_tela_5 = StringVar()
entrada_tela_5 = Entry(frame_botoes_tela_5,textvariable=conteudo_texto_tela_5)
entrada_tela_5["font"] = (" ",12)
entrada_tela_5["background"] = fundo_esc_esc
entrada_tela_5["foreground"] = frente_esc_texto_geral
entrada_tela_5["highlightcolor"] = borda_esc_frente
entrada_tela_5["highlightthickness"] = 1
entrada_tela_5["highlightbackground"] = borda_esc_frente
entrada_tela_5.bind("<Return>", (lambda event: processo_rec.transferir_controlador_partes()))
entrada_tela_5.grid(row=1,column=2,sticky=EW)

botão_enviar_tela_5 = Button(frame_botoes_tela_5,text="enviar",command=processo_rec.transferir_controlador_partes,background=fundo_esc_esc,activebackground=fundo_esc_esc,foreground=frente_esc_texto_geral,activeforeground="#05d1ff",highlightthickness=0,relief=FLAT,border=0,padx=10,font=("",13))
botão_enviar_tela_5.grid(row=1,column=3)

frame_botoes_tela_5.grid(row=3,column=1,sticky=EW)
# tela de interação puramente escrita
#===========================================================================
# tela de interação escrita e com resposta de fala

# Carregameto de imagens
escreve_fala_imagem = PhotoImage(file="Imagens/tela_fala_escreve/esperando.png")
escreve_fala_voltar_img = PhotoImage(file="Imagens/tela_fala_escreve/voltar.png")
escreve_fala_enviar_img = PhotoImage(file="Imagens/tela_fala_escreve/enviar.png")

# Redimensionamento das imagens
escreve_fala_enviar_img = escreve_fala_enviar_img.subsample(2,2)
escreve_fala_voltar_img = escreve_fala_voltar_img.subsample(2,2)

# Definições de cores:
cor_fundo_geral = "#e7e7e7" # Todos os backgrounds
borda_dos_botoes = "#e7e7e7" # Todas as bordas dos três principais botões
cor_tx_titulo = "black" # Cor do titulo
cor_tx_resposta = "black" # Cor da resposta
cor_en_entrada = "black"

cor_tx_titulo_superior = "#05d1ff"
cor_fundo_titulo = "#496a7c"

borda_da_entrada = "#333"


# Definições da tela básica
frame_escreve_fala = Frame(tela,background=cor_fundo_geral)
frame_escreve_fala.rowconfigure(2,weight=1)

frame_escreve_fala.grid_columnconfigure(1,weight=1)
# Título da tela
escreve_fala_texto = Label(frame_escreve_fala,text="Tela em modo beta")
escreve_fala_texto.configure(font=("",25),background=cor_fundo_titulo,foreground=cor_tx_titulo_superior,pady=10)
escreve_fala_texto.grid(row=1,column=1,sticky=W+E)

# Imagem principal de retorno
escreve_fala_imagem_btn = Label(frame_escreve_fala, image=escreve_fala_imagem,background=cor_fundo_geral,highlightbackground=borda_dos_botoes)
escreve_fala_imagem_btn.grid(row=2,column=1)

# Label com o retorno
escreve_fala_base = delimitador.delimitar("Olá, vamos conversar!")
escreve_fala_resposta = Label(frame_escreve_fala,text=escreve_fala_base,font =(" ",14),foreground=cor_tx_resposta,background=cor_fundo_geral)
escreve_fala_resposta.grid(row=3,column=1)

# Frame da parte inferior
escreve_fala_frame_botoes = Frame(frame_escreve_fala)
escreve_fala_frame_botoes.configure(background=cor_fundo_geral)

# Botão voltar
escreve_fala_voltar_img_botao = Button(escreve_fala_frame_botoes,image=escreve_fala_voltar_img,command=atualizacoes.interacao_menu)
escreve_fala_voltar_img_botao.configure(background=cor_fundo_geral,activebackground=cor_fundo_geral,highlightbackground=borda_dos_botoes,relief=FLAT)
escreve_fala_voltar_img_botao.grid(row=1,column=1)

# Text de interação
escreve_fala_frame_botoes.grid_columnconfigure(2,weight=1)
escreve_fala_conteudo = StringVar()
escreve_fala_entrada = Entry(escreve_fala_frame_botoes,textvariable=escreve_fala_conteudo)
escreve_fala_entrada.bind("<Return>", (lambda event: processo_rec.transferir_controlador_partes()))
escreve_fala_entrada.configure(font=(" ",20), bg=cor_fundo_geral, fg=cor_en_entrada, highlightbackground=borda_da_entrada,highlightcolor=borda_da_entrada,border=0,highlightthickness=1)
escreve_fala_entrada.grid(row=1,column=2,sticky=EW)

# Botão enviar
escreve_fala_enviarenviar = Button(escreve_fala_frame_botoes, image=escreve_fala_enviar_img, command=processo_rec.transferir_controlador_partes)
escreve_fala_enviarenviar.configure(background=cor_fundo_geral,activebackground=cor_fundo_geral,highlightbackground=borda_dos_botoes,relief=FLAT)
escreve_fala_enviarenviar.grid(row=1,column=3)

# Finaliza frame dos botões
escreve_fala_frame_botoes.grid(row=4,column=1)
# FIM DA TELA DE INTERAÇÃO ESCRITA E COM RESPOSTA DE FALA #
#===========================================================================
# TELA DE AVALIAÇÃO #
frame_telas_de_avaliacao = Frame(tela)
frame_telas_de_avaliacao.configure(background="white")
frame_telas_de_avaliacao.grid_columnconfigure(1, weight=1)
frame_telas_de_avaliacao.rowconfigure(1, weight=1)

frame_inicial_avaliacao = Frame(frame_telas_de_avaliacao)
frame_inicial_avaliacao.grid_columnconfigure(1, weight=1)

frame_inicial_avaliacao.rowconfigure(3, weight=1)
frame_inicial_avaliacao.configure(background="white")

texto=Label(frame_inicial_avaliacao,text="Avalie-me")
texto.configure(font=(" ",50),foreground="black", background="red")
texto.grid(row=1,column=1,sticky=EW)

frame_avaliar = Frame(frame_inicial_avaliacao,background="white")

escala = Label(frame_avaliar,text="PIOR")
escala.configure(font=(" ",20),background="white",foreground="black")
escala.grid(row=1,column=1,columnspan=3,sticky=EW)

escala = Label(frame_avaliar,text="MEIDA")
escala.configure(font=(" ",20),background="white",foreground="black")
escala.grid(row=1,column=4,columnspan=3,sticky=EW)

escala = Label(frame_avaliar,text="MELHOR")
escala.configure(font=(" ",20),background="white",foreground="black")
escala.grid(row=1,column=7,columnspan=3,sticky=EW)

imagem_estrela_1 = PhotoImage(file="Imagens/avaliação/1.png")
imagem_estrela_1 = imagem_estrela_1.subsample(5,5)
botão_estrela_1 = Button(frame_avaliar,image=imagem_estrela_1,command=acao_primeira_tela)
botão_estrela_1.configure(background="white",highlightbackground="white",activebackground="white",activeforeground="white",relief=FLAT)
botão_estrela_1.grid(row=2,column=1,sticky=EW)

imagem_estrela_2 = PhotoImage(file="Imagens/avaliação/2.png")
imagem_estrela_2 = imagem_estrela_2.subsample(5,5)
botão_estrela_2 = Button(frame_avaliar,image=imagem_estrela_2,command=acao_segunda_estrela)
botão_estrela_2.configure(background="white",highlightbackground="white",activebackground="white",activeforeground="white",relief=FLAT)
botão_estrela_2.grid(row=2,column=2,sticky=EW)

imagem_estrela_3 = PhotoImage(file="Imagens/avaliação/3.png")
imagem_estrela_3 = imagem_estrela_3.subsample(5,5)
botão_estrela_3 = Button(frame_avaliar,image=imagem_estrela_3,command=acao_terceira_estrela)
botão_estrela_3.configure(background="white",highlightbackground="white",activebackground="white",activeforeground="white",relief=FLAT)
botão_estrela_3.grid(row=2,column=3,sticky=EW)

imagem_estrela_4 = PhotoImage(file="Imagens/avaliação/4.png")
imagem_estrela_4 = imagem_estrela_4.subsample(5,5)
botão_estrela_4 = Button(frame_avaliar,image=imagem_estrela_4,command=acao_quarta_estrela)
botão_estrela_4.configure(background="white",highlightbackground="white",activebackground="white",activeforeground="white",relief=FLAT)
botão_estrela_4.grid(row=2,column=4,sticky=EW)

imagem_estrela_5= PhotoImage(file="Imagens/avaliação/5.png")
imagem_estrela_5= imagem_estrela_5.subsample(5,5)
botão_estrela_5 = Button(frame_avaliar,image=imagem_estrela_5,command=acao_quarta_estrela)
botão_estrela_5.configure(background="white",highlightbackground="white",activebackground="white",activeforeground="white",relief=FLAT)
botão_estrela_5.grid(row=2,column=5,sticky=EW)

imagem_estrela_6 = PhotoImage(file="Imagens/avaliação/6.png")
imagem_estrela_6 = imagem_estrela_6.subsample(5,5)
botão_estrela_6 = Button(frame_avaliar,image=imagem_estrela_6,command=acao_seis)
botão_estrela_6.configure(background="white",highlightbackground="white",activebackground="white",activeforeground="white",relief=FLAT)
botão_estrela_6.grid(row=2,column=6,sticky=EW)

imagem_estrela_7 = PhotoImage(file="Imagens/avaliação/7.png")
imagem_estrela_7 = imagem_estrela_7.subsample(5,5)
botão_estrela_7 = Button(frame_avaliar,image=imagem_estrela_7,command=acao_sete_oito)
botão_estrela_7.configure(background="white",highlightbackground="white",activebackground="white",activeforeground="white",relief=FLAT)
botão_estrela_7.grid(row=2,column=7,sticky=EW)

imagem_estrela_8 = PhotoImage(file="Imagens/avaliação/8.png")
imagem_estrela_8 = imagem_estrela_8.subsample(5,5)
botão_estrela_8 = Button(frame_avaliar,image=imagem_estrela_8,command=acao_sete_oito)
botão_estrela_8.configure(background="white",highlightbackground="white",activebackground="white",activeforeground="white",relief=FLAT)
botão_estrela_8.grid(row=2,column=8,sticky=EW)

imagem_estrela_9 = PhotoImage(file="Imagens/avaliação/9.png")
imagem_estrela_9 = imagem_estrela_9.subsample(5,5)
botão_estrela_9 = Button(frame_avaliar,image=imagem_estrela_9,command=acao_nove)
botão_estrela_9.configure(background="white",highlightbackground="white",activebackground="white",activeforeground="white",relief=FLAT)
botão_estrela_9.grid(row=2,column=9,sticky=EW)

frame_avaliar.grid(row=3,column=1,sticky=EW)

voltar = Button(frame_inicial_avaliacao,text="Voltar",command=atualizacoes.avaliacao_menu)
voltar.configure(font=(" ",20),background="blue",foreground="white",highlightbackground="blue",activebackground="blue",activeforeground="black",relief=FLAT)
voltar.grid(row=4,column=1,sticky=EW)

frame_inicial_avaliacao.grid(row=1,column=1,sticky=NSEW)
# FINALIZA TELA INICIAL DA AVALIAÇÃO #
#===========================================================================
# TELA DA SEGUNDA ESTRELA #
frame_segunda_estrela = Frame(frame_telas_de_avaliacao)
frame_segunda_estrela.grid_columnconfigure(1, weight=1)
frame_segunda_estrela.rowconfigure(1, weight=1)
frame_segunda_estrela.configure(background="white")

segunda_estrela_label = Label(frame_segunda_estrela,text="Você tem ideia do tanto\nde tempo que eu demorei\n para ser feita?")
segunda_estrela_label.configure(font=(" ",20),background="white")
segunda_estrela_label.grid(row=1,column=1)
# FINALIZA TELA DA SEGUNDA ESTRELA #
#===========================================================================
# TELA DA TERCEIRA ESTRELA #
frame_terceira_estrela = Frame(frame_telas_de_avaliacao)
frame_terceira_estrela.grid_columnconfigure(1, weight=1)
frame_terceira_estrela.rowconfigure(1, weight=1)
frame_terceira_estrela.configure(background="white")

terceira_estrela_label = Label(frame_terceira_estrela,text="Oi?")
terceira_estrela_label.configure(font=(" ",20),background="white")
terceira_estrela_label.grid(row=1,column=1)

terceira_btn_desculpa = Button(frame_terceira_estrela,text="Desculpa",command=acao_terceira_estrela_desculpa,background="green",activebackground="green",foreground="white",activeforeground="white",relief=FLAT)
terceira_btn_dane_se = Button(frame_terceira_estrela,text="Dane-se",command=acao_terceira_estrela_dane_se,background="red",activebackground="red",foreground="white",activeforeground="white",relief=FLAT)

frame_terceira_estrela_botoes = Frame(frame_terceira_estrela)
frame_terceira_estrela_botoes.configure(background="white")

terceira_estrela_botao_1 = Button(frame_terceira_estrela_botoes,text="Não poderia fazer melhor",command=acao_terceira_estrela_nao)
terceira_estrela_botao_1.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
terceira_estrela_botao_1.grid(row=1,column=1)

terceira_estrela_botao_2 = Button(frame_terceira_estrela_botoes,text="Não poderia fazer melhor",command=acao_terceira_estrela_nao)
terceira_estrela_botao_2.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
terceira_estrela_botao_2.grid(row=2,column=1)

terceira_estrela_botao_3 = Button(frame_terceira_estrela_botoes,text="Não poderia fazer melhor",command=acao_terceira_estrela_nao)
terceira_estrela_botao_3.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
terceira_estrela_botao_3.grid(row=3,column=1)

terceira_estrela_botao_4 = Button(frame_terceira_estrela_botoes,text="Não poderia fazer melhor",command=acao_terceira_estrela_nao)
terceira_estrela_botao_4.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
terceira_estrela_botao_4.grid(row=4,column=1)

terceira_estrela_botao_5 = Button(frame_terceira_estrela_botoes,text="Não poderia fazer melhor",command=acao_terceira_estrela_nao)
terceira_estrela_botao_5.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
terceira_estrela_botao_5.grid(row=5,column=1)

terceira_estrela_botao_6 = Button(frame_terceira_estrela_botoes,text="Não poderia fazer melhor",command=acao_terceira_estrela_nao)
terceira_estrela_botao_6.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
terceira_estrela_botao_6.grid(row=6,column=1)

terceira_estrela_botao_7 = Button(frame_terceira_estrela_botoes,text="Sim poderia fazer melhor",command=acao_terceira_estrela_sim)
terceira_estrela_botao_7.configure(background="white",activebackground="white",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
terceira_estrela_botao_7.grid(row=7,column=1)

terceira_estrela_botao_8 = Button(frame_terceira_estrela_botoes,text="Não poderia fazer melhor",command=acao_terceira_estrela_nao)
terceira_estrela_botao_8.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
terceira_estrela_botao_8.grid(row=8,column=1)

terceira_estrela_botao_9 = Button(frame_terceira_estrela_botoes,text="Não poderia fazer melhor",command=acao_terceira_estrela_nao)
terceira_estrela_botao_9.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
terceira_estrela_botao_9.grid(row=9,column=1)
# FINALIZA TELA DA TERCEIRA ESTRELA #
#===========================================================================
# TELA DA QUARTA/QUINTA ESTRELA #
frame_quarto_quinto_estrela = Frame(frame_telas_de_avaliacao)
frame_quarto_quinto_estrela.grid_columnconfigure(1, weight=1)
frame_quarto_quinto_estrela.rowconfigure(1, weight=1)
frame_quarto_quinto_estrela.configure(background="white")

quarta_quinta_estrela_label = Label(frame_quarto_quinto_estrela,text="Oi?")
quarta_quinta_estrela_label.configure(font=(" ",20),background="white")
quarta_quinta_estrela_label.grid(row=1,column=1)

quarta_quinta_estrela_btn_desculpa = Button(frame_quarto_quinto_estrela,text="Desculpa",command=acao_quarto_quinto_desculpa) 
quarta_quinta_estrela_btn_dane_se = Button(frame_quarto_quinto_estrela,text="Dane-se",command=acao_quarto_quinto_dane_se) 

frame_quarta_quinta_estrela_btn = Frame(frame_quarto_quinto_estrela)
frame_quarta_quinta_estrela_btn.configure(background="white")

quarta_quinta_estrela_btn_1 = Button(frame_quarta_quinta_estrela_btn,text="não",command=acao_quarto_quinto_estrela_nao) 
quarta_quinta_estrela_btn_1.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
quarta_quinta_estrela_btn_1.grid(row=1,column=1)

quarta_quinta_estrela_btn_2 = Button(frame_quarta_quinta_estrela_btn,text="não",command=acao_quarto_quinto_estrela_nao)
quarta_quinta_estrela_btn_2.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
quarta_quinta_estrela_btn_2.grid(row=2,column=1)

quarta_quinta_estrela_btn_3 = Button(frame_quarta_quinta_estrela_btn,text="não",command=acao_quarto_quinto_estrela_nao)
quarta_quinta_estrela_btn_3.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
quarta_quinta_estrela_btn_3.grid(row=3,column=1)

quarta_quinta_estrela_btn_4 = Button(frame_quarta_quinta_estrela_btn,text="não",command=acao_quarto_quinto_estrela_nao)
quarta_quinta_estrela_btn_4.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
quarta_quinta_estrela_btn_4.grid(row=4,column=1)

quarta_quinta_estrela_btn_5 = Button(frame_quarta_quinta_estrela_btn,text="não",command=acao_quarto_quinto_estrela_nao)
quarta_quinta_estrela_btn_5.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
quarta_quinta_estrela_btn_5.grid(row=5,column=1)

quarta_quinta_estrela_btn_6 = Button(frame_quarta_quinta_estrela_btn,text="não",command=acao_quarto_quinto_estrela_nao)
quarta_quinta_estrela_btn_6.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
quarta_quinta_estrela_btn_6.grid(row=6,column=1)

quarta_quinta_estrela_btn_7 = Button(frame_quarta_quinta_estrela_btn,text="sim",command=acao_quarto_quinto_estrela_sim)
quarta_quinta_estrela_btn_7.configure(background="white",activebackground="white",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
quarta_quinta_estrela_btn_7.grid(row=7,column=1)

quarta_quinta_estrela_btn_8 = Button(frame_quarta_quinta_estrela_btn,text="não",command=acao_quarto_quinto_estrela_nao)
quarta_quinta_estrela_btn_8.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
quarta_quinta_estrela_btn_8.grid(row=8,column=1)

quarta_quinta_estrela_btn_9 = Button(frame_quarta_quinta_estrela_btn,text="não",command=acao_quarto_quinto_estrela_nao)
quarta_quinta_estrela_btn_9.configure(background="white",activebackground="green",foreground="black",activeforeground="white",highlightbackground="white",relief=FLAT,font=("",20))
quarta_quinta_estrela_btn_9.grid(row=9,column=1)
# FINALIZA TELA DA QUARTA/QUINTA ESTRELA #
#===========================================================================
# TELA DA SEXTA ESTRELA #
frame_sexta_estrela = Frame(frame_telas_de_avaliacao)
frame_sexta_estrela.grid_columnconfigure(1, weight=1)
frame_sexta_estrela.rowconfigure(1, weight=1)
frame_sexta_estrela.configure(background="white")

se_label = Label(frame_sexta_estrela,text="Que falta de consideração,\n mas obrigado pela sua \navaliação, você já pensou\n em mandar uma mensagem\n para o meu criador? Sabe,\n ele precisa de algumas \nideias para me deixar\nmelhor! Você pode fazer \nisso? É rapidinho! Não doi\n nada, eu acho!")
se_label.configure(font=(" ",20),background="white")
se_label.grid(row=1,column=1)
se_btn_enviar = Button(frame_sexta_estrela,text="Enviar Mensagem",command=acao_sexto_link) 
# FINALIZA TELA DA SEXTA ESTRELA #
#===========================================================================
# TELA DA SETIMA/OITAVA ESTRELA #
frame_sete_oito_estrela = Frame(frame_telas_de_avaliacao,background="white")
frame_sete_oito_estrela.grid_columnconfigure(1, weight=1)
frame_sete_oito_estrela.rowconfigure(1, weight=1)

setima_oitava_estrela_label = Label(frame_sete_oito_estrela,text="Eita, tem certeza?",font=(" ",20),background="white")
setima_oitava_estrela_label.grid(row=1,column=1)

setimo_oitava_estrela_btn_enviarenviar = Button(frame_sete_oito_estrela,text="Enviar uma mensagem no site",command=acao_sete_oito_link) 
setimo_oitava_estrela_btn_enviarenviar.configure(background="green",foreground="white",highlightbackground="white",activeforeground="white",activebackground="green",relief=FLAT,font=("",18))
# FINALIZA DA SETIMA/OITAVA ESTRELA #
#===========================================================================
# TELA DA NONA ESTRELA #
frame_nove_estrela = Frame(frame_telas_de_avaliacao,background="#00cccc")
frame_nove_estrela.grid_columnconfigure(1, weight=1)
frame_nove_estrela.rowconfigure(1, weight=1)

nona_estrela_label = Label(frame_nove_estrela,text="Calma ai, sério?",font=(" ",20),background="white")
nona_estrela_label.grid(row=1,column=1)
nona_estrela_btn_enviar = Button(frame_nove_estrela,text="Deixa uma mensagem no site por favor",command=acao_nove_link) 
# FINALIZA TELAS DE AVALIAÇÃO #
#===========================================================================
# TELA DE INTERAÇÃO, RECONHECIMENTO DE VOZ E RESPOSTA POR TEXTO #

# Esquema de cores
rec_esc_fundo_geral = "#00d1ff" # Fundo azul dos frames e dos botões
fundo__titulo_geral = "#00d1ff" # Fundo do título principal
cor_titulo_geral = "#496a7c"    # Cor do título principal
cor_text_preto = "black"        # Cor do texto do Text
fundo_f3 = "#f3f3f3"            # Cor de fundo do Text
rec_esc_frente_geral = "black"  # Cor do texto do Entry
bordas_db = "#dbdbdb"           # Bordas do Entry
# Carregamento de imagens
tela_rec_img_mic = PhotoImage(file="Imagens/reconhece_escreve/clique-me.png")
tela_rec_img_voltar = PhotoImage(file="Imagens/reconhece_escreve/voltar.png")
# Redimensionamento de imagens
tela_rec_img_mic = tela_rec_img_mic.subsample(3,3)
tela_rec_img_voltar=tela_rec_img_voltar.subsample(3,3)

# Definições da tela
tela_rec_esc = Frame(tela)
tela_rec_esc.configure(background=rec_esc_fundo_geral)
tela_rec_esc.grid_columnconfigure(1,weight=1)

# Título superior
tela_rec_titulo = Label(tela_rec_esc,text="Diana - vbeta")
tela_rec_titulo.configure(background=fundo__titulo_geral,foreground=cor_titulo_geral,font=("",17),pady=10)
tela_rec_titulo.grid(row=1,column=1,sticky=EW)

'''Atualizações. Isso dá responsividade a tela e garante
um melhor funcionamento em múltiplas telas'''
tela_rec_esc.grid_columnconfigure(1,weight=1)
tela_rec_esc.rowconfigure(2,weight=1)

# Caixa de texto, onde é exibido dados da interação
tela_rec_text = Text(tela_rec_esc,background=fundo_f3,foreground=cor_text_preto,highlightthickness=0,border=0)
tela_rec_text.configure(font=("consolas", 12), undo=True, wrap='word')
tela_rec_text.insert(1.0, "Diana: Diga alguma coisa!")
tela_rec_text.grid(row=2,column=1,sticky=NSEW)

tela_rec_esc.grid_columnconfigure(1,weight=1)
# Parte inferior com a entrada e os botões
tela_rec_inferior = Frame(tela_rec_esc,background=rec_esc_fundo_geral)
tela_rec_inferior.grid_columnconfigure(2,weight=1)

# botão voltar
tela_rec_voltar = Button(tela_rec_inferior,image=tela_rec_img_voltar,command=atualizacoes.reconhece_escreve_menu,highlightbackground=rec_esc_fundo_geral,border=0,background=rec_esc_fundo_geral,relief=FLAT,activebackground=rec_esc_fundo_geral)
tela_rec_voltar.grid(row=1,column=1)

# Entrada de texto
tela_rec_entry = Entry(tela_rec_inferior,foreground=rec_esc_frente_geral,background=rec_esc_fundo_geral,highlightbackground=bordas_db,highlightcolor=bordas_db,font=("",14)) 
tela_rec_entry.bind("<Return>", (lambda event: usar_modo_texto()))
tela_rec_entry.grid(row=1,column=2,sticky=NSEW)

# Botão ouvir
tela_rec_ouvir = Button(tela_rec_inferior,image=tela_rec_img_mic,command=processo_rec.controlador_partes,highlightbackground=rec_esc_fundo_geral,border=0,background=rec_esc_fundo_geral,relief=FLAT,activebackground=rec_esc_fundo_geral)
tela_rec_ouvir.grid(row=1,column=3)
tela_rec_inferior.grid(row=3,column=1,sticky=EW)

# FINALIZA TELA DE INTERAÇÃO, RECONHECIMENTO DE VOZ E RESPOSTA POR TEXTO #
#===========================================================================
# TELA DE CONFIGURAÇÃO #

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
arquivo = atualizar_dados_de_controle_rec_voz_arqler_total()
status_loc_voz = arquivo[1] # VOZ
status_loc_rec = arquivo[0] # REC

# Condicionais de imagem para o botão de estado da fala
if status_loc_voz=="n":
        configuracoes_fala_imagem = PhotoImage(file="Imagens/configurações/desativado.png")
else:
        configuracoes_fala_imagem = PhotoImage(file="Imagens/configurações/ativado.png")

# Condicionais de imagem para o botão de estado do reconhecimento de voz
if status_loc_rec=="n":
        configuracoes_reconhecimento_imagem = PhotoImage(file="Imagens/configurações/desativado.png")
else:
        configuracoes_reconhecimento_imagem = PhotoImage(file="Imagens/configurações/ativado.png")

# Definições do frame Configurações
tela_frame_configuracoes = Frame(tela,background=fundo_configuracoes)
tela_frame_configuracoes.grid_columnconfigure(1,weight=1)
tela_frame_configuracoes.rowconfigure(1,weight=1)

# Definições do frame Secundário
configuracoes_frame = Frame(tela_frame_configuracoes)
configuracoes_frame.configure(background=fundo_azul_titulo)

# Redimensionando as imagens
configuracoes_fala_imagem = configuracoes_fala_imagem.subsample(4,4)
configuracoes_voltar_imagem = configuracoes_voltar_imagem.subsample(3,3)
configuracoes_reconhecimento_imagem = configuracoes_reconhecimento_imagem.subsample(4,4)

# Meteoro para voltar
configuracoes_voltar_texto = Button(configuracoes_frame,image=configuracoes_voltar_imagem,command=atualizacoes.config_menu)
configuracoes_voltar_texto.configure(font=("",17),background=fundo_azul_titulo,foreground="white",highlightbackground=fundo_azul_titulo,activeforeground=fundo_azul_titulo,activebackground=fundo_azul_titulo,relief=FLAT)
configuracoes_voltar_texto.grid(row=1,column=1,sticky=EW,pady=10)

# Texto configurações gerais
configuracoes_logo_texto = Label(configuracoes_frame,text="Configurações gerais   ")
configuracoes_logo_texto.configure(font=("",20),background=fundo_azul_titulo,foreground=letra_titulos)
configuracoes_logo_texto.grid(row=1,column=2,sticky=EW,pady=10)
configuracoes_frame.grid(row=0,column=1,sticky=EW)
configuracoes_frame.grid_columnconfigure(1,weight=1)

# Frame de testes do reconhecimento de voz
configuracoes_frame_1 = Frame(tela_frame_configuracoes)
configuracoes_frame_1.configure(background=fundo_configuracoes,pady=5,padx=10)
# Titulo da primeira opção de teste
configuracoes_reconhecimento_texto = Label(configuracoes_frame_1,text="RECONHECIMENTO DE VOZ ")
configuracoes_reconhecimento_texto.configure(fg=dois_titulos,bg=fundo_configuracoes,font=("",15))
configuracoes_reconhecimento_texto.grid(row=1,column=1,sticky=W)
# Botão de status do reconhecimento de voz
configuracoes_reconhecimento_imagem_botao = Button(configuracoes_frame_1,image=configuracoes_reconhecimento_imagem,command=atualiza_configuracoes_reconhecimento)
configuracoes_reconhecimento_imagem_botao.configure(bg=fundo_configuracoes,highlightbackground=fundo_botao,relief=FLAT,bd=0,activebackground=fundo_botao)
configuracoes_reconhecimento_imagem_botao.grid(row=1,column=2)
# Texto avisando da função
configuracoes_reconhecimento_testar_label = Label(configuracoes_frame_1,text="Clique em testar, e diga alguma coisa!")
configuracoes_reconhecimento_testar_label.configure(bg=fundo_configuracoes,fg=letra_roxa,highlightbackground=letra_roxa,relief=FLAT,bd=0,activebackground="white",font=("Arial",12))
configuracoes_reconhecimento_testar_label.grid(row=2,column=1,columnspan=2,sticky=E)
# Botão para testes
configuracoes_reconhecimento_testar_botao = Button(configuracoes_frame_1,text="TESTAR",command=testar_configuracoes_reconhecimento_de_voz)
configuracoes_reconhecimento_testar_botao.configure(bg=fundo_configuracoes,fg=letra_roxa,highlightbackground=letra_roxa,relief=FLAT,bd=0,activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_ok,font=("Arial",12))
configuracoes_reconhecimento_testar_botao.grid(row=2,column=1,columnspan=2,sticky=W)

# Frame geral (solucionando problemas)
configuracoes_frame_1.grid(row=1,column=1,sticky=EW)
configuracoes_frame_1.grid_columnconfigure(1, weight=3)
# Frame do teste da fala
configuracoes_frame_2 = Frame(tela_frame_configuracoes)
configuracoes_frame_2.configure(background=fundo_configuracoes,pady=5,padx=10)
# Texto
configuracoes_fala_texto = Label(configuracoes_frame_2,text="FALA ONLINE PT-BR ")
configuracoes_fala_texto.configure(foreground=dois_titulos,background=fundo_configuracoes,font=("",13))
configuracoes_fala_texto.grid(row=1,column=1,sticky=W)
# Status do reconhecimento de voz
configuracoes_fala_imagem_botao = Button(configuracoes_frame_2,image=configuracoes_fala_imagem,command=atualiza_configuracoes_fala)
configuracoes_fala_imagem_botao.configure(background=fundo_configuracoes,highlightbackground=fundo_botao,relief=FLAT,bd=0,activebackground=fundo_botao)
configuracoes_fala_imagem_botao.grid(row=1,column=2,sticky=W)
# Botão para testar o modo
configuracoes_fala_testar_botao = Button(configuracoes_frame_2,text="TESTAR O MODO FALA",command=testar_configuracoes_voz)
configuracoes_fala_testar_botao.configure(background=fundo_configuracoes,foreground=letra_roxa,highlightbackground=letra_roxa,relief=FLAT,bd=0,activeforeground=texto_modo_ativo_ok, activebackground=fundo_modo_ativo,font=("Arial",12))
configuracoes_fala_testar_botao.grid(row=2,column=1,columnspan=2,sticky=E+W)
configuracoes_frame_2.grid(row=2,column=1,sticky=EW)
configuracoes_frame_2.grid_columnconfigure(1, weight=3)

# Guia dos módulos necessários
configuracoes_modulo = Label(tela_frame_configuracoes,text="  Módulos necessários  ")
configuracoes_modulo.configure(background=fundo_azul_titulo,foreground=letra_titulos,pady=5,padx=10,font=("",15))
configuracoes_modulo.grid(row=3,column=1,sticky=EW)

# Frame do Mipand
configuracoes_frame_3 = Frame(tela_frame_configuracoes)
# Carregamento do botão de acordo com o status na inicialização
if mipand == "0":
    configuracoes_mipand = Button(configuracoes_frame_3,text="Preciso do Mipand!")
    configuracoes_mipand.configure(font=("",16),background=fundo_configuracoes,foreground="red",highlightbackground="red",activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_erro,relief=FLAT)
else:
    configuracoes_mipand = Button(configuracoes_frame_3,text="Mipand")
    configuracoes_mipand.configure(font=("",16),background=fundo_configuracoes,foreground=letra_verde,highlightbackground=letra_verde,activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_ok,relief=FLAT)
configuracoes_mipand.grid(row=2,column=1,columnspan=2,sticky=EW)
# Carregamento com  o site do Mipand
configuracoes_mipand_link = Button(configuracoes_frame_3,text=" SITE ",command=abrir_site_mipand)
configuracoes_mipand_link.configure(font=("",16),background=fundo_configuracoes,foreground=letra_azul_site,highlightbackground=letra_azul_site,activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_ok,relief=FLAT)
configuracoes_mipand_link.grid(row=2,column=1,columnspan=2,sticky=E)
configuracoes_frame_3.grid(row=4,column=1,sticky=EW)
configuracoes_frame_3.grid_columnconfigure(1, weight=3)

# Frame do reconhecimento de voz
configuracoes_frame_4 = Frame(tela_frame_configuracoes)
# Carregamento do botão de acordo com o status na inicialização
if speechrecognition=="1":
    configuracoes_speechrecognition = Button(configuracoes_frame_4,text="Speech Recognition")
    configuracoes_speechrecognition.configure(font=("",16),background=fundo_configuracoes,foreground=letra_verde,highlightbackground=letra_verde,activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_ok,relief=FLAT)
else:
    configuracoes_speechrecognition = Button(configuracoes_frame_4,text="Instalar Speech Recognition")
    configuracoes_speechrecognition.configure(font=("",16),background=fundo_configuracoes,foreground="red",highlightbackground="red",activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_erro,relief=FLAT)
configuracoes_speechrecognition.grid(row=2,column=1,columnspan=2,sticky=EW)
# Carregamento do botão com o site
configuracoes_speechrecognition_link = Button(configuracoes_frame_4,text=" SITE ",command=abrir_site_SPEECHRECOGNITION)
configuracoes_speechrecognition_link.configure(font=("",16),background=fundo_configuracoes,foreground=letra_azul_site,highlightbackground=letra_azul_site,activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_ok,relief=FLAT)
configuracoes_speechrecognition_link.grid(row=2,column=1,columnspan=2,sticky=E)
configuracoes_frame_4.grid(row=5,column=1,sticky=EW)
configuracoes_frame_4.grid_columnconfigure(1, weight=3)

# Frame do Pyaudio
configuracoes_frame_5 = Frame(tela_frame_configuracoes)
# Carregamento do botão com o status do pyaudio
if pyaudio == "1":
    configuracoes_pyaudio = Button(configuracoes_frame_5,text="Pyaudio")
    configuracoes_pyaudio.configure(font=("",16),background=fundo_configuracoes,foreground=letra_verde,highlightbackground=letra_verde,activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_ok,relief=FLAT)
else:
    configuracoes_pyaudio = Button(configuracoes_frame_5,text="Instalar pyaudio")
    configuracoes_pyaudio.configure(font=("",16),background=fundo_configuracoes,foreground="red",highlightbackground="red",activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_erro,relief=FLAT)
configuracoes_pyaudio.grid(row=2,column=1,columnspan=2,sticky=EW)
# Carregamento do botão com o site do pyaudio
configuracoes_pyaudio_link = Button(configuracoes_frame_5,text=" SITE ",command=abrir_site_pyaudio)
configuracoes_pyaudio_link.configure(font=("",16),background=fundo_configuracoes,foreground=letra_azul_site,highlightbackground=letra_azul_site,activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_ok,relief=FLAT)
configuracoes_pyaudio_link.grid(row=2,column=1,columnspan=2,sticky=E)
configuracoes_frame_5.grid(row=6,column=1,sticky=EW)
configuracoes_frame_5.grid_columnconfigure(1, weight=3)

# Frame do playsound
configuracoes_frame_6 = Frame(tela_frame_configuracoes)
# Carregamento do botão com o status do playsound
if playsound == "1":
    configuracoes_playsound = Button(configuracoes_frame_6,text="Playsound")
    configuracoes_playsound.configure(font=("",16),background=fundo_configuracoes,foreground=letra_verde,highlightbackground=letra_verde,activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_ok,relief=FLAT)
else:
    configuracoes_playsound = Button(configuracoes_frame_6,text="Instalar playsound")
    configuracoes_playsound.configure(font=("",16),background=fundo_configuracoes,foreground="red",highlightbackground="red",activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_erro,relief=FLAT)
configuracoes_playsound.grid(row=2,column=1,columnspan=2,sticky=EW)
# Carregamento do botão site
configuracoes_playsound_link = Button(configuracoes_frame_6,text=" SITE ",command=abrir_site_playsound)
configuracoes_playsound_link.configure(font=("",16),background=fundo_configuracoes,foreground=letra_azul_site,highlightbackground=letra_azul_site,activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_ok,relief=FLAT)
configuracoes_playsound_link.grid(row=2,column=1,columnspan=2,sticky=E)
configuracoes_frame_6.grid(row=7,column=1,sticky=EW)
configuracoes_frame_6.grid_columnconfigure(1, weight=3)

# Frame do GTTS
configuracoes_frame_7 = Frame(tela_frame_configuracoes)
# Carregamento do botão de acordo com o status na inicialização
if gtts=="1":
    configuracoes_gtts = Button(configuracoes_frame_7,text="GTTS")
    configuracoes_gtts.configure(font=("",16),background=fundo_configuracoes,foreground=letra_verde,highlightbackground=letra_verde,activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_ok,relief=FLAT)
else:
    configuracoes_gtts = Button(configuracoes_frame_7,text="Instalar gtts")
    configuracoes_gtts.configure(font=("",16),background=fundo_configuracoes,foreground="red",highlightbackground="red",activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_erro,relief=FLAT)
configuracoes_gtts.grid(row=2,column=1,columnspan=2,sticky=EW)
# Carregamento do botão site
configuracoes_gtts_link = Button(configuracoes_frame_7,text=" SITE ",command=abrir_site_gtts)
configuracoes_gtts_link.configure(font=("",16),background=fundo_configuracoes,foreground=letra_azul_site,highlightbackground=letra_azul_site,activebackground=fundo_modo_ativo,activeforeground=texto_modo_ativo_ok,relief=FLAT)
configuracoes_gtts_link.grid(row=2,column=1,columnspan=2,sticky=E)
configuracoes_frame_7.grid(row=8,column=1,sticky=EW)
configuracoes_frame_7.grid_columnconfigure(1, weight=3)

# Frame de controle da taxa de variação do mipand
configuracoes_frame_8 = Frame(tela_frame_configuracoes)
configuracoes_frame_8.configure(background=fundo_verde,padx=9,pady=9)
# Texto sobre a função
taxa_variacao = Label(configuracoes_frame_8,text="Taxa de variação para o Mipand")
taxa_variacao.configure(font=("",17),background=fundo_verde,foreground=letra_titulos)
taxa_variacao.grid(row=0,column=1,sticky=N+S+E+W)
# Escala da taxa de variação
scale_config = Scale(configuracoes_frame_8,from_=1, to=100, orient=HORIZONTAL,command=resize)
scale_config.configure(background=fundo_verde,foreground=letra_titulos,highlightbackground=fundo_verde,troughcolor=fundo_verde,bd=1)
scale_config.set(scale) # Aqui a escala é colocada na sua devida posição
scale_config.grid(row=1,column=1,sticky=NSEW)
configuracoes_frame_8.grid(row=10,column=1,sticky=N+S+E+W)
configuracoes_frame_8.grid_columnconfigure(1, weight=1)
configuracoes_frame_8.rowconfigure(1, weight=1)

# FINALIZA TELA DE CONFIGURAÇÃO 
#===========================================================================
# TELA DE INTERAÇÃO 
interacao_esperando_img = PhotoImage(file="Imagens/fala/esperando.png")
interacao_voltar_img = PhotoImage(file="Imagens/fala/voltar.png")
interacao_falar_img = PhotoImage(file="Imagens/fala/falar.png")
interacao_ajuda_img = PhotoImage(file="Imagens/fala/ajuda.png")

# Configurações de cores
cor_fg_titulo_sub = "black"
cor_fundo = "white"
cor_bd_hg_at = "white"

# Configurações de redimensionamento
interacao_esperando_img = interacao_esperando_img.subsample(1,1)
interacao_voltar_img = interacao_voltar_img.subsample(2,2)
interacao_falar_img = interacao_falar_img.subsample(2,2)
interacao_ajuda_img = interacao_ajuda_img.subsample(2,2)

# Definições da tela de interação
frame_interacao = Frame(tela, background=cor_fundo)
frame_interacao.grid_columnconfigure(1,weight=1)
frame_interacao.rowconfigure(3,weight=1)

# Título do frame interação
interacao_titulo_label = Label(frame_interacao,text="DIANA")
interacao_titulo_label.configure(font=("Arial",50), foreground=cor_fg_titulo_sub, background=cor_fundo, highlightbackground=cor_bd_hg_at)
interacao_titulo_label.grid(row=1, column=1,sticky=EW)

# Descrição simples da interação
interacao_descricao_label = Label(frame_interacao, text="Bom dia, hoje está um belo dia!")
interacao_descricao_label.configure(font=("",12),foreground=cor_fg_titulo_sub,background=cor_fundo,highlightbackground=cor_bd_hg_at)
interacao_descricao_label.grid(row=2, column=1,sticky=EW)

# Imagem principal da tela
interacao_esperando_img_botao = Button(frame_interacao, image=interacao_esperando_img)
interacao_esperando_img_botao.configure(relief=SUNKEN,highlightbackground=cor_bd_hg_at,activeforeground=cor_bd_hg_at,background=cor_fundo,activebackground=cor_bd_hg_at,highlightthickness=0,border=0)
interacao_esperando_img_botao.grid(row=3, column=1,sticky=EW)

# Frame dos botões inferiores
interacao_botoes = Frame(frame_interacao,background=cor_fundo)
interacao_botoes.grid_columnconfigure(2,weight=1)

# Botão voltar
interacao_voltar_img_botao = Button(interacao_botoes, image=interacao_voltar_img,command=atualizacoes.interacao_menu)#,command=tela.quit)
interacao_voltar_img_botao.configure(background=cor_fundo,foreground=cor_fg_titulo_sub,highlightbackground=cor_bd_hg_at,activebackground=cor_bd_hg_at,activeforeground=cor_bd_hg_at,relief=FLAT)
interacao_voltar_img_botao.grid(row=4,column=1,sticky=W+E)

# Botão central de pergunta
interacao_falar_img_botao = Button(interacao_botoes, image=interacao_falar_img,command=processo_rec.controlador_partes)
interacao_falar_img_botao.configure(background=cor_fundo,foreground=cor_fg_titulo_sub,highlightbackground=cor_bd_hg_at,activebackground=cor_bd_hg_at,activeforeground=cor_bd_hg_at,relief=FLAT)
interacao_falar_img_botao.grid(row=4, column=2)

# Botão lateral de ajuda
interacao_ajuda_img_botao=Button(interacao_botoes,image=interacao_ajuda_img,command=abrir_site_ajuda)
interacao_ajuda_img_botao.configure(background=cor_fundo,foreground=cor_fg_titulo_sub,highlightbackground=cor_bd_hg_at,activebackground=cor_bd_hg_at,activeforeground=cor_bd_hg_at,relief=FLAT)
interacao_ajuda_img_botao.grid(row=4,column=3,sticky=W+E)
interacao_botoes.grid(row=4,column=1,sticky=NSEW)

# FINALIZA TELA DE INTERAÇÃO #
#===========================================================================
# TELA DO HISTÓRICO #

fundo_branco = "white"         # Todos os backgrounds brancos
fundo_azul = "#1976d3"         # Todos os backgrounds azuis
fg_bt_volt = "white"           # Texto do botão voltar
bg_bt_volt = "#009899"         # Fundo do botão voltar
bd_bt_volt = "#009899"         # Borda do botão voltar
bg_ac_bt_volt = "#009899"      # Fundo do botão voltar destaque
tx_bt_limpar = "white"         # Texto do botão limpar
bg_bt_limpar = "#fe0000"       # Fundo do botão limpar
tx_lb_historico = "#fff"       # Texto do título "histórico"
tx_lb_inf = "white"            # Cor do texto dos label histórico e aprendizados
bg_lb_inf = "#00cccb"          # Cor de fundo dos label histórico e aprendizados
bd_lb_inf = "#00cccb"          # Cor da borda dos label histórico e aprendizados
fg_tx_princ = "black"          # Cor do texto do Text principal
bd_tx_princ = "#fff"           # Cor da borda do text

# Definições do frame
frame_historico = Frame(tela,background=fundo_branco)
frame_historico.grid_columnconfigure(1,weight=1)
frame_historico.rowconfigure(3,weight=1)

# Titulo principal superior
hist_lb = Label(frame_historico, text="Histórico",background=fundo_azul,font=("",23))
hist_lb.configure(highlightbackground="#1976d3", foreground=tx_lb_historico, pady=4)
hist_lb.grid(row=1,column=1,sticky=EW)

# Frame do histórico/aprendizado
supe_hist = Frame(frame_historico,background="red")
supe_hist.grid_columnconfigure(1, weight=1)
# Label do histórico
hist_inte = Label(supe_hist, text="historico",background=bg_lb_inf,)
hist_inte.configure(highlightbackground=bd_lb_inf,foreground=tx_lb_inf,font=("",14))
hist_inte.grid(row=1,column=1,sticky=NSEW)
supe_hist.grid_columnconfigure(2, weight=1)
# Label do Aprendizados
hist_apren= Label(supe_hist,text="Aprendizados",background=bg_lb_inf)
hist_apren.configure(highlightbackground=bd_lb_inf,foreground=tx_lb_inf,font=("",14))
hist_apren.grid(row=1,column=2,sticky=NSEW)
supe_hist.grid(row=2,column=1,sticky=NSEW)

# Acesso do arquivo histórico
historico_arquivo = open("Analise/histórico.txt","r", encoding="utf8")
historico_arquivo_ler = historico_arquivo.read()
historico_arquivo.close()
# Carregamento de dados
historico_arquivo_ler = str(historico_arquivo_ler)
# Condicional para evitar erros na leitura da atualiza_histórico
try:
    historico_arquivo_ler = str(atualizar_historico()[0])
except:
    historico_arquivo_ler = " "

# Definições do frame do bloco Text
historico_bloco_principal = Frame(frame_historico)
historico_bloco_principal.grid_columnconfigure(1,weight=1)
# Text do bloco principal
historico_texto_text = Text(historico_bloco_principal)
historico_texto_text.configure(background=fundo_branco, highlightbackground=bd_tx_princ, border=2,foreground=fg_tx_princ)
historico_texto_text.config(font=("consolas", 12), undo=True, wrap='word')
historico_texto_text.insert(1.0, historico_arquivo_ler) # Inserção de dados
historico_texto_text.grid(row=1, column=1, sticky=EW)
# Scrollb do Text
historico_scrollb = Scrollbar(historico_bloco_principal, command=historico_texto_text.yview)
historico_scrollb.configure(background=fundo_branco, activebackground="#f9f9f9", highlightbackground="white", highlightcolor="white")
historico_scrollb.grid(row=1, column=2, sticky=NS)
historico_texto_text['yscrollcommand'] = historico_scrollb.set
historico_bloco_principal.grid(row=3,column=1)

# Definições do frame inferior
frame_inferior_historico = Frame(frame_historico,background="black")
frame_inferior_historico.grid_columnconfigure(1,weight=1)
# Botão voltar
historico_voltar_botao = Button(frame_inferior_historico, text="Voltar",command=atualizacoes.historico_menu)
historico_voltar_botao.configure(background=bg_bt_volt, foreground=fg_bt_volt, activebackground=bg_ac_bt_volt, activeforeground="#fff", highlightbackground=bd_bt_volt, relief=FLAT, font=("Arial",12))
historico_voltar_botao.grid(row=4, column=1,sticky=EW)
# Atualização de frame
frame_inferior_historico.grid_columnconfigure(2,weight=1) 
# Botão limpar histórico
historico_limpar_botao = Button(frame_inferior_historico, text="Limpar histórico",command=limpar_historico)
historico_limpar_botao.configure(background=bg_bt_limpar, foreground=tx_bt_limpar, activebackground="#fe0000", activeforeground="#fff", highlightbackground="#fe0000", relief=FLAT, font=("Arial",12))
historico_limpar_botao.grid(row=4, column=2,sticky=EW)
frame_inferior_historico.grid(row=4,column=1,sticky=EW)

# FINALIZA TELA DO HISTÓRICO #
#===========================================================================

# TELA DO MENU #

# Definições do tema
tema_fundo = "white"                       # Tema geral do fundo
tema_botao = "#1976d2"                     # Múltiplas funções
tema_botao_frente = "white"                # Múltiplas funções
tema_botao_frente_ativo = "white"          # Múltiplas funções
menu_fundo = "#1976d2"                     # Múltiplas funções
menu_texto_branco_verde = "white"          # Múltiplas funções
fundo_verde_azul = "#1976d2"               # Múltiplas funções

# Atualização de dados
arquivo = atualizar_dados_de_controle_rec_voz_arqler_total()
status_rec = arquivo[0]
status_voz = arquivo[1]

if status_voz== "n":
    controlar_voz  = "n"
    menu_fala_img = PhotoImage(file="Imagens/Menu/fala_des.png")
else:
    controlar_voz  = "s" 
    menu_fala_img = PhotoImage(file="Imagens/Menu/fala_ati.png")

# Condicionais de imagem do reconhecimento de voz para tela inicial
if status_rec== "n": # Rec desativada e tema normal
    controlar_reconhecimento = "n" 
    menu_reconhecimento_img = PhotoImage(file="Imagens/Menu/rec_des.png")
else:
    menu_reconhecimento_img = PhotoImage(file="Imagens/Menu/rec_ati.png")

# Definições de imagem sem animação
menu_ajuda_img = PhotoImage(file="Imagens/Menu/ajuda.png")               # ícone de ajuda
menu_historico_img = PhotoImage(file="Imagens/Menu/histórico.png")       # ícone do histórico
menu_config_img = PhotoImage(file="Imagens/Menu/config.png")             # ícone das configurações

# Redimensionamento das imagens
menu_fala_img = menu_fala_img.subsample(1,1)
menu_ajuda_img = menu_ajuda_img.subsample(1,1)
menu_config_img = menu_config_img.subsample(5,5)
menu_historico_img = menu_historico_img.subsample(1,1)
menu_reconhecimento_img = menu_reconhecimento_img.subsample(1,1)

# Definições da tela
frameMenu = Frame(tela,background=tema_fundo)
frameMenu.grid_columnconfigure(1,weight=1)
frameMenu.rowconfigure(2,weight=1)

# Definições do frame
menu_footer = Label(frameMenu)
menu_footer.grid_columnconfigure(1,weight=1)
menu_footer.configure(background=menu_fundo, highlightbackground=menu_fundo)

# Menu superior (título)
menu_titulo = Label(menu_footer,text="DIANA CHATBOT")
menu_titulo.configure(background=menu_fundo, foreground=menu_texto_branco_verde, highlightbackground=fundo_verde_azul, font=("",25),border=2)
menu_titulo.grid(row=1,column=1)
# Icone de configurações(Ao lado do título)
menu_config_img_botao = Button(menu_footer,image=menu_config_img,command=atualizacoes.menu_config)
menu_config_img_botao.configure(background=menu_fundo, foreground=menu_fundo, highlightbackground=menu_fundo, relief=FLAT, activeforeground=menu_fundo, activebackground=menu_fundo)
menu_config_img_botao.grid(row=1,column=2)
menu_footer.grid(row=1,column=1,sticky=EW)

# Frame dos blocos
lider_dos_blocos = Frame(frameMenu,background=tema_fundo)
# Menu superior (blocos)
menu_superior = Frame(lider_dos_blocos,background=tema_fundo)
menu_superior.rowconfigure(1,weight=1)
# Ícone de fala
menu_menu_fala_img_botao = Button(menu_superior,image=menu_fala_img)
menu_menu_fala_img_botao["command"] = atualiza_configuracoes_fala
menu_menu_fala_img_botao.configure(relief=FLAT,background=tema_fundo,highlightbackground=tema_fundo,foreground=tema_fundo,activebackground=tema_fundo)
menu_menu_fala_img_botao.grid(row=1,column=1,sticky=EW)
# Ícone de reconhecimento de voz
menu_reconhecimento_img_botao = Button(menu_superior,image=menu_reconhecimento_img)
menu_reconhecimento_img_botao["command"] = atualiza_configuracoes_reconhecimento
menu_reconhecimento_img_botao.configure(relief=FLAT,background=tema_fundo,highlightbackground=tema_fundo, foreground=tema_fundo,activebackground=tema_fundo)
menu_reconhecimento_img_botao.grid(row=1,column=2,sticky=EW)
menu_superior.grid(row=3, column=1,sticky=EW)

# Menu inferior (blocos)
menu_superior_2 = Frame(lider_dos_blocos,background="white")
# Ícone ajuda
menu_ajuda_img_botao = Button(menu_superior_2,image=menu_ajuda_img)
menu_ajuda_img_botao.configure(command=abrir_site_ajuda,relief=FLAT,background=tema_fundo,highlightbackground=tema_fundo,foreground=tema_fundo,activebackground=tema_fundo)
menu_ajuda_img_botao.grid(row=2,column=1,sticky=W+E)
# Ícone histórico
menu_historico_img_botao = Button(menu_superior_2,image=menu_historico_img,command=atualizacoes.menu_historico)
menu_historico_img_botao.configure(relief=FLAT,background=tema_fundo,highlightbackground=tema_fundo,foreground=tema_fundo,activebackground=tema_fundo)
menu_historico_img_botao.grid(row=2,column=2,sticky=W+E)
menu_superior_2.grid(row=4, column=1,sticky=EW)
lider_dos_blocos.grid(row=2,column=1)
''' Botões que podem alternar na parte inferior '''
# Botões inferiores
botoes_do_menu_c_a = Frame(frameMenu,background=tema_fundo)
botoes_do_menu_c_a.grid_columnconfigure(1,weight=1)

# Botão avalie-me
menu_avaliar = Button(botoes_do_menu_c_a, text="Avalie-me",command=atualizacoes.menu_avaliacao)
menu_avaliar.configure(background=tema_botao,foreground=tema_botao_frente,font=("",14),pady=2,relief=FLAT,activeforeground="blue",activebackground=tema_botao,highlightbackground=tema_botao)

# Botão conversar
menu_conversar = Button(botoes_do_menu_c_a, text="conversar",command=atualizacoes.menu_interacao)
menu_conversar.configure(background=tema_botao,foreground=tema_botao_frente,font=("",14),pady=2,relief=FLAT,activeforeground="blue",activebackground=tema_botao,highlightbackground=tema_botao)
menu_conversar.grid(row=1,column=1,sticky=EW)
botoes_do_menu_c_a.grid(row=3,column=1,sticky=EW)
# FINALIZA TELA DO MENU #

#===========================================================================

# TELA DE TESTES BÁSICOS #
# Cores do tema
fundo_load = "white"             # fundo de toda a tela
fundo_load_texto = "black"       # texto básico de toda a tela
titulo_cor_branca = "white"      # Cor do titulo
titulo_cor_fundo = "#00d1ff"     # Cor de fundo do título

inicia_config_img = PhotoImage(file="Imagens/Testes/20.png")

# Configurações do frame da tela de testes
inicia_frame = Frame(tela)
inicia_frame.configure(background=fundo_load)
inicia_frame.grid_columnconfigure(1,weight=1)
inicia_frame.rowconfigure(2,weight=1)

# Título superior
inicia_mensagem = Label(inicia_frame ,text="ETAPA DE TESTES",foreground=titulo_cor_branca)
inicia_mensagem.configure(background=titulo_cor_fundo,font=("Arial",15))
inicia_mensagem.grid(row=1,column=1, sticky=EW)

# Botão continuar
inicia_config_img_label = Button(inicia_frame, image=inicia_config_img,command=atualizacoes.tela_testes_menu)
inicia_config_img_label.configure(background=fundo_load, foreground="#fff", highlightbackground=fundo_load, relief=SUNKEN, activeforeground="white", activebackground=fundo_load,highlightthickness=0,border=0)
inicia_config_img_label.grid(row=2,column=1,sticky=EW)

# Guia das informações
guias_de_testes = Frame(inicia_frame,background=fundo_load,highlightbackground="#00ff01")
guias_de_testes.grid_columnconfigure(1,weight=1)

# label do módulo GTTS
inicia_gtts_img_label = Label(guias_de_testes,text="GTTS: ")
inicia_gtts_img_label.configure(background=fundo_load,foreground=fundo_load_texto)
inicia_gtts_img_label.grid(row=1,column=1,sticky=E)
guias_de_testes.grid_columnconfigure(2,weight=1)
if gtts == "0":
    inicia_nao_label = Button(guias_de_testes ,text="Erro. Clique aqui para instalar...")
    inicia_nao_label.configure(background=fundo_load,foreground="red")
if gtts == "1":
    inicia_nao_label = Button(guias_de_testes ,text="Funcionando...")
    inicia_nao_label.configure(background=fundo_load,foreground=fundo_load_texto)
# status do GTTS
inicia_nao_label.configure(command=abrir_site_gtts,relief=FLAT,highlightbackground=fundo_load)
inicia_nao_label.configure(activebackground="#111",activeforeground="white")
inicia_nao_label.grid(row=1,column=2,sticky=W)

# label do playsound
inicia_playsound_label = Label(guias_de_testes ,text="PLAYSOUND: ")
inicia_playsound_label.configure(background=fundo_load,foreground=fundo_load_texto)
inicia_playsound_label.grid(row=2,column=1,sticky=E)
# status do playsound
if playsound == "0":
    inicia_erro_label = Button(guias_de_testes ,text="Erro. Clique aqui para instalar...")
    inicia_erro_label.configure(background=fundo_load,foreground="red")
if playsound == "1":
    inicia_erro_label = Button(guias_de_testes ,text="Funcionando...")
    inicia_erro_label.configure(background=fundo_load,foreground=fundo_load_texto)
inicia_erro_label.configure(command=abrir_site_playsound,relief=FLAT,highlightbackground=fundo_load, activebackground="#111",activeforeground="white")
inicia_erro_label.grid(row=2,column=2,sticky=W)

# label do mipand
inicia_mipand_label = Label(guias_de_testes ,text="MIPAND: ")
inicia_mipand_label.configure(background=fundo_load,foreground=fundo_load_texto)
inicia_mipand_label.grid(row=3,column=1,sticky=E)
if mipand == "0":
    inicia_funcionando_label = Button(guias_de_testes ,text="Erro. Clique aqui para instalar...")
    inicia_funcionando_label.configure(background=fundo_load,foreground="red")
if mipand == "1":
    inicia_funcionando_label = Button(guias_de_testes ,text="Funcionando...")
    inicia_funcionando_label.configure(background=fundo_load,foreground=fundo_load_texto)
# status do mipand
inicia_funcionando_label.configure(command=abrir_site_mipand, relief=FLAT, highlightbackground=fundo_load, activebackground="#111", activeforeground="white")
inicia_funcionando_label.grid(row=3,column=2,sticky=W)

# label do pip3
inicia_pip3_label = Label(guias_de_testes ,text="PIP3: ")
inicia_pip3_label.configure(background=fundo_load,foreground=fundo_load_texto)
inicia_pip3_label.grid(row=4,column=1,sticky=E)
# Status do pip3
inicia_testando_label = Button(guias_de_testes ,text="Não testado...")
inicia_testando_label.configure(background=fundo_load,foreground="blue", command=abrir_site_PIP3,relief=FLAT,highlightbackground=fundo_load, activebackground="#111",activeforeground="white")
inicia_testando_label.grid(row=4,column=2,sticky=W)

# label do pyaudio
inicia_pyaudio_label = Label(guias_de_testes ,text="PYAUDIO: ")
inicia_pyaudio_label.configure(background=fundo_load,foreground=fundo_load_texto)
inicia_pyaudio_label.grid(row=5,column=1,sticky=E)
# status do pyaudio
if pyaudio == "0":
    inicia_em_espera_label = Button(guias_de_testes ,text="Erro. Clique aqui para instalar...")
    inicia_em_espera_label.configure(background=fundo_load,foreground="red")
if pyaudio == "1":
    inicia_em_espera_label = Button(guias_de_testes ,text="Funcionando...")
    inicia_em_espera_label.configure(background=fundo_load,foreground=fundo_load_texto)
inicia_em_espera_label.configure(command=abrir_site_pyaudio,relief=FLAT,highlightbackground=fundo_load, activebackground="#111",activeforeground="white")
inicia_em_espera_label.grid(row=5,column=2,sticky=W)

# label do Speech Recognition
inicia_espeechrecognition_label = Label(guias_de_testes ,text="SPEECH RECOGNITION: ")
inicia_espeechrecognition_label.configure(background=fundo_load,foreground=fundo_load_texto)
inicia_espeechrecognition_label.grid(row=6,column=1,sticky=E)
# status do Speech Recognition
if speechrecognition == "0":
    inicia_em_espera_2_label = Button(guias_de_testes ,text="Erro. Clique aqui para instalar...")
    inicia_em_espera_2_label.configure(background=fundo_load,foreground="red")
if speechrecognition == "1":
    inicia_em_espera_2_label = Button(guias_de_testes ,text="Funcionando...")
    inicia_em_espera_2_label.configure(background=fundo_load, foreground=fundo_load_texto)
inicia_em_espera_2_label.configure(command=abrir_site_SPEECHRECOGNITION, relief=FLAT, highlightbackground=fundo_load, activebackground="#111",activeforeground="white")
inicia_em_espera_2_label.grid(row=6, column=2,sticky=W)

guias_de_testes.grid(row=3,column=1,sticky=EW)
# FINALIZA TELA DE TESTES BÁSICOS #

#--------------------------------------------#

# COMEÇA TELA DE LOAD
tela.configure(background="#dcdcdc") 

# Configuração da tela de load
tela_de_load = Frame(tela,border=0)
tela_de_load.rowconfigure(1,weight=1)

tela_de_load["background"] = "#dcdcdc" # Tela de fundo
imagem = PhotoImage(file="Imagens/load/animação/1.png") # Imagem inicial
image_botao = Label(tela_de_load,image=imagem, background="#dcdcdc")# Imagem_label

image_botao.grid(row=1,column=1)
tela_de_load.grid(row=1,column=1,sticky=NSEW)
# Termina tela de load

atualizar() # Chamar o load
tela.mainloop() 

 
#1 0 0 1 1 0 1 0 1 0 0 0 0 0 1 0 1 0 1
#             .        | 
#         *           -o-               
#             .__.     |       __
#          ../    \n.         /  \
# ________/         \n________|__|
#0 0 1 0 0 1 0 1 0 1 0 0 0 1 0 0 0 1 0 1

'''
************ Módulos especiais ************

Módulo:       Pip 3
Função:       Instalador de bibliotecas
Site:         https://pypi.org/project/pip/
Instalação:   Confira no site
Créditos:     Desenvolvedores do pip < pypa-dev@groups.google.com >

Módulo:       Playsound
Função:       Executa arquivos mp3
Site:         https://pypi.org/project/playsound/
Instalação:   pip3 install playsound
Créditos:     Copyright (c) 2016 Taylor Marks < taylor@marksfam.com >

Módulo:       GTTS 2.0.3
Função:       Gera aquivos de áudio em mp3
Site:         https://pypi.org/project/gTTS/
Instalação:   pip3 install gtts
Créditos:     Copyright © 2014-2018 Pierre Nicolas Durette

Módulo:       Pyaudio v0.2.11
Função:       Acessar o microfone
Site:         https://pypi.org/project/PyAudio/
Instalação:   pip3 install PyAudio
Créditos:     PyAudio is distributed under the MIT License:
Créditos:     Copyright (c) 2006 Hubert Pham
Créditos:     Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

Módulo:       SpeechRecognition 3.8.1
Função:       Fazer o reconhecimento de voz
Site:         https://pypi.org/project/SpeechRecognition/
Instalação:   pip3 install speechrecognition
Créditos:     Copyright 2014-2017 Anthony Zhang (Uberi).
'''
