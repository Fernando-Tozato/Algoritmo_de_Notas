import PySimpleGUI as sg
from funcoes import *
from banco_de_dados import *

# Define o layout das janelas
def janela_inicio():
    sg.theme('DarkBlack')
    layout = [
        [sg.Text('Seja bem-vindo! O que você gostaria de fazer?')],
        [sg.Button('Olhar as notas')],
        [sg.Button('Inserir matérias')],
        [sg.Button('Calcular CR')]
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
        [sg.Text()]
    ]
    return sg.Window('Notas',layout,finalize='true')

# Cria a janela inicial
janela1, janela2, janela3 = janela_inicio(), None, None

# Cria um loop de leitura de eventos
while True:
    window,event,values = sg.read_all_windows()
    # Fecha as janelas
    if window == janela1 and event == sg.WIN_CLOSED:
        break
    if window == janela2 and event == sg.WIN_CLOSED:
        break
    if window == janela3 and event == sg.WIN_CLOSED:
        break
    # Muda de janela
    if window == janela1 and event == 'Olhar as notas':
        escolha = 1
        janela2 = janela_login()
        janela1.hide()
    if window == janela1 and event == 'Inserir matérias':
        escolha = 2
        janela2 = janela_login()
        janela1.hide()
    if window == janela1 and event == 'Calcular CR':
        escolha = 3
        janela2 = janela_login()
        janela1.hide()
    if window == janela2 and event == 'Entrar':
        if not verifica_senha_connection(values['host'],values['user'],values['senha']):
            janela3 = janela_erro()
            janela2.hide()
        else:
            print('ok')