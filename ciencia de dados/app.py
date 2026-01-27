import streamlit as st
import mysql.connector
import pandas as pd


# 1. Configuração de conexão
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="sakila"
    )


st.title("📂 Explorador de Tabelas Sakila")

try:
    conn = conectar()

    # 2. Buscar nomes de todas as tabelas existentes no banco
    query_tabelas = "SHOW TABLES"
    tabelas_df = pd.read_sql(query_tabelas, conn)
    lista_tabelas = tabelas_df.iloc[:, 0].tolist()  # Transforma a coluna em uma lista

    # 3. Criar um seletor (Selectbox) no menu lateral
    tabela_selecionada = st.sidebar.selectbox("Selecione uma tabela", lista_tabelas)

    if tabela_selecionada:
        st.subheader(f"Visualizando dados da tabela: {tabela_selecionada}")

        # 4. Carregar os dados da tabela escolhida
        query_dados = f"SELECT * FROM {tabela_selecionada} LIMIT 100"
        df = pd.read_sql(query_dados, conn)

        # 5. Mostrar na tela
        st.write(f"Mostrando as primeiras 100 linhas de {len(df)} carregadas.")
        st.dataframe(df, use_container_width=True)

    conn.close()

except Exception as e:
    st.error(f"Erro ao conectar ao MySQL: {e}")