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
        self.pos_linha = 0
        self.pos_coluna = 0
        self.buffer = []
        self.pensamento = ()
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
    def show_pens(self):
        for (i,linha) in enumerate(self.pensamento):
            print(linha)
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
            self.plvr_reservada()

    #
    #
    #
    def plvr_reservada(self):
        #
        self.buffer.append(self.token[0])
        #
        if(self.token[1] == 'PALAVRA_RESERVADA'):

            if(self.token[0] == 'begin' or self.token[0] == 'end'):
                self.pensamento = self.pensamento + (self.buffer,)
                self.buffer = []
                self.pos_linha = self.pos_linha + 1

            self.token = self.get_token()
            self.plvr_reservada()


        #
        elif(self.token[1] == 'SIMB_PONT'):
            terminal = self.sim_pont()
            if(terminal == 0):
                self.token = self.get_token()
                self.plvr_reservada()
            else:
                self.pensamento = self.pensamento + (self.buffer,)
                self.buffer = []
                self.pos_linha = self.pos_linha + 1
                self.token = self.get_token()
        #
        elif(self.token[1] == 'ID' or self.token[1] == 'SIMB_REL' or self.token[1] == 'ATT' or self.token[1] == 'NUM_INT' or self.token[1] == 'SIMB_ARIT'):
            self.token = self.get_token()
            self.plvr_reservada()
        else:
            if(self.token != ['&','&','&']):
                print('erro sintatico',self.token[2])
    #
    #
    #
    def sim_pont(self):
        if(self.token[0] == '.' or self.token[0] == ';'):
            #print(self.token)
            return 1 # 1 == terminal
        else:
            return 0 # 0 == nao terminal


#
# FIM DA CLASSE DO ANALISADOR SINTATICO
#

sintatico = a_sintatico(tokens)

sintatico.inicio()
sintatico.show_pens()
#sintatico.show_tokens()
