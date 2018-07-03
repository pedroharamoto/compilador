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
