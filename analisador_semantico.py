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
        self.tab_variaveis = [] #tabela de variaveis
        self.tab_armazenamento = [] #tabela de variaveis de armazenamento
        self.pos_arb = 100 #posicao para armazenar MEPA
        self.tab_operacoes = [] #tabela para as operacoes >> FIFO
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
    def realiza_exp(self):
        #
        #esse método irá fazer as 'contas'
        #lembrando: tab_variaveis -> tira do topo
        #lembrando: tab_operacoes -> FIFO
        #primeiro: carregar as variaveis, depois executar as operacoes. dois a dois
        #carrega 2 valores, executa 1 operação e chama realiza_exp novamente
        #até que tab_var seja None
        #
        if(self.tab_variaveis):
            x1 = self.tab_variaveis.pop(0) #pop() pega o topo da lista
            #
            if(x1[1] in ['NUM_FLOAT','NUM_INT']):
                cod = "CRCT " + str(x1[0])
                self.codigo_mepa.append(cod)
            elif(x1[1] == 'ID'):
                #buscar o endereço da variavel
                x1 = self.procura_id(x1[0])
                cod = "CRVL " + str(x1[0]) + ""
                self.codigo_mepa.append(cod)
            #
            self.realiza_exp()
        #
        elif(self.tab_operacoes):
            op1 = self.tab_operacoes.pop() #pop() pega o primeiro
            if(op1 == '+'):
                self.codigo_mepa.append("SOMA")
            elif(op1 == '-'):
                self.codigo_mepa.append("SUB")
            elif(op1 == '*'):
                self.codigo_mepa.append("MULT")
            elif(op1 == '/'):
                self.codigo_mepa.append("DIV")
            elif(op1 == 'div'):
                self.codigo_mepa.append("DIVI")
            self.realiza_exp()
        else:
            return

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
                    self.tab_variaveis = []
                    self.exp()
                    #
                    #aqui devo chamar a realiza_exp
                    #
                    print(self.tab_operacoes)
                    self.realiza_exp()
                    #
                    if(self.token[self.i][0] == ';'):
                        #
                        texto = "ARMZ " + str(var[1])
                        self.codigo_mepa.append(texto)
                        self.token = self.get_pensamento()
                        self.statm()
            else:
                print("erro semantico:", self.token[0][0], "inesperado")
        #end ID
        elif(self.token[0][0] == 'end'):
            self.token = self.get_pensamento()
            if(self.token[0][0] == '.'):
                self.codigo_mepa.append("PARA")
        #END end
    #
    #
    #
    def exp(self):
        #
        #estado para ler uma expressao
        #
        self.si_exp()
        #
        if(self.token[self.i][1] == 'SIMB_REL'):
            self.i += 1

            if(not (self.token[self.i][1] in ['ID','NUM_FLOAT','NUM_INT','STRING1','STRING2'])):
                self.err2(self.token)

            self.exp()

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
        if(self.token[self.i][0] in ['+','-','or']):
            self.tab_operacoes.insert(0,self.token[self.i][0])
            #jogar na tab de OPERACOES
            self.i += 1
            if((self.token[0][1] not in ['ID','NUM_FLOAT','NUM_INT'])):
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
            self.tab_operacoes.insert(0,self.token[self.i][0])
            self.i += 1

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
        elif(self.token[self.i][1] in ['NUM_FLOAT','NUM_INT','ID']):
            self.tab_variaveis.insert(0,self.token[self.i])
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
    #
    #
    def err2(self,token):
        print('ERRO:::: "',token,'" não esperado na linha',token)
        exit(0)


#
# FIM DA CLASSE A_SEMANTICO()
#

semantico = a_semantico(arv_sintatica,cod_mepa,tab_id)
