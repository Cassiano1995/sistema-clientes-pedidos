from conexao import conectar
from mysql.connector import Error


def inserir_pedido(id_cliente, id_produto, quantidade, status="pendente"):
    """
    Cria um novo pedido com um único produto.
    Faz 3 operações em sequência: insere o pedido, insere o item,
    e atualiza o valor_total do pedido.
    """
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        # 1. Busca o preço atual do produto (pra guardar como preco_unitario)
        cursor.execute("SELECT preco FROM produtos WHERE id_produto = %s", (id_produto,))
        resultado = cursor.fetchone()

        if resultado is None:
            print(f"Produto ID {id_produto} não encontrado.")
            return

        preco_unitario = resultado[0]
        valor_total = preco_unitario * quantidade

        # 2. Insere o pedido (ainda sem o valor_total, ele é 0 por padrão)
        sql_pedido = """
            INSERT INTO pedidos (id_cliente, status, valor_total)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql_pedido, (id_cliente, status, valor_total))
        id_pedido = cursor.lastrowid  # pega o ID do pedido recém-criado

        # 3. Insere o item vinculado a esse pedido
        sql_item = """
            INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_item, (id_pedido, id_produto, quantidade, preco_unitario))

        conexao.commit()  # só confirma tudo depois que as duas inserções deram certo
        print(f"Pedido {id_pedido} criado com sucesso! Valor total: R${valor_total:.2f}")

    except Error as erro:
        conexao.rollback()  # desfaz tudo se algo deu errado no meio do processo
        print(f"Erro ao criar pedido: {erro}")

    finally:
        cursor.close()
        conexao.close()


def listar_pedidos():
    """
    Retorna todos os pedidos com detalhes do cliente e do produto (via JOIN).
    """
    conexao = conectar()
    if conexao is None:
        return []

    pedidos = []
    try:
        cursor = conexao.cursor()
        sql = """
            SELECT p.id_pedido, c.nome AS cliente, pr.nome AS produto,
                   i.quantidade, i.preco_unitario, p.valor_total,
                   p.status, p.data_pedido
            FROM pedidos p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            JOIN itens_pedido i ON p.id_pedido = i.id_pedido
            JOIN produtos pr ON i.id_produto = pr.id_produto
            ORDER BY p.id_pedido
        """
        cursor.execute(sql)
        pedidos = cursor.fetchall()

    except Error as erro:
        print(f"Erro ao listar pedidos: {erro}")

    finally:
        cursor.close()
        conexao.close()

    return pedidos


def atualizar_status_pedido(id_pedido, novo_status):
    """
    Atualiza apenas o status de um pedido (ex: pendente -> enviado).
    """
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()
        sql = "UPDATE pedidos SET status = %s WHERE id_pedido = %s"
        cursor.execute(sql, (novo_status, id_pedido))
        conexao.commit()

        if cursor.rowcount == 0:
            print(f"Nenhum pedido encontrado com ID {id_pedido}.")
        else:
            print(f"Status do pedido {id_pedido} atualizado para '{novo_status}'.")

    except Error as erro:
        print(f"Erro ao atualizar status: {erro}")

    finally:
        cursor.close()
        conexao.close()


def deletar_pedido(id_pedido):
    """
    Remove um pedido e seus itens vinculados.
    Precisa deletar de itens_pedido ANTES de deletar de pedidos,
    por causa da FOREIGN KEY.
    """
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        # 1. Deleta os itens do pedido primeiro
        cursor.execute("DELETE FROM itens_pedido WHERE id_pedido = %s", (id_pedido,))

        # 2. Depois deleta o pedido em si
        cursor.execute("DELETE FROM pedidos WHERE id_pedido = %s", (id_pedido,))

        conexao.commit()

        if cursor.rowcount == 0:
            print(f"Nenhum pedido encontrado com ID {id_pedido}.")
        else:
            print(f"Pedido {id_pedido} removido com sucesso!")

    except Error as erro:
        conexao.rollback()
        print(f"Erro ao deletar pedido: {erro}")

    finally:
        cursor.close()
        conexao.close()


# Bloco de teste - só roda se você executar este arquivo diretamente
if __name__ == "__main__":
    # Cria um pedido: cliente ID 1 comprando produto ID 1, quantidade 2
    inserir_pedido(id_cliente=1, id_produto=1, quantidade=2)

    print("\nPedidos cadastrados:")
    for pedido in listar_pedidos():
        print(pedido)