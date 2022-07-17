from banco_de_dados import *
from funcoes import *

# A fazer:
# - Fazer um display

escolha = escolhe_operacao()

if escolha == '1':
    mostra_notas()
    repete_ou_fim()
elif escolha == '2':
    insere_materias()
    repete_ou_fim()
elif escolha == '3':
    calcula_cr()
    repete_ou_fim()
elif escolha == 'admin':
    if verifica_admin():
        modo_admin()
        repete_ou_fim()