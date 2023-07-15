# Outlet Mesha

Este é o programa Outlet Mesha que permite aos usuários fazer pedidos, consultar pedidos registrados e visualizar relatórios. O programa é desenvolvido em Python usando a biblioteca Streamlit e se integra a um banco de dados PostgreSQL.

## Pré-requisitos
Antes de executar o programa, certifique-se de ter as seguintes dependências instaladas:

1. __Python 3.x__
2. __PostgreSQL (ou outro banco de dados compatível)__
3.  __Bibliotecas Python: Streamlit, pandas, psycopg2, altair__
 


## Configuração do Banco de Dados
Certifique-se de ter um banco de dados PostgreSQL configurado e acessível. Você precisará fornecer as informações de conexão ao banco de dados no arquivo **service/database.py**. Certifique-se de ter as credenciais corretas para se conectar ao seu banco de dados.

## Instalação das Dependências

    1. Abra um terminal ou prompt de comando.
####
    2. Navegue até o diretório do projeto Outlet Mesha.
####
    3. Crie um ambiente virtual (opcional): 
__python -m venv venv__
####
    4. Ative o ambiente virtual (opcional): 
__Windows: venv\Scripts\activate__
####
    5.  Instale as dependências:
__pip install -r requirements.txt__
####
## Executando o Programa

    1. Certifique-se de ter o ambiente virtual ativado (se aplicável).
####

    2. No terminal ou prompt de comando, navegue até o diretório do projeto Outlet Mesha.
####    
    3. Execute o comando:
__streamlit run main.py__
####
    4. O programa será iniciado e estará disponível em seu navegador padrão.
####

    5.  Use o menu lateral para navegar entre as opções de fazer pedido, 
        consultar pedidos e relatórios. 

## Considerações finais

Sinta-se à vontade para adicionar mais detalhes, instruções de uso e qualquer outra informação relevante para os usuários.
