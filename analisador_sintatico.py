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
        while(self.token != ['&','&','&']):
            # o elemento ['&','&','&'] é o final da lista
            print(self.token)
            self.token = self.get_token()
    #
    #
    #
    def inicio(self):

        while(self.token != ['&','&','&'] and self.token):
            self.progr()
            self.bloco()



            print(self.pensamento,"\n")
            self.token = self.get_token()

    #
    #
    #
    def progr(self):
        #progr ::= progr ID '(' {ID | ','}+ ')' ';' bloco '.'
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
    #
    #
    def var(self):
        #
        #estado para ler a declarão de variavel
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
                            self.err()
                    else:
                        self.err()

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

#
# FIM DA CLASSE DO ANALISADOR SINTATICO
#

sintatico = a_sintatico(tokens)

sintatico.inicio()
#sintatico.show_saida()
#sintatico.show_tokens()
