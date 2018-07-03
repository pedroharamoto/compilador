class tab_variaveis:
    #
    #classe para a tabela de variaveis
    #
  def __init__(self):
    self.items = []

  def push(self, item):
      #adiciona no inicio da pilha
    self.items.insert(0,item)

  def pop(self,pos):
      #remove o elemento q está no topo da pilha
    return self.items.pop(pos)

class pilha_pol:
    def __init__(self):
        self.op = []
    def empilha(self,op):
        if(op!=None):
            self.op.insert(0,op)
    def desempilha(self):
        if(self.op):
            return self.op.pop(0)
        else:
            return None
#
#
#
def codigo(t):
    if(t == '+'):
        return "SOMA"
    elif(t == '*'):
        return "MULT"
    elif(t == '-'):
        return "SUB"
    elif(t == '/'):
        return "DIV"

#
#
#
def prioridade(c, t):
    #
    #função de prioridade para a pos-fixa
    #
    pc = 0
    pt = 0
    if(c == '^'):
        pc = 4
    elif(c == '*' or c == '/'):
        pc = 2
    elif(c == '+' or c == '-'):
        pc = 1
    elif(c == '('):
        pc = 4

    if(t == '^'):
        pt = 3
    elif(t == '*' or t == '/'):
        pt = 2
    elif(t == '+' or t == '-'):
        pt = 1
    elif(t == '('):
        pt = 0
    else:
        pt = 0

    return (pc > pt)

codigo('+')
