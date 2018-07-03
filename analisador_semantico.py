#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Pedro Vitor Jhum Haramoto RA: 161024157
# João Pedro Marin Comini   RA: 161020551
#

#importando a classe do analisador lexico
import analisador_lexico

#importando a classe do analisador sintatico
import analisador_sintatico

#importando a classe que contém as estruturas
import classes

#gerando a tabela de tokens com a função get_tokens da classe do analisador lexico
tokens = analisador_lexico.afd_lexico().create_table_token() #executa a analise lexica e cria a tabela dos tokens

#gerando a arvore sintatica
sintatico = analisador_sintatico.a_sintatico(tokens)
sintatico.inicio() #executa a analise sintatica
arv_sintatica = sintatico.create_arv_sintatica() #cria a arvore sintatica
cod_mepa = sintatico.create_cod_mepa()
tab_id = sintatico.create_tab_id()
#
#   INICIO DA CLASSE A_SEMANTICO()
#
class a_semantico():

    def __init__(self,arvore,mepa,tab_id):
        #
        #self.show_arvore(arvore)
        #
        self.tab_sintatica = arvore
        #
        #MEPA
        #***************************
        self.i = 0 #variavel para saber qual token dentro de um pensamento
        self.codigo_mepa = mepa
        self.tab_id = tab_id
        self.tab_variaveis = classes.tab_variaveis() #tabela de variaveis
        self.tab_armazenamento = [] #tabela de variaveis de armazenamento
        self.pos_arb = 100 #posicao para armazenar MEPA
        #***************************
        self.tam_tab_sint = len(self.tab_sintatica) #tamanho de 'pensamentos'
        #
        self.posicao = len(mepa)
        #posição inicial dos pensamentos
        #começo em len(mepa)+1, já pegou a parte do program e var no sintatico
        #o gerador mepa irá se preocupar a partir do begin/procedure
        self.token = self.get_pensamento()
        #self.show_pensamento()
        self.inicio()
        print(self.codigo_mepa)
    #
    #
    #
    def inicio(self):
        self.bloco()
    #
    #
    #
    def procura_id(self,id):
        #
        #procura na tabela tab_id o id, se existir,
        #retorna sua 'tupla'. Ex ['a',100], senao retorna None
        #
        for(i,linha) in enumerate(self.tab_id):
            if(linha[0] == id):
                return linha
        #
        return None #nao achou nada
    #
    #
    def bloco(self):
        if(self.token[0][0] == 'begin'):
            self.codigo_mepa.append('LEIT')
            self.token = self.get_pensamento()
            #
            self.statm()
    #
    #
    #
    def statm(self):

        self.i = 0

        if(self.token[0][1] == 'ID'):
            #
            #possível atribuição
            #
            var = self.procura_id(self.token[0][0])
            if(var):
                #
                self.i = 1
                if(self.token[self.i][0] == ':='):
                    #atribuição
                    self.i += 1
                    self.exp()
                    #
                    if(self.token[self.i][0] == ';'):
                        #
                        texto = "ARMZ " + str(var[1])
                        self.codigo_mepa.append(texto)
                        self.token = self.get_pensamento()
                        self.statm()
            else:
                print("erro semantico:", self.token[0][0], "inesperado")
    #
    #
    #
    def exp(self):
        #
        #estado para ler uma expressao
        #
        self.si_exp()
        #
        if(self.token[1] == 'SIMB_REL'):
            self.buffer.append(self.token)
            self.token = self.get_token()

            if(not (self.token[1] in ['ID','NUM_FLOAT','NUM_INT','STRING1','STRING2'])):
                self.err2(self.token)

            self.exp()

        #
        elif(self.token[0] == ';'):
            self.buffer.append(self.token)
            self.pensamento += (self.buffer,)
            self.buffer = []
            self.token = self.get_token()
            return
        #
    #
    #
    #
    def si_exp(self):
        #
        #estado para reconhecer '+,-,or'
        #
        self.term()
        #
        if(self.token[0] in ['+','-','or']):
            self.buffer.append(self.token)
            self.token = self.get_token()

            if((self.token[1] not in ['ID','NUM_FLOAT','NUM_INT'])):
                #erro do tipo a := a-++b;
                self.err2(self.token)

            self.term()
            self.si_exp()
        #
    #
    #
    #
    def term(self):
        #
        #estado para reconhecer '*,/,div,mod,and'
        #
        self.factor()

        if(self.token[self.i][0] in ['*','/','div','mod','and']):
            self.buffer.append(self.token)
            self.token = self.get_token()

            if((self.token[self.i][1] not in ['ID','NUM_FLOAT','NUM_INT'])):
                #erro do tipo a := **mod a;
                self.err2(self.token)

            self.factor()
            self.term()
        #
    #
    #
    #
    def factor(self):
        #
        #estado para reconhecer alguma variavel,numero ou string
        #
        if(self.token[self.i][0] == '('):
            self.i += 1
            self.exp()
            if(self.token[self.i][0] == ')'):
                self.i += 1
                return
        #
        elif(self.token[self.i][1] in ['NUM_FLOAT','NUM_INT']):
            texto = "CRCT " + str(self.token[self.i][0])
            self.codigo_mepa.append(texto)
            self.i += 1
        #
    #
    #
    #
    def get_pensamento(self):
        while(self.posicao < self.tam_tab_sint):
            self.posicao += 1
            return (self.tab_sintatica[self.posicao])

#
# FIM DA CLASSE A_SEMANTICO()
#

semantico = a_semantico(arv_sintatica,cod_mepa,tab_id)
