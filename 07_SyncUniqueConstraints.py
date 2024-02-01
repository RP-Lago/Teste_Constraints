import pyodbc

import pyodbc

def conectar_bd(servidor, banco_dados, usuario, senha, driver):
    try:
        conn = pyodbc.connect(
            f"DRIVER={driver};SERVER={servidor};DATABASE={banco_dados};UID={usuario};PWD={senha}")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados {banco_dados}: {e}")
        return None

def obter_detalhes_restricoes_exclusivas(conn, tabela):
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 
            tc.CONSTRAINT_NAME, 
            STRING_AGG(kcu.COLUMN_NAME, ', ') WITHIN GROUP (ORDER BY kcu.ORDINAL_POSITION)
        FROM 
            INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
        JOIN 
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS kcu ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
        WHERE 
            tc.TABLE_NAME = '{tabela}' AND tc.CONSTRAINT_TYPE = 'UNIQUE'
        GROUP BY
            tc.CONSTRAINT_NAME
    """)
    return {row[0]: row[1] for row in cursor.fetchall()}

def modificar_restricoes_exclusivas(conn, tabela, restricoes_standard, restricoes_cloned):
    cursor = conn.cursor()
    # Remover restrições que não correspondem ou estão ausentes em db_standard
    for nome in restricoes_cloned:
        if nome not in restricoes_standard or restricoes_cloned[nome] != restricoes_standard[nome]:
            cursor.execute(f"ALTER TABLE {tabela} DROP CONSTRAINT {nome}")
            print(f"Restrição exclusiva '{nome}' removida da tabela '{tabela}'.")
    
    # Adicionar ou recriar restrições de db_standard que estão ausentes ou foram removidas de db_cloned
    for nome, colunas in restricoes_standard.items():
        if nome not in restricoes_cloned or restricoes_cloned[nome] != colunas:
            colunas_str = ', '.join(colunas.split(', '))
            cursor.execute(f"ALTER TABLE {tabela} ADD CONSTRAINT {nome} UNIQUE ({colunas_str})")
            print(f"Restrição exclusiva '{nome}' com colunas {colunas_str} adicionada ou recriada na tabela '{tabela}'.")

    conn.commit()

# Configurações de conexão
USER = "db_constrain"                            # Substituir pelo nome do usuário do banco de dados
PASSWORD = "******"                              # Substituir pela senha do banco de dados
SERVER = r"*******\SQLEXPRESS"                   # Substituir pelo nome do servidor
PRIMARY_DB = "db_standard"                       # Substituir pelo nome do banco de dados
CLONED_DB = "db_cloned"                          # Substituir pelo nome do banco de dados
DRIVER_ODBC = "ODBC Driver 17 for SQL Server"    # Substituir pelo driver ODBC se necessário
TABELA = "tb_people"                             # Substituir pelo nome da tabela


# Configurações de conexão mantêm-se iguais

if __name__ == "__main__":
    conn_standard = conectar_bd(SERVER, PRIMARY_DB, USER, PASSWORD, DRIVER_ODBC)
    conn_cloned = conectar_bd(SERVER, CLONED_DB, USER, PASSWORD, DRIVER_ODBC)

    restricoes_standard = obter_detalhes_restricoes_exclusivas(conn_standard, TABELA)
    restricoes_cloned = obter_detalhes_restricoes_exclusivas(conn_cloned, TABELA)

    modificar_restricoes_exclusivas(conn_cloned, TABELA, restricoes_standard, restricoes_cloned)

    print("Processo de sincronização de restrições exclusivas concluído.")


    conn_standard.close()
    conn_cloned.close()
