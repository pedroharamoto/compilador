#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Pedro Vitor Jhum Haramoto RA: 161024157
# João Pedro Marin Comini   RA: 161020551
#

#
#   INICIO DA CLASSE AFD_LEXICO()
#
class afd_lexico():

    def __init__(self):
        #
        #
        #tab.tokens é a "tabela" com todos os tokens
        #ela funciona assim:
        #[token,tipo,linha]
        #por exemplo >>> tab_token[1] = ['program','RESERVADA',1]
        #tab_token[0][1] = 'RESERVADA'
        #
        #
        self.tab_tokens = []
        #
        #
        #
        #variavel para a tabela de palavras reservadas
        self.palavras_reservadas = ['and','array','asm','begin','case','const','constructor',
                                      'destructor','div','do','downto','else','end','file','for'
                                      ,'foward','function','goto','if','implementation','in','inline'
                                      ,'interface','label','mod','nil','not','object','of','or','packed'
                                      ,'procedure','program','read','record','repeat','set','shl','shr','string'
                                      ,'then','to','type','unit','until','uses','var','while','with','write','xor'
                                      ]
        #variavel para a tabela de simbolos de pontuacao
        self.simbolos_pontuacao = ["(", ")", ",", ".", "..", ":", ";", "[", "]", "ˆ"]

        #variavel para a tabela de simbolos de relação
        self.simbolos_relacao = ["<", "<=", "<>", "=", ">", ">="]

        #variavel para a tabela de simbolos aritmeticos
        self.simbolos_arit = ['%','*','+','-','/']

        #variavel para guardar o codigo fonte do programa a ser analisado
        self.codigo_fonte = ''

        #variavel para retornar o token ao analisador sintatico
        self.buffer = ''

        #variavel para armazenar a posicao lida do codigo fonte
        self.pos_chr = 0

        self.linha = 1
        self.file_size = 0
        self.tipo_numero = 3    #se tipo_numero = 3 -> inteiro
                                #se tipo_numero = 4 -> float

        if(self.abre_arquivo('correto.txt')):
            self.estado_inicial(self.buffer)
        else:
            print('erro ao abrir o arquivo!')
    #
    #
    #
    def abre_arquivo(self,prog):

        arq = open(prog, 'r')
        if(arq):
            self.codigo_fonte = str.lower(arq.read())
            self.codigo_fonte += '\0'
            arq.close()
            return True
        return False
    #
    #
    #
    def estado_inicial(self,chr):

        while(self.codigo_fonte[self.pos_chr] != '\0'):

            #
            self.buffer = ''

            chr = self.codigo_fonte[self.pos_chr]
            #
            if( (chr == ' ') or (chr == '\n') or (chr == '\t')):
                if(chr == '\n'):
                    self.linha += 1
                self.pos_chr += 1
            #
            if(str.isalpha(chr)): ####ESTADO 0 -> 1 || IDENTIFICADOR (pode ser PALAVRA RESERVADA ou IDENTIFICADOR)
                self.saida(self.estado_1(chr))

            elif(str.isdigit(chr)):
                self.saida(self.estado_2(chr)) ####ESTADO 0 -> 2 NUMERO (INT OU FLOAT)

            elif(chr == ' ' or chr == '\n' or chr == '\t'):
                self.saida(0) ### ESTADO 0 -> ??? ESPACO EM BRANCO

            elif(self.isArit(chr)):
                self.saida(self.estado_8(chr)) #ESTADO PARA OS SIMBOLOS ARITMETICOS

            elif(self.isPontSymbol(chr)):
                self.saida(self.estado_6(chr)) #ESTADO PARA OS SIMBOLOS DE PONTUAÇÃO

            elif(self.isPontRela(chr)):
                self.saida(self.estado_7(chr)) #ESTADO PARA OS SIMBOLOS DE RELACAO

            elif(chr == '"'):
                self.saida(self.estado_10(chr)) #ESTADO PARA STRING

            elif(chr == "'"):
                self.saida(self.estado_11(chr)) #ESTADO PARA STRING

            else:
                self.saida(self.estado_9(chr)) #ESTADO PARA OS CARACTERES INVALIDOS
    #
    #
    #
    def get_tokens(self):
        return self.tab_tokens
    #
    #
    #
    def saida(self,codigo):
        if(codigo == 1): # PALAVRA RESERVADA
            self.tab_tokens.append([self.buffer,'PALAVRA_RESERVADA',self.linha])
            #print('<',self.buffer,', PALAVRA RESERVADA > linha: ' , self.linha)

        elif(codigo == 2): # IDENTIFICADOR
            self.tab_tokens.append([self.buffer,'ID',self.linha])
            #print('<',self.buffer,', IDENTIFICADOR > linha: ' , self.linha)

        elif(codigo == 3): # NUMERO INTEIRO
            self.tab_tokens.append([self.buffer,'NUM_INT',self.linha])
            #print('<',self.buffer,', NUM INTEIRO > linha: ' , self.linha)

        elif(codigo == 4): # NUMERO FLOAT
            self.tab_tokens.append([self.buffer,'NUM_FLOAT',self.linha])
            #print('<', self.buffer, ', NUM FLOAT > linha: ' , self.linha)

        elif(codigo == 5): # PONTUACAO
            self.tab_tokens.append([self.buffer,'SIMB_PONT',self.linha])
            #print('<', self.buffer, ', SIMBOLO DE PONTUACAO > linha: ' , self.linha)

        elif(codigo == 6):
            self.tab_tokens.append([self.buffer,'ERR_SIMB_PONT',self.linha])
            #print('<', self.buffer, ', ERRO DE SIMBOLO DE PONTUACAO > linha: ' , self.linha)

        elif(codigo == 7):
            self.tab_tokens.append([self.buffer,'SIMB_REL',self.linha])
            #print('<', self.buffer, ', SIMBOLO DE RELACAO > linha: ' , self.linha)

        elif(codigo == 8):
            self.tab_tokens.append([self.buffer,'ERR_SIMB_REL',self.linha])
            #print('<', self.buffer, ', ERRO DE SIMBOLO DE RELACAO > linha: ' , self.linha)

        elif(codigo == 9):
            self.tab_tokens.append([self.buffer,'SIMB_ARIT',self.linha])
            #print('<', self.buffer, ', SIMBOLO ARITMETICO > linha: ' , self.linha)

        elif(codigo == 10):
            self.tab_tokens.append([self.buffer,'ERR_SIMB_ARIT',self.linha])
            #print('<', self.buffer, ', ERRO DE SIMBOLO ARITMETICO > linha: ' , self.linha)

        elif(codigo == 11):
            self.tab_tokens.append([self.buffer,'ATT',self.linha])
            #print('<', self.buffer, ', ATRIBUICAO > linha: ' , self.linha)

        elif(codigo == 12):
            self.tab_tokens.append([self.buffer,'STRING1',self.linha])
            #print('<', self.buffer, ', STRING ASPAS DUPLAS > linha: ' , self.linha)

        elif(codigo == 13):
            self.tab_tokens.append([self.buffer,'STRING2',self.linha])
            #print('<', self.buffer, ', STRING ASPAS SIMPLES> linha: ' , self.linha)

        elif(codigo == 191):
            self.tab_tokens.append([self.buffer,'ERR_NUM_INT',self.linha])
            #print('<',self.buffer,', ERRO NUM INTEIRO > linha: ' , self.linha)

        elif(codigo == 192):
            self.tab_tokens.append([self.buffer,'ERR_NUM_FLOAT',self.linha])
            #print('<',self.buffer,', ERRO NUM FLOAT > linha: ' , self.linha)

        elif(codigo == 193):
            self.tab_tokens.append([self.buffer,'ERR_CARAC_INVALID',self.linha])
            #print('<',self.buffer,', ERRO DE CARACTERE INVALIDO > linha: ' , self.linha)

        elif(codigo == 0): # ESPACO EM BRANCO
            pass
    #
    #
    #
    def isPontSymbol(self,x):
        return self.busca_binaria(x,self.simbolos_pontuacao)
    #
    #
    #
    def isPontRela(self,x):
        return self.busca_binaria(x, self.simbolos_relacao)
    #
    #
    #
    def isArit(self,x):
        return (self.busca_binaria(x, self.simbolos_arit))
    #
    #
    #
    def busca_binaria(self,busca,vetor):

        tamanho_vet = len(vetor)

        esq = 0
        dir = tamanho_vet - 1

        while (esq <= dir):
            m = int((esq+dir)/2)

            if (vetor[m] == busca):
                return True

            if(vetor[m] < busca):
                esq = m + 1
            else:
                dir = m - 1

        return False
    #
    #
    #
    def veri_reservada(self):
        return (self.busca_binaria(self.buffer,self.palavras_reservadas) and ( (self.codigo_fonte[self.pos_chr] == '(') or(self.codigo_fonte[self.pos_chr] == '\0') or (self.codigo_fonte[self.pos_chr] == ' ' or (self.codigo_fonte[self.pos_chr] == '\n') or (self.codigo_fonte[self.pos_chr] == '.') or (self.codigo_fonte[self.pos_chr] == ';'))))
    #
    #
    #
    def estado_1(self,chr):
        #
        #   IDENTIFICADOR
        #
        reservada = False
        self.buffer += chr
        self.pos_chr += 1

        while 1:

            if(not self.veri_reservada()):
                chr = self.codigo_fonte[self.pos_chr]

                if(str.isalnum(chr) or chr == '_'):
                    self.buffer += chr
                    self.pos_chr += 1
                else:
                    break
            else:
                reservada = True
                break

        if(reservada):
            return 1 #ENCONTROU UMA PALAVRA RESERVADA
        else:
            return 2 #ENCONTROU UM IDENTIFICADOR
    #
    #
    #
    def estado_2(self,chr):
        #
        #tipo = 3 => inteiro
        #tipo = 4 => float
        #
        self.buffer += chr
        self.pos_chr += 1

        chr = self.codigo_fonte[self.pos_chr]

        if(self.estado_2loop(chr)):
            return self.tipo_numero
        else:
            return self.tipo_numero
    #
    #
    #
    def estado_2loop(self,chr):

        isnumber = False
        self.tipo_numero = 3

        while 1:

            chr = self.codigo_fonte[self.pos_chr]

            if(str.isdigit(chr)):
                self.buffer += chr
                self.pos_chr += 1
                isnumber = True

            elif(str.isalpha(chr)):
                isnumber = False
                break

            elif(chr == '.'):
                self.estado_4(chr) # POSSIVEL FLOAT
                if (self.tipo_numero == 4):
                    isnumber = True
                else:
                    isnumber = False
                break

            elif(self.isArit(chr)):
                isnumber = True
                break

            elif(self.isPontSymbol(chr)):
                isnumber = True
                break

            elif(self.isPontRela(chr)):
                isnumber = True
                break

            elif((chr == '\n') or (chr == ' ') or (chr == '\x00') or (chr == '\0')):
                isnumber = True
                break

        return isnumber
    #
    #
    #
    def erro_estado3(self,chr):
        #
        while 1:
            chr = self.codigo_fonte[self.pos_chr]

            if(str.isalnum(chr)):
                self.buffer += chr
                self.pos_chr += 1
            else:
                break

        return 191
    #
    #
    #
    def estado_4(self,chr):

        self.buffer += chr
        self.pos_chr += 1
        self.tipo_numero = 4

        chr = self.codigo_fonte[self.pos_chr]

        if(self.estado_4loop(chr)):
            return 4
        else:
            return (self.erro_estado5(chr))
    #
    #
    #
    def estado_4loop(self,chr):

        isnumber = False

        while 1:
            chr = self.codigo_fonte[self.pos_chr]

            if(str.isdigit(chr)):
                self.buffer += chr
                self.pos_chr += 1
                isnumber = True

            elif(str.isalpha(chr)):
                isnumber = False
                break

            elif(self.isArit(chr)):
                isnumber = True
                break

            elif(self.isPontSymbol(chr)):
                isnumber = True
                break

            elif(self.isPontRela(chr)):
                isnumber = True
                break

            elif ((chr == '\n') or (chr == ' ') or (chr == '\x00') or (chr == '\0')):
                isnumber = True
                break

        return isnumber
    #
    #
    #
    def erro_estado5(self,chr):
        #
        self.tipo_numero = 192
        #
        while 1:

            chr = self.codigo_fonte[self.pos_chr]

            if(str.isalnum(chr)):
                self.buffer += chr
                self.pos_chr += 1
            else:
                break

        return 192
    #
    #
    #
    def estado_6(self,chr):

        self.buffer += chr
        self.pos_chr += 1
        isSymbol = 6

        if(self.isPontSymbol(chr)):
            if(chr == ':'):
                chr = self.codigo_fonte[self.pos_chr]
                if(chr == '='):
                    #encontrou uma operacao de atribuição
                    self.buffer += chr
                    self.pos_chr += 1
                    return 11
            isSymbol = 5
        else:
            isSymbol = 6

        return isSymbol
    #
    #
    #
    def estado_7(self,chr):

        self.buffer += chr
        self.pos_chr += 1
        isSymbol = 8


        while 1:

            chr = self.codigo_fonte[self.pos_chr]

            if(self.isPontRela(chr)):
                self.buffer += chr
                self.pos_chr += 1
                isSymbol = 7
                break #### voltar
            elif(str.isalnum(chr)):
                isSymbol = 7
                break
            else:
                isSymbol = 8
                break

        return isSymbol
    #
    #
    #
    def estado_8(self,chr):

        self.buffer += chr
        self.pos_chr += 1
        is_Arit = 10

        if(self.isArit(chr)):
            is_Arit = 9
        else:
            is_Arit = 10

        return is_Arit
    #
    #
    #
    def estado_9(self,chr):
        #
        #pode ser um comentario ou um CARACTERE INVALIDO
        #
        if( chr == '{' ):
            #comentario do tipo {comentario}
            while( chr != '}'):
                self.pos_chr += 1
                chr = self.codigo_fonte[self.pos_chr]

            self.pos_chr += 1
            chr = self.codigo_fonte[self.pos_chr]

        elif( ord(chr) == 92): #comentario do tipo \\comentario
            #achou um "\"
            self.pos_chr += 1
            chr = self.codigo_fonte[self.pos_chr]
            #se achar outro "\" => é comentario, senao é erro lexico

            if( ord(chr) == 92):
                while (chr != '\n'):
                    self.pos_chr += 1
                    chr = self.codigo_fonte[self.pos_chr]

                self.pos_chr += 1
                chr = self.codigo_fonte[self.pos_chr]
            else:
                return 193
        else:
            self.buffer += chr
            self.pos_chr += 1
            return 193
    #
    #
    #
    def estado_10(self,chr):
        #
        # estado para string de ASPAS DUPLAS (" AAAA ")
        #
        self.buffer += chr
        self.pos_chr += 1

        while 1:
            chr = self.codigo_fonte[self.pos_chr]

            if( chr != '"' and chr != "\0"):
                self.buffer += chr
                self.pos_chr += 1
            else:
                self.pos_chr += 1
                break

        self.buffer += chr

        return 12
    #
    #
    #
    def estado_11(self,chr):
        #
        # estado para string de ASPAS SIMPLES (' AAAA ')
        #
        self.buffer += chr
        self.pos_chr += 1

        while 1:
            chr = self.codigo_fonte[self.pos_chr]

            if( chr != "'" and chr != "\0"):
                self.buffer += chr
                self.pos_chr += 1
            else:
                self.pos_chr += 1
                break

        self.buffer += chr

        return 13
    #
    #
    #
#
# FIM DA CLASSE
#


#
#
#o codigo comentado abaixo é apenas um exemplo de leitura dos tokens
#tokens = afd_lexico().get_tokens()
#for (i, token) in enumerate(tokens):
#    print(token[2],":")
#    for (j, elemento) in enumerate(token):
#        print("\t",elemento)
