def prioridade(c, t):
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


opera = '(a-b)*c;'
print(opera)
i = 0
p = pilha_pol()
p.empilha('(')
j = len(opera)
while(i<j):
    c = opera[i]
    i += 1
    if(c >= 'a' and c <= 'z'):
        print(c)
    #
    elif(c == '('):
            p.empilha('(')
        #
    elif(c == ')' or c == ';'):
        while True:
            t = p.desempilha()
            if(t != '('):
                print(t)
            elif(t == '('):
                break
    #
    elif(c == '+' or c == '-' or c == '*' or c == '/'):
        while True:
            t = p.desempilha()
            if(prioridade(c,t)):
                p.empilha(t)
                p.empilha(c)
                break
            else:
                print(t)
