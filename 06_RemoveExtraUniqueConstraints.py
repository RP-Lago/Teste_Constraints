import pyodbc

def conectar_bd(servidor, banco_dados, usuario, senha, driver):
    try:
        conn = pyodbc.connect(
            f"DRIVER={driver};SERVER={servidor};DATABASE={banco_dados};UID={usuario};PWD={senha}")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados {banco_dados}: {e}")
        return None

def obter_restricoes_exclusivas(conn, tabela):
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 
            tc.CONSTRAINT_NAME
        FROM 
            INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
        WHERE 
            tc.CONSTRAINT_TYPE = 'UNIQUE' AND tc.TABLE_NAME = '{tabela}'
    """)
    return [row[0] for row in cursor]

def remover_restricao_exclusiva(conn, tabela, restricao):
    cursor = conn.cursor()
    try:
        cursor.execute(f"ALTER TABLE {tabela} DROP CONSTRAINT {restricao}")
        conn.commit()
        print(f"Restrição exclusiva '{restricao}' removida da tabela '{tabela}'.")
    except Exception as e:
        print(f"Erro ao remover restrição exclusiva '{restricao}': {e}")

# Configurações de conexão
USER = "db_constrain"                            # Substituir pelo nome do usuário do banco de dados
PASSWORD = "******"                              # Substituir pela senha do banco de dados
SERVER = r"*******\SQLEXPRESS"                   # Substituir pelo nome do servidor
PRIMARY_DB = "db_standard"                       # Substituir pelo nome do banco de dados
CLONED_DB = "db_cloned"                          # Substituir pelo nome do banco de dados
DRIVER_ODBC = "ODBC Driver 17 for SQL Server"    # Substituir pelo driver ODBC se necessário
TABELA = "tb_people"                             # Substituir pelo nome da tabela


if __name__ == "__main__":
    conn_standard = conectar_bd(SERVER, PRIMARY_DB, USER, PASSWORD, DRIVER_ODBC)
    conn_cloned = conectar_bd(SERVER, CLONED_DB, USER, PASSWORD, DRIVER_ODBC)

    if conn_standard and conn_cloned:
        restricoes_standard = set(obter_restricoes_exclusivas(conn_standard, TABELA))
        restricoes_cloned = set(obter_restricoes_exclusivas(conn_cloned, TABELA))

        restricoes_a_remover = restricoes_cloned - restricoes_standard

        for restricao in restricoes_a_remover:
            remover_restricao_exclusiva(conn_cloned, TABELA, restricao)

        if not restricoes_a_remover:
            print("Não há restrições exclusivas em 'db_cloned' que não existam em 'db_standard'.")

        conn_standard.close()
        conn_cloned.close()
