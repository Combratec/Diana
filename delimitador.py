#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Esse módulo está em modo alfa, ele limita caracteres de uma frase

def delimitar(variável_nao_tupla):
     variável_nao_tupla = str(variável_nao_tupla)
     total = len(variável_nao_tupla)
     andar = 35 # andar de 5 em 5 casas
     maximo = 160 # Quantidade máxima de caracteres
     inicial = 0
     virtual = ""
     bug = 0
     if total<maximo:
         continuar = int(maximo-total)
         string = " "*continuar
         variável_nao_tupla = variável_nao_tupla+string
     if total>maximo:
         variável_nao_tupla = variável_nao_tupla[0:maximo]
     while True:
        if andar>=maximo:
            if bug==0:
                virtual = variável_nao_tupla
            break
        else:         
            virtual = virtual+"\n"+variável_nao_tupla[inicial:andar]
            inicial = andar        
        andar=andar+35
        bug = bug+1
     base = virtual
     return base
