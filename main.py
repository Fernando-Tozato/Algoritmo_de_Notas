import PySimpleGUI as sg
from funcoes import *
from banco_de_dados import *

global host,user,database,pw

# Define o layout das janelas
def janela_inicio():
    sg.theme('DarkBlack')
    layout = [
        [sg.Text('Seja bem-vindo! O que você gostaria de fazer?')],
        [sg.Button('Olhar as notas')],
        [sg.Button('Inserir matérias')],
        [sg.Button('Admin')]
    ]
    return sg.Window('Início',layout,finalize='true')

def janela_login():
    sg.theme('DarkBlack')
    layout = [
        [sg.Text('Para continuar, insira algumas informações: ')],
        [sg.Text('Host: '),sg.Input(key='host',size=(20,1))],
        [sg.Text('Usuário: '),sg.Input(key='user',size=(20,1))],
        [sg.Text('Banco de Dados: '),sg.Input(key='database',size=(20,1))],
        [sg.Text('Senha: '),sg.Input(key='senha',password_char='*',size=(20,1))],
        [sg.Button('Entrar')]
    ]
    return sg.Window('Login',layout,finalize='true')

def janela_erro():
    sg.theme('DarkBlack')
    layout = [
        [sg.Text('Para continuar, insira algumas informações: ')],
        [sg.Text('Host: '),sg.Input(key='host',size=(20,1))],
        [sg.Text('Usuário: '),sg.Input(key='user',size=(20,1))],
        [sg.Text('Banco de Dados: '),sg.Input(key='database',size=(20,1))],
        [sg.Text('Senha: '),sg.Input(key='senha',password_char='*',size=(20,1))],
        [sg.Button('Entrar')],
        [sg.Text('Informações erradas, por favor tente novamente.')]
    ]
    return sg.Window('Login',layout,finalize='true')

def janela_tabela():
    sg.theme('DarkBlack')
    layout = [
        [sg.Text(calcula_cr(host,user,pw,database))],
        [sg.Text(mostra_notas(host,user,pw,database))],
        [sg.Button('Voltar')]
    ]
    return sg.Window('Notas',layout,finalize='true')

def janela_dados():
    sg.theme('DarkBlack')
    layout = [
        [sg.Text('Se alguma das avaliações não foi realizada, coloque 0')],
        [sg.Text('Matéria: '),sg.Input(key='materia',size=(50,1))],
        [sg.Text('Código: '),sg.Input(key='codigo',size=(10,1))],
        [sg.Text('AV1: '),sg.Input(key='av1',size=(4,1))],
        [sg.Text('AV2: '),sg.Input(key='av2',size=(4,1))],
        [sg.Text('AV3: '),sg.Input(key='av3',size=(4,1))],
        [sg.Text('AVA1: '),sg.Input(key='ava1',size=(4,1))],
        [sg.Text('AVA2: '),sg.Input(key='ava2',size=(4,1))],
        [sg.Text('AVD: '),sg.Input(key='avd',size=(4,1))],
        [sg.Text('AVDS: '),sg.Input(key='avds',size=(4,1))],
        [sg.Button('Ok')]
    ]
    return sg.Window('Dados',layout,finalize='true')

def janela_admin():
    sg.theme('DarkBlack')
    layout = [
        [sg.Text('Criar Database:')],
        [sg.Text('Nome: '),sg.Input(key='nome_db',size=(20,1))],
        [sg.Button('Criar')],
        [sg.Text('')],
        [sg.Text('Escrever código:')],
        [sg.Input(key='comandos',size=(100,100))],
        [sg.Button('Commit')],
        [sg.Button('Voltar')]
    ]
    return sg.Window('Admin',layout,finalize='true')

# Cria a janela inicial
janela1, janela2, janela3, janela4, janela5 = janela_inicio(), None, None, None, None

# Cria um loop de leitura de eventos
while True:
    window,event,values = sg.read_all_windows()
    
    # Fecha as janelas
    if window == janela1 and event == sg.WIN_CLOSED: break
    if window == janela2 and event == sg.WIN_CLOSED: break
    if window == janela3 and event == sg.WIN_CLOSED: break
    if window == janela4 and event == sg.WIN_CLOSED: break
    if window == janela5 and event == sg.WIN_CLOSED: break
    
    # Janela 1, janela de início com login
    if window == janela1 and event == 'Olhar as notas':
        escolha = 1
        janela2 = janela_login()
        janela1.hide()
    
    if window == janela1 and event == 'Inserir matérias':
        escolha = 2
        janela2 = janela_login()
        janela1.hide()
    
    if window == janela1 and event == 'Admin':
        escolha = 3
        janela2 = janela_login()
        janela1.hide()
    
    # Janelas 2 e 3, janelas de login e erro de login
    if (window == janela2 or window == janela3) and event == 'Entrar':
        if (window == janela2 or window == janela3) and not verifica_senha_connection(values['host'],values['user'],values['senha']):
            janela3 = janela_erro()
            janela2.hide()
        else:
            host = values['host']
            user = values['user']
            database = values['database']
            pw = values['senha']
            
            if escolha == 1:
                janela4 = janela_tabela()
                janela2.hide()
            
            if escolha == 2:
                janela4 = janela_dados()
                janela2.hide()
            
            if escolha == 3:
                if user == 'root':
                    janela4 = janela_admin()
                    janela2.hide()
                else:
                    janela3 = janela_erro()
                    janela2.hide()
    
    # Janela 4, todas as janelas com operações
    if window == janela4 and event == 'Voltar':
        janela5 = janela_inicio()
        janela4.hide()
    
    if window == janela4 and event == 'Ok':
        insere_materias(host,user,pw,database,values['materia'],values['codigo'],float(values['av1']),float(values['av2']),float(values['av3']),float(values['ava1']),float(values['ava2']),float(values['avd']),float(values['avds']))
        janela4.hide()
        janela4 = janela_tabela()
    
    if window == janela4 and event == 'Criar':
        cria_tabela(host,user,pw,values['nome_db'])
    
    if window == janela4 and event == 'Commit':
        connection = create_db_connection(host,user,pw,database)
        execute_query(connection,values['comandos'])
    
    # Janela 5, janela de início com login apenas para admin
    if window == janela5 and event == 'Olhar as notas':
        janela4 = janela_tabela()
        janela5.hide()
    
    if window == janela5 and event == 'Inserir matérias':
        janela4 = janela_dados()
        janela5.hide()
    
    if window == janela5 and event == 'Admin':
        escolha = 3
        janela2 = janela_login()
        janela5.hide()