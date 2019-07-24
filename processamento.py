#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__       = 'Gabriel Gregório da Silva'
__email__        = 'gabriel.gregorio.1@outlook.com'
__description__  = 'Processamento de respostas para chatbots'
__status__       = 'Development'
__date__         = '18/04/2019'
__last_update__  = '18/06/2019'
__version__      = '1.2'

from pyanalise import compare
import os

def analise(resposta):
    best_likeness = [0,0,0,0]
    have_after = 0
    for route in os.listdir('arquivos/conteudo/'):
        route_full = str('arquivos/conteudo/' + str(route))
        file = open (route_full,'r',encoding='utf8')
        string = str(file.read())
        file.close()
        lista = string.split(';')
        y = 0
        while True:
            try:
                analyze = compare.frase(resposta,lista[y])
            except:
                break
            if analyze > float(best_likeness[0]):
                if (len(lista) <= y+1):
                    have_after = 0
                else:
                    have_after = 1
                best_likeness = [analyze,route,y,have_after] 
            y = y+1
    # [precisão , pos_file , pos_fras , p_frase+1 existe]
    return best_likeness

def analise_comandos(resposta,link):
    best_likeness = [0,0]
    file = open (link,'r',encoding='utf8')
    string = str(file.read())
    file.close()
    lista = string.split('\n')
    for x in range (len(lista)):
        y = lista[x].split(';')
        if len(y)>0:
            analyze = compare.frase(resposta,y[0])
            if analyze > float(best_likeness[0]):
                what_to_answer = y[1]
                what_was = y[0]
                best_likeness = [analyze,what_to_answer,what_was] 
    return best_likeness
