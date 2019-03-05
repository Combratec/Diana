#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Deixei aqui alguns trechos de código que a Diana usa com bastante frequência, eles fazem testes, processamentos e até salvam dados no histórico.

class diana(): # Classe principal 
   def __init__(self):
      pass

   # Esta definição realiza testes dos principais módulos e retorna o status de funcionamento deles, além de tentar instalar módulos ausentes.
   def testa_modulos():
      mipand_modulo            = "1"    # Módulo de processamento de texto
      os_modulo                = "1"    # Módulo básico não usado!
      speechrecognition_modulo = "1"    # Módulo de reconhecimento de voz
      pyaudio_modulo           = "1"    # Módulo auxiliar que pode ser necessário
      playsound_modulo         = "1"    # Módulo de reprodução de arquivos em mp3
      gtts_modulo              = "1"    # Módulo gerador de fala
      # Setando valores padrão.
      RES_OS                   ="[*]"
      RES_AST                  ="[*]"
      RES_TIME                 ="[*]"
      RES_GTTS                 ="[*]"
      RES_MIPAND               ="[*]"
      RES_TKINTER              ="[*]"
      RES_PYAUDIO              ="[*]"
      RES_PLAYSOUND            ="[*]"
      RES_WEBBROWSER           ="[*]"
      RES_DEFINICOES           ="[*]"
      RES_ALTERNATIVA          ="[*]"
      RES_DELIMITADOR          ="[*]"
      RES_SPEECH_RECOGNITION   ="[*]"
      ERRO = "[?]"

      #######################################################################################################
      # Deixei aqui diversos códigos que podem ser necessários para a instalação de algumas bibliotecas.    #
      # Eles levam em conta alguns problemas já relatados e alguns problemas que eu pessoalmente ja passei .#
      # Caso aconteça algum problema na sua máquina em relação aos códigos, é da sua total responsabilidade!#
      #######################################################################################################

      # Função caso  haja necessidade de instalação do pip3
      def instalar_atualizar_pip_3():
          try:
              import pip
          except:
             os.system("py get-pip.py") # Instalação do pip se necessário
          # Atualizações necessárias!
          os.system("python -m pip install --upgrade pip setuptools wheel")
          os.system("python -m pip install --upgrade pip")
          os.system("py -m pip install --upgrade pip")
          os.system("sudo pip3 install --upgrade pip")
          os.system("sudo pip install --upgrade pip")
          os.system("pip install --upgrade pip")


      ''' Decisão se haverá tentativa de instalação ou não de algum módulo faltante '''
      arquivo = open("Analise/quantidade_acesso.txt","r",encoding="utf8") # começa com 1
      arquivo_acessar = int(arquivo.read())
      arquivo.close()

#      ignorar_instalacao="sim" # Ignorar qualquer tipo de instalação
#      if arquivo_acessar<5:        

      ignorar_instalacao="nao"

      try:
         import os
      except:
         print("[X] OS NÃO ENCONTRADO")
         RES_OS = ERRO
         os_modulo = "0"

      try:
         import ast                 
      except:
         print("[X] AST NÃO ENCONTRADO")
         RES_AST = ERRO

      try:
         import time                 
      except:
         print("[X] TIME NÃO ENCONTRADO")
         RES_TIME = ERRO

      try:
         import mipand
      except:
         print("[X] MIPAND NÃO ENCONTRADO")
         RES_MIPAND = ERRO
         mipand_modulo = "0"

      try:
          import webbrowser           
      except:
         print("[X] WEBBROWSER NÃO ENCONTRADO")
         RES_WEBBROWSER = ERRO

      try:
         import definicoes          
      except:
         print("[X] DEFINIÇÕES NÃO ENCONTRADO")
         RES_DEFINICOES = ERRO           

      try:
         import alternativa  
      except:
         print("[X] ALTERNATIVA NÃO ENCONTRADO")
         RES_ALTERNATIVA = ERRO

      try:
         import delimitador    
      except:
         print("[X] DELIMITADOR NÃO ENCONTRADO")
         RES_DELIMITADOR = ERRO
 
      try:
         import tkinter          
      except:
         try:
            import Tkinter          
         except:
            print("[X] TKINTER NÃO ENCONTRADO")
            RES_TKINTER = ERRO    

      try:
         import gtts               
      except:
         print("[X] GTTS não encontrado!")
         if ignorar_instalacao=="nao":
             instalar_atualizar_pip_3()
             os.system("pip install gTTS")
             os.system("py -m pip install -U gtts")
             os.system("sudo pip3 install gtts")
             os.system("pip install gtts")
             os.system("pip install gTTS")
         try:
            import gtts               
         except:
            print("[ERRO] Não consegui instalar o GTTS, preciso dele para falar")
            print("[ERRO] Instale por esse link: https://pypi.org/project/gTTS/")
            RES_GTTS    = ERRO
            gtts_modulo = "0"

      def instalacao_pyaudio_definicao():
          try:
              import pyaudio            
          except:
              print("[X] PYAUDIO não encontrado!")
              if ignorar_instalacao=="nao":
                  # Instalar ou atualizar o pip3 se necessário
                  instalar_atualizar_pip_3()
                  # Instalação de ferramentas que podem o pyaudio depende
                  os.system("py -m pip install -U wheel")
                  os.system("python -m pip install pyaudio")
                  os.system("py -m pip install pyaudio")
                  os.system("pip install -U setuptools")  
                  os.system("pip install -U virtualenv")
                  os.system("pip install setuptools --upgrade")
                  os.system("py -m pip install -U setuptools")  
                  os.system("py -m pip install -U virtualenv")
                  os.system("py -m pip install setuptools --upgrade")
                  os.system("sudo pip3 install -U setuptools")  
                  os.system("sudo pip3 install -U virtualenv")
                  os.system("sudo pip3 install setuptools --upgrade")
                  # Tentativa de instalação básica
                  os.system("brew install portaudio")
                  os.system("pip install pyaudio")
                  os.system("pip3 install pyaudio")
                  os.system("sudo pip3 install pyaudio")
                  os.system("pip install PyAudio")
                  os.system("py -m pip install -U pyaudio")
                  # Instalação para sistemas linux
                  os.system("sudo apt-get install portaudio19-dev python-all-dev python3-all-dev && sudo pip3 install pyaudio")
                  os.system("sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev")
                  os.system("sudo apt-get install python-pyaudio python3-pyaudio")
                  os.system("sudo apt-get install python3-pyaudio")
                  os.system("sudo apt-get install portaudio19-dev")
                  os.system("sudo apt-get install libportaudio-dev")
                  os.system("sudo apt-get install python-dev")
                  os.system("sudo pip3 install pyaudio")
                  os.system("sudo pip install pyaudio")  
              try:
                  import pyaudio            
              except:
                 if ignorar_instalacao=="nao":
                     os.system("python pacotes/instalador_pyaudio.py")
                     os.system("py pacotes/instalador_pyaudio.py")
                 try:
                     import pyaudio            
                 except:
                     print("[ERRO] Não consegui instalar o PyAudio 0.2.11!")
                     print("[ERRO] Baixe e instale por esse link: https://pypi.org/project/PyAudio/")
                     pyaudio_modulo = "0"
                     RES_PYAUDIO = ERRO
      instalacao_pyaudio_definicao()

      # Importação básica
      verificar_atualizar_pyaudio = "sim"
      try:
         import pyaudio            
      except:
         verificar_atualizar_pyaudio = "nem tenta"

      if verificar_atualizar_pyaudio == "sim":
          try:
              versao_pyaudio = str(pyaudio.__version__)
          except:
              print("A pasta pyaudio está interferindo no funcionamento da\n Diana no seu sistema operacional, posso remove-la?")
              os.system("del pyaudio")
              instalacao_pyaudio_definicao()
              versao_pyaudio == "deu ruim!"

          # PyAudio na versão correta
          if versao_pyaudio == "0.2.11":
              print("PyAudio na versão {}".format(versao_pyaudio))
          else:
              os.system("sudo pip3 install --ignore-installed pyaudio")
              os.system("py -m pip install -U pyaudio")
              os.system("python -m pip install --upgrade pyaudio")
              os.system("py -m pip install --upgrade pyaudio")

      try:
         import playsound
      except:
         print("[X] PLAYSOUND não encontrado!")
         if ignorar_instalacao=="nao":
             # Instalar ou atualizar o pip3 se necessário
             instalar_atualizar_pip_3()
             os.system("py get-pip.py")
             os.system("py -m pip install -U pyaudio")
             os.system("python -m pip install --upgrade pip")
             os.system("py -m pip install -U playsound")
             os.system("sudo pip3 install playsound")
             os.system("sudo pip install playsound")
             os.system("pip install playsound")
             os.system("pip3 install playsound")
         try:
            import playsound           
         except:
             print("[ERRO] Não consegui instalar o playsound, preciso dele para reproduzir arquivos de audio")
             print("[ERRO] Baixe e instale por esse link: https://pypi.org/project/playsound/")
             RES_PLAYSOUND = ERRO
             playsound_modulo = "0"

      try:
         import speech_recognition
      except:
         print("[X] SPEECH_RECOGNITION não encontrado! ")
         if ignorar_instalacao=="nao":
             # Instalar ou atualizar o pip3 se necessário
             instalar_atualizar_pip_3()
             # Instalação para Linux
             os.system("sudo pip3 install speechrecognition")
             os.system("sudo pip3 install SpeechRecognition")
             # Instalação para Windows
             os.system("py -m pip install -U speechrecognition")
             # Instalação geral
             os.system("pip3 install speechrecognition")
             os.system("pip install speechrecognition")
         try:
             import speech_recognition
         except:
            print("[ERRO] Não consegui instalar o Speech Recognition, preciso dele para fazer reconhecimento de voz")
            print("[ERRO] Baixe por esse link: https://pypi.org/project/SpeechRecognition/")
            RES_SPEECH_RECOGNITION = ERRO
            speechrecognition_modulo = "0"

      print("{} OS                ".format(RES_OS))     
      print("{} AST               ".format(RES_AST))
      print("{} TIME              ".format(RES_TIME))
      print("{} GTTS              ".format(RES_GTTS))
      print("{} MIPAND            ".format(RES_MIPAND))    
      print("{} TKINTER           ".format(RES_TKINTER))       
      print("{} PYAUDIO           ".format(RES_PYAUDIO))    
      print("{} PLAYSOUND         ".format(RES_PLAYSOUND))       
      print("{} WEBBROWSER        ".format(RES_WEBBROWSER))       
      print("{} DEFINICOES        ".format(RES_DEFINICOES))       
      print("{} ALTERNATIVA       ".format(RES_ALTERNATIVA))       
      print("{} DELIMITADOR       ".format(RES_DELIMITADOR))       
      print("{} SPEECH RECOGNITION".format(RES_SPEECH_RECOGNITION))       
 
     # Retorno dos dados coletados
      return mipand_modulo,os_modulo,speechrecognition_modulo,pyaudio_modulo,playsound_modulo,gtts_modulo

   # Teste completo do conjunto de fala
   def testeFala():
      from gtts import gTTS             # Importação do gerador de fala
      from playsound import playsound   # Importação do reprodutor de áudio
      # os testes serão feitos linha a linha aqui!
      try:
         tts = gTTS(text="Geração e reprodução de fala funcionando" , lang='pt')
      except:
          return "[Erro] Por favor, se conecte a internet"
      try:
         tts.save("teste.mp3")
      except:
          return "[Erro] Não consegui salvar o arquivo teste.mp3"
      try:
         playsound("teste.mp3")
      except:
          return "[Erro] playsound não consegui executar o arquivo gerado"
      return "[online] Sistemas de fala funcionando!"
   
   # Teste quase completo do reconhecimento de voz
   def testeReconhecimento():
      import speech_recognition as sr
      microfone = sr.Recognizer()
      with sr.Microphone() as source:
         try:
            microfone.adjust_for_ambient_noise(source)
         except:
            return "[Erro] Não consegui ajustar o ruido!"
         print("Diga alguma coisa: ")
         try:
            audio = microfone.listen(source)
         except:
            return "[Erro] audio = microfone.listen(source) "
         try:
            frase = microfone.recognize_google(audio,language='pt-BR')
         except:
            return "[Erro] Não ouvi nada, ou você não me disse nada ou você está com a internet desconectada!"
      frase = "\033[1;35;40m"+frase
      return frase
   
   # Entrada de texto via terminal - extinto na versão 7.1.2
   def entradaTexto(mensagem): # Entrada digitando
      digitado = str(input(mensagem))
      return digitado

   # Entrada de dados por voz
   def entrada_de_voz(mensagem): # Reconhecimento de voz   
      import speech_recognition as sr
      microfone = sr.Recognizer()
      with sr.Microphone() as source:
         microfone.adjust_for_ambient_noise(source)
         print(mensagem)
         audio = microfone.listen(source)
         try:
            frase = microfone.recognize_google(audio,language='pt-BR')
         except:
            return "\033[1;31;40mERRO!"
      return frase
  
   # Processamento de dados
   def processamento(digitado): 
      import mipand
      armazena = 0 # Variável de inicialização da precisão
      var = 1

      quantidade = open("conversas/d_list.txt","r", encoding="utf8")
      qt_conv = int(quantidade.read())
      quantidade.close()

      while var<=qt_conv:
         gerador = "conversas/"+str(var)+".txt"
         arquivo = open(gerador,"r", encoding="utf8")
         arquivo_dado = arquivo.read()
         arquivo.close()

         lista = open(gerador,"r", encoding="utf8")
         listagem = lista.read()
         listagem=str(listagem)

         lista.close()
         lista_falas=listagem.split(";")
         digitar=1
         lim=len(lista_falas)
         x=0
         while lim>x:
            comeca=0
            fim=len(lista_falas[x])
            p=0
            while p<fim:
               p=p+1
               if p==fim:
                  finaliza=p
                  banco=lista_falas[x][comeca:finaliza]
                  result=mipand.ler(digitado.lower(),banco.lower()) # IMPORTANTE - MELHORA OS RESULTADOS 
                  if result>armazena:
                     busca=x
                     arquivos_dad = var
                     armazena=float(result)
            x=x+1
         var=var+1
      precisão = armazena         # Precisão das frases
      assunto = arquivos_dad      # Arquivo assunto
      posição_no_assunto = busca  # Posição do frase
      return precisão,assunto,posição_no_assunto

   # Gerador de respostas
   def gerar_resposta(precisão_resp,assunto_resp,posição_no_assunto_resp,precisão_esperada_resp):
      if precisão_resp<precisão_esperada_resp:
         return "__CRIAR NOVO ASSUNTO__"
      else:
        acessar_arquivo = "conversas/"+str(assunto_resp)+".txt"
        lista = open(acessar_arquivo,"r", encoding="utf8")
        listagem = lista.read()
        listagem=str(listagem)
        lista.close()
        lista_falas=listagem.split(";") # Converter strings para lista
        lim=len(lista_falas)-1 # Descobrir quantos objetos tem na lista
        if posição_no_assunto_resp == lim: # Se a palavra encontrada estiver no limite do assunto
           return "__CONTINUAR LISTA__"
        else:
           return lista_falas[posição_no_assunto_resp+1]
 
   # Criar um novo assunto
   def criar_assunto (digitado,resposta):
      arquivo = open("conversas/d_list.txt","r", encoding="utf8")
      assuntos_numeros = int(arquivo.read())
      arquivo.close()
      criar_novo_assunto = "conversas/"+str(assuntos_numeros+1)+".txt"
      arquivo = open(criar_novo_assunto,"w", encoding="utf8")
      digitado_e_nova_resposta =str(digitado)+";"+str(resposta) 
      arquivo.write(digitado_e_nova_resposta)
      arquivo.close()
      arquivo = open("conversas/d_list.txt","w", encoding="utf8")
      adicionar = str(assuntos_numeros+1)
      arquivo.write(adicionar)
      arquivo.close()

   # Continuar um assunto
   def continuar_assunto(assunto_resp,resposta):
      acessar_arquivo = "conversas/"+str(assunto_resp)+".txt"
      arquivo = open(acessar_arquivo,"r", encoding="utf8")
      sobrescrever = str(arquivo.read())
      arquivo.close()
      arquivo = open(acessar_arquivo,"w", encoding="utf8")
      sobrescrever = str(sobrescrever)+";"+str(resposta) 
      arquivo.write(sobrescrever)
      arquivo.close()
      return "OK"

   # Resposta por áudio
   def saidaAudio(resposta): # Gera arquivo de áudio
      from gtts import gTTS
      from playsound import playsound
      try:
         tts = gTTS(text=resposta , lang='pt')
      except:
          return "ERRO!"
      try:
         tts.save("arquivo.mp3")
      except:
          return "ERRO!"
      try:
         playsound("arquivo.mp3")
      except:
          return "ERRO!"
      return "OK"

   # Salvar a pergunta e a resposta no arquivo do histórico
   def salvaHistorico(pergunta,resposta): # armazenas dados no histórico
      arquivo = open("Analise/histórico.txt","a", encoding="utf8")
      arquivo_gravar = pergunta+"\n"+resposta+"\n\n"
      arquivo.write(arquivo_gravar)
      arquivo.close()
      return "salvo"

   # Faz a leitura do histórico ( remover trecho e refazer testes )
   def lerHistorico(): # Faz leitura no histórico
      arquivo = open("Analise/histórico.txt","r", encoding="utf8")
      arquivo_gravar = str(arquivo.read())
      arquivo.close()
      return arquivo_gravar
      
