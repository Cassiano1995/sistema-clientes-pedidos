from conexao import conectar
from mysql.connector import Error


def inserir_cliente(nome, email, telefone, endereco):
    """
    Insere um novo cliente no banco de dados.
    """
    conexao = conectar()  # abre a conexão com o banco
    if conexao is None:    # se a conexão falhou, encerra a função aqui
        return

    try:
        cursor = conexao.cursor()  # cursor é o objeto que executa comandos SQL

        # %s são "placeholders" - o MySQL substitui pelos valores da tupla abaixo
        # isso evita SQL Injection (nunca formate a query com f-string)
        sql = """
            INSERT INTO clientes (nome, email, telefone, endereco)
            VALUES (%s, %s, %s, %s)
        """
        valores = (nome, email, telefone, endereco)

        cursor.execute(sql, valores)  # executa o INSERT
        conexao.commit()              # confirma a operação no banco (sem isso, nada é salvo de verdade)

        print(f"Cliente '{nome}' cadastrado com sucesso! (ID: {cursor.lastrowid})")
        # lastrowid pega automaticamente o ID que o MySQL gerou pro novo registro

    except Error as erro:
        print(f"Erro ao inserir cliente: {erro}")

    finally:
        # roda sempre, com ou sem erro, garantindo que a conexão não fique aberta
        cursor.close()
        conexao.close()


def listar_clientes():
    """
    Retorna todos os clientes cadastrados no banco.
    """
    conexao = conectar()
    if conexao is None:
        return []  # retorna lista vazia se não conseguiu conectar

    clientes = []
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM clientes")  # busca todos os registros
        clientes = cursor.fetchall()               # traz todos os resultados como lista de tuplas

    except Error as erro:
        print(f"Erro ao listar clientes: {erro}")

    finally:
        cursor.close()
        conexao.close()

    return clientes  # devolve a lista pra quem chamou a função


def atualizar_cliente(id_cliente, nome, email, telefone, endereco):
    """
    Atualiza os dados de um cliente existente, pelo id.
    """
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        # SET define quais colunas mudam, WHERE define qual registro é afetado
        sql = """
            UPDATE clientes
            SET nome = %s, email = %s, telefone = %s, endereco = %s
            WHERE id_cliente = %s
        """
        valores = (nome, email, telefone, endereco, id_cliente)

        cursor.execute(sql, valores)
        conexao.commit()

        # rowcount diz quantas linhas foram alteradas - se for 0, o ID não existia
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
    Se o cliente tiver pedidos vinculados, o banco vai bloquear a exclusão
    (por causa da FOREIGN KEY criada na tabela pedidos).
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
        # esse erro geralmente acontece quando o cliente tem pedidos vinculados
        print(f"Erro ao deletar cliente: {erro}")
        print("Dica: esse cliente pode ter pedidos vinculados a ele.")

    finally:
        cursor.close()
        conexao.close()


# Bloco de teste - só roda se você executar este arquivo diretamente
# (não roda se este arquivo for apenas importado em outro, como main.py)
if __name__ == "__main__":
    inserir_cliente("Maria Souza", "maria@email.com", "21988887777", "Rua B, 456")

    print("\nClientes cadastrados:")
    for cliente in listar_clientes():
        print(cliente)