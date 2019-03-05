#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Esse script procura arquivos sem o ";", o ";" serve como delimitador entre uma pergunta e uma resposta!.

Cada ";" sinaliza uma posição diferente para a Diana, no exemplo abaixo, a Diana encherga três posições, 0, 1 e 2. Sendo 0 igual a "olá tudo bem", 1 igual a "tudo sim e você?" e 2 igual a "Eu também!". Caso você faça uma pergunta similar a posição 1, a Diana vai responder a posição 2.
 
Exemplo: olá tudo bem?; tudo sim e você; Eu também!

Esse script localiza pedaços sem a separação. Foi um processo demorado, cansativo e tedioso organizar os mais de 300 assuntos. Esse algoritimo simples achou pelo menos 2 arquivos que eu havia esquecido de colocar os separadores.
"""
x=1
while True:
  nano = str(x)+".txt"
  try:
     arquivo = open(nano,"r")
  except:
     print("\n\nNão achei nenhum arquivo sem o ;!\n\n")
     break
  string = arquivo.read()
  print(str(x)+".txt")
  if ";" in string:
    x=x+1
  else:
    print(x)
