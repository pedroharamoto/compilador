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
        self.token = self.get_token() #ja pega o primeiro token
    #
    #
    #
    def get_token(self):
        #essa função irá retornar o token que está no topo da pilha
        if(len(self.tab_tokens) != 0):
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
        while(self.token != ['&','&','&']):
            # o elemento ['&','&','&'] é o final da lista
            print(self.token)
            self.token = self.get_token()
    #
    #
    #
    def inicio(self):
        #mostra os tokens

        while(self.token != ['&','&','&'] and (self.token)):
            # o elemento ['&','&','&'] é o final da lista

            if(self.token[1] == "PALAVRA_RESERVADA"):
                print('palavra reservada')
                self.token = self.get_token()
                self.plvr_reservada()

            self.token = self.get_token()
    #
    #
    #
    def plvr_reservada(self):

        if(self.token[1] == 'SIMB_PONT'):
            self.token = self.get_token()

        elif(self.token[1] == 'ID'):
            print(self.token)
            self.token = self.get_token()
            self.plvr_reservada()

    #
    #
    #



#
# FIM DA CLASSE DO ANALISADOR SINTATICO
#

sintatico = a_sintatico(tokens)

sintatico.inicio()
