"""
    Neste projeto, você terá a oportunidade de criar um Sistema Bancário em Python.
    O objetivo é implementar três operações essenciais: depósito, saque e extrato.
    O sistema será desenvolvido para um banco que busca monetizar suas operações.
    Durante o desafio, você terá a chance de aplicar seus conhecimentos em programação
    Python e criar um sistema funcional que simule as operações bancárias.
    Prepare-se para aprimorar suas habilidades e demonstrar sua capacidade de desenvolver soluções práticas e eficientes.
"""

from datetime import datetime as dt


class SistemaBancario():

    def __init__(self) -> None:

        self.LIMITE_QTD_SAQUES = 3
        self.LIMITE_VR_SAQUE = 500
        self.proximo_id_usuario = 1
        self.proximo_numero_conta = 1
        self.usuarios = []
        self.contas = []

        self.iniciar_interacao_usuario()

        pass
    
    @staticmethod
    def menu(opcao):
        match(opcao):
            case 1:
                return """
----------- Bem vindo ao banco Tabajara -----------------
Escolha uma opção:

[1] Ja tenho cadastro
[2] Criar cadastro
[0] Sair

=>
"""
            case 2:
                return """
---------------------------------------------------------
Escolha uma opção:

[1] Ja tenho uma conta
[2] Criar conta
[0] Voltar pro menu anterior

=>
"""
            case 3:
                return """
---------------------------------------------------------
Qual transação deseja fazer:

[d] Depositar
[s] Sacar
[e] Extrato
[q] Voltar ao menu anterior 

=>"""

    @staticmethod
    def resgatar_cpf():
        return input("Digite o numero do seu cpf: \n=>").replace(".", "").replace("-", "")

    def depositar(self, conta):
        valor_depositar = float(input("Digite o valor que deseja depositar: \n"))
        conta['saldo'] += valor_depositar
        conta['extrato'] += f"{dt.now()} - Valor depositado: R${valor_depositar:.2f}\n"
        print("Deposito feito!")

    def sacar(self, conta):
        valor_sacar = float(input("Digite o valor que deseja sacar: \n=>"))
        if valor_sacar > self.LIMITE_VR_SAQUE:
            print("Valor acima do limite de saque!")
        elif conta['numero_saques'] >= self.LIMITE_QTD_SAQUES:
            print("Você atingiu o limite de saques!")
        elif valor_sacar > conta['saldo']:
            print("Saldo indisponivel!")
        else:
            conta['saldo'] -= valor_sacar
            conta['extrato'] += f"{dt.now()} - Valor sacado: R${valor_sacar:.2f}\n"
            conta['numero_saques'] += 1
            print("Saque feito!")

    def ver_extrato(self, usuario, conta):
        print("-------------------------- Extrato ----------------------")
        print(f"ID: {usuario['id']}")
        print(f"Nome: {usuario['nome']}")
        print(f"CPF: {usuario['cpf']}")
        print(f"Data de Nascimento: {usuario['data_nascimento']}")
        print(f"Endereco: {usuario['endereco']}")
        print("---------------------------------------------------------")
        print(f"Agencia: {conta['agencia']}")
        print(f"Conta: {conta['conta']}")
        print("---------------------------------------------------------")
        print(conta['extrato'])
        print("---------------------------------------------------------")
        print(f"Saldo Atual: R${conta['saldo']:.2f}")
        print("---------------------------------------------------------")
        
    def conta_existente(self, usuario, conta):

        for conta_verifica in self.contas:
            if conta_verifica['usuario'] == usuario['id'] \
                and conta == conta_verifica['conta']:
                return True, conta_verifica
        return False, None

    def criar_conta(self, usuario):

        conta = {
            "usuario": usuario["id"],
            "agencia": "0001",
            "conta": self.proximo_numero_conta,
            "saldo": 0,
            "extrato": "",
            "numero_saques": 0,
        }
        self.proximo_numero_conta += 1
        self.contas.append(conta)

        if bool(input("Deseja realizar transações nesta conta? 1 - Sim\n=>")):
            self.realizar_transacoes(usuario, conta)

    def listar_contas(self, usuario):
        print("------------------------- Contas ------------------------")
        for conta in self.contas:
            if conta['usuario'] == usuario['id']:
                print(f"Agencia: {conta['agencia']} - Conta: {conta['conta']}")
        print("---------------------------------------------------------")

    def usuario_existente(self, cpf):
        for usuario in self.usuarios:
            if usuario['cpf'] == cpf:
                return True, usuario
        return False, None

    def criar_usuario(self):

        cpf = self.resgatar_cpf()
        ic_existe, usuario = self.usuario_existente(cpf)
        if ic_existe:
            print("Usuario ja existe.")
        else:
            nome = input("Digite o nome: ")
            data_nascimento = input("Digite a data de nascimento: ")

            print("Vamos cadastrar o endereço! \n")
            logradouro = input("Digite o logradouro: ")
            numero = input("Digite o numero: ")
            bairro = input("Digite o bairo: ")
            cidade = input("Digite a cidade: ")
            sigla_estado = input("Digite a sigla do estado: ")

            endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{sigla_estado}"

            usuario = {
                'id': self.proximo_id_usuario,
                'cpf': cpf,
                'nome': nome,
                'data_nascimento': data_nascimento,
                'endereco': endereco,
            }

            self.proximo_id_usuario += 1
            self.usuarios.append(usuario)
            print("Usuario criado")

        if bool(input("Deseja realizar transações? 1 - Sim\n=>")):
            self.iniciar_interacao_conta(usuario)

    def realizar_transacoes(self, usuario, conta):
        while(True):
            # Transações
            opcao = input(self.menu(3))
            match(opcao):
                case "d":
                    self.depositar(conta)
                case "s":
                    self.sacar(conta)
                case "e":
                    self.ver_extrato(usuario, conta)
                case "q":
                    break
                case _:
                    print("Opção invalida! Tente novamente")

    def iniciar_interacao_conta(self, usuario):

        while(True):
            self.listar_contas(usuario)
            opcao = int(input(self.menu(2)))
            match(opcao):
                case 1:
                    numero_conta = int(input("Digite o numero da conta: "))
                    ic_existe, conta = self.conta_existente(usuario, numero_conta)
                    if ic_existe:
                        self.realizar_transacoes(usuario, conta)
                    else:
                        print("Conta inexistente, confira o numero ou crie uma.")
                case 2:
                    self.criar_conta(usuario)
                case 0:
                    break
                case _:
                    print("Opção invalida!")

    def iniciar_interacao_usuario(self):

        while(True):
            # Menu inicial
            opcao = int(input(self.menu(1)))
            match(opcao):
                case 1:
                    cpf = self.resgatar_cpf()
                    ic_existe, usuario_existente = self.usuario_existente(cpf)
                    if ic_existe:
                        self.iniciar_interacao_conta(usuario_existente)
                    else:
                        print("Usuario inexistente, confira o cpf ou crie um cadastro")
                case 2:
                    self.criar_usuario()
                case 0:
                    break
                case _:
                    print("Opção invalida!")

    pass


if __name__ == "__main__":
    SistemaBancario()
