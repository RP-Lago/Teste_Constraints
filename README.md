**Titulo**: Sincronização de Restrições de Banco de Dados em SQL Server

Autor: **Robson P. Lago**.

**Script 1 - Criação de Chave Primária Ausente**
**Objetivo:** Adiciona uma chave primária na tabela `tb_people` no `db_cloned` se ela existir no `db_standard` mas não no `db_cloned`.

**Pontos Importantes:**
- Verificação da existência da chave primária nas duas bases de dados.
- Criação da chave primária no `db_cloned` utilizando as mesmas colunas e configurações presentes no `db_standard`.

**Script 2 - Adição de Restrições db_standard**
**Objetivo:** Adiciona restrições específicas (denominadas `db_standard`) na tabela `tb_people` no `db_cloned` que estão presentes no `db_standard` mas ausentes no `db_cloned`.

**Pontos Importantes:**
- Identificação de restrições específicas (`db_standard`) em ambas as bases.
- Adição das restrições ausentes no `db_cloned` para igualar ao `db_standard`.

**Script 3 - Remoção de Chave Primária Extra**
**Objetivo:** Remove uma chave primária na tabela `tb_people` no `db_cloned` se ela não existir no `db_standard`.

**Pontos Importantes:**
- Verificação de chaves primárias que estão no `db_cloned` mas não no `db_standard`.
- Remoção segura da chave primária extra no `db_cloned`.

**Script 4 - Sincronização de Chaves Primárias**
**Objetivo:** Modifica a definição da chave primária na tabela `tb_people` no `db_cloned` para corresponder exatamente à do `db_standard`, quando ambas existem mas diferem.

**Pontos Importantes:**
- Comparação detalhada das definições de chaves primárias entre as bases.
- Ajuste da chave primária no `db_cloned` para garantir identidade com o `db_standard`.

**Script 5 - Adição de Restrições Exclusivas**
**Objetivo:** Adiciona restrições exclusivas na tabela `tb_people` no `db_cloned` que estão presentes no `db_standard` mas ausentes no `db_cloned`.

**Pontos Importantes:**
- Identificação e adição de índices ou chaves únicas ausentes para sincronizar as bases.

**Script 6 - Remoção de Restrições Exclusivas Extras**
**Objetivo:** Remove restrições exclusivas da tabela `tb_people` no `db_cloned` que não existem no `db_standard`.

**Pontos Importantes:**
- Verificação de restrições exclusivas que devem ser removidas para alinhamento entre as bases.

**Script 7 - Sincronização de Restrições Exclusivas**
**Objetivo:** Ajusta restrições exclusivas na tabela `tb_people` no `db_cloned` para corresponder exatamente às encontradas no `db_standard`, focando em discrepâncias identificadas anteriormente.

**Pontos Importantes:**
- Análise detalhada e ajuste das restrições para garantir consistência total.

**Script 8 - Remoção de Restrições db_standard Extras**
**Objetivo:** Remove qualquer restrição (denominada `db_standard`) na tabela `tb_people` no `db_cloned` que não esteja presente no `db_standard`.

**Pontos Importantes:**
- Limpeza de restrições que não correspondem ao padrão definido pelo `db_standard`.

**Script 9 - Registro de Resultados**
**Objetivo:** Registra os resultados das comparações de restrição e ajustes realizados nos scripts anteriores, dentro de um sistema denominado MasterCheck.

**Pontos Importantes:**
- Implementação de registro de operações para auditoria e controle de mudanças.
- Uso de uma tabela de log para armazenar informações sobre as operações realizadas, facilitando a rastreabilidade.

**Considerações Gerais:**
- A automação dessas tarefas é crucial para manter a integridade e a consistência dos dados entre bancos de dados que devem ser espelhados ou sincronizados.
- É importante testar esses scripts em um ambiente de desenvolvimento ou teste antes de aplicá-los em produção para evitar impactos indesejados.
- A gestão adequada de erros e a verificação das operações são essenciais para garantir a eficácia e a segurança desses processos.
- A documentação detalhada e a manutenção dos scripts são fundamentais para facilitar a compreensão e a manutenção futura desses processos.
