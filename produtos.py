from conexao import conectar
from mysql.connector import Error


def inserir_produto(nome, descricao, preco, estoque):
    """
    Insere um novo produto no banco de dados.
    """
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        sql = """
            INSERT INTO produtos (nome, descricao, preco, estoque)
            VALUES (%s, %s, %s, %s)
        """
        valores = (nome, descricao, preco, estoque)

        cursor.execute(sql, valores)
        conexao.commit()

        print(f"Produto '{nome}' cadastrado com sucesso! (ID: {cursor.lastrowid})")

    except Error as erro:
        print(f"Erro ao inserir produto: {erro}")

    finally:
        cursor.close()
        conexao.close()


def listar_produtos():
    """
    Retorna todos os produtos cadastrados no banco.
    """
    conexao = conectar()
    if conexao is None:
        return []

    produtos = []
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()

    except Error as erro:
        print(f"Erro ao listar produtos: {erro}")

    finally:
        cursor.close()
        conexao.close()

    return produtos


def atualizar_produto(id_produto, nome, descricao, preco, estoque):
    """
    Atualiza os dados de um produto existente, pelo id.
    """
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        sql = """
            UPDATE produtos
            SET nome = %s, descricao = %s, preco = %s, estoque = %s
            WHERE id_produto = %s
        """
        valores = (nome, descricao, preco, estoque, id_produto)

        cursor.execute(sql, valores)
        conexao.commit()

        if cursor.rowcount == 0:
            print(f"Nenhum produto encontrado com ID {id_produto}.")
        else:
            print(f"Produto ID {id_produto} atualizado com sucesso!")

    except Error as erro:
        print(f"Erro ao atualizar produto: {erro}")

    finally:
        cursor.close()
        conexao.close()


def deletar_produto(id_produto):
    """
    Remove um produto do banco, pelo id.
    Se o produto estiver vinculado a algum item de pedido, o banco vai
    bloquear a exclusão (por causa da FOREIGN KEY em itens_pedido).
    """
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()
        sql = "DELETE FROM produtos WHERE id_produto = %s"
        cursor.execute(sql, (id_produto,))
        conexao.commit()

        if cursor.rowcount == 0:
            print(f"Nenhum produto encontrado com ID {id_produto}.")
        else:
            print(f"Produto ID {id_produto} removido com sucesso!")

    except Error as erro:
        print(f"Erro ao deletar produto: {erro}")
        print("Dica: esse produto pode estar vinculado a itens de pedido.")

    finally:
        cursor.close()
        conexao.close()


# Bloco de teste - só roda se você executar este arquivo diretamente
if __name__ == "__main__":
    inserir_produto("Teclado Mecânico", "Teclado gamer RGB", 250.00, 10)
    inserir_produto("Mouse Óptico", "Mouse sem fio 1600 DPI", 89.90, 25)

    print("\nProdutos cadastrados:")
    for produto in listar_produtos():
        print(produto)