#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Analisador de arquivos repetidos

x=1
sair="nao"
while sair=="nao":
  nano = str(x)+".txt"
  try:
     arquivo = open(nano,"r")
  except:
     print("\n\nNão achei conteúdo repetido!\n\n")
     break
  string = arquivo.read()
  arquivo.close()
  y=1
  while True:
    analise = str(y)+".txt"
    if x==y:
      pass
    else:
      try:
        arquivo = open(analise,"r")
      except:
        break
      exibir = arquivo.read()
      arquivo.close()
      print(exibir,string)
      if exibir == string:
        sair="sim"
        print("Arquivo {}.txt é igual ao arquivo {}.txt".format(x,y))
        break
    y=y+1
  x=x+1
