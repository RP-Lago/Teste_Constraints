import random
from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Date, BigInteger, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker, registry
from sqlalchemy.orm import declarative_base

# Constantes
USUARIO = "db_constrain"                           # Substituir pelo nome do usuário do banco de dados
SENHA = "******"                                   # Substituir pela senha do banco de dados
NOME_SERVIDOR = r"******\SQLEXPRESS"               # Substituir pelo nome do servidor
BD_PRINCIPAL = "db_standard"                       # Substituir pelo nome do banco de dados
DRIVER_ODBC = "ODBC+Driver+17+for+SQL+Server"      # Substituir pelo driver ODBC se necessário
ESQUEMA_PRINCIPAL = "dbo"                          # Substituir pelo esquema do banco de dados
NOME_TABELA = "tb_people"                          # Substituir pelo nome da tabela

# Configuração do banco de dados
Base = declarative_base()

# Definição da tabela
class Pessoa(Base):
    __tablename__ = NOME_TABELA
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    sobrenome = Column(String(50), nullable=False)
    genero = Column(String(1), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    cpf = Column(BigInteger, unique=True, nullable=False)
    salario = Column(Integer, nullable=False)
    estado = Column(String(50), nullable=False)
    telefone = Column(String(20), nullable=False)

motor_principal = create_engine(f"mssql+pyodbc://{USUARIO}:{SENHA}@{NOME_SERVIDOR}/{BD_PRINCIPAL}?driver={DRIVER_ODBC}")

Base.metadata.create_all(motor_principal)

Session = sessionmaker(bind=motor_principal)
sessao = Session()

# Função para gerar números únicos
def gerar_numeros_unicos(quantidade, limite_inferior, limite_superior):
    numeros_unicos = set()
    while len(numeros_unicos) < quantidade:
        numero = random.randint(limite_inferior, limite_superior)
        numeros_unicos.add(numero)
    return numeros_unicos

# Função para gerar números de telefone
def gerar_telefone():
    return f'{random.randint(100,999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}'

fake = Faker()

# Gerar os números CPF únicos
numeros_cpf_unicos = gerar_numeros_unicos(100, 10000000000, 99999999999)

try:
    with sessao.begin():
        for cpf in numeros_cpf_unicos:
            novo_registro = Pessoa(
                nome=fake.first_name(),
                sobrenome=fake.last_name(),
                genero=random.choice(['M', 'F']),
                data_nascimento=fake.date_of_birth(),
                cpf=cpf,
                salario=random.randint(1000, 10000),
                estado=fake.state(),
                telefone=gerar_telefone()  # Use a função personalizada aqui
            )
            sessao.add(novo_registro)
except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    sessao.close()
    print("Fim da execução")
