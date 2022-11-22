
import os
import socket
import time
from datetime import datetime



HOST = 'localhost'
PORT = 30000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Definindo socket, IPV4
s.connect((HOST,PORT))
clear = lambda: os.system('cls')


def opcoesVendedor():
    clear()
    print("1 - Realizar nova Venda")
    print ("0 - Voltar")
    opcaodesejada = int(input("Digite a opção desejada: "))

    if opcaodesejada == 0:
        main()
    else:
        clear()
        print("========= INICIANDO VENDA ============")
        codigoOperacao = 1
        nomeVendedor = str(input("Digite o nome do vendedor: "))
        identificacaoLoja = str(input("Digite a identificação da loja: "))
        dataDaVenda = str(input("Data da venda dd/MM/YYYY: "))
        valorVenda = str(input("Valor da venda: "))
        clear()

        format = "%d/%m/%Y"
        res = True
        try:
            res = bool(datetime.strptime(dataDaVenda, format))
        except ValueError:
            res = False

        if(res == False):
            print("Formato da data invalido")
            input("Pressione ENTER para continuar")
            opcoesVendedor()


        else:
            print("Digite 1 para confirmar os dados ou 0 para cancelar:")
            print("Codigo Operação: "+str(codigoOperacao)+"\n"+"Nome do Vendedor: "+nomeVendedor+"\n"+"Identificação Loja: "+identificacaoLoja+"\n"+"Data Venda: "+dataDaVenda+"\n"+"Valor Venda: "+valorVenda+"\n")
            opcaodesejada = int(input("Digite 1 para confirmar os dados ou 0 para cancelar: "))
            if (opcaodesejada==1):
                s.sendall(str.encode(str(codigoOperacao)+'|'+str(nomeVendedor)+'|'+str(identificacaoLoja)+'|'+str(dataDaVenda)+'|'+str(valorVenda)))
                data = s.recv(1024)
                print('Mensagem Servidor: ', data.decode())
                print('Aguarde...')
                time.sleep(5)
                s.close
                main()
                print("Transação confirmada")   
                
            else:
                main()
       


def opcoesGerente():
    clear()
    print("1 - Total de Vendas por vendedor")
    print("2 - Total de vendas de uma loja")
    print("3 - Melhor vendedor")
    print("4 - Melhor loja")
    print("5 - Total de vendas da rede de lojas em um período")
    print("0 - Voltar")
    opcaodesejada = int(input("Digite a opção desejada: "))

    if(opcaodesejada == 1):
        nomeVendedor = str(input("Informe o nome do vendedor: "))
        codigoOperacao = 2
        s.sendall(str.encode(str(codigoOperacao)+'|'+str(nomeVendedor)))
        data = s.recv(1024)
        print(data.decode())
        input("Pressione ENTER para continuar")
        opcoesGerente()
    
    elif(opcaodesejada == 2):
        codigoloja = str(input("Informe o codigo da loja: "))
        codigoOperacao = 3
        s.sendall(str.encode(str(codigoOperacao)+'|'+str(codigoloja)))
        data = s.recv(1024)
        print(data.decode())
        input("Pressione ENTER para continuar")
        opcoesGerente()

    elif(opcaodesejada == 3):
        codigoOperacao = 4
        s.sendall(str.encode(str(codigoOperacao)))
        data = s.recv(1024)
        print(data.decode())
        input("Pressione ENTER para continuar")
        opcoesGerente()

    elif(opcaodesejada == 4):
        codigoOperacao = 5
        s.sendall(str.encode(str(codigoOperacao)))
        data = s.recv(1024)
        print(data.decode())
        input("Pressione ENTER para continuar")
        opcoesGerente()

    elif(opcaodesejada == 5):
        codigoOperacao = 6
        print("Informe as datas no padrão dd/MM/YYYY")
        datainicial = str(input("Informe a data inicial: "))
        datafinal = str(input("Informea a data final: "))
        s.sendall(str.encode(str(codigoOperacao)+'|'+str(datainicial)+'|'+str(datafinal)))
        data = s.recv(1024)
        print(data.decode())
        input("Pressione ENTER para continuar")
        opcoesGerente()

    elif(opcaodesejada == 0):
        main()

    else:
        print("Opção invalida")
        input("Pressione ENTER para continuar")
        main()
    
   


def main():
    clear()
    print("=============== BEM VINDO =================")
    print("Selecione o usuario")
    print("Digite 1 para entrar no modo Vendedor ou 2 para entrar no modo Gerente ")
    tipoUsuario = int(input("Informe a opção desejada: "))
    print(tipoUsuario)
    if (tipoUsuario == 1):
        opcoesVendedor()
    elif (tipoUsuario == 2):
        opcoesGerente()
    else:
        print('Opção Invalida')
        input("Pressione ENTER para continuar")
        main()


main()
    


