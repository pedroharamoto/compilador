#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Pedro Vitor Jhum Haramoto RA: 161024157
# João Pedro Marin Comini   RA: 161020551
#

#importando a classe do analisador lexico
import analisador_lexico

#gerando a tabela de tokens com a função get_tokens da classe do analisador lexico
tokens = analisador_lexico.afd_lexico().get_tokens()

#
#   INICIO DA CLASSE A_SINTATICO()
#
class a_sintatico():
    #
    #
    #
    def __init__(self, tokens):
        #construtor
        self.show_tokens(tokens)
    #
    #
    #
    def show_tokens(self, tokens):
        #mostra os tokens
        for (i, token) in enumerate(tokens):
            print(token[2],":")
            for (j, elemento) in enumerate(token):
               print("\t",elemento)

re = a_sintatico(tokens)
