import pyodbc
import datetime

def conectar_bd(servidor, banco_dados, usuario, senha, driver):
    """
    Estabelece conexão com o banco de dados especificado.
    """
    try:
        conn = pyodbc.connect(f"DRIVER={driver};SERVER={servidor};DATABASE={banco_dados};UID={usuario};PWD={senha}")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados {banco_dados}: {e}")
        return None

def obter_restricoes_exclusivas(conn, tabela):
    """
    Recupera as restrições exclusivas e as colunas associadas de uma tabela específica.
    """
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT tc.CONSTRAINT_NAME, 
               STRING_AGG(kcu.COLUMN_NAME, ', ') WITHIN GROUP (ORDER BY kcu.ORDINAL_POSITION)
        FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
        JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS kcu ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
        WHERE tc.TABLE_NAME = '{tabela}' AND tc.CONSTRAINT_TYPE = 'UNIQUE'
        GROUP BY tc.CONSTRAINT_NAME
    """)
    return {row[0]: row[1].split(', ') for row in cursor.fetchall()}

def sincronizar_restricoes_exclusivas(conn_standard, conn_cloned, tabela):
    """
    Compara e ajusta restrições exclusivas da tabela no db_cloned para corresponder ao db_standard.
    """
    restricoes_standard = obter_restricoes_exclusivas(conn_standard, tabela)
    restricoes_cloned = obter_restricoes_exclusivas(conn_cloned, tabela)

    cursor = conn_cloned.cursor()
    for nome, colunas in restricoes_cloned.items():
        # Se a restrição exclusiva não corresponde ou está ausente no db_standard
        if nome not in restricoes_standard or sorted(colunas) != sorted(restricoes_standard.get(nome, [])):
            cursor.execute(f"ALTER TABLE {tabela} DROP CONSTRAINT {nome}")
            print(f"Restrição exclusiva '{nome}' removida de '{tabela}' no db_cloned.")

    for nome, colunas in restricoes_standard.items():
        # Se a restrição exclusiva está ausente ou difere no db_cloned
        if nome not in restricoes_cloned or sorted(colunas) != sorted(restricoes_cloned.get(nome, [])):
            colunas_str = ', '.join(colunas)
            cursor.execute(f"ALTER TABLE {tabela} ADD CONSTRAINT {nome} UNIQUE ({colunas_str})")
            print(f"Restrição exclusiva '{nome}' adicionada/recriada em '{tabela}' no db_cloned.")

    conn_cloned.commit()

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
        sincronizar_restricoes_exclusivas(conn_standard, conn_cloned, TABELA)
        print("Sincronização de restrições exclusivas concluída.")

    conn_standard.close()
    conn_cloned.close()
