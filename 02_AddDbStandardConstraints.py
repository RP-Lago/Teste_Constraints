import pyodbc

def conectar_bd(servidor, banco_dados, usuario, senha, driver):
    try:
        conn = pyodbc.connect(
            f"DRIVER={driver};SERVER={servidor};DATABASE={banco_dados};UID={usuario};PWD={senha}")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados {banco_dados}: {e}")
        return None

def verificar_restricoes(conn, tabela):
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 
            CONSTRAINT_NAME, 
            CHECK_CLAUSE
        FROM 
            INFORMATION_SCHEMA.CHECK_CONSTRAINTS
        WHERE 
            CONSTRAINT_NAME IN (
                SELECT 
                    CONSTRAINT_NAME
                FROM 
                    INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE
                WHERE 
                    TABLE_NAME = '{tabela}'
            )
    """)
    return {row[0]: row[1] for row in cursor.fetchall()}

def adicionar_restricoes(conn, tabela, restricoes):
    cursor = conn.cursor()
    for restricao, clausula in restricoes.items():
        sql = f"ALTER TABLE {tabela} ADD CONSTRAINT {restricao} CHECK ({clausula})"
        cursor.execute(sql)
    conn.commit()
    print(f"Restrições adicionadas à tabela {tabela}: {list(restricoes.keys())}")


# Configurações de conexão
USER = "db_constrain"                            # Substituir pelo nome do usuário do banco de dados
PASSWORD = "******"                              # Substituir pela senha do banco de dados
SERVER = r"*******\SQLEXPRESS"                   # Substituir pelo nome do servidor
PRIMARY_DB = "db_standard"                       # Substituir pelo nome do banco de dados
CLONED_DB = "db_cloned"                          # Substituir pelo nome do banco de dados
DRIVER_ODBC = "ODBC Driver 17 for SQL Server"    # Substituir pelo driver ODBC se necessário
TABELA = "tb_people"                             # Substituir pelo nome da tabela


# Executar o script
if __name__ == "__main__":
    conn_standard = conectar_bd(SERVER, PRIMARY_DB, USER, PASSWORD, DRIVER_ODBC)
    conn_cloned = conectar_bd(SERVER, CLONED_DB, USER, PASSWORD, DRIVER_ODBC)

    if conn_standard and conn_cloned:
        restricoes_standard = verificar_restricoes(conn_standard, TABELA)
        restricoes_cloned = verificar_restricoes(conn_cloned, TABELA)

        restricoes_a_adicionar = {r: clausula for r, clausula in restricoes_standard.items() if r not in restricoes_cloned}

        if restricoes_a_adicionar:
            adicionar_restricoes(conn_cloned, TABELA, restricoes_a_adicionar)
        else:
            print("Não há restrições db_standard ausentes em tb_people no db_cloned.")

        conn_standard.close()