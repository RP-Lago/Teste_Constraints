import pyodbc

def conectar_bd(servidor, banco_dados, usuario, senha, driver):
    try:
        conn = pyodbc.connect(
            f"DRIVER={driver};SERVER={servidor};DATABASE={banco_dados};UID={usuario};PWD={senha}")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados {banco_dados}: {e}")
        return None

def obter_restricoes_exclusivas_com_colunas(conn, tabela):
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 
            tc.CONSTRAINT_NAME, 
            kcu.COLUMN_NAME
        FROM 
            INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
        JOIN 
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS kcu
            ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
        WHERE 
            tc.CONSTRAINT_TYPE = 'UNIQUE' 
            AND tc.TABLE_NAME = '{tabela}'
    """)
    restricoes = {}
    for row in cursor.fetchall():
        if row[0] not in restricoes:
            restricoes[row[0]] = []
        restricoes[row[0]].append(row[1])
    return restricoes

def adicionar_restricao_exclusiva(conn, tabela, restricao, colunas):
    cursor = conn.cursor()
    colunas_str = ', '.join(colunas)
    try:
        cursor.execute(f"ALTER TABLE {tabela} ADD CONSTRAINT {restricao} UNIQUE ({colunas_str})")
        conn.commit()
        print(f"Restrição exclusiva '{restricao}' com colunas {colunas_str} adicionada à tabela '{tabela}'.")
    except Exception as e:
        print(f"Erro ao adicionar restrição exclusiva '{restricao}': {e}")


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
        restricoes_standard = obter_restricoes_exclusivas_com_colunas(conn_standard, TABELA)
        restricoes_cloned = obter_restricoes_exclusivas_com_colunas(conn_cloned, TABELA)

        for restricao, colunas in restricoes_standard.items():
            if restricao not in restricoes_cloned:
                adicionar_restricao_exclusiva(conn_cloned, TABELA, restricao, colunas)

        conn_standard.close()