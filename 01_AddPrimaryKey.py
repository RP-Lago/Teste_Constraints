import pyodbc

# Função para conectar ao banco de dados
def conectar_bd(servidor, banco_dados, usuario, senha, driver):
    try:
        conn = pyodbc.connect(
            f"DRIVER={driver};SERVER={servidor};DATABASE={banco_dados};UID={usuario};PWD={senha}")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados {banco_dados}: {e}")
        return None
# Função para obter as colunas de uma tabela
def obter_colunas(conn, tabela):
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{tabela}'
    """)
    return [row[0] for row in cursor]
# Função para ajustar as colunas de uma tabela
def ajustar_colunas(conn, tabela, colunas_adicionar, colunas_remover):
    cursor = conn.cursor()
    for coluna in colunas_adicionar:
        cursor.execute(f"ALTER TABLE {tabela} ADD {coluna} VARCHAR(255)")
        print(f"Coluna '{coluna}' adicionada à tabela '{tabela}'.")
    
    for coluna in colunas_remover:
        cursor.execute(f"ALTER TABLE {tabela} DROP COLUMN {coluna}")
        print(f"Coluna '{coluna}' removida da tabela '{tabela}'.")
    
    conn.commit()
# Configurações de conexão
def verificar_chave_primaria(conn, tabela):
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT Col.Column_Name from 
            INFORMATION_SCHEMA.TABLE_CONSTRAINTS Tab, 
            INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE Col 
        WHERE 
            Col.Constraint_Name = Tab.Constraint_Name
            AND Col.Table_Name = Tab.Table_Name
            AND Constraint_Type = 'PRIMARY KEY'
            AND Col.Table_Name = '{tabela}'
        ORDER BY Col.Column_Name
    """)
    return [row[0] for row in cursor]

def criar_chave_primaria(conn, tabela, colunas):
    cursor = conn.cursor()
    try:
        colunas_str = ', '.join(colunas)
        cursor.execute(f"ALTER TABLE {tabela} ADD PRIMARY KEY ({colunas_str})")
        conn.commit()
        print(f"Chave primária adicionada à tabela {tabela} com colunas {colunas_str}.")
    except Exception as e:
        print(f"Erro ao adicionar chave primária: {e}")

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
        # Verificar e ajustar chaves primárias
        colunas_standard = verificar_chave_primaria(conn_standard, TABELA)
        colunas_cloned = verificar_chave_primaria(conn_cloned, TABELA)

        if colunas_standard and not colunas_cloned:
            criar_chave_primaria(conn_cloned, TABELA, colunas_standard)
            print(f"Chave primária com colunas {colunas_standard} adicionada à tabela '{TABELA}' no db_cloned.")
        elif not colunas_standard and colunas_cloned:
            print("Chave primária não existe em tb_people no db_standard, mas existe no db_cloned.")
        else:
            print("Chave primária já existe em tb_people no db_cloned ou não existe em db_standard.")

        # Verificar e ajustar colunas
        colunas_standard = set(obter_colunas(conn_standard, TABELA))
        colunas_cloned = set(obter_colunas(conn_cloned, TABELA))

        colunas_adicionar = colunas_standard - colunas_cloned
        colunas_remover = colunas_cloned - colunas_standard

        if colunas_adicionar or colunas_remover:
            ajustar_colunas(conn_cloned, TABELA, colunas_adicionar, colunas_remover)
        else:
            print("As estruturas das tabelas tb_people já são idênticas nos dois bancos de dados.")

        conn_standard.close()
        conn_cloned.close()