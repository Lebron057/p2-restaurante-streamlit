# Views/PageMesas.py
"""
Página de Gerenciamento de Mesas.
Interface Streamlit para gerenciar as mesas do restaurante.
Permite criar, consultar, alterar e deletar mesas.
Também controla o status das mesas (livre, ocupada, reservada).
"""

import streamlit as st
import pandas as pd
from Controllers.MesaController import (
    incluir_mesa, 
    consultar_mesas, 
    excluir_mesa, 
    alterar_mesa
)
from Models.Mesa import Mesa

def show_mesas_page():
    """
    Função principal da página de mesas.
    Gerencia o cadastro e status das mesas do restaurante.
    """
    st.title("Gerenciamento de Mesas")

    operacao = st.sidebar.selectbox("Operações", ["Incluir", "Consultar", "Alterar", "Excluir"])

    # ===== OPERAÇÃO: INCLUIR =====
    if operacao == "Incluir":
        st.subheader("Adicionar Nova Mesa")
        with st.form(key="form_incluir_mesa"):
            capacidade = st.number_input("Capacidade da Mesa:", min_value=1, step=1)
            # Novas mesas são sempre criadas com status 'livre' por padrão
            
            submit = st.form_submit_button("Adicionar Mesa")
            if submit:
                try:
                    nova_mesa = Mesa(0, 'livre', capacidade)
                    incluir_mesa(nova_mesa)
                    st.success(f"Mesa com capacidade {capacidade} adicionada!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar: {e}")

    # ===== OPERAÇÃO: CONSULTAR =====
    elif operacao == "Consultar":
        st.subheader("Status das Mesas")
        dados = consultar_mesas()
        if dados:
            df = pd.DataFrame(dados, columns=["ID da Mesa", "Status", "Capacidade"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma mesa cadastrada.")

    # ===== OPERAÇÃO: ALTERAR =====
    elif operacao == "Alterar":
        st.subheader("Alterar Mesa")
        dados = consultar_mesas()
        if not dados:
            st.warning("Nenhuma mesa para alterar.")
            return

        df = pd.DataFrame(dados, columns=["ID", "Status", "Capacidade"])
        labels = [f"Mesa {row['ID']} (Cap: {row['Capacidade']})" for index, row in df.iterrows()]
        
        selecao_label = st.selectbox("Selecione a mesa para alterar:", options=labels)
        if selecao_label:
            id_selecionado = int(selecao_label.split(" ")[1])
            dados_atuais = next((item for item in dados if item[0] == id_selecionado), None)
            
            with st.form(key="form_alterar_mesa"):
                capacidade = st.number_input(
                    "Capacidade:", 
                    min_value=1, 
                    value=dados_atuais[2], 
                    step=1
                )
                # Permite alterar o status da mesa
                status = st.selectbox(
                    "Status:", 
                    options=['livre', 'ocupada', 'reservada'], 
                    index=['livre', 'ocupada', 'reservada'].index(dados_atuais[1])
                )
                
                submit = st.form_submit_button("Salvar Alterações")
                if submit:
                    try:
                        mesa_alterada = Mesa(id_selecionado, status, capacidade)
                        alterar_mesa(mesa_alterada)
                        st.success("Mesa alterada com sucesso!")
                        st.rerun() 
                    except Exception as e:
                        st.error(f"Erro ao alterar: {e}")

    # ===== OPERAÇÃO: EXCLUIR =====
    elif operacao == "Excluir":
        st.subheader("Excluir Mesa")
        # Apenas mesas com status 'livre' podem ser excluídas
        # Mesas ocupadas ou reservadas não devem ser removidas
        dados = [m for m in consultar_mesas() if m[1] == 'livre']
        if not dados:
            st.warning("Nenhuma mesa 'livre' disponível para exclusão.")
            return
            
        df = pd.DataFrame(dados, columns=["ID", "Status", "Capacidade"])
        labels = [f"Mesa {row['ID']} (Cap: {row['Capacidade']})" for index, row in df.iterrows()]
        
        selecao_label = st.selectbox("Selecione a mesa (livre) para excluir:", options=labels)
        
        if st.button("Excluir", type="primary"):
            try:
                id_selecionado = int(selecao_label.split(" ")[1])
                excluir_mesa(id_selecionado)
                st.success("Mesa excluída com sucesso!")
                st.rerun() 
            except Exception as e:
                st.error(f"Erro ao excluir: {e}")