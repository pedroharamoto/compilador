#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Pedro Vitor Jhum Haramoto RA: 161024157
# João Pedro Marin Comini   RA: 161020551
#

#importando a classe do analisador lexico
import analisador_lexico

#gerando a tabela de tokens com a função get_tokens da classe do analisador lexico
tokens = analisador_lexico.afd_lexico().create_table_token()

#
#   INICIO DA CLASSE A_SINTATICO()
#
class a_sintatico():
    #
    #
    #
    def __init__(self, tokens):
        #construtor
        self.tab_tokens = tokens
    #
    #
    #
    def get_token(self):
        return (self.tab_tokens.pop(0))
        #
        # a função pop(p1) remove e retorna um elemento da lista
        # p1 é um parametro para a posição da lista
        # se p1 não for especificado, pop() irá retornar e remover o ultimo elemento da lista
        # por isso vamos usar pop(0) para retornar e remover sempre o primeiro elemento
        #
        #
    #
    #
    #
    def show_tokens(self):
        #mostra os tokens
        token = self.get_token()

        while(token != ['&','&','&']):
            # o elemento ['&','&','&'] é o final da lista
            print(token)
            token = self.get_token()




sintatico = a_sintatico(tokens)

sintatico.show_tokens()
