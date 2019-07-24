#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__       = 'Gabriel Gregório da Silva'
__email__        = 'gabriel.gregorio.1@outlook.com'
__description__  = 'Comparador de frases'
__status__       = 'Development'
__date__         = '05/04/2019'
__last_update__  = '18/06/2019'
__version__      = '1.2'


# Módulo pyanalise
class compare():
    # Inicia a comparação
    def frase(a,b):
        # Dados inválidos
        if a == '' or b == '' or a.isspace() or b.isspace():
            return 0
        # o 'b' tem que ser maior que o 'a' ou no minimo igual!
        if len(a)>len(b):
            c = b
            b = a
            a = c
        # Remoção de espaços | Todos para minisculos | Adição de espaços | Para lista
        a = a.replace(' ','').lower()
        b = b.replace(' ','').lower()

        # Retorna a soma entre a análise por letras e a análise por duas silabas
        return (int(compare.letras(a,b)) + int(compare.bisilabas(a,b)))


    def letras(a,b):
        # Isolamento das variáveis 'a' e 'b'
        a_1 = a
        b_1 = b

        # Adição de espaços nas variáveis isoladas e tranformação em lista
        a_1 = a_1.replace('',' ').split(" ")
        b_1 = b_1.replace('',' ').split(" ")

        # Corte dos espaços no começo e no fim
        a = str(a[1:len(a)-1])
        b = str(b[1:len(b)-1])

        # Salva o total de posições na maior variável isolada (b)
        total_b = len(b_1)

        # Processamento de letras
        for x in a_1:
            for y in b_1:
                if x == y:
                    b_1.remove(y)
                    break
        # Retorna um valor de 0 a 50!
        try:
            return ((50/total_b)*(total_b-len(b_1)))
        except:
            print("Erro na saida da definição letras")
            return 0


    def bisilabas(a,b):
        # Isolamento das variáveis 'a' e 'b'
        ab = a
        bb = b

        # Criação das listas
        c = []
        d = []

        # Declaração dos andantes
        x = 0
        y = 0

        # Loops de 2 em 2 para criar uma lista de bisilabas
        while y < len(ab):
            c.append(ab[y:y+2])
            y=y+1
        while x < len(bb):
            d.append(bb[x:x+2])
            x=x+1

        # Registra o valor da maior variável isolada (b)
        b_salva = len(d)

        # Processamento de silabas
        for p in c:
            for l in d:
                if p == l:
                    d.remove(l)
                    break
        # Retorna um valor de 0 a 50!
        try:
            return ((50*(b_salva - len(d)) )/b_salva)
        except:
            print("Erro na saida da definição bissilabas")
            return 0