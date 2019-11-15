#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__       = 'Gabriel Gregório da Silva'
__email__        = 'gabriel.gregorio.1@outlook.com'
__description__  = 'Geração de respostas para a Diana'
__status__       = 'Development'
__date__         = '15/11/2019'
__last_update__  = '15/11/2019'
__version__      = '1.0'

# pip3.6 install wikipedia
# pip install wikipedia
import wikipedia
from pyanalise import compare
import datetime

class wiki():
    def __init__(self):
        # definir idioma: pt-br não funciona mais
        wikipedia.set_lang('pt')

    def removeChaves(frase):
        fraseFiltrada = ''
        lerTexto = True

        for caractere in frase:
            if caractere == '(':
                lerTexto = False

            if lerTexto == False:
                pass
            else:
                if caractere.isalnum() or caractere == ' ' or caractere == ',':
                    fraseFiltrada += caractere

            if caractere == ')':
                lerTexto = True

        return fraseFiltrada

    def wikiAnalise(self, frase):
        frase = frase.lower()

        # Remoção de caracteres especiais
        novaFrase = ''
        for caractere in frase:
            if ((caractere.isnumeric()) or (caractere.isalpha())) or caractere == ' ':
                novaFrase += caractere
  
        buscarNaWikipedia = False
        listaBuscar = ['quem foi a','quem foi o','quem foi','quem é a','quem é o','quem é','o que o','o que a','o que é']
        for item in listaBuscar:
            if item in novaFrase:
                buscarNaWikipedia = True
                novaFrase = novaFrase.replace(item,'')
 
        if buscarNaWikipedia:
            try:
                lista = wiki.pesquisar(self,novaFrase)
            except Exception as erro1:
                return [False,erro1]
            else:
                maior = 0
                melhor = ''

                for item in lista:
                    novo = compare.frase(item, novaFrase)
                    if novo > maior:
                        maior = novo
                        melhor = item

                if melhor != '':
                    try:
                        resultado = wiki.obterS(self,melhor)
                    except Exception as erro2:
                        return [False,erro2]
                    else:
                        resultado = wiki.removeChaves(resultado)
                        return [True,resultado]

        return [False, "Nenhuma condição foi atendida"]

    # Pesquisa por um pais e retorna uma série de links
    def pesquisar(self,pesquisa):
        return wikipedia.search(pesquisa)

    # obter os sumários
    def obterS(self,link):
        return wikipedia.summary(link, sentences=1)
