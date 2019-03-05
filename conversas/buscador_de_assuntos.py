x=1
busca=str(input("O que buscar?: "))
print("====================")
while True:
 arquivo = str(x)+".txt"
 try:
  a = open(arquivo,"r")
 except:
  print("\nFim das buscas!")
  break
 string = str(a.read())
 if busca.lower() in string.lower():
  print("Arquivo {}".format(x))
  print(" conteudo: {}\n".format(string))
 x=x+1
