import socket 
import pandas as pd
import numpy as np
from collections import Counter

HOST = 'localhost'
PORT = 30000
valores = 'NULL'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Definindo socket, IPV4
s.bind((HOST, PORT))


def main ():
    escutaServidor()

def escutaServidor():
    global valores
    s.listen()
    print('Aguardando Conexão STATUS: Escutando')
    conn, ender = s.accept()
    print('Conectado em: ', ender)
    while True:
        data = conn.recv(1024)
        validacodigo = verificaCodigo(data.decode())
        
        if(validacodigo == '1'):
            print(data.decode())
            salvaVendaBanco(data.decode())
            conn.sendall(b"Ok")
            
        if(validacodigo == '2'):
            retorno = consultaVendedor(data.decode())
            retornoemBytes = retorno.encode('utf=8')
            conn.sendall(retornoemBytes)
            print('Codigo 2: Total de vendas por vendedor')

        if(validacodigo == '3'):
            retorno = consultaLoja(data.decode())
            retornoemBytes = retorno.encode('utf=8')
            conn.sendall(retornoemBytes)
            print('Codigo 3: Total de vendas por loja')

        if(validacodigo == '4'):
            retorno = "Melhor Vendedor: "+str(consultaMelhorVendedor())
            retornoemBytes = retorno.encode('utf=8')
            conn.sendall(retornoemBytes)
            print('Codigo 4: Melhor Vendedor')

        if(validacodigo == '5'):
            retorno = "Melhor loja: "+str(consultaMelhorLoja())
            retornoemBytes = retorno.encode('utf=8')
            conn.sendall(retornoemBytes)
            print('Codigo 5: Melhor Loja')

        if(validacodigo == '6'):
            retorno = "Vendas no Periodo: "+str(consultaPeriodo(data.decode()))
            retornoemBytes = retorno.encode('utf=8')
            conn.sendall(retornoemBytes)
            print('Codigo 6: Vendas no periodo')

        if not data:
            print ('Fechando Conexão')
            conn.close
            break    
            
    main()



def verificaCodigo(parametros):
    listaItens = parametros.split('|')
    codigoOperacao = listaItens[0]
    return codigoOperacao

def salvaVendaBanco(parametros):
      
    listaItens = parametros.split('|')
    
    if(len(listaItens) == 5):
        codigoOperacao = listaItens[0]
        nomeVendedor = listaItens[1]
        identificacaoLoja = listaItens[2]
        dataDaVenda = listaItens[3]
        valorVenda = listaItens[4]
 
    
        if(codigoOperacao == '1'):
            df = pd.read_csv("bancodedados.csv", encoding='utf-8', sep=',', index_col='id')
            df.loc[len(df)] = [codigoOperacao,nomeVendedor,identificacaoLoja, dataDaVenda,valorVenda]
            df.to_csv('bancodedados.csv')


def consultaVendedor(parametros):
    listaItens = parametros.split('|')
    variavelChave = listaItens[1]
    df = pd.read_csv("bancodedados.csv", encoding='utf-8', sep=',', index_col='id')
    lista = df.loc[df['nomevendedor'] == str(variavelChave)]
    retorno = ('Vendedor: '+str(variavelChave)+'\nVendas: '+str(len(lista)))
    return retorno

def consultaLoja(parametros):
    listaItens = parametros.split('|')
    variavelChave = listaItens[1]
    df = pd.read_csv("bancodedados.csv", encoding='utf-8', sep=',', index_col='id')
    lista2 = df.loc[df['identificaloja'] == str(variavelChave)]
    retorno = ('Loja Codigo: '+str(variavelChave)+'\nVendas: '+str(len(lista2)))
    return retorno

def consultaMelhorVendedor():
    df = pd.read_csv("bancodedados.csv", encoding='utf-8', sep=',', index_col='id')
    counter = Counter(df['nomevendedor'])
    melhorVendedor = (dict(counter.most_common(1)))
    formatavendedor = str(melhorVendedor).split(':')
    vendedor = formatavendedor[0]
    vendedor = vendedor.replace('{','')
    vendedor = vendedor.replace("'",'')
    return vendedor

def consultaMelhorLoja():
    df = pd.read_csv("bancodedados.csv", encoding='utf-8', sep=',', index_col='id')
    counter = Counter(df['identificaloja'])
    melhorLoja = (dict(counter.most_common(1)))
    formataloja = str(melhorLoja).split(':')
    loja = formataloja[0]
    loja = loja.replace('{','')
    loja = loja.replace("'",'')
    return loja


def consultaPeriodo(parametros):
    listaItens = parametros.split('|')
    datainicial = listaItens[1]
    datafinal = listaItens[2]
    df = pd.read_csv("bancodedados.csv", encoding='utf-8', sep=',', index_col='id')
    lista = (df.loc[(df['datadavenda'] >= datainicial) & (df['datadavenda'] <= datafinal)])
    return len(lista)
    




main()



        