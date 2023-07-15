import streamlit as st
import service.database as db
import pandas as pd
import altair as alt


def main():
    # Página inicial com o menu lateral
    st.sidebar.title('Menu')
    page_cliente = st.sidebar.selectbox('Outlet', ['Fazer pedido', 'Consultar pedidos', 'Relatórios'])

    # Página "Fazer pedido"
    if page_cliente == "Fazer pedido":
        st.image(logo_image, width=100)
        st.title("Outlet Mesha - Realizar pedido")

        # Dicionário com os produtos disponíveis e seus respectivos preços
        produtos = {
            "Camiseta": 29.90,
            "Calça": 79.90,
            "Tênis": 99.90,
            "Boné": 27.90,
            "Terno": 174.99
        }

        # Formulário para realizar o pedido
        with st.form(key="processa_pedido"):
            input_name = st.text_input(label="Insira o seu nome")
            input_products = st.multiselect(label="Escolha seu produto", options=list(produtos.keys()))
            input_quantidade = st.number_input(label="Insira a quantidade", format="%d", step=1)
            input_button_submit = st.form_submit_button("Enviar")

        # Validações
        if input_button_submit:
            if input_name == "":
                st.error("Por favor, insira o seu nome.")
            elif input_quantidade < 0:
                st.error("A quantidade deve ser maior que zero.")
            elif input_quantidade == 0:
                st.error("Por favor, insira a quantidade.")
            else:
                # Calcular o valor total do pedido
                total = 0.0
                for product in input_products:
                    valor_unitario = produtos[product]
                    total += valor_unitario * input_quantidade

                # Inserir o pedido no banco de dados
                db_insert(input_name, input_products, input_quantidade, total)
                st.success("Pedido feito com sucesso!")

    # Página Consultar pedidos
    elif page_cliente == 'Consultar pedidos':
        st.image(logo_image, width=100)
        st.title("Outlet Mesha - Consultar pedido")

        # Obter os pedidos registrados no banco de dados
        costumer_list = db_SelectAll()

        # Criar um DataFrame com os dados dos pedidos
        df = pd.DataFrame(costumer_list, columns=['Nome', 'Produto', 'Quantidade', 'Total', 'Data'])

        # Formatar a coluna 'Total' para exibir o valor com 2 casas decimais e adicionar o símbolo 'R$'
        df['Total'] = df['Total'].apply(lambda x: f'R$ {x:.2f}')

        # Exibir a tabela com os pedidos
        st.table(df)

        # Adicionar o botão de exportação
        csv_export = df.to_csv(index=False).encode('utf-8')
        st.download_button("Exportar como CSV", data=csv_export, file_name='pedidos.csv', mime='text/csv')

    # Página "Relatórios"
    elif page_cliente == "Relatórios":
        st.image(logo_image, width=100)
        st.title('Outlet Mesha - Relatórios')

        # Obter todos os pedidos registrados no banco de dados
        relatorio_list = db_SelectAll()

        # Criar um DataFrame com os dados dos pedidos
        df = pd.DataFrame(relatorio_list, columns=['Nome', 'Produto', 'Quantidade', 'Total', 'Data'])

        # Selecionar a métrica desejada
        metrica = st.selectbox("Selecione a métrica",
                               ["Geral", "Venda mais alta", "Produto mais vendido", "Produto menos vendido"])

        if metrica == "Geral":
            # Criar o gráfico de barras
            chart = alt.Chart(df).mark_bar(size=35).encode(
                x=alt.X('Data', title='Data'),
                y=alt.Y('Quantidade', title='Quantidade'),
                color='Quantidade:Q',
                tooltip=['Data', 'Quantidade']
            )

            st.altair_chart(chart, use_container_width=True)

        elif metrica == "Venda mais alta":
            # Encontrar a venda mais alta
            venda_mais_alta = df['Total'].max()

            # Filtrar os dados para incluir apenas a venda mais alta
            filtered_data = df[df['Total'] == venda_mais_alta]

            # Criar gráfico de barras da venda mais alta
            chart = alt.Chart(filtered_data).mark_bar().encode(
                x=alt.X('Produto', title='Produto'),
                y=alt.Y('Total', title='Total'),
                tooltip=['Produto', 'Total', 'Nome']
            )

            # Exibir o gráfico
            st.altair_chart(chart, use_container_width=True)

        elif metrica == "Produto mais vendido":
            # Contar a quantidade de vendas para cada produto
            produtos_contagem = df['Produto'].value_counts()

            # Puxar o produto com a maior contagem
            # O método idxmax é do pandas ele puxa o maior índice em um dataframe
            produto_mais_vendido = produtos_contagem.idxmax()

            # Filtrar o DataFrame para exibir apenas as vendas do produto mais vendido
            filtro_produto_mais_vendido = df['Produto'] == produto_mais_vendido
            vendas_produto_mais_vendido = df[filtro_produto_mais_vendido]

            # Exibir o gráfico de barras do produto mais vendido com a quantidade
            st.bar_chart(vendas_produto_mais_vendido[['Produto', 'Quantidade']])

        elif metrica == "Produto menos vendido":
            # Contar a quantidade de vendas para cada produto
            produtos_contagem = df['Produto'].value_counts()

            # Puxar o produto com a menor contagem
            # O método idxmin é do pandas ele puxa o menor índice em um dataframe
            produto_menos_vendido = produtos_contagem.idxmin()

            # Filtrar o DataFrame para exibir apenas as vendas do produto menos vendido
            filtro_produto_menos_vendido = df['Produto'] == produto_menos_vendido
            vendas_produto_menos_vendido = df[filtro_produto_menos_vendido]

            # Exibir o gráfico de barras do produto menos vendido com a quantidade
            st.bar_chart(vendas_produto_menos_vendido[['Produto', 'Quantidade']])

        else:
            pass


def db_insert(nome, produtos, quantidade, total):
    cursor = db.conn.cursor()  # Cria um cursor para executar comandos SQL
    # Executa o comando SQL para inserir os valores na tabela 'mesha'
    cursor.execute("INSERT INTO mesha (nome, produto, quantidade, total) VALUES(%s, %s, %s, %s)",
                   (nome, ", ".join(produtos), quantidade, total))
    db.conn.commit()  # Confirma a transação no banco de dados


def db_SelectAll():
    cursor = db.conn.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute("SELECT * FROM mesha ORDER BY data DESC")
    rows = cursor.fetchall()  # Recupera todos os registros retornados pelo comando SQL
    all_list = []  # Cria uma lista vazia para armazenar os resultados

    # Percorre cada registro retornado e extrai as colunas 'nome', 'produto', 'quantidade', 'total' e 'data'
    for row in rows:
        nome = row[1]
        produto = row[2]
        quantidade = row[3]
        total = row[4]
        data = row[5]
        all_list.append((nome, produto, quantidade, total, data))  # Adiciona os valores extraídos à lista

    return all_list  # Retorna a lista contendo todos os registros selecionados do banco de dados


if __name__ == "__main__":
    logo_image = 'meshalogo.png'
    main()
