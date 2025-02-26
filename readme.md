# Desafio de Engenharia de Dados

Este repositório contém a solução para o Desafio de Engenharia de Dados, dividido em duas tarefas principais:

1. **Desafio 1**: Processamento e transformação de dados de um arquivo JSON para um banco de dados relacional.
2. **Desafio 2**: Consumo de APIs, armazenamento de dados em um Data Lake, o escolhido para esse projeto foi o Google Cloud Storage (GCS), e organização de uma estrutura eficiente para manipulações futuras.

---

## Pré-requisitos

### Configuração do Ambiente
1. **Ferramentas Utilizadas**:
   - **Airflow**: Para orquestração das tarefas.
   - **PostgreSQL**: Para armazenar os dados relacionais no Desafio 1.
   - **Google Cloud Storage (GCS)**: Para armazenar os arquivos `.csv` gerados no Desafio 2.
   - **Python e Pandas**: Para a manipulação de Dataframes e sintaxe do Apache Airflow.

2. **Credenciais Necessárias**:
   - **GCS**:
     - Configure a variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS` com o caminho para o arquivo de credenciais JSON.
     - Adicione a conexão `google_conn_default` no Airflow para integração com o GCS.
   - **PostgreSQL**:
     - Configure a conexão `postgres_conn_default` no Airflow.

3. **Observação Importante**:
   - **Bucket no GCS**:
     Embora o projeto tenha sido implementado com suporte ao GCS usando o `GCSHook`, **não foi possível criar e testar o bucket devido às restrições de uso da plataforma paga**.
   - Apesar disso, o pipeline foi projetado para ser funcional em ambientes reais com o GCS configurado.

---

## Instalação do Apache Airflow

Siga os passos abaixo para configurar e rodar o Apache Airflow localmente usando Docker.

### 1. Configuração do usuário do Airflow
   - **Para usuários Linux**:
     Execute o seguinte comando para configurar corretamente o usuário do Airflow:
     ```bash
     echo -e "AIRFLOW_UID=$(id -u)" > .env
     ```

   - **Para outros sistemas operacionais**:
     Crie um arquivo `.env` na mesma pasta onde está o arquivo `docker-compose.yaml` e insira o seguinte conteúdo:
     ```
     AIRFLOW_UID=50000
     ```

### 2. Inicializar o banco de dados do Airflow
   Execute o comando abaixo para inicializar o banco de dados do Airflow:
   ```bash
   docker-compose up airflow-init
   ```

### 3. Iniciar os serviços do Airflow
   Após inicializar o banco de dados, inicie todos os serviços do Airflow com o comando:
   ```bash
   docker-compose up
   ```

Agora o Airflow estará rodando.

### 4. Acessar a interface do Airflow
   Para acessar a interface do Airflow, abra o navegador e acesse:
   [http://localhost:8080](http://localhost:8080)

   - **Usuário**: airflow  
   - **Senha**: airflow

---

## Desafio 1 - Processamento de Dados do JSON

### Descrição
O objetivo deste desafio foi processar um arquivo **ERP.json**, contendo informações de pedidos, itens de menu e impostos, e transformá-lo em tabelas relacionais adequadas para um banco de dados fazendo sentido para operações de restaurante.

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
#### Por que separar o JSON em tabelas relacionais?
A separação foi feita para organizar os dados de maneira lógica, evitar redundâncias e facilitar consultas futuras. Essa abordagem normalizada melhora o desempenho e a escalabilidade.

#### Estrutura das Tabelas
1. **`guest_checks`**: Armazena informações básicas dos pedidos, como ID do pedido, data e valor total. Essencial para análises operacionais.
2. **`taxes`**: Detalhes sobre impostos aplicados a cada pedido. Facilita auditorias fiscais.
3. **`detail_lines`**: Linhas de detalhe de cada pedido, incluindo itens, quantidades e preços. Crucial para controle de estoque e vendas.
4. **`menu_items`**: Informações dos itens do menu, como preços e impostos associados. Útil para atualizações e análises de desempenho do menu.

#### Por que PostgreSQL?
Escolhi PostgreSQL por sua confiabilidade, suporte a SQL avançado e facilidade de integração com pipelines e ferramentas de BI, além de fácil instalação.

#### Benefícios da Normalização
- Reduz redundâncias e melhora a manutenção.
- Suporta mudanças no esquema do JSON com ajustes mínimos.
- Facilita análises específicas, como controle de estoque e impostos.

#### Como isso atende às necessidades de um restaurante?
A estrutura permite:
- Rastrear vendas por pedido e item.
- Gerar relatórios fiscais e operacionais.
- Escalar para múltiplas lojas de forma centralizada.

### Como Executar
1. Certifique-se de que o PostgreSQL está configurado.
2. Coloque o arquivo `ERP.json` no diretório especificado no código.
3. Execute a DAG `erp_cb` na interface do Airflow.

---

## Desafio 2 - Consumo de APIs e Armazenamento no GCS

### Descrição
O segundo desafio consistiu em consumir 5 endpoints de APIs, processar as respostas e armazená-las em um Data Lake.

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
   - As respostas JSON das APIs foram normalizadas utilizando `pandas` e convertidas em arquivos `.csv`.

3. **Armazenamento no GCS**:
   - Os arquivos `.csv` foram organizados no bucket em uma estrutura hierárquica:
     ```
     gs://cb_bucket/data_lake/<endpoint_name>/<busDt>/<storeId>.csv
     ```

4. **Automação com Airflow**:
   - Uma DAG foi configurada para consumir as APIs, transformar os dados e armazená-los no GCS.

### Justificativas
- **Organização no GCS**:
  - A estrutura hierárquica facilita buscas e análises futuras.
- **Formato CSV**:
  - Escolhi o arquivo `.csv` por ser amplamente suportado e por facilitar integrações com ferramentas de análise de dados como também pela sua simplicidade de uso, de ler e manipular.
- **Uso do Airflow**:
  - O Airflow foi escolhido para orquestrar e escalar o pipeline de maneira confiável.

### Como Executar
1. Configure as credenciais do GCS no Airflow.
2. Certifique-se de que a conexão `google_conn_default` está configurada.
3. Execute a DAG `api_cb_data_lake` na interface do Airflow.

---

## Considerações Finais

### Desafio 1
- **Impacto de Alterações no JSON**:
  - O código suporta mudanças limitadas no esquema do JSON. Alterações significativas, como renomeação de campos, exigirão ajustes no código de transformação.

### Desafio 2
- **Impacto de Alterações nas APIs**:
  - Alterações no esquema das APIs (como pontuado no arquivo `.pdf` do desafio: renomeação de `taxes` para `taxation`) exigiriam atualizações na lógica de normalização.
- **Ambiente Real**:
  - Apesar de o GCS não ter sido configurado devido a limitações de acesso, o pipeline foi desenvolvido para funcionar plenamente em ambientes reais de produção, desde que o bucket esteja configurado, como também a URI base das API's que se encontra no arquivo `config.py`.
