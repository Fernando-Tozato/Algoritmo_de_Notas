from banco_de_dados import *
import os

#host = 'localhost'
#user = 'python'
#database = 'notas'
#duas_etapas = 'sua_senha'

# Pega a tabela do banco de dados e imprime ao usuário
def mostra_notas(host,user,pw,database):
    # Pega os dados
    ler_tabela = """
    SELECT *
    FROM Notas;
    """
    connection = create_db_connection(host,user,pw,database)
    aux = read_query(connection,ler_tabela)
    
    leituras = []
    
    for i in aux:
        i = list(i)
        leituras.append(i)
    
    # Cria um DataFrame com Panda
    colunas = ['ID','Matéria','Cód.','Carga','AV1','AV2','AV3','AVA1','AVA2','AVD','AVDS','Média']
    df = pd.DataFrame(leituras, columns = colunas)
    return df

# Calcula a média
def calcula_media(av1,av2,av3,ava1,ava2,avd,avds):
    soma = 0
    av1 += ava1
    av2 += ava2
    if av1 > 10: av1 = 10
    if av2 > 10: av2 = 10
    if av1 < av2:
        soma += av2
        if av1 > av3: soma += av1 
        else: soma += av3
    else:
        soma += av1
        if av2 > av3: soma+= av2
        else: soma += av3
    if avd > avds: soma += avd
    else: soma += avds
    media = round(soma / 3,2)
    return media

# Preenche a tabela com as informções que o usuário insere
def insere_materias(host,user,pw,database,materia,codigo,av1,av2,av3,ava1,ava2,avd,avds):
    media = calcula_media(av1,av2,av3,ava1,ava2,avd,avds)
    
    # Cria os comandos em SQL
    inserir_dados = f"insert into notas(materia,codigo,carga,av1,av2,av3,ava1,ava2,avd,avds,media) value ('{materia}','{codigo}',80,{av1},{av2},{av3},{ava1},{ava2},{avd},{avds},{media})"
    print(inserir_dados)
    # Faz a conexão com a DB e comita os comandos
    connection = create_db_connection(host,user,pw,database)
    execute_query(connection,inserir_dados)

# Calcula o CR usando a DB
def calcula_cr(host,user,pw,database):
    # Pega os dados
    ler_tabela = """
    SELECT *
    FROM Notas;
    """
    connection = create_db_connection(host,user,pw,database)
    leituras = read_query(connection,ler_tabela)
    
    # Calcula e mostra ao usuário
    soma = 0
    for leitura in leituras:
        soma += float(leitura[11]) * 80
    cr = round(soma / (int(leituras[-1][0]) * 80),2)
    return f"CR: {cr}.  De {leituras[-1][0]} matérias cursadas."

def cria_tabela(host,user,pw,nome_db):
    criar_db = (f"CREATE DATABASE {nome_db};")
    connection = create_server_connection(host,user,pw)
    create_database(connection,criar_db)