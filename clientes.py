from conexao import conectar
from mysql.connector import Error


def inserir_cliente(nome, email, telefone, endereco):
    """
    Insere um novo cliente no banco de dados.
    """
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()
        sql = """
            INSERT INTO clientes (nome, email, telefone, endereco)
            VALUES (%s, %s, %s, %s)
        """
        valores = (nome, email, telefone, endereco)
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"Cliente '{nome}' cadastrado com sucesso! (ID: {cursor.lastrowid})")

    except Error as erro:
        print(f"Erro ao inserir cliente: {erro}")

    finally:
        cursor.close()
        conexao.close()


def listar_clientes():
    """
    Retorna todos os clientes cadastrados no banco.
    """
    conexao = conectar()
    if conexao is None:
        return []

    clientes = []
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()

    except Error as erro:
        print(f"Erro ao listar clientes: {erro}")

    finally:
        cursor.close()
        conexao.close()

    return clientes


def atualizar_cliente(id_cliente, nome, email, telefone, endereco):
    """
    Atualiza os dados de um cliente existente, pelo id.
    """
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()
        sql = """
            UPDATE clientes
            SET nome = %s, email = %s, telefone = %s, endereco = %s
            WHERE id_cliente = %s
        """
        valores = (nome, email, telefone, endereco, id_cliente)
        cursor.execute(sql, valores)
        conexao.commit()

        if cursor.rowcount == 0:
            print(f"Nenhum cliente encontrado com ID {id_cliente}.")
        else:
            print(f"Cliente ID {id_cliente} atualizado com sucesso!")

    except Error as erro:
        print(f"Erro ao atualizar cliente: {erro}")

    finally:
        cursor.close()
        conexao.close()


def deletar_cliente(id_cliente):
    """
    Remove um cliente do banco, pelo id.
    Bloqueado automaticamente pelo banco se houver pedidos vinculados.
    """
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()
        sql = "DELETE FROM clientes WHERE id_cliente = %s"
        cursor.execute(sql, (id_cliente,))
        conexao.commit()

        if cursor.rowcount == 0:
            print(f"Nenhum cliente encontrado com ID {id_cliente}.")
        else:
            print(f"Cliente ID {id_cliente} removido com sucesso!")

    except Error as erro:
        print(f"Erro ao deletar cliente: {erro}")
        print("Dica: esse cliente pode ter pedidos vinculados a ele.")

    finally:
        cursor.close()
        conexao.close()


if __name__ == "__main__":
    inserir_cliente("Maria Souza", "maria@email.com", "21988887777", "Rua B, 456")

    print("\nClientes cadastrados:")
    for cliente in listar_clientes():
        print(cliente)