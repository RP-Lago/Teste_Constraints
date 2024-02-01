import pyodbc

def conectar_bd(servidor, banco_dados, usuario, senha, driver):
    try:
        conn = pyodbc.connect(
            f"DRIVER={driver};SERVER={servidor};DATABASE={banco_dados};UID={usuario};PWD={senha}")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados {banco_dados}: {e}")
        return None

def obter_definicao_chave_primaria(conn, tabela):
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT Col.Column_Name FROM 
            INFORMATION_SCHEMA.TABLE_CONSTRAINTS Tab, 
            INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE Col 
        WHERE 
            Col.Constraint_Name = Tab.Constraint_Name
            AND Col.Table_Name = Tab.Table_Name
            AND Constraint_Type = 'PRIMARY KEY'
            AND Col.Table_Name = '{tabela}'
    """)
    return [row[0] for row in cursor]

def modificar_chave_primaria(conn, tabela, colunas):
    cursor = conn.cursor()
    try:
        # Obter o nome da chave primária atual
        cursor.execute(f"SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE TABLE_NAME = '{tabela}' AND CONSTRAINT_TYPE = 'PRIMARY KEY'")
        constraint_name = cursor.fetchone()
        if constraint_name:
            # Remover a chave primária existente
            cursor.execute(f"ALTER TABLE {tabela} DROP CONSTRAINT {constraint_name[0]}")
        # Adicionar a nova chave primária
        colunas_str = ', '.join(colunas)
        cursor.execute(f"ALTER TABLE {tabela} ADD CONSTRAINT {constraint_name[0] if constraint_name else 'PK_' + tabela} PRIMARY KEY ({colunas_str})")
        conn.commit()
        print(f"Chave primária modificada na tabela {tabela} para as colunas {colunas_str}.")
    except Exception as e:
        print(f"Erro ao modificar chave primária: {e}")

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
        chave_primaria_standard = obter_definicao_chave_primaria(conn_standard, TABELA)
        chave_primaria_cloned = obter_definicao_chave_primaria(conn_cloned, TABELA)

        if set(chave_primaria_standard) != set(chave_primaria_cloned):
            modificar_chave_primaria(conn_cloned, TABELA, chave_primaria_standard)
        else:
            print("As chaves primárias em tb_people já são idênticas nos dois bancos de dados.")

        conn_standard.close()
        conn_cloned.close()
