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
        self.show_arvore(arvore)
        #self.show_saida(arvore)

    def show_saida(self,arvore):
        #esta função mostra os comandos reconhecidos
        for (i,linha) in enumerate(arvore):
            for(j,coluna) in enumerate(linha):
               print(coluna)

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
