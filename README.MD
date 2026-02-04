Este projeto implementa uma solução completa de **ELT (Extract, Load, Transform)** para o processamento e modelagem das demonstrações contábeis das operadoras de saúde suplementar (Dados Abertos da ANS).
Trade Off - estarão disponíveis e numerados de acordo com cada desafio ao final do read.me

# Pré-requisitos


-Python 3.8 + instalado.


-PostgreSQL configurado e rodando


-Node 24.12


# Clone o repositório


    git clone [git@github.com:KaiqueZiantoni/Analise-de-dados-ANS-Financas.git](git@github.com:KaiqueZiantoni/Analise-de-dados-ANS-Financas.git)


    cd Analise-de-dados-ANS-Financas


## Inicie o seu Ambiente Virtual (VENV):


**1. Crie o ambiente virtual:**


    python -m venv venv


**2. Ative seu ambiente virtual:**


(##Linux // Mac##)


    source venv/bin/activate 
    



ou


(## Windows ##)


    venv\Scripts\activate 
    
    



**3. Instale todas as dependências necessárias:**


    pip install -r .\requirements\requirements.txt


## Iniciando o projeto 


Após realizar o passo 1 (instalação dos pré requisitos)-->- [Clone o repositório](#clone-o-repositório)


**Inicialização**


Rode  o arquivo


    python3 main.py  
     
presente na raiz do projeto 



## Criar tabelas de banco de dados:
Com todos os arquivos CSV gerados (Ficarão disponíveis na pasta “Output” / raiz do projeto), iremos abrir o PostgreSQL (versão 8.0)

Executar os arquivos da pasta → *“Script PostgreSQL”* → *“script.sql”*.

Isso irá criar as tabelas necessárias para interpretação do banco de dados:

Feito isso, subiremos os dados para essas tabelas utilizando o arquivo **carga_dados.py**, presente na raiz do projeto, assim os dados selecionados estarão presentes nas tabelas respectivas.

    Ajuste sua conexão com chave e senha na variavel **engine = create_engine**

# Para filtrar as Querys no leitos de banco de dados:
Pasta: *“Script postgreSQL”* → Arquivo: *“script_querys_1_2_3.sql”*


- Query 1 - As 5 operadoras com maior crescimento percentual de despesas
- Query 2 - Os 5 estados com maiores despesas totais.
- Query 3 - Quais operadoras tiveram despesas acima da média geral

# Teste de API e interface WEB:
**Certifique-se de que a dependência está instalada** 

    pip install fastapi uvicorn sqlalchemy pandas psycopg2-binary

**configure o banco de dados**

Verifique a conexão no arquivo **ex4_1.py** (dentro da pasta script_ex4) 

    Ajuste sua conexão com chave e senha na variavel **engine = create_engine**

# Inicie o servidor:

No diretório 


    script_ex4 
    
    
execute o comando


     uvicorn ex4_1:app --reload


**Documentação Interativa (Swagger):** 
    O servidor estará rodando em:   
   
   
     http://127.0.0.1:8000/docs 


A interface web consome a API acima para exibir os dados. 
-Em um novo terminal, vá para a raiz e acesse a pasta do frontend: 
    
    
    cd frontend


-Instale as dependências: 
  
  
    npm install 


-Inicie a aplicação: 


    npm run dev 


-Acesse no navegador: 


    http://localhost:5173

# Tecnologias e dependências (Frameworks):
**Processamento de Dados (ETL):**


*Pandas e Numpy:* Manipulação, limpeza e análise estatística dos dados da ANS.


*BeautifulSoup4 e Requests:* Extração automatizada e web scraping dos arquivos no FTP/Site da ANS.


**API & Servidor (Backend):**


*FastAPI:* Framework moderno e assíncrono para a construção da API.


*Uvicorn:* Servidor ASGI de alta performance para rodar a aplicação.


*Pydantic:* Validação de dados e garantia de tipos (Type Safety).


**Banco de Dados:**


*SQLAlchemy:* ORM para abstração e comunicação com o banco.


*Psycopg2-binary:* Adaptador PostgreSQL para Python.


*MySQL-connector-python:* Suporte para integração com bancos MySQL (se aplicável).


**Infraestrutura e Tipagem:**


*Typing-extensions e Annotated-types:* Garantia de robustez do código e melhor experiência de desenvolvimento (DX).
# Decisões Técnicas e Trade-offs

**1. Requests + BeautifulSoup versus Selenium**

Para a tarefa de download de arquivos de um diretório aberto (Index of /FTP/...), escolhi a
integração entre requests e BeautifulSoup.


O Selenium é ótimo para interagir com páginas que utilizam bastante
JavaScript ou demandam cliques complexos, consome mais memória RAM e desacelera a execução, uma vez que precisa renderizar a página.


○​ Decisão: Como a página da ANS é estática (HTML simples listando arquivos), utilizar o Selenium seria um over-engineering (excesso de complexidade). A solução utilizando requests é mais simples, ágil e fácil de executar em qualquer servidor Linux sem interface gráfica.

**2. Lógica de "Busca Reversa"**

Escolhi listar os anos e organizá-los em ordem decrescente (reverse=True) antes de
repetir.
●​ Decisão: Confiar na data do sistema pode causar problemas caso a ANS não envie a publicação de um arquivo. Ao ler o HTML da página

**3 .Escolha: Processamento Incremental (Chunking)**


Prós:


Escalabilidade: o sistema não trava ao processar arquivos de qualquer tamanho.


Consumo Baixo de RAM: mantém o uso da memória estável e sob controle.


Resiliência: possibilita a continuidade ou monitoramento parcial do processamento.


Desvantagens:


Complexidade: o código requer lógica de iteração e métodos de "append" no banco de dados.


Tempo total: pode ser um pouco mais lento do que o processamento em memória devido às várias operações de leitura e escrita.


Tratamento de Inconsistências (Data Cleaning)

**1. CNPJs duplicados com Razões Sociais diferentes**

Tratamento: Prioridade por atualização e frequência. Preservei a ligação do CNPJ com a Razão Social mais atual ou mais recorrente na base.


Justificativa: Assegura a integridade referencial no banco de dados, prevenindo que uma única entidade seja apresentada como duas empresas diferentes em relatórios.

**2. Valores zerados ou negativos**


Tratamento: Manutenção com sinalização (Zero-filling). Valores zerados foram preservados; valores negativos foram transformados em zero ou nulos, conforme a norma contábil do campo.


Justificativa: Valores zerados podem ser reais (sem movimentação), porém negativos em campos de "valor absoluto" sinalizam um erro de input que afetaria os cálculos de soma e média.

**3. Trimestres com formatos de data inconsistentes**


Tratamento: padronização por meio do Datetime. Desenvolvemos uma função de parsing para transformar strings (como "1T2023", "01/2023", "2023-Q1") no formato padrão YYYY-MM-DD (primeiro dia do trimestre).


Justificativa: A normalização temporal é essencial para habilitar filtros de séries históricas e garantir a ordenação cronológica adequada no SQL.
Quarentena e Log de Erros (Isolamento de Dados)
Para este projeto, a abordagem escolhida foi o isolamento em quarentena ,em vez de simplesmente excluir ou tentar corrigir os CNPJs inválidos.


Prós:
Integridade: Garante que apenas dados válidos entrem no banco de dados evitando erros de relacionamento e buscas inconsistentes.


Auditabilidade: Mantém uma trilha de auditoria (arquivo de log) que permite identificar quais operadoras enviaram dados malformados.


Recuperação: Permite que dados importantes não sejam perdidos definitivamente; eles podem ser corrigidos e reimportados após análise manual.


Contras:
Complexidade de Pipeline: Exige a criação de um fluxo extra de saída para os registros rejeitados.


- Gestão de Dados: Cria a necessidade de gerenciar um volume adicional de "lixo eletrônico" ou dados pendentes.


Escolha: FastAPI + SQLAlchemy + Pydantic


Prós:
Desempenho: FastAPI é um dos frameworks Python mais rápidos (baseado em Starlette), perfeito para gerenciar várias solicitações de consulta aos dados da ANS.


Segurança de Dados: O Pydantic assegura que os dados que entram e saem da API estejam no formato adequado, evitando os erros de tipo frequentemente encontrados em Python.


Documentação Automática: O FastAPI cria automaticamente o Swagger (/docs), o que simplifica testes rápidos sem a necessidade de ferramentas externas.


Contras:
Configuração Inicial: O setup inicial do boilerplate (FastAPI + ORM + Migrations) é um pouco mais trabalhoso do que em frameworks "micro" como o Flask.
- Ordenação via Banco de Dados (SQL ORDER BY)
Prós:


Eficiência de Memória: Delegamos a ordenação ao motor do banco de dados, que é otimizado para gerenciar grandes volumes sem estourar a memória RAM da aplicação Python.


Uso de Índices: Ao criar índices nas colunas de ordenação (como o registro da operadora ou data), a busca se torna quase instantânea.


Escalabilidade: Funciona de forma consistente independentemente do tamanho da base, utilizando o disco se necessário (External Merge Sort).


Contras:


Carga no Banco: Transfere o esforço computacional do script para o servidor de banco de dados.


Dependência de Schema: Exige que os índices estejam bem configurados para não gerar lentidão em inserções 
- Normalização do Banco de Dados


Escolha: Opção B (Tabelas Normalizadas)


Prós:


Integridade: Evita redundância (ex: repetir o nome da operadora em cada linha de despesa).


Performance de Escrita: Atualizações cadastrais são feitas em um só lugar.


Economia de Espaço: Reduz drasticamente o peso total do banco ao usar chaves estrangeiras (FKs).


Contras:


Complexidade: Exige o uso de JOINs para consultas analíticas.


Justificativa: Dado o alto volume de dados, a desnormalização geraria um desperdício imenso de disco e memória. A normalização garante que o banco cresça de 

forma sustentável e organizada.


# Trade-off: Tipos de Dados


**1. Valores Monetários**


Escolha: DECIMAL (15,2)


Prós: precisão absoluta em ponto fixo. Ao contrário do FLOAT, não apresenta problemas de arredondamento binário.


Contras: ligeiramente mais lento em operações matemáticas do que o INTEGER.


Justificativa: A precisão é imprescindível em sistemas financeiros e contábeis, como os da ANS. Centavos não podem "desaparecer" devido a falhas de precisão de ponto flutuante.


**Datas**


Escolha: DATE


Prós: Ocupa menos espaço, valida automaticamente o formato e permite funções nativas de tempo (ex: extrair ano/mês).


Contras: Não armazena hora/minuto (o que não é necessário para despesas trimestrais).


Justificativa: O tipo DATE é superior ao VARCHAR por permitir ordenação cronológica nativa e filtros de período performáticos no SQL.
Tratamento de Inconsistências na Importação


**Encoding (UTF-8)**


Abordagem: Conversão forçada de ISO-8859-1 (comum nos arquivos ANS) para UTF-8 durante a leitura no Pandas.


Justificativa: Evitar erros de inserção no banco de dados devido a caracteres especiais e garantir a portabilidade do sistema em diferentes ambientes (Docker, Linux, Windows).


**Valores NULL em campos obrigatórios**


Abordagem: Rejeitar (Quarentena). Linhas com campos chave vazios (ex: Registro ANS, Valor, Trimestre) foram desviadas para um log de erros.


Justificativa: Dados obrigatórios faltantes inviabilizam a análise. Usar valores padrão (como zero) poderia gerar conclusões erradas sobre o faturamento ou despesas das operadoras.


**Strings em campos numéricos**


Abordagem: Tentar conversão (Coerce). Utilizamos a função de conversão para numérico forçando erros para NaN. Registros não convertíveis foram movidos para a Quarentena.


Justificativa: Garante que a coluna no SQL receba apenas valores válidos para cálculos, isolando registros "sujos" que continham textos onde deveriam estar valores monetários.


**Datas em formatos inconsistentes**


Abordagem: Normalização. Uso de algoritmos de parsing flexíveis para converter diversos formatos (DD/MM/YYYY, YYYY-MM-DD) para o padrão ISO.


Justificativa: A padronização é essencial para permitir que o banco de dados realize filtros de data e ordenação cronológica de forma nativa e performática.



# Front-end


**React vs Vue:** 

Apesar do teste indicar Vue, escolhi React por ter um conhecimento mais avançado da ferramenta, assegurando uma entrega com código mais organizado, componentização adequada e gerenciamento de estados (Hooks) mais eficaz.


**Busca no Servidor (Server-side):** 

Escolhi executar a busca/filtro no backend em vez de fazê-lo no frontend. Como trabalhamos com dados paginados, filtrar apenas a "página atual" no front-end seria inadequado. A pesquisa no servidor assegura que examinamos todo o banco de dados.


**CSS Modules vs Styled Components:** 


Optei por CSS Modules para preservar a simplicidade e evitar o overhead de runtime das bibliotecas CSS-in-JS, mantendo o estilo próximo ao componente, porém em arquivos distintos.

---
Desenvolvido por [Kaique Ziantoni Guedes Rosa](https://www.linkedin.com/in/kaiqueziantoni/)
