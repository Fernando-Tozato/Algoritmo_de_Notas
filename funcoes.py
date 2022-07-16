from banco_de_dados import *
import os

host = 'localhost'
user = 'python'
database = 'notas'
duas_etapas = 'sua_senha'

# Verifica a senha de acesso ao database
def verifica_senha():
    global pw
    os.system('cls' if os.name == 'nt' else 'clear')
    pw = input("Para continuar, insira a senha do banco de dados: ")
    while not verifica_senha_connection(host,user,pw):
        os.system('cls' if os.name == 'nt' else 'clear')
        pw = input("Senha errada. Por favor, tente novamente: ")

# Pergunta ao usuário qual operação vai ser efetuada
def escolhe_operacao():
    escolha_ok = True
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Seja bem-vindo! O que você gostaria de fazer?")
    while escolha_ok:
        print("""
        1 - Olhar as notas.
        2 - Inserir matérias.
        3 - Calcular CR.
        """)
        escolha = input("--> ")
        
        if not (escolha == '1' or escolha == '2' or escolha == '3' or escolha == 'admin'):
            print("Operação inválida, tente novamente.\n")
        else:
            escolha_ok = False
    
    return escolha

# Pega a tabela do banco de dados e imprime ao usuário
def mostra_notas():
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
    colunas = ['ID','Matéria','Cód.','Carga','AV1','AVA1','AV2','AVA2','AV3','AVD','AVDS','Média']
    df = pd.DataFrame(leituras, columns = colunas)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(df)

# Calcula a média
def calcula_media(av1,ava1,av2,ava2,av3,avd,avds):
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
    media = round(soma / 3,1)
    return media

# Preenche a tabela com as informções que o usuário insere
def insere_materias():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Pergunta ao usuário quantas matérias serão inseridas
    num = int(input("Quantas matérias você gostaria de inserir? --> "))
    
    for i in range(num):
        print("Matéria número",i)
        # Define todas as informações da tabela e imprime a média ao usuário
        os.system('cls' if os.name == 'nt' else 'clear')
        materia = input("Insira o nome completo da matéria: ")
        codigo = input("Insira o código da matéria: ")
        carga = 80
        av1 = round(float(input("Insira a nota da AV1. Caso não tenha feito, coloque 0: ")),2)
        av2 = round(float(input("Insira a nota da AV2. Caso não tenha feito, coloque 0: ")),2)
        av3 = round(float(input("Insira a nota da AV3. Caso não tenha feito, coloque 0: ")),2)
        ava1 = round(float(input("Insira a nota da AVA1. Caso não tenha feito, coloque 0: ")),2)
        ava2 = round(float(input("Insira a nota da AVA2. Caso não tenha feito, coloque 0: ")),2)
        avd = round(float(input("Insira a nota da AVD. Caso não tenha feito, coloque 0: ")),2)
        avds = round(float(input("Insira a nota da AVDS. Caso não tenha feito, coloque 0: ")),2)
        media = calcula_media(av1,ava1,av2,ava2,av3,avd,avds)
        
        # Cria os comandos em SQL
        inserir_dados = f"insert into notas(materia,codigo,carga,av1,av2,av3,ava1,ava2,avd,avds,media) value ('{materia}','{codigo}',{carga},{av1},{av2},{av3},{ava1},{ava2},{avd},{avds},{media})"
        
        # Faz a conexão com a DB e comita os comandos
        connection = create_db_connection(host,user,pw,database)
        execute_query(connection,inserir_dados)

# Calcula o CR usando a DB
def calcula_cr():
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
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Seu CR é:",cr,"\nCálculo feito a partir de",leituras[-1][0],"matérias.")

# Verifica se o usuário é admin
def verifica_admin():
    # Faz a verificação com o SQL
    verifica_senha()
    # Inicia uma verificação em duas etapas com senha definida no topo do código
    count = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    enter = input("Insira a senha de verificação em duas etapas: ")
    if enter == duas_etapas:
        return True
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        enter = input("Senha incorreta, tente novamente: ")
        if enter == duas_etapas:
            return True
        # Limita o número de tentativas a três no total
        count += 1
        if count >= 2: 
            print('Números de tentativas excedido, tente novamente mais tarde.')
            return False

# Permite criar uma db e comitar
def modo_admin():
    # Escolhe o tipo de operção a ser realizada
    os.system('cls' if os.name == 'nt' else 'clear')
    print('O que vocÊ deseja fazer?')
    escolha_ok = True
    while escolha_ok:
        print("""
        1 - Criar uma DataBase
        2 - Escrever meu próprio código
        """)
        escolha = input("--> ")
        
        if not (escolha == '1' or escolha == '2'):
            print("Operação inválida, tente novamente.\n")
        else:
            escolha_ok = False
    
    # Cria uma db
    if escolha == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        nome_db = input('Digite o nome da DataBase: ')
        criar_db = (f"CREATE DATABASE '{nome_db}';")
        connection = create_server_connection(host,user,pw)
        create_database(connection,criar_db)
        
    # Executa comandos definidos pelo usuário
    elif escolha == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        database = input("Digite o nome da DataBase a ser editada: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Digite os comandos a serem executados (escreva tudo em uma linha, só dê enter quando terminar.)")
        comandos = input("> ")
        connection = create_db_connection(host,user,pw,database)
        execute_query(connection,comandos)
        
# Pergunta se o usuário quer realizar outra operação
def repete_ou_fim():
    print("\n\nVocê gostaria de executar mais alguma operação?")
    escolha_ok = True
    while escolha_ok:
        print("""
        1 - Olhar as notas.
        2 - Inserir matérias.
        3 - Calcular CR.
        4 - Encerrar o programa.
        """)
        escolha = input("--> ")
        
        if not (escolha == '1' or escolha == '2' or escolha == '3' or escolha == '4' or escolha == 'admin'):
            print("Operação inválida, tente novamente.\n")
        else:
            escolha_ok = False
    
    if escolha == '1':
        mostra_notas()
        repete_ou_fim()
    elif escolha == '2':
        insere_materias()
        repete_ou_fim()
    elif escolha == '3':
        calcula_cr()
        repete_ou_fim()
    elif escolha == '4':
        print("Programa encerrado com sucesso.")
        return
    elif escolha == 'admin': 
        if verifica_admin():
            modo_admin()
            repete_ou_fim()