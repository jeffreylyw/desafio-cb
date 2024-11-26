# Desafio de Engenharia de Dados - Coco Bambu

Este repositório contém a solução para o Desafio de Engenharia de Dados, dividido em duas tarefas principais:

1. **Desafio 1**: Processamento e transformação de dados de um arquivo JSON para um banco de dados relacional.
2. **Desafio 2**: Consumo de APIs, armazenamento de dados no Google Cloud Storage (GCS) e organização de uma estrutura eficiente para manipulações futuras.

---

## Pré-requisitos

### Configuração do Ambiente
1. **Ferramentas Utilizadas**:
   - **Airflow**: Para orquestração das tarefas.
   - **PostgreSQL**: Para armazenar os dados relacionais no Desafio 1.
   - **Google Cloud Storage (GCS)**: Para armazenar os arquivos CSV gerados no Desafio 2.

2. **Credenciais Necessárias**:
   - **GCS**:
     - Configure a variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS` com o caminho para o arquivo de credenciais JSON.
     - Adicione a conexão `google_conn_default` no Airflow para integração com o GCS.
   - **PostgreSQL**:
     - Configure a conexão `postgres_conn_default` no Airflow.

3. **Observação Importante**:
   - **Bucket no GCS**:
     Embora o projeto tenha sido implementado com suporte ao GCS usando o `GoogleCloudStorageHook`, **não foi possível criar e testar o bucket devido às restrições de uso da plataforma paga**.
   - Apesar disso, o pipeline foi projetado para ser funcional em ambientes reais com o GCS configurado.

---

## Desafio 1 - Processamento de Dados do JSON

### Descrição
O objetivo deste desafio foi processar um arquivo **ERP.json**, contendo informações de pedidos, itens de menu e impostos, e transformá-lo em tabelas relacionais adequadas para um banco de dados.

### Implementação
1. **Extração de Dados**:
   - O arquivo JSON foi lido e os dados foram organizados em múltiplas tabelas:
     - `guest_checks`: Informações dos pedidos.
     - `taxes`: Detalhes dos impostos.
     - `detail_lines`: Detalhes dos itens dos pedidos.
     - `menu_items`: Detalhes dos itens do menu.

2. **Transformação**:
   - Os dados foram normalizados e tratados utilizando a biblioteca `pandas`.

3. **Carregamento no Banco de Dados**:
   - As tabelas geradas foram carregadas no PostgreSQL usando o `PostgresHook` do Airflow.

### Justificativas
- **Estrutura Relacional**:
  - A separação dos dados em tabelas normalizadas otimiza consultas futuras e facilita a análise de dados.
- **PostgreSQL**:
  - Foi escolhido por ser uma solução robusta, confiável e amplamente utilizada em produção.

### Como Executar
1. Certifique-se de que o PostgreSQL está configurado.
2. Coloque o arquivo `ERP.json` no diretório especificado no código.
3. Execute a DAG `erp_cb` na interface do Airflow.

---

## Desafio 2 - Consumo de APIs e Armazenamento no GCS

### Descrição
O segundo desafio consistiu em consumir 5 endpoints de APIs, processar as respostas e armazená-las no Google Cloud Storage (GCS) em formato CSV.

### Implementação
1. **Consumo de APIs**:
   - Através da biblioteca `requests`, os dados foram consumidos utilizando o payload padrão:
     ```json
     {
       "busDt": "2024-11-25",
       "storeId": "001"
     }
     ```

2. **Transformação dos Dados**:
   - As respostas JSON das APIs foram normalizadas utilizando `pandas` e convertidas em arquivos CSV.

3. **Armazenamento no GCS**:
   - Os arquivos CSV foram organizados no bucket em uma estrutura hierárquica:
     ```
     gs://cb_bucket/data_lake/<endpoint_name>/<busDt>/<storeId>.csv
     ```

4. **Automação com Airflow**:
   - Uma DAG foi configurada para consumir as APIs, transformar os dados e armazená-los no GCS.

### Justificativas
- **Organização no GCS**:
  - A estrutura hierárquica facilita buscas e análises futuras.
- **Formato CSV**:
  - Escolhemos CSV por ser amplamente suportado e por facilitar integrações com ferramentas de análise de dados.
- **Uso do Airflow**:
  - O Airflow foi escolhido para gerenciar e escalar o pipeline de maneira confiável.

### Como Executar
1. Configure as credenciais do GCS e do PostgreSQL no Airflow.
2. Certifique-se de que as conexões `google_conn_default` e `postgres_conn_default` estão configuradas.
3. Execute a DAG `api_cb_data_lake` na interface do Airflow.

---

## Considerações Finais

### Desafio 1
- **Impacto de Alterações no JSON**:
  - O código suporta mudanças limitadas no esquema do JSON. Alterações significativas, como renomeação de campos, exigirão ajustes no código de transformação.

### Desafio 2
- **Impacto de Alterações nas APIs**:
  - Alterações no esquema das APIs (ex.: renomeação de `taxes` para `taxation`) exigiriam atualizações na lógica de normalização.
- **Ambiente Real**:
  - Apesar de o GCS não ter sido configurado devido a limitações de acesso, o pipeline foi desenvolvido para funcionar plenamente em ambientes reais, desde que o bucket esteja configurado.
