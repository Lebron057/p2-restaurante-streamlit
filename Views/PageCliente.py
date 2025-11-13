# Views/PageCliente.py
"""
Página de Gerenciamento de Clientes.
Interface Streamlit para realizar operações CRUD (Criar, Ler, Atualizar, Deletar) de clientes.
"""

import streamlit as st
import pandas as pd
from Controllers.ClienteController import (
    incluir_cliente, 
    consultar_clientes, 
    excluir_cliente, 
    alterar_cliente
)
from Models.Cliente import Cliente

def show_cliente_page():
    """
    Função principal da página de clientes.
    Apresenta um menu lateral com opções de CRUD e renderiza a operação selecionada.
    """
    st.title("Cadastro de Clientes")

    # Menu lateral para selecionar operação
    operacao = st.sidebar.selectbox("Operações", ["Incluir", "Consultar", "Alterar", "Excluir"])

    # ===== OPERAÇÃO: INCLUIR =====
    if operacao == "Incluir":
        st.subheader("Incluir Novo Cliente")
        # Formulário para inserção de novo cliente
        with st.form(key="form_incluir_cliente"):
            cpf = st.text_input("CPF (apenas números):", max_chars=11)
            nome = st.text_input("Nome Completo:")
            telefone = st.text_input("Telefone (Ex: 11999998888):", max_chars=14)
            
            submit = st.form_submit_button("Cadastrar")
            if submit:
                if not cpf or not nome:
                    st.warning("Por favor, preencha CPF e Nome.")
                else:
                    try:
                        # Cria objeto Cliente e insere no banco
                        novo_cliente = Cliente(0, cpf, nome, telefone)
                        incluir_cliente(novo_cliente)
                        st.success(f"Cliente {nome} cadastrado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao cadastrar: {e}")

    # ===== OPERAÇÃO: CONSULTAR =====
    elif operacao == "Consultar":
        st.subheader("Clientes Cadastrados")
        dados = consultar_clientes()
        if dados:
            # Converte dados em DataFrame para exibição em tabela
            df = pd.DataFrame(dados, columns=["ID", "CPF", "Nome", "Telefone"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum cliente cadastrado.")

    # ===== OPERAÇÃO: ALTERAR =====
    elif operacao == "Alterar":
        st.subheader("Alterar Cliente")
        dados = consultar_clientes()
        if not dados:
            st.warning("Nenhum cliente para alterar.")
            return

        # Cria lista de labels para seleção (ID - Nome)
        df = pd.DataFrame(dados, columns=["ID", "CPF", "Nome", "Telefone"])
        labels = [f"{row['ID']} - {row['Nome']}" for index, row in df.iterrows()]
        
        selecao_label = st.selectbox("Selecione o cliente para alterar:", options=labels)
        if selecao_label:
            # Extrai o ID do label selecionado
            id_selecionado = int(selecao_label.split(" - ")[0])
            # Encontra os dados atuais do cliente
            dados_atuais = next((item for item in dados if item[0] == id_selecionado), None)
            
            with st.form(key="form_alterar_cliente"):
                cpf = st.text_input("CPF:", value=dados_atuais[1], max_chars=11)
                nome = st.text_input("Nome Completo:", value=dados_atuais[2])
                telefone = st.text_input("Telefone:", value=dados_atuais[3], max_chars=14)
                
                submit = st.form_submit_button("Salvar Alterações")
                if submit:
                    try:
                        # Cria objeto Cliente com dados alterados e atualiza
                        cliente_alterado = Cliente(id_selecionado, cpf, nome, telefone)
                        alterar_cliente(cliente_alterado)
                        st.success("Cliente alterado com sucesso!")
                        st.rerun()  # Recarrega a página para refletir mudanças
                    except Exception as e:
                        st.error(f"Erro ao alterar: {e}")

    # ===== OPERAÇÃO: EXCLUIR =====
    elif operacao == "Excluir":
        st.subheader("Excluir Cliente")
        dados = consultar_clientes()
        if not dados:
            st.warning("Nenhum cliente para excluir.")
            return
            
        df = pd.DataFrame(dados, columns=["ID", "CPF", "Nome", "Telefone"])
        labels = [f"{row['ID']} - {row['Nome']}" for index, row in df.iterrows()]
        
        selecao_label = st.selectbox("Selecione o cliente para excluir:", options=labels)
        
        if st.button("Excluir", type="primary"):
            try:
                id_selecionado = int(selecao_label.split(" - ")[0])
                excluir_cliente(id_selecionado)
                st.success("Cliente excluído com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao excluir. Verifique se o cliente está vinculado a uma comanda. Erro: {e}")