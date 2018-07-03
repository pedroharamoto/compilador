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

#gerando a tabela de tokens com a função get_tokens da classe do analisador lexico
tokens = analisador_lexico.afd_lexico().create_table_token() #executa a analise lexica e cria a tabela dos tokens

#gerando a arvore sintatica
sintatico = analisador_sintatico.a_sintatico(tokens)
sintatico.inicio() #executa a analise sintatica
arv_sintatica = sintatico.create_arv_sintatica() #cria a arvore sintatica

#
#   INICIO DA CLASSE A_SEMANTICO()
#
class a_semantico():

    def __init__(self,arvore):
        #
        #self.show_arvore(arvore)
        #
        self.tab_sintatica = arvore
        self.tab_variaveis = () #tupla para a table de variaveis. ela é ([variavel,tipo,valor]). EX: ([a,integer,4]), ao declarar, o valor é dado como 0
        self.tab_procedures = []
        #

        self.tam_tab_sint = len(self.tab_sintatica)
        self.posicao = 0 #posição inicial dos pensamentos
        #começo em 1, pois a posição 0 é a 'program ex1;', como ja passou pelo sintatico, não preciso verificar essa parte, semanticamente
        #e a posição 1 é o pensamento "var"
    #
    #
    #
    def show_tab_var(self):
        #
        for(i,linha) in enumerate(self.tab_variaveis):
            print(linha)
    #
    #
    #
    def show_pensamento(self):
        while(self.posicao < self.tam_tab_sint):
            print(self.tab_sintatica[self.posicao],'\n')
            self.posicao += 1
    #
    #
    #
    def show_saida(self,arvore):
        #esta função mostra os comandos reconhecidos
        for (i,linha) in enumerate(arvore):
            for(j,coluna) in enumerate(linha):
               print(coluna)
    #
    #
    #
    def show_arvore(self,arvore):
        #
        buffer = ""
        #
        for(i,linha) in enumerate(arvore):
            for(j,coluna) in enumerate(linha):
                buffer += coluna[0] + " "
            #
            print(buffer)
            buffer = ""

#
# FIM DA CLASSE A_SEMANTICO()
#

semantico = a_semantico(arv_sintatica)
semantico.show_pensamento()
