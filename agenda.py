import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a' 
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração.
 

def adicionar(descricao, extras):

  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    return False
  else:
    desc = descricao
  lExtras = extras.split(' ')
  data = '' 
  hora = ''
  pri = ''
  contexto = ''
  projeto = ''
     

  if len(lExtras)>=1:
    if dataValida(lExtras[0]):
      data = lExtras[0]
      del lExtras[0]
      
  if len(lExtras)>=1:
    if horaValida(lExtras[0]):
      hora = lExtras[0]
      del lExtras[0]
  
  if len(lExtras)>=1:
    if prioridadeValida(lExtras[0]):
      pri = lExtras[0]
      del lExtras[0]
  
  if len(lExtras)>=1:
    if contextoValido(lExtras[0]):
      contexto = lExtras[0]
      del lExtras[0]
  
  if len(lExtras)>=1:
    if projetoValido(lExtras[0]):
      projeto = lExtras[0]
      del lExtras[0]
  
   
  novaAtividade = data +' '+ hora+' ' + pri+' ' + desc+' ' + contexto+' ' + projeto

  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a',encoding="utf8")
    fp.write("\n" + novaAtividade)
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):
  letras = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q',
            'R','S','T','U','V','W','X','Y','Z']
  if len(pri) !=3 or pri[1].upper() not in letras :
    return False
  elif pri[0] != '(' or pri[2] != ')':
    return False
  else:
    return True


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    validH = True
    validM = True
    h = int(horaMin[0]+horaMin[1])
    m = int(horaMin[2]+horaMin[3])
    if h>23 or h<0 :
      validH = False
    if m>59 or m<0 :
      validM = False
    if validH and validM:
      return True
    else:
      return False
  
# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  if len(data) != 8 or not soDigitos(data):
    return False
  else:
    d = int(data[0]+data[1])
    m = int(data[2]+data[3])
    y = int(data[4]+data[5]+data[6]+data[7])
    validD = True
    validM = True
    if m>12 or m<0 :
      validM = False 
    for x in (1,3,5,7,8,10,12):
      if  m == x:
        if d>31 or d<0 :
          validD = False    
    for x in (4,6,9,11):
      if m == x :
        if d>30 or d<0 :
          validD = False
    if m == 2:
      if d>29 or d<0 :
        validD = False      
    if validM and validD:
      return True

  return False

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if len(proj) <2 or proj[0] != '+':
    return False
  else:
    return True


# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  if len(cont) <2 or cont[0] != '@':
    return False
  else:
    return True
  

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.

def preOrdenar(texto):
  i = 0
  atividade = ''
  Llinhas = []
  while i < len(texto):
    if texto[i] != "\n":
      atividade = atividade + texto[i]
    else:
      Llinhas.append(atividade.split(' '))
      atividade = ''
    i += 1
  Llinhas.append(atividade.split(' '))
  return Llinhas

# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
def organizar(linhas):
  preItens = preOrdenar(linhas)
  itens = []
  data = '' 
  hora = ''
  pri = ''
  desc = ''
  contexto = ''
  projeto = ''
  i = 0
  while i < len(preItens) :
    if projetoValido(preItens[i][-1]):
      projeto = preItens[i][-1]
      del preItens[i][-1]
    if contextoValido(preItens[i][-1]):
      contexto = preItens[i][-1]
      del preItens[i][-1]
    if dataValida(preItens[i][0]):
      data = preItens[i][0]
      del preItens[i][0]
    if horaValida(preItens[i][0]):
      hora = preItens[i][0]
      del preItens[i][0]
    if prioridadeValida(preItens[i][0]):
      pri = preItens[i][0]
      del preItens[i][0]
    j = 0
    while j < len(preItens[i]):
      desc = desc + preItens[i][j] + ' '
      j+=1

    itens.append((desc, (data, hora, pri, contexto, projeto)))
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
    i += 1   
       
  
#    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
#    tokens = l.split() # quebra o string em palavras

    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 
  return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#((desc, (data, hora, pri, contexto, projeto)))
    

def listar():
    f = open("C:/p/todo.txt","r",encoding="utf8")
    dados = f.read()
    f.close
    itens = organizar(dados)
    k = 0
    listatupla = []
    
    while k < len(itens):
      listatupla.append('')
      listatupla[k] = [k+1,itens[k]]
      k+=1 
    listao = ordenarPorPrioridade(listatupla)   

    i = 0    
    itensListar = []
    while i < len(listao):
      texto = str(listao[i][0]) + ' '+listao[i][1][1][0]+' '+listao[i][1][1][1]+' '+listao[i][1][1][2]+' '+listao[i][1][0]+' '+listao[i][1][1][3]+' '+listao[i][1][1][4]
      itensListar.append(texto)
      i+=1
    j = 0 
    while j < len(itensListar):
      print(itensListar[j])   
      j +=1
  
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)
  
    
      
    return 

#         m = 0
 #       limp = ''
 #       while m<len(listatemp):
 #         if listatemp != '':
 #           limp = listatemp[m]
 #         m+=1
 #       print(limp)

def ordenarPorDataHora(itens):

  ################ COMPLETAR

  return itens
   
def ordenarPorPrioridade(itens):
  listatemp = itens
  listaOrdenada = []
  listaSemOrdem = []
  letras = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q',
            'R','S','T','U','V','W','X','Y','Z']
  i = 0
  while i < len(itens):
    if listatemp[i][1][1][2] == '':
        listaSemOrdem.append(itens[i])
    i +=1
  j = 0
  while j<len(letras):
    k = 0
    while k<len(listatemp):
      if listatemp[k][1][1][2] != '':
        if itens[k][1][1][2][1].upper() == letras[j]:
          listaOrdenada.append(listatemp[k])
      k+=1
    j+=1

  listao = listaOrdenada+listaSemOrdem  

  return listao

def lerTodoLinhas():
    f = open(TODO_FILE,'r',encoding="utf8")
    lista = []
    for i in f:
        lista.append(i)
    f.close()
    return lista

def fazer(num):

  ################ COMPLETAR

  return 

def remover(num):
  ordem = int(num) - 1
  todo = lerTodoLinhas()
  if num<=0:
    return print('Este número não corresponde a uma atividade')
  if ordem< len(todo):
    del todo[ordem]
    f = open(TODO_FILE,'w')
    f.writelines(todo)
    f.close()
    return print('Atividade removida com Sucesso')
  else:
    return print('Este número não corresponde a uma atividade')
    
  
  
  

  ################ COMPLETAR

  return


# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):

  ################ COMPLETAR

  return 



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    #comandos.pop(0) # remove 'agenda.py'
    #comandos.pop(0) # remove 'a'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
  elif comandos[1] == LISTAR:
    lista = listar()
    return  lista

  elif comandos[1] == REMOVER:
    remover(comandos[2])
    return    

    ################ COMPLETAR    

  elif comandos[1] == FAZER:
    return    

    ################ COMPLETAR

  elif comandos[1] == PRIORIZAR:
    return    

    ################ COMPLETAR

  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
#
#processarComandos(sys.argv)

