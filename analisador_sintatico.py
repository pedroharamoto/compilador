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
    def show_saida(self):
        for (i,linha) in enumerate(self.pensamento):
            print(linha)
    #
    #
    #
    def show_tokens(self):
        #mostra os tokens
        for (i,linha) in enumerate(self.tab_tokens):
            print(linha)
    #
    #
    #
    def inicio(self):

        while(self.token != ['&','&','&'] and self.token):
            self.progr()
            self.bloco()

            self.token = self.get_token()
        self.show_saida()
    #
    #
    #
    def progr(self):
        #
        #regra para o inicio de um programa em pascal:::
        #progr ::= progr ID '(' {ID | ','}+ ')' ';' bloco '.'
        #
        if(self.token[0] == 'program'):
            self.buffer.append(self.token[0])
            self.token = self.get_token()
            #
            if(self.token[1] == 'ID'):
                self.buffer.append(self.token[0])
                self.token = self.get_token()
                #
                if(self.token[0] == ';'):
                    self.buffer.append(self.token[0])
                    self.token = self.get_token()
                    self.pensamento += (self.buffer,)
                    self.buffer = []
                    return
                else:
                    self.err(";",self.token[0])
            else:
                self.err(";",self.token[0])
    #
    #
    #
    def bloco(self):
        #
        self.var()
        #
        self.begin()
    #
    #
    #
    def begin(self):
        #
        #estado para ler a partir do begin de um codigo, até o ultimo end
        #
        if(self.token[0] == 'begin'):
            self.buffer.append(self.token[0])
            self.pensamento += (self.buffer,)
            self.buffer = []
            self.token = self.get_token()

            self.statm()
    #
    #
    #
    def statm(self):
        #
        #estado para ler um statment
        #
        if(self.token[1] == 'ID'):

            self.buffer.append(self.token[0])
            self.token = self.get_token()

            if(self.token[0] == ':='):
                self.buffer.append(self.token[0])
                self.token = self.get_token()
                self.exp()
                self.statm()
        #
        elif(self.token[0] == ';'):
            self.buffer.append(self.token[0])
            self.pensamento += (self.buffer,)
            self.buffer = []
            return
    #
    #
    #
    def exp(self):
        #
        #estado para ler uma expressao
        #
        if(self.token[0] == '('):
            self.buffer.append(self.token[0])
            self.token = self.get_token()
            self.exp();
        #
        elif(self.token[1] in ['NUM_INT','NUM_FLOAT','STRING1','STRING2','ID']):
            self.buffer.append(self.token[0])
            self.token = self.get_token()
            self.termo()
        #
        elif(self.token[1] in ['SIMB_REL','SIMB_ARIT']):
            self.buffer.append(self.token[0])
            self.token = self.get_token()
            self.exp()
        #
        elif(self.token[0] == ')'):
            self.buffer.append(self.token[0])
            self.token = self.get_token()
            self.exp();
        #
        elif(self.token[0] == ';'):
            return
        else:
            self.err2(self.token)
    #
    #
    #
    def termo(self):
        pass
    #
    #
    #
    def var(self):
        #
        #estado para ler a declarão de variavel. COMPLETO
        #
        if(self.token[0] == 'var'):
            self.buffer.append(self.token[0])
            self.token = self.get_token()

            if(self.token[1] == 'ID'):

                self.buffer.append(self.token[0])
                self.token = self.get_token()

                while(self.token[0] != ':'):

                    if(self.token[0] == ','):
                        self.buffer.append(self.token[0])
                        self.token = self.get_token()

                        if(self.token[1] == 'ID'):
                            self.buffer.append(self.token[0])
                            self.token = self.get_token()
                        else:
                            self.err(";",self.token[0])
                    else:
                        self.err(";",self.token[0])

                if(self.token[0] == ':'):
                    self.buffer.append(self.token[0])
                    self.token = self.get_token()

                    if(self.token[0] == 'integer'):
                        self.buffer.append(self.token[0])
                        self.token = self.get_token()

                        if(self.token[0] == ';'):
                            self.buffer.append(self.token[0])
                            self.pensamento += (self.buffer,)
                            self.buffer = []
                        else:
                            self.err(";",self.token[0])
                    else:
                        self.err(";",self.token[0])
                else:
                    self.err(";",self.token[0])
            else:
                self.err(";",self.token[0])
    #
    #
    #
    def err(self,l,f):
        print('erro> ',l,' não encontrado. Encontrado: "',f,'"')

    def err2(self,token):
        print('"',token[0],'" não esperado na linha',token[2])

#
# FIM DA CLASSE DO ANALISADOR SINTATICO
#

sintatico = a_sintatico(tokens)

sintatico.inicio()
#sintatico.show_saida()
#sintatico.show_tokens()
