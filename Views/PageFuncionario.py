# Views/PageFuncionario.py
import streamlit as st
import pandas as pd
from Controllers.FuncionarioController import (
    incluir_funcionario, 
    consultar_funcionarios, 
    excluir_funcionario, 
    alterar_funcionario
)
from Models.Funcionario import Funcionario

def show_funcionario_page():
    st.title("Cadastro de Funcionários")

    operacao = st.sidebar.selectbox("Operações", ["Incluir", "Consultar", "Alterar", "Excluir"])

    # --- INCLUIR ---
    if operacao == "Incluir":
        st.subheader("Incluir Novo Funcionário")
        with st.form(key="form_incluir_func"):
            cpf = st.text_input("CPF (apenas números):", max_chars=11)
            nome = st.text_input("Nome Completo:")
            
            submit = st.form_submit_button("Cadastrar")
            if submit:
                if not cpf or not nome:
                    st.warning("Por favor, preencha CPF e Nome.")
                else:
                    try:
                        novo_func = Funcionario(0, cpf, nome)
                        incluir_funcionario(novo_func)
                        st.success(f"Funcionário {nome} cadastrado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao cadastrar: {e}")

    # --- CONSULTAR ---
    elif operacao == "Consultar":
        st.subheader("Funcionários Cadastrados")
        dados = consultar_funcionarios()
        if dados:
            df = pd.DataFrame(dados, columns=["ID", "CPF", "Nome"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum funcionário cadastrado.")

    # --- ALTERAR ---
    elif operacao == "Alterar":
        st.subheader("Alterar Funcionário")
        dados = consultar_funcionarios()
        if not dados:
            st.warning("Nenhum funcionário para alterar.")
            return

        df = pd.DataFrame(dados, columns=["ID", "CPF", "Nome"])
        ids_funcionarios = [f"{row['ID']} - {row['Nome']}" for index, row in df.iterrows()]
        
        selecao_label = st.selectbox("Selecione o funcionário para alterar:", options=ids_funcionarios)
        if selecao_label:
            id_selecionado = int(selecao_label.split(" - ")[0])
            # Encontra os dados atuais do funcionário selecionado
            dados_atuais = next((item for item in dados if item[0] == id_selecionado), None)
            
            with st.form(key="form_alterar_func"):
                cpf = st.text_input("CPF:", value=dados_atuais[1], max_chars=11)
                nome = st.text_input("Nome Completo:", value=dados_atuais[2])
                
                submit = st.form_submit_button("Salvar Alterações")
                if submit:
                    try:
                        func_alterado = Funcionario(id_selecionado, cpf, nome)
                        alterar_funcionario(func_alterado)
                        st.success("Funcionário alterado com sucesso!")
                        st.rerun() 
                    except Exception as e:
                        st.error(f"Erro ao alterar: {e}")

    # --- EXCLUIR ---
    elif operacao == "Excluir":
        st.subheader("Excluir Funcionário")
        dados = consultar_funcionarios()
        if not dados:
            st.warning("Nenhum funcionário para excluir.")
            return
            
        df = pd.DataFrame(dados, columns=["ID", "CPF", "Nome"])
        ids_funcionarios = [f"{row['ID']} - {row['Nome']}" for index, row in df.iterrows()]
        
        selecao_label = st.selectbox("Selecione o funcionário para excluir:", options=ids_funcionarios)
        
        if st.button("Excluir", type="primary"):
            try:
                id_selecionado = int(selecao_label.split(" - ")[0])
                excluir_funcionario(id_selecionado)
                st.success("Funcionário excluído com sucesso!")
                st.rerun() # Atualiza a lista
            except Exception as e:
                st.error(f"Erro ao excluir. Verifique se o funcionário está vinculado a uma comanda. Erro: {e}")