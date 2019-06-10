#!/usr/bin/python3
# -*- coding: utf-8 -*-

class diana(): # Classe principal 
   def __init__(self):
      pass

   # Esta definição realiza testes dos principais módulos e retorna o status de funcionamento deles, além de tentar instalar módulos ausentes.
   def testa_modulos():
      mipand_modulo            = "1"
      os_modulo                = "1"
      speechrecognition_modulo = "1"
      pyaudio_modulo           = "1"
      playsound_modulo         = "1"   
      gtts_modulo              = "1"
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

      def instalar_atualizar_pip_3():
          try:
              import pip
          except:
            
      ignorar_instalacao = "nao"
      
      try:
         import os
      except:
         RES_OS = ERRO
         os_modulo = "0"

      try:
         import ast                 
      except:
         RES_AST = ERRO

      try:
         import time                 
      except:
         RES_TIME = ERRO

      try:
         import mipand
      except:
         RES_MIPAND = ERRO
         mipand_modulo = "0"

      try:
          import webbrowser           
      except:
         RES_WEBBROWSER = ERRO

      try:
         import definicoes          
      except:
         RES_DEFINICOES = ERRO           

      try:
         import alternativa  
      except:
         RES_ALTERNATIVA = ERRO

      try:
         import delimitador    
      except:
         RES_DELIMITADOR = ERRO
 
      try:
         import tkinter          
      except:
         try:
            import Tkinter          
         except:
            RES_TKINTER = ERRO    

      try:
         import gtts               
      except:
         try:
            import gtts               
         except:
            RES_GTTS    = ERRO
            gtts_modulo = "0"

      def instalacao_pyaudio_definicao():
          try:
              import pyaudio            
          except:
              pyaudio_modulo = "0"
              RES_PYAUDIO = ERRO

      instalacao_pyaudio_definicao()

      verificar_atualizar_pyaudio = "sim"
      
      try:
         import playsound
      except:
         RES_PLAYSOUND = ERRO
         playsound_modulo = "0"

      try:
         import speech_recognition
      except:
         RES_SPEECH_RECOGNITION = ERRO
         speechrecognition_modulo = "0"

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
      
