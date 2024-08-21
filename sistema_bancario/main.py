"""
    Neste projeto, você terá a oportunidade de criar um Sistema Bancário em Python.
    O objetivo é implementar três operações essenciais: depósito, saque e extrato.
    O sistema será desenvolvido para um banco que busca monetizar suas operações.
    Durante o desafio, você terá a chance de aplicar seus conhecimentos em programação
    Python e criar um sistema funcional que simule as operações bancárias.
    Prepare-se para aprimorar suas habilidades e demonstrar sua capacidade de desenvolver soluções práticas e eficientes.
"""

from datetime import datetime as dt

LIMITE_QTD_SAQUES = 3
LIMITE_VR_SAQUE = 500

saldo = 0
extrato = ""
numero_saques = 0

def menu():
    return """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair 

=>"""

def depositar():
    global saldo, extrato
    valor_depositar = float(input("Digite o valor que deseja depositar: \n"))
    saldo += valor_depositar
    extrato += f"{dt.now()} - Valor depositado: R${valor_depositar:.2f}\n"

def sacar():
    global LIMITE_QTD_SAQUES, LIMITE_VR_SAQUE, saldo, extrato, numero_saques

    valor_sacar = float(input("Digite o valor que deseja sacar: \n"))
    if valor_sacar > LIMITE_VR_SAQUE:
        print("Valor acima do limite de saque!")
    elif numero_saques >= LIMITE_QTD_SAQUES:
        print("Você atingiu o limite de saques!")
    elif valor_sacar > saldo:
        print("Saldo indisponivel!")
    else:
        saldo -= valor_sacar
        extrato += f"{dt.now()} - Valor sacado: R${valor_sacar:.2f}\n"
        numero_saques += 1

    pass

def ver_extrato():
    global saldo, extrato
    print("--------- Extrato ------------\n")
    print(extrato)
    print(f"Saldo Atual: R${saldo:.2f}")

while(True):
    opcao = input(menu())
    match(opcao):
        case "d":
            depositar()
        case "s":
            sacar()
        case "e":
            ver_extrato()
        case "q":
            break
        case _:
            print("Opção invalida! Tente novamente")

