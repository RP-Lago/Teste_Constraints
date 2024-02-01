import pyodbc

def conectar_bd(servidor, banco_dados, usuario, senha, driver):
    try:
        conn = pyodbc.connect(
            f"DRIVER={driver};SERVER={servidor};DATABASE={banco_dados};UID={usuario};PWD={senha}")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados {banco_dados}: {e}")
        return None

def verificar_chave_primaria(conn, tabela):
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

def remover_chave_primaria(conn, tabela):
    cursor = conn.cursor()
    try:
        # Encontrar o nome da chave primária
        cursor.execute(f"SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE TABLE_NAME = '{tabela}' AND CONSTRAINT_TYPE = 'PRIMARY KEY'")
        constraint_name = cursor.fetchone()
        if constraint_name:
            # Remover a chave primária
            sql = f"ALTER TABLE {tabela} DROP CONSTRAINT {constraint_name[0]}"
            cursor.execute(sql)
            conn.commit()
            print(f"Chave primária removida da tabela {tabela}.")
    except Exception as e:
        print(f"Erro ao remover chave primária: {e}")

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
        chave_primaria_standard = verificar_chave_primaria(conn_standard, TABELA)
        chave_primaria_cloned = verificar_chave_primaria(conn_cloned, TABELA)

        if not chave_primaria_standard and chave_primaria_cloned:
            remover_chave_primaria(conn_cloned, TABELA)
        else:
            print("A chave primária em tb_people no db_standard existe ou não existe no db_cloned.")

        conn_standard.close()
        conn_cloned.close()
