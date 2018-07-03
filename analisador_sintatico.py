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
        self.buffer = [] #indica os comandos que farão parte um pensamento. ex: program, ex, ;
        self.pensamento = () #indica um comando. Ex: program ex;
        self.tab_tokens = tokens
        self.token = self.get_token() #ja pega o primeiro token
        #MEPA#
        #**********#
        self.cont_vars = 0 #variavel para contar a quantidade de variaveis que serao alocadas
        self.cod_mepa = [] #variavel para guardar as instruções MEPA
        #**********#
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
    def create_arv_sintatica(self):
        return self.pensamento
    #
    #
    #
    def create_cod_mepa(self):
        return self.cod_mepa
    #
    #
    #
    def show_saida(self):
        #esta função mostra os comandos reconhecidos
        for (i,linha) in enumerate(self.pensamento):
            for(j,coluna) in enumerate(linha):
               print(coluna)
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
        self.progr()
    #
    #
    #
    def progr(self):
        #
        #regra para o inicio de um programa em pascal:::
        #progr ::= progr ID '(' {ID | ','}+ ')' ';' bloco '.'
        #
        if(self.token[0] == 'program'):
            self.buffer.append(self.token)
            self.token = self.get_token()
            #
            if(self.token[1] == 'ID'):
                self.buffer.append(self.token)
                self.token = self.get_token()
                #
                if(self.token[0] == ';'):
                    self.buffer.append(self.token)
                    self.token = self.get_token()
                    self.pensamento += (self.buffer,)
                    self.buffer = []
                    #
                    # fim do 'program xxx;'. Portanto, chama-se bloco()
                    #

                    #MEPA#
                    #**********#
                    #como achei um program xxxx;, devo add a instrução mepa INPP
                    self.cod_mepa.append("INPP")
                    #
                    #**********#
                    self.bloco()
                    #
                    if(self.token[0] == '&'): #não achou nada
                        self.err()
                    #
                    self.token = self.get_token()
                    #
                    #pego o proximo token, se for um '.'
                    #então, é o fim do programa
                    #
                    if(self.token[0] == '.'):
                        self.buffer.append(self.token)
                        self.pensamento += (self.buffer,)
                        self.buffer = []
                    else:
                        #se não achou um '.'
                        self.err2(self.token)
                else:
                    #se não achou um ';'
                    self.err2(self.token)
            #
            else:
                #se não achou um ID
                self.err2(self.token)
        else:
            #não achou um program
            self.err2(self.token)
    #
    #
    #
    def type(self):
        #
        #estado para reconhcer os tipos de variavel
        #
        if(self.token[0] in ['boolean','char','integer', 'real', 'string']):
            self.buffer.append(self.token)
            self.token = self.get_token()
        #
        elif(self.token[0] == 'array'):
            self.buffer.append(self.token)
            self.token = self.get_token()
            #
            if(self.token[0] == '['):
                self.buffer.append(self.token)
                self.token = self.get_token()
                #
                while(True):
                    #
                    self.sitype()
                    #
                    if(self.token[0] == ']'):
                        self.buffer.append(self.token)
                        self.token = self.get_token()
                        break;
                    #
                    elif(self.token[0] == ','):
                        self.buffer.append(self.token)
                        self.token = self.get_token()
                    #
                    else:
                        self.err2(self.token)
                #
                #
                #
                if(self.token[0] == 'of'):
                    self.buffer.append(self.token)
                    self.token = self.get_token()
                    self.type()
                    #
                    if(self.token[0] == ';'):
                        self.buffer.append(self.token)
                        self.pensamento += (self.buffer,)
                        self.buffer = []
                        self.token = self.get_token()
                    #
                    else:
                        self.err2(self.token)
                else:
                    self.err2(self.token)
            #
            else:
                self.err2(self.token)
        else:
            self.err2(self.token)
    #
    #
    #
    def sitype(self):
        #
        self.const()
        #
        if(self.token[0] == '..'):
            self.buffer.append(self.token)
            self.token = self.get_token()
            self.const()
        else:
            self.err2(self.token)
    #
    #
    #
    def const(self):
        #
        if(self.token[1] in ['STRING1','STRING2','ID','NUM_INT','NUM_FLOAT']):
            self.buffer.append(self.token)
            self.token = self.get_token()
        #
        else:
            self.err2(self.token)

    #
    #
    #
    def bloco(self):
        #
        #estado para ler os BLOCKS.
        #
        if(self.token[0] == 'var'):
            #
            self.buffer.append(self.token)
            self.pensamento += (self.buffer,)
            self.buffer = []
            #
            self.token = self.get_token()
            #
            self.var() #aqui vou pegar TODAS as variaveis possiveis
            #
            self.bloco()
            #
        ##
        ##fim da declaração de variavel
        ##
        elif(self.token[0] == 'begin'):
            ##
            ## se encontrar um begin, no inicio do programa.
            ##
            self.buffer.append(self.token)
            self.pensamento += (self.buffer,)
            self.buffer = []
            self.token = self.get_token()
            #
            while(self.token[0] != 'end'):
                #
                self.statm()
                #
                #self.token = self.get_token()
            #
            #saiu do while, logo self.token guarda um 'end', o que é um estado para 'begin'
            #
            self.buffer.append(self.token)
            self.pensamento += (self.buffer,)
            self.buffer = []
            ##
            ##fim do begin
            ##
        else:
            self.err2(self.token)
    #
    #
    #
    def statm(self):
        #
        #estado para ler um statment
        #
        #print('oi',self.token)
        #
        if(self.token[1] == 'ID'):
            #statment para o tipo atribuição (a:= b+c;)
            self.buffer.append(self.token)
            self.token = self.get_token()
            #
            #pode encontrar algo do tipo a[xxx-14]
            #
            self.infipo();
            #
            if(self.token[0] == ':='):
                #se encontrar uma operação de atr, chamara a função para verificar se o proximo 'comando'
                #é uma expressão
                self.buffer.append(self.token)
                self.token = self.get_token()
                self.exp()
            else:
                self.err2(self.token)
        #
        #
        elif(self.token[0] == 'case'):
            #
            #case -> exp -> of -> string | number | id -> , | : -> statm -> ; | end
            #
            self.buffer.append(self.token)
            self.token = self.get_token()
            #
            self.exp()
            #
            if(self.token[0] == 'of'):
                #
                self.buffer.append(self.token)
                self.pensamento += (self.buffer,)
                self.buffer = []
                self.token = self.get_token()
                #
                while(self.token[0] != 'end'):
                    #
                    if(self.token[1] in ['ID','NUM_FLOAT','NUM_INT','STRING1','STRING2']):
                        #
                        self.buffer.append(self.token)
                        self.token = self.get_token()
                        #
                        if(self.token[0] == ':'):
                            #
                            self.buffer.append(self.token)
                            self.pensamento += (self.buffer,)
                            self.buffer = []
                            self.token = self.get_token()
                            #
                            self.statm()
                        #
                        else:
                            #nao encontrou um ':'
                            self.err2(self.token)
                        #
                    else:
                        #nao encontrou um id, number ou STRING
                        self.err2(self.token)
                    #
                #
                self.buffer.append(self.token)
                self.token = self.get_token()
                #
                if(self.token[0] == ';'):
                    self.buffer.append(self.token)
                    self.pensamento += (self.buffer,)
                    self.buffer = []
                    self.token = self.get_token()
                #
                else:
                    #nao encontrou um ';' apos o end
                    self.err2(self.token)
            #
            else:
                #nao encontrou um 'of'
                self.err2(self.token)
        #
        #
        #
        elif(self.token[0] == 'for'):
            #for -> id -> := -> exp -> to | downto -> exp -> do -> statm
            self.buffer.append(self.token)
            self.token = self.get_token()
            #
            if(self.token[1] == 'ID'):
                #
                self.buffer.append(self.token)
                self.token = self.get_token()
                #
                if(self.token[0] == ':='):
                    #se encontrar uma operação de atr, chamara a função para verificar se o proximo 'comando'
                    #é uma expressão
                    self.buffer.append(self.token)
                    self.token = self.get_token()
                    self.exp()
                    #
                    if(self.token[0] == 'to' or self.token[0] == 'downto'):
                        #
                        self.buffer.append(self.token)
                        self.token = self.get_token()
                        #
                        self.exp()
                        #
                        if(self.token[0] == 'do'):
                            self.buffer.append(self.token)
                            self.pensamento += (self.buffer,)
                            self.buffer = []
                            #
                            self.token = self.get_token()
                            #
                            self.statm()
                        #
                        else:
                            #nao encontrou um 'do'
                            self.err2(self.token)
                    #
                    else:
                        #nao encntrou um 'to' ou 'downto'
                        self.err2(self.token)
                #
                else:
                    #nao encontrou uma atribuição
                    self.err2(self.token)
            #
            else:
                #nao encontrou um ID para o for
                self.err2(self.token)
        #
        elif(self.token[0] == 'while'):
            #while -> EXP -> do -> STATM
            self.buffer.append(self.token)
            self.token = self.get_token()
            #
            self.exp()
            #
            if(self.token[0] == 'do'):
                #
                self.buffer.append(self.token)
                self.pensamento += (self.buffer,)
                self.buffer = []
                #
                self.token = self.get_token()
                #
                self.statm()
                #
        #
        elif(self.token[0] == 'if'):
            #
            self.buffer.append(self.token)
            self.token = self.get_token()
            #
            self.exp()
            #
            if(self.token[0] == 'then'):
                #se ler um 'then', add a buffer esse token, add ao pensamento, limpa o buffer e pega o proximo token
                self.buffer.append(self.token)
                self.pensamento += (self.buffer,)
                self.buffer = []
                self.token = self.get_token()
                #
                #supostamente, agora começam os comandos para o if, logo, deve-se chamar um statm()
                #
                self.statm()
                #
                if(self.token[0] == 'else'):
                    #
                    self.buffer.append(self.token)
                    self.pensamento += (self.buffer,)
                    self.buffer = []
                    #
                    self.token = self.get_token()
                    #
                    self.statm()
                    #
                    #deve-se pedir o proximo token
                #
            else:
                #se nao achou um 'then' >> ERRO
                self.err2(self.token)
            #
            #
            #
        #
        elif(self.token[0] == 'begin'):
            #
            self.buffer.append(self.token)
            self.pensamento += (self.buffer, )
            self.buffer = []
            #
            self.token = self.get_token()
            #
            while(self.token[0] != 'end'):
                self.statm()
            #
            #encontrou aqui um 'end'
            #
            if(self.token[0] == 'end'):
                #
                #add 'end' ao buffer e pede o proximo token
                #pois pode ser um if-else
                #
                self.buffer.append(self.token)
                self.token = self.get_token()
                #
                if(self.token[0] == ';'):
                    #
                    self.buffer.append(self.token)
                    self.token = self.get_token()
                    #
                    #se entrou aqui por causa de um if composto, e houver um 'else' nesse token
                    #então será um erro, pois um 'end;' fechará o if, o que não permitirá um 'else'
                    #
                    if(self.token[0] == 'else'):
                        self.err2(self.token)
                #
                elif(self.token[0] != 'else'):
                    #
                    #se nao encontrou um ';' e nem um 'else', pode ser algo do tipo:
                    #else begin
                    # x := 454654;
                    #end
                    #
                    self.err2(self.token)
                #
                self.pensamento += (self.buffer,)
                self.buffer = []
                #
            #
            elif(self.token == ['&','&','&']):
                self.err2(self.token)
            #
            else:
                #se nao encontrar um 'end' é um ERRO
                self.err2(self.token)
        #
        else:
            self.err2(self.token)
            self.token = self.get_token()
    #
    #
    #
    def infipo(self):
        #le vetores e etc
        if(self.token[0] == '['):
            self.buffer.append(self.token)
            self.token = self.get_token();
            #
            self.exp();
            #
            while(self.token[0] == ','):
                #guardo no buffer e pego o proximo token
                self.buffer.append(self.token);
                self.token = self.get_token();
                #
                self.exp();
            #
            if(self.token[0] == ']'):
                self.buffer.append(self.token)
                self.token = self.get_token()
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

        if(self.token[0] in ['*','/','div','mod','and']):
            self.buffer.append(self.token)
            self.token = self.get_token()

            if((self.token[1] not in ['ID','NUM_FLOAT','NUM_INT'])):
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
        if(self.token[0] == '('):
            self.buffer.append(self.token)
            self.token = self.get_token()
            self.exp()
            if(self.token[0] == ')'):
                self.buffer.append(self.token)
                self.token = self.get_token()
                return
        elif(self.token[1] in ['ID','NUM_FLOAT','NUM_INT','STRING1','STRING2']):
            self.buffer.append(self.token)
            self.token = self.get_token()
            return
        #
    #
    #
    #
    def var(self):
        #
        #estado para ler a declarão de variavel. COMPLETO
        #
        if(self.token[1] == 'ID'):
            #MEPA#
            #aqui vou contar quantas variaveis serão alocadas pelo comando AMEM
            #**********#
            self.cont_vars = 0 #devo iniciar com 0, caso haja mais alguma declaração
            self.cont_vars = self.cont_vars + 1 #como encontrei 1 ID, há pelo menos 1 variavel para ser alocada
            #**********#
            self.buffer.append(self.token)
            self.token = self.get_token()
            #
            while(self.token[0] == ','):
                #
                self.buffer.append(self.token)
                self.token = self.get_token()
                #
                if(self.token[1] == 'ID'):
                    #MEPA#
                    #procurando mais variaveis
                    #**********#
                    self.cont_vars = self.cont_vars + 1
                    #**********#
                    #
                    self.buffer.append(self.token)
                    self.token = self.get_token()
                    #
                else:
                    #erro, não encontrou nenhum id
                    self.err2(self.token)
            #fim while
            if(self.token[0] == ':'):
                #
                self.buffer.append(self.token)
                self.token = self.get_token()
                #
                self.type()
                #
                if(self.token[0] == ';'):
                    #MEPA#
                    #encontrei todas para o exemplo a,b : integer;
                    #**********#
                    cod = "AMEM " + str(self.cont_vars)
                    self.cod_mepa.append(cod)
                    #**********#

                    #
                    #fim de uma declaração ex> a,b :integer; PODEM OCORRER MAIS DECLARAÇÕES. ESTE É O FIM DE APENAS 1
                    #
                    self.buffer.append(self.token)
                    self.pensamento += (self.buffer,)
                    self.buffer = []
                    #
                    self.token = self.get_token()
                    #
                    if(self.token[1] == 'ID'):
                        #se encontrar outro id, deve-se voltar a esse estado para os mesmos passos.
                        #ou seja, há outra declaração
                        self.var()
                    #endif
    #
    #
    #
    def err(self):
        print('ERRO::::  Fim de arquivo não esperado!!')
        exit(0)
    #
    def err2(self,token):
        print('ERRO:::: "',token[0],'" não esperado na linha',token[2])
        exit(0)

#
# FIM DA CLASSE DO ANALISADOR SINTATICO
#

sintatico = a_sintatico(tokens)

sintatico.inicio()
#sintatico.show_saida()
#sintatico.show_tokens()
#sintatico.show_mepa()
