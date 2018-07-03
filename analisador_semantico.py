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
#
#   INICIO DA CLASSE A_SEMANTICO()
#
class a_semantico():

    def __init__(self,arvore,mepa):
        #
        #self.show_arvore(arvore)
        #
        self.tab_sintatica = arvore
        self.tab_variaveis = classes.tab_variaveis() #tabela de variaveis
        #
        self.tam_tab_sint = len(self.tab_sintatica) #tamanho de 'pensamentos'
        self.posicao = len(mepa)+1 #posição inicial dos pensamentos
        #começo em len(mepa)+1, já pegou a parte do program e var no sintatico
        #o gerador mepa irá se preocupar a partir do begin/procedure
        self.show_pensamento()
    #
    #
    #
    def show_pensamento(self):
        while(self.posicao < self.tam_tab_sint):
            print(self.tab_sintatica[self.posicao])
            self.posicao += 1

#
# FIM DA CLASSE A_SEMANTICO()
#

semantico = a_semantico(arv_sintatica,cod_mepa)
