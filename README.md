# Script para Conferência de Serviços Realizados

ETL ad hoc para extração e cruzamento de dados entre relatórios de solicitações de exames e relatórios de faturamento mensal.
**Status do Projeto**: Concluido com inviabilidade de uso. [Limitações](#limitações-conhecidas).

## Contexto
Os exames laboratoriais realizados para os municipes que utilizam o SUS na cidade Capela do Alto são realizados por laboratório terceirizado. Seus fechamentos para pagamento são mensais e a conferência é manual. Uma das etapas dessa conferência é a validação entre cada exame faturado e cada exame solicitado para o respectivo paciente, demandando tempo e atenção para cruzar as informações das guias de exames e o relatório da empresa, sendo assim, tentei desenvolver uma automação para otimização de tempo.

Mais informações: [Relatório de Desenvolvimento](./Relatorio_de_Desenvolvimento.docx).


## Visão Geral

- **PDF Saúde:** ~2107 páginas, ~96.922 linhas(Variável), formato tabular (uma linha por exame)
- **PDF Clínica:** Quantidade variável de páginas/linhas, formato livre por Unidade de Saúde (faturamento mensal)

A divergência de nomenclatura de exames entre os dois sistemas exigiu a criação de uma tabela de padronização (`padrao.xlsx`) com 131 entradas mapeando exames laboratoriais e alérgenos. 

## Uso

1. Coloque os PDFs de entrada nos caminhos esperados pelo `main.py`
2. Garanta que a pasta `output/` existe
3. Na pasta `output/` consta as planilhas iniciais devido serem produto da extração dos pdfs, por isso não estão na pasta `data/`

## Limitações Conhecidas

Documentadas em detalhe no [Relatório de Desenvolvimento](./Relatorio_de_Desenvolvimento.docx). Resumo:

### 1. Ausência de chave única por solicitação

O cruzamento entre as duas bases é feito **apenas pelo nome do paciente**, pois nenhum dos relatórios fornece um identificador único de solicitação (como número de guia). Em pacientes com múltiplas solicitações ao longo dos 6 meses analisados, é impossível determinar qual remessa de exames faturados corresponde a qual solicitação específica.

### 2. Desalinhamento temporal entre relatórios

O fechamento mensal de faturamento da clínica não corresponde ao mês das solicitações: um exame solicitado em junho pode ser faturado em outubro. A solução adotada foi expandir a janela do relatório de saúde para cobrir os 6 meses anteriores ao faturamento, mas isso amplifica o problema do item 1.

### 3. Divergências de grafia em nomes

Nomes escritos de forma ligeiramente diferente nos dois PDFs ("João Silva" vs "JOAO  SILVA") aparecem como "Não Encontrado" no cruzamento. A função `limpar()` mitiga (remove acentos, normaliza espaços, lowercase), mas erros maiores precisam de correção manual.


## Sobre os Dados de Exemplo (Anonimização e LGPD)

### Os dados deste repositório são fictícios e anonimizados

Os arquivos `.xlsx` incluídos servem **apenas como exemplo funcional** para que qualquer pessoa possa rodar o pipeline e verificar as etapas do ETL. Nenhum dado real de pacientes está presente neste repositório.

### Processo de anonimização aplicado

A anonimização foi feita em três camadas:

1. **Substituição de nomes:** todos os nomes reais foram substituídos por identificadores genéricos no formato `Paciente_0001`, `Paciente_0002`, etc. A consistência entre as tabelas é preservada — o mesmo nome real recebe o mesmo identificador em todas as planilhas, mantendo a viabilidade do cruzamento por nome.

2. **Embaralhamento de datas:** todas as datas foram deslocadas com um offset aleatório entre -5 e +5 dias, somado a uma subtração de 1 ano (datas originais de 2025 → 2024). A consistência interna é preservada: solicitações que ocorreram no mesmo dia para o mesmo paciente continuam agrupadas no mesmo dia após a anonimização (mantendo o funcionamento de `normaliza_saude()`).

3. **PDFs originais não incluídos:** os arquivos-fonte (`pdf_saude.pdf`, `pdf_clinica.pdf`) não são distribuídos, apenas as planilhas derivadas e já anonimizadas.

### Considerações sobre LGPD

A Lei Geral de Proteção de Dados (Lei nº 13.709/2018) classifica dados referentes à saúde como **dados pessoais sensíveis** (Art. 5º, II). Mesmo com nomes substituídos, datas e listas de exames poderiam, em tese, permitir re-identificação em cenários específicos (município pequeno, combinações raras de exames). 

Por isso este repositório aplica anonimização agressiva (deslocamento temporal + substituição de identificadores + ausência dos PDFs originais), de forma que os dados deixem de ser considerados dados pessoais conforme o Art. 12 da LGPD — que prevê que dados anonimizados de forma irreversível saem do escopo da lei.

Em ambiente de produção, dentro da instituição de origem, os dados são tratados sob as bases legais aplicáveis ao serviço público de saúde.

---
