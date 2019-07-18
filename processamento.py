#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__       = 'Gabriel Gregório da Silva'
__email__        = 'gabriel.gregorio.1@outlook.com'
__description__  = 'Processamento de respostas para chatbots'
__status__       = 'Development'
__date__         = '18/04/2019'
__last_update__  = '18/06/2019'
__version__      = '1.2'

# Importação do pyanalise
from pyanalise import compare
import os

def analise(resposta):

    maior = [0,0,0,0]
    tem_depois = 0

    for rota in os.listdir('arquivos/conteudo/'):
        rota_full = str('arquivos/conteudo/' + str(rota))

        arquivo = open (rota_full,'r',encoding='utf8')
        string = str(arquivo.read())
        arquivo.close()

        lista = string.split(';')

        y = 0

        while True:
            try:
                analise = compare.frase(resposta,lista[y])
            except:
                break

            # Precisão
            if analise > float(maior[0]):

                # Tem alguma frase na posicao + 1?
                if (len(lista) <= y+1):
                    tem_depois = 0
                else:
                    tem_depois = 1

                # precisão | pos_file | pos_fras | p_frase+1 existe?
                maior = [analise,rota,y,tem_depois] 
            y = y+1
   
    # precisão | pos_file | pos_fras | p_frase+1 existe?
    return maior

def analise_comandos(resposta,link):
    maior = [0,0]
    arquivo = open (link,'r',encoding='utf8')
    string = str(arquivo.read())
    arquivo.close()

    lista = string.split('\n')

    for x in range (len(lista)):
        y = lista[x].split(';')
        if len(y)>0:
            analise = compare.frase(resposta,y[0])
            if analise > float(maior[0]):
                o_que_responder = y[1]
                o_que_era = y[0]
                maior = [analise,o_que_responder,o_que_era] 

    return maior
