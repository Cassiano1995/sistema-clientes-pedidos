import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def conectar():
    """
    Cria e retorna uma conexão com o banco de dados MySQL.
    Se der erro, avisa o que aconteceu e retorna None.
    """
    try:
        conexao = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conexao

    except Error as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None


if __name__ == "__main__":
    conexao = conectar()

    if conexao is not None and conexao.is_connected():
        print("Conexão bem-sucedida!")
        conexao.close()
    else:
        print("Falha na conexão.")