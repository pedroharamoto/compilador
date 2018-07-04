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
        self.tab_armazenamento = [] #tabela de variaveis de armazenamento
        self.pos_arb = 100 #posicao para armazenar MEPA
        self.prioridade = False
        self.rotulo = 1
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
        self.show_mepa()
        #self.show_saida()
    #
    #
    #
    def show_mepa(self):
        for(i,comandos) in enumerate(self.codigo_mepa):
            print(comandos)
    #
    #
    #
    def inicio(self):
        self.bloco()
    #
    #
    #
    def realiza_exp(self,exp):
        #
        #esse método irá fazer as 'contas'
        #é o metodo da notação polonesa reversa ou pos-fixa
        #
        k = 0
        j = len(exp)
        #
        pilha_op = classes.pilha_pol() #tabela para as operacoes >> pós-fixa
        pilha_op.empilha('(')
        #
        while(k<j):
            c = exp[k]
            #
            if(c[1] in ['NUM_INT','NUM_FLOAT']):
                codigo = "CRCT " + str(c[0])
                self.codigo_mepa.append(codigo)
            elif(c[1] == 'ID'):
                p = self.procura_id(c[0])
                codigo = "CRVL " + str(p[0])
                self.codigo_mepa.append(codigo)
            #
            elif(c[0] == '('):
                    pilha_op.empilha('(')
            #
            elif(c[0] == ')' or c[0] == ';' or c[0] == 'then' or c[0] == ',' or c[0] == 'do'):
                while True:
                    t = pilha_op.desempilha()
                    if(t != '('):
                        codigo = classes.codigo(t)
                        self.codigo_mepa.append(codigo)
                    elif(t == '('):
                        break
            #
            elif(c[0] == '+' or c[0] == '-' or c[0] == '*' or c[0] == '/' or c[0] in ['<','<=','>','>=','=','=>','=<']):
                while True:
                    t = pilha_op.desempilha()
                    if(classes.prioridade(c[0],t)):
                        pilha_op.empilha(t)
                        pilha_op.empilha(c[0])
                        break
                    else:
                        codigo = classes.codigo(t[0])
                        self.codigo_mepa.append(codigo)
            #
            k += 1
            #
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
            self.token = self.get_pensamento()
            #
            self.statm()
            #
            if(self.token[self.i][0] == 'end'):
                    self.token = self.get_pensamento()
                    if(self.token[self.i][0] == '.'):
                        self.codigo_mepa.append("PARA")
            #END end
    #
    #
    #
    def statm(self):

        self.i = 0
        #
        if(self.token[self.i][0] == 'begin'):
            self.token = self.get_pensamento()
            self.statm()
            #
            #aqui acabou o begin .. end;
            #
        #
        elif(self.token[self.i][0] == 'while'):
            n_rotulo = self.rotulo
            codigo = "L"+str(n_rotulo)+" NADA"
            self.rotulo += 1
            n_rotulo += 1
            self.codigo_mepa.append(codigo)
            self.i+=1
            #
            #aqui devo chamar a realiza_exp
            #
            exp = []
            while(True):
                exp.append(self.token[self.i])
                self.i += 1
                if(self.token[self.i][0] == 'do'):
                    exp.append(self.token[self.i])
                    break
            #
            self.realiza_exp(exp)
            #
            # devo add uma chamada ao prox label para sair do while
            #
            codigo = "DSVF L"+str(n_rotulo)
            self.rotulo += 1
            self.codigo_mepa.append(codigo)
            #
            self.token = self.get_pensamento()
            self.statm()
            #devo add uma chamada ao primeiro label, para fazer o looping
            codigo = "DVSV L"+str((n_rotulo-1))
            self.codigo_mepa.append(codigo)
            codigo = "L"+str((n_rotulo)) + " NADA"
            self.codigo_mepa.append(codigo)

        #
        elif(self.token[self.i][0] == 'write'):
            #write(a,b*c);
            self.i += 1 # >>> (
            self.i += 1
            #
            while(True):

                exp = []
                while(True):
                    exp.append(self.token[self.i])
                    self.i += 1
                    if(self.token[self.i][0] == ','):
                        exp.append(self.token[self.i])
                        self.realiza_exp(exp)
                        self.codigo_mepa.append('IMPR')
                        self.i += 1
                        break
                    if(self.token[self.i][0] == ')'):
                        exp.append([',','SIMB_PONT',self.i])
                        self.realiza_exp(exp)
                        self.codigo_mepa.append('IMPR')
                        self.i+=1
                        break
                #
                if(self.token[self.i][0] in [')',';']):
                    break


        #end write
        #
        elif(self.token[self.i][0] == 'read'):
            #read(a,b);
            self.i += 1 #aqui será um parenteses
            self.i += 1 #será a primeira variavel
            #
            while(True):
                var = self.procura_id(self.token[self.i][0])
                if(var):
                    self.codigo_mepa.append('LEIT')
                    #
                    codigo = "ARMZ " + str(var[0]) #0: nome; 1:posicao
                    self.codigo_mepa.append(codigo)
                #
                else:
                    self.err2(self.token[self.i])
                self.i += 1
                if(self.token[self.i][0] == ','):
                    self.i += 1
                elif(self.token[self.i][0] == ')'):
                    break
            #
            self.token = self.get_pensamento()
            self.statm()

        #end read
        elif(self.token[0][1] == 'ID'):
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
                    #
                    #aqui devo chamar a realiza_exp
                    #
                    exp = []
                    while(True):
                        exp.append(self.token[self.i])
                        self.i += 1
                        if(self.token[self.i][0] == ';'):
                            exp.append(self.token[self.i])
                            break
                    #
                    self.realiza_exp(exp)
                    #
                    if(self.token[self.i][0] == ';'):
                        #
                        texto = "ARMZ " + str(var[0])
                        self.codigo_mepa.append(texto)
                        self.token = self.get_pensamento()
                        self.statm()
            else:
                self.err2(self.token[self.i])
        #end ID
        elif(self.token[0][0] == 'if'):
            self.i += 1
            #prepara para chamar o realiza_exp()
            exp = []
            while(True):
                exp.append(self.token[self.i])
                self.i += 1
                if(self.token[self.i][0] == 'then'):
                    exp.append(self.token[self.i])
                    break
            #
            self.realiza_exp(exp)
            #
            #pulo pro else, se tiver é necessario tratar, senão é só ignora
            #
            codigo = "DSVF L" + str(self.rotulo)
            self.codigo_mepa.append(codigo)
            #
            #
            self.token = self.get_pensamento()
            self.statm()
        #end if
        elif(self.token[0][0] == 'else'):
            codigo = "L" + str(self.rotulo) + " NADA"
            self.rotulo += 1
            self.codigo_mepa.append(codigo)
            self.token = self.get_pensamento()
            self.statm()
        #end else
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
    def show_saida(self):
        for(i,linha) in enumerate(self.tab_sintatica):
            print(linha,'\n')
    #
    #
    #
    def err2(self,token):
        print('ERRO semantico:::: "',token[0],'" não esperado na linha',token[2])
        exit(0)


#
# FIM DA CLASSE A_SEMANTICO()
#

semantico = a_semantico(arv_sintatica,cod_mepa,tab_id)
