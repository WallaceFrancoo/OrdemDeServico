import sqlite3
import datetime
conn = sqlite3.connect('clientes_servicos.db')
cursor = conn.cursor()
# Criar tabelas se não existirem
cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    CPF TEXT NOT NULL,
    NOME TEXT NOT NULL,
    TELEFONE TEXT, 
    ENDERECO TEXT,
    EMAIL TEXT    
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS servicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    data TEXT,
    servico TEXT,
    expiracao_servicos TEXT,
    notificao_servico TEXT,
    forma_de_pagamento TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
)
''')
conn.commit()


def adicionar_cliente(cpf, nome, telefone, endereco, email):
    cursor.execute('INSERT INTO clientes (CPF, NOME, TELEFONE, ENDERECO, EMAIL) VALUES (?, ?, ?, ?, ?)', (cpf, nome, telefone, endereco, email))
    conn.commit()
    print(f"Cliente '{nome}' adicionado com sucesso.")
def registrar_servico(identificacao, servico, formadepagamento):
    cursor.execute('SELECT NOME FROM clientes WHERE CPF = ?', (identificacao,))
    cliente = cursor.fetchone()
    if cliente:
        cliente_id = cliente[0]
        data_atual = datetime.datetime.now()
        dataVenc = data_atual + datetime.timedelta(days=30)
        dataNot = dataVenc - datetime.timedelta(days=20)
        data_atual_str = data_atual.strftime("%d/%m/%Y")
        dataVenc_str = dataVenc.strftime("%d/%m/%Y")
        dataNot_str = dataNot.strftime("%d/%m/%Y")
        cursor.execute('INSERT INTO servicos (cliente_id, data, servico, expiracao_servicos, notificao_servico, forma_de_pagamento) VALUES (?, ?, ?, ?, ?, ? )', (cliente_id, data_atual_str, servico,dataVenc_str,dataNot_str,formadepagamento))
        conn.commit()
        print(f"Serviço '{servico}' registrado para o cliente com o registro: '{identificacao}' na data {data_atual_str}. e expira dia: {dataVenc_str} e a forma de pagamento foi {formadepagamento}")
    else:
        print(f"Cliente '{identificacao}' não encontrado. Por favor, cadastre o cliente primeiro.")
def exibir_historicoI(identificacao):
    cursor.execute('SELECT NOME FROM clientes WHERE CPF = ?', (identificacao,))
    cliente = cursor.fetchone()
    if cliente:
        cliente_id = cliente[0]
        cursor.execute('SELECT data, servico, forma_de_pagamento FROM servicos WHERE cliente_id = ? ORDER BY data', (cliente_id,))
        servicos = cursor.fetchall()
        if servicos:
            print(f"Histórico de serviços para o cliente '{cliente_id}':")
            for servico in servicos:
                print(f"Data: {servico[0]}, Serviço: {servico[1]}, forma de pagamento: {servico[2]}")
        else:
            print(f"Nenhum serviço registrado para o cliente '{cliente_id}'.")
    else:
        print(f"Cliente '{identificacao}' não encontrado.")
def exibir_historicoD(identificacao):
    cursor.execute('SELECT * FROM clientes')
    cliente = cursor.fetchone()
    cursor.execute('SELECT * FROM servicos')
    dataSelecionada = cursor.fetchone()
    if dataSelecionada:
        data_selecionada = dataSelecionada[0]
        cursor.execute('SELECT cliente_id, data, servico, forma_de_pagamento FROM servicos WHERE data = ? ORDER BY data', (identificacao,))
        servicos = cursor.fetchall()
        if servicos:
            print(f"Histórico de serviços para data: '{identificacao}':")
            for servico in servicos:
                print(f"Cliente: {servico[0]} | Data: {servico[1]} | Serviço: {servico[2]} | Forma de pagamento: {servico[3]}")
        else:
            print(f"Nenhum serviço registrado no dia: '{identificacao}'.")
    else:
        print(f"Data '{identificacao}' não encontrado.")
def exibir_historicoG():
    cursor.execute('SELECT * FROM servicos')
    servicos = cursor.fetchone()
    if servicos:
        cursor.execute('SELECT cliente_id, data, servico, forma_de_pagamento FROM servicos')
        servicos = cursor.fetchall()
        if servicos:
            print(f"Histórico dos serviços: \n':")
            for servico in servicos:
                print(f"Cliente: {servico[0]} | Data: {servico[1]} | Serviço: {servico[2]} | Forma de pagamento: {servico[3]}")
        else:
            print(f"Sem serviço!.")
    else:
        print(f"Não tem serviços! .")
def consulta_vencimentos():
    data_atual = datetime.datetime.now()
    data_atual_str = data_atual.strftime("%d/%m/%Y")

    cursor.execute(
        'SELECT c.NOME, s.servico, s.notificao_servico FROM servicos s JOIN clientes c ON s.cliente_id = c.id WHERE s.notificao_servico <= ?',
        (data_atual_str,))
    vencimentos = cursor.fetchall()

    if vencimentos:
        print("Serviços que expiram nos próximos 20 dias:")
        for vencimento in vencimentos:
            print(f"Cliente: {vencimento[0]}, Serviço: {vencimento[1]}, Expiração: {vencimento[2]}")
    else:
        print("Nenhum serviço expira nos próximos 20 dias.")
def mostrar_Cadastros(cpf):
    cursor.execute('SELECT CPF FROM clientes WHERE CPF = ?', (cpf,))
    cliente = cursor.fetchone()
    if cliente:
        cliente_cpf = cliente[0]
        cursor.execute('SELECT CPF, NOME, TELEFONE, ENDERECO, EMAIL FROM clientes WHERE cpf = ? ORDER BY cpf', (cliente_cpf,))
        dados = cursor.fetchall()
        if dados:
            print(f"O Cadastro referente ao CPF:'{cpf}' é:")
            for dado in dados:
                print(f"CPF: {dado[0]}, \nNOME: {dado[1]}\nTELEFONE: {dado[2]}\nENDERECO: {dado[3]}\nEMAIL: {dado[4]} ")
        else:
            print(f"Nenhum cadastro para o CPF: '{cpf}'.")
    else:
        print(f"CPF: '{cpf}' não encontrado.")
def cadastros_Gerais():
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchone()
    if clientes:
        identificacao = clientes[1]

        cursor.execute('SELECT * FROM clientes')
        dados = cursor.fetchall()
        if dados:
            for dado in dados:
                print(f"Cliente: {dado[2]}, Identificao: {dado[1]} ")
        else:
            print("sem dados pra preencher")
def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Adicionar Cliente")
        print("2. Registrar Serviço")
        print("3. Exibir Histórico")
        print("4. Consultar Itens expirados")
        print("5. Pesquisar cadastro")
        print("6. Mostrar usuarios cadastrados")
        print("10. Sair")
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            cpf = input("Digite o CPF: ")
            nome = input("Digite o nome do Cliente: ")
            telefone = input("Telefone: ")
            endereco = input("CEP: ")
            email =  input("Email: ")
            adicionar_cliente(cpf, nome, telefone, endereco, email)
        elif escolha == '2':
            identificao = input("Digite o CPF/CNPJ do cliente: ")
            servico = input("Digite o serviço realizado: ")

            pagamento = input("Qual foi a forma de pagamento: \n1- PIX\n2- DINHEIRO\n3- DEBITO\n4- CREDITO:\n")
            if pagamento == "1":
                formadepagamento = "PIX"
            elif pagamento == "2":
                formadepagamento = "DINHEIRO"
            elif pagamento == "3":
                formadepagamento = "DEBITO"
            elif pagamento == "4":
                formadepagamento = "CREDITO"
            else:
                print("Opção Invalida!")
            registrar_servico(identificao, servico, formadepagamento)
        elif escolha == '3':
            funcao = input("1- Consulta por CPF/CNPJ\n2- Consulta por data\n3- Consulta Geral\n")
            if funcao == "1":
                identificacao = input("Digite o CPF/CNPJ do cliente: ").replace(".","").replace(",","").replace("/","").replace("-","")
                exibir_historicoI(identificacao)
            elif funcao == "2":
                identificacao = input("Digite a data desejada: \n Por favor colocar em formato dd/mm/aaaa: \n")
                exibir_historicoD(identificacao)
            elif funcao == "3":
                exibir_historicoG()
            else:
                print("Opção invalida! \nVoltando ao menu princial")
                menu()
        elif escolha == "4":
            print("Consultando....")
            consulta_vencimentos()
        elif escolha == "5":
            cpf = input("Qual CPF gostaria de verificar: ").replace(".","").replace(",","").replace("/","").replace("-","")
            mostrar_Cadastros(cpf)
        elif escolha == "6":
            cadastros_Gerais()
        elif escolha == '10':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")
menu()
conn.close()