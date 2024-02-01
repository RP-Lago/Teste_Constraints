-- Adicionando restrições de verificação (CHECK CONSTRAINTS) na tabela tb_people
-- Restrição de idade
ALTER TABLE dbo.tb_people
ADD CONSTRAINT chk_Idade
CHECK (idade >= 18 AND idade <= 65);
GO

-- Restrição de sexo
ALTER TABLE dbo.tb_people
ADD CONSTRAINT chk_Sexo
CHECK (sexo = 'M' OR sexo = 'F');
GO

-- Restrição de estado civil
ALTER TABLE dbo.tb_people
ADD CONSTRAINT chk_EstadoCivil
CHECK (estado_civil IN ('Solteiro', 'Casado', 'Divorciado', 'Viúvo'));
GO

-- Restrição de ID positivo
ALTER TABLE dbo.tb_people
ADD CONSTRAINT chk_Id
CHECK (id > 0);
GO

-- Adicionando índice único para testes em db_standard
ALTER TABLE dbo.tb_people ADD CONSTRAINT ID_tb_people_Std1 UNIQUE NONCLUSTERED ([id])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY];
GO

-- Adicionando índice único para testes em db_cloned
-- Assegure-se de estar conectado ao banco de dados db_cloned antes de executar este comando
ALTER TABLE dbo.tb_people ADD CONSTRAINT ID_tb_people_Cnd1 UNIQUE NONCLUSTERED ([id])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY];
GO


USE [db_standard]; -- Ou db_cloned, dependendo de onde você quer verificar as restrições
GO

-- Consulta para verificar restrições únicas na tabela tb_people
SELECT 
    tc.CONSTRAINT_NAME, 
    tc.TABLE_NAME, 
    kcu.COLUMN_NAME
FROM 
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
JOIN 
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS kcu ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
WHERE 
    tc.CONSTRAINT_TYPE = 'UNIQUE'
    AND tc.TABLE_NAME = 'tb_people';
GO
