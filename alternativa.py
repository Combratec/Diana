#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Esse módulo recebe uma entrada e procura se há semelhanças entre a pergunta que foi digitada pelo usuário e o conteúdo de “texto” de alguns arquivos de áudio já gerados, para otimizar as possíveis respostas.

def alternativa(entrada):
    lista = ("Você conhece","Você sabia","Você já","Você gosta de","O que é","Quando isso","Você pode me recomendar","Como se diz","O que você recomenda","Você estava")

    x=0
    total = int(len(lista))-1
    posição = -1

    while x<=total:
        if (lista[x].lower() in entrada.lower()):
            posição = x
        x=x+1
    if posição == -1:
        return "none"
    else:
        return lista[posição]
