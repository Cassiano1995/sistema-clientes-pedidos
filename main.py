# menu e interação com usuário

from clientes import inserir_cliente, listar_clientes, atualizar_cliente, deletar_cliente
from produtos import inserir_produto, listar_produtos, atualizar_produto, deletar_produto
from pedidos import inserir_pedido, listar_pedidos, atualizar_status_pedido, deletar_pedido


def menu_clientes():
    while True:
        print("\n--- MENU CLIENTES ---")
        print("1. Cadastrar cliente")
        print("2. Listar clientes")
        print("3. Atualizar cliente")
        print("4. Deletar cliente")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            endereco = input("Endereço: ")
            inserir_cliente(nome, email, telefone, endereco)

        elif opcao == "2":
            clientes = listar_clientes()
            if not clientes:
                print("Nenhum cliente cadastrado.")
            for c in clientes:
                print(c)

        elif opcao == "3":
            id_cliente = input("ID do cliente a atualizar: ")
            nome = input("Novo nome: ")
            email = input("Novo email: ")
            telefone = input("Novo telefone: ")
            endereco = input("Novo endereço: ")
            atualizar_cliente(id_cliente, nome, email, telefone, endereco)

        elif opcao == "4":
            id_cliente = input("ID do cliente a deletar: ")
            deletar_cliente(id_cliente)

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


def menu_produtos():
    while True:
        print("\n--- MENU PRODUTOS ---")
        print("1. Cadastrar produto")
        print("2. Listar produtos")
        print("3. Atualizar produto")
        print("4. Deletar produto")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            descricao = input("Descrição: ")
            preco = float(input("Preço: "))
            estoque = int(input("Estoque: "))
            inserir_produto(nome, descricao, preco, estoque)

        elif opcao == "2":
            produtos = listar_produtos()
            if not produtos:
                print("Nenhum produto cadastrado.")
            for p in produtos:
                print(p)

        elif opcao == "3":
            id_produto = input("ID do produto a atualizar: ")
            nome = input("Novo nome: ")
            descricao = input("Nova descrição: ")
            preco = float(input("Novo preço: "))
            estoque = int(input("Novo estoque: "))
            atualizar_produto(id_produto, nome, descricao, preco, estoque)

        elif opcao == "4":
            id_produto = input("ID do produto a deletar: ")
            deletar_produto(id_produto)

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


def menu_pedidos():
    while True:
        print("\n--- MENU PEDIDOS ---")
        print("1. Criar pedido")
        print("2. Listar pedidos")
        print("3. Atualizar status do pedido")
        print("4. Deletar pedido")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            id_cliente = input("ID do cliente: ")
            id_produto = input("ID do produto: ")
            quantidade = int(input("Quantidade: "))
            inserir_pedido(id_cliente, id_produto, quantidade)

        elif opcao == "2":
            pedidos = listar_pedidos()
            if not pedidos:
                print("Nenhum pedido cadastrado.")
            for p in pedidos:
                print(p)

        elif opcao == "3":
            id_pedido = input("ID do pedido: ")
            novo_status = input("Novo status (pendente/enviado/entregue/cancelado): ")
            atualizar_status_pedido(id_pedido, novo_status)

        elif opcao == "4":
            id_pedido = input("ID do pedido a deletar: ")
            deletar_pedido(id_pedido)

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


def menu_principal():
    while True:
        print("\n===== SISTEMA DE CLIENTES E PEDIDOS =====")
        print("1. Gerenciar Clientes")
        print("2. Gerenciar Produtos")
        print("3. Gerenciar Pedidos")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_clientes()
        elif opcao == "2":
            menu_produtos()
        elif opcao == "3":
            menu_pedidos()
        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()