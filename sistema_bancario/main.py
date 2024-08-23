"""
    Neste projeto, você terá a oportunidade de criar um Sistema Bancário em Python.
    O objetivo é implementar três operações essenciais: depósito, saque e extrato.
    O sistema será desenvolvido para um banco que busca monetizar suas operações.
    Durante o desafio, você terá a chance de aplicar seus conhecimentos em programação
    Python e criar um sistema funcional que simule as operações bancárias.
    Prepare-se para aprimorar suas habilidades e demonstrar sua capacidade de desenvolver soluções práticas e eficientes.
"""

from datetime import datetime as dt

class Usuario():

    usuarios = []
    proximo_id_usuario = 1

    def __init__(self, id, nome, cpf, data_nascimento, **dados_enderecos):

        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.logradouro = dados_enderecos['logradouro']
        self.numero = dados_enderecos['numero']
        self.bairro = dados_enderecos['bairro']
        self.cidade = dados_enderecos['cidade']
        self.sigla_estado = dados_enderecos['sigla_estado']
        self._endereco = f"{self.logradouro}, {self.numero} - {self.bairro} - {self.cidade}/{self.sigla_estado}"

        pass 
    
    @property
    def endereco(self):
        return self._endereco

    @classmethod
    def usuario_existente(cls, cpf):
        for usuario in cls.usuarios:
            if usuario.cpf == cpf:
                return True, usuario
        return False, None

    @classmethod
    def criar_usuario(cls, cpf):

        ic_existe, usuario = cls.usuario_existente(cpf)
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

            usuario = Usuario(**{
                'id': cls.proximo_id_usuario,
                'cpf': cpf,
                'nome': nome,
                'data_nascimento': data_nascimento,
                'logradouro': logradouro,
                'numero': numero,
                'bairro': bairro,
                'cidade': cidade,
                'sigla_estado': sigla_estado,
            })

            cls.proximo_id_usuario += 1
            cls.usuarios.append(usuario)
            print("Usuario criado")
        return usuario

    pass


class Conta():

    LIMITE_QTD_SAQUES = 3
    LIMITE_VR_SAQUE = 500
    proximo_numero_conta = 1
    contas = []

    def __init__(self, usuario, conta):
        self.usuario = usuario
        self._agencia = "0001"
        self.conta = conta
        self._saldo = 0
        self._extrato = []
        self._numero_saques = 0

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def extrato(self):
        return self._extrato
    
    @extrato.setter
    def extrato(self, mensagem):
        self._extrato.append(f"{dt.now()} - {mensagem}")

    @extrato.getter
    def extrato(self):
        mensagem_extrato = ""
        for mensagem in self._extrato:
            mensagem_extrato += (mensagem + "\n")
        return mensagem_extrato
        
    @property
    def numero_saques(self):
        return self._numero_saques
    
    @numero_saques.setter
    def numero_saques(self, incremento):
        self._numero_saques += incremento

    @classmethod
    def criar_conta(cls, usuario):
        conta = cls(usuario=usuario,conta=cls.proximo_numero_conta)
        cls.proximo_numero_conta += 1
        cls.contas.append(conta)
        return conta
    
    @classmethod
    def listar_contas(cls, usuario):
        print("------------------------- Contas ------------------------")
        for conta in cls.contas:
            if conta.usuario == usuario:
                print(f"Agencia: {conta.agencia} - Conta: {conta.conta}")
        print("---------------------------------------------------------")

    @classmethod
    def conta_existente(cls, usuario, numero_conta):
        for conta_verifica in cls.contas:
            if conta_verifica.usuario == usuario \
                and numero_conta == conta_verifica.conta:
                return True, conta_verifica
        return False, None

    def depositar(self, valor_depositar):
        self._saldo += valor_depositar
        self.extrato = f"Valor depositado: R${valor_depositar:.2f}"
        print("Deposito feito!")

    def sacar(self, valor_sacar):
        if valor_sacar > self.LIMITE_VR_SAQUE:
            print("Valor acima do limite de saque!")
        elif self.numero_saques >= self.LIMITE_QTD_SAQUES:
            print("Você atingiu o limite de saques!")
        elif valor_sacar > self._saldo:
            print("Saldo indisponivel!")
        else:
            self._saldo -= valor_sacar
            self.extrato = f"Valor sacado: R${valor_sacar:.2f}"
            self.numero_saques = 1
            print("Saque feito!")

    def ver_extrato(self):
        print("-------------------------- Extrato ----------------------")
        print(f"ID: {self.usuario.id}")
        print(f"Nome: {self.usuario.nome}")
        print(f"CPF: {self.usuario.cpf}")
        print(f"Data de Nascimento: {self.usuario.data_nascimento}")
        print(f"Endereco: {self.usuario.endereco}")
        print("---------------------------------------------------------")
        print(f"Agencia: {self.agencia}")
        print(f"Conta: {self.conta}")
        print("---------------------------------------------------------")
        print(self.extrato)
        print("---------------------------------------------------------")
        print(f"Saldo Atual: R${self.saldo:.2f}")
        print("---------------------------------------------------------")

    pass


class SistemaBancario():

    def __init__(self):
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

    def realizar_transacoes(self, conta):
        while(True):
            # Transações
            opcao = input(self.menu(3))
            match(opcao):
                case "d":
                    valor_depositar = float(input("Digite o valor que deseja depositar: \n"))
                    conta.depositar(valor_depositar)
                case "s":
                    valor_sacar = float(input("Digite o valor que deseja sacar: \n=>"))
                    conta.sacar(valor_sacar)
                case "e":
                    conta.ver_extrato()
                case "q":
                    break
                case _:
                    print("Opção invalida! Tente novamente")

    def iniciar_interacao_conta(self, usuario):

        while(True):
            Conta.listar_contas(usuario)
            opcao = int(input(self.menu(2)))
            match(opcao):
                case 1:
                    numero_conta = int(input("Digite o numero da conta: "))
                    ic_existe, conta = Conta.conta_existente(usuario, numero_conta)
                    if ic_existe:
                        self.realizar_transacoes(conta)
                    else:
                        print("Conta inexistente, confira o numero ou crie uma.")
                case 2:
                    conta = Conta.criar_conta(usuario)
                    if bool(input("Deseja realizar transações nesta conta? 1 - Sim\n=>")):
                        self.realizar_transacoes(conta)
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
                    ic_existe, usuario_existente = Usuario.usuario_existente(cpf)
                    if ic_existe:
                        self.iniciar_interacao_conta(usuario_existente)
                    else:
                        print("Usuario inexistente, confira o cpf ou crie um cadastro")
                case 2:
                    cpf = self.resgatar_cpf()
                    usuario = Usuario.criar_usuario(cpf)
                    if bool(input("Deseja realizar transações? 1 - Sim\n=>")):
                        self.iniciar_interacao_conta(usuario)
                case 0:
                    break
                case _:
                    print("Opção invalida!")

    pass


if __name__ == "__main__":
    SistemaBancario()
