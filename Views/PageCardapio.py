# Views/PageCardapio.py
"""
Página de Gerenciamento do Cardápio.
Interface Streamlit para realizar operações CRUD de itens do cardápio.
O cardápio é a lista de pratos/bebidas disponíveis no restaurante.
"""

import streamlit as st
import pandas as pd
from Controllers.ItemCardapioController import (
    incluir_item, 
    consultar_itens, 
    excluir_item, 
    alterar_item
)
from Models.ItemCardapio import ItemCardapio

def show_cardapio_page():
    """
    Função principal da página de cardápio.
    Permite gerenciar os itens disponíveis no restaurante.
    """
    st.title("Gerenciamento do Cardápio")

    operacao = st.sidebar.selectbox("Operações", ["Incluir", "Consultar", "Alterar", "Excluir"])

    # ===== OPERAÇÃO: INCLUIR =====
    if operacao == "Incluir":
        st.subheader("Incluir Novo Item no Cardápio")
        with st.form(key="form_incluir_item"):
            desc = st.text_input("Descrição do Item:")
            sub_desc = st.text_input("Sub-descrição (Opcional):")
            valor = st.number_input("Valor Unitário (R$):", min_value=0.0, format="%.2f")
            
            submit = st.form_submit_button("Cadastrar Item")
            if submit:
                if not desc or valor <= 0:
                    st.warning("Preencha a Descrição e um Valor Unitário válido.")
                else:
                    try:
                        novo_item = ItemCardapio(0, desc, sub_desc, valor)
                        incluir_item(novo_item)
                        st.success(f"Item '{desc}' cadastrado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao cadastrar: {e}")

    # ===== OPERAÇÃO: CONSULTAR =====
    elif operacao == "Consultar":
        st.subheader("Itens do Cardápio")
        dados = consultar_itens()
        if dados:
            df = pd.DataFrame(dados, columns=["ID", "Descrição", "Sub-descrição", "Valor (R$)"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum item cadastrado no cardápio.")

    # ===== OPERAÇÃO: ALTERAR =====
    elif operacao == "Alterar":
        st.subheader("Alterar Item do Cardápio")
        dados = consultar_itens()
        if not dados:
            st.warning("Nenhum item para alterar.")
            return

        df = pd.DataFrame(dados, columns=["ID", "Descrição", "Sub-descrição", "Valor (R$)"])
        labels = [f"{row['ID']} - {row['Descrição']}" for index, row in df.iterrows()]
        
        selecao_label = st.selectbox("Selecione o item para alterar:", options=labels)
        if selecao_label:
            id_selecionado = int(selecao_label.split(" - ")[0])
            dados_atuais = next((item for item in dados if item[0] == id_selecionado), None)
            
            with st.form(key="form_alterar_item"):
                desc = st.text_input("Descrição:", value=dados_atuais[1])
                sub_desc = st.text_input("Sub-descrição:", value=dados_atuais[2])
                valor = st.number_input("Valor Unitário (R$):", min_value=0.0, value=float(dados_atuais[3]), format="%.2f")
                
                submit = st.form_submit_button("Salvar Alterações")
                if submit:
                    try:
                        item_alterado = ItemCardapio(id_selecionado, desc, sub_desc, valor)
                        alterar_item(item_alterado)
                        st.success("Item alterado com sucesso!")
                        st.rerun() 
                    except Exception as e:
                        st.error(f"Erro ao alterar: {e}")

    # ===== OPERAÇÃO: EXCLUIR =====
    elif operacao == "Excluir":
        st.subheader("Excluir Item do Cardápio")
        dados = consultar_itens()
        if not dados:
            st.warning("Nenhum item para excluir.")
            return
            
        df = pd.DataFrame(dados, columns=["ID", "Descrição", "Sub-descrição", "Valor (R$)"])
        labels = [f"{row['ID']} - {row['Descrição']}" for index, row in df.iterrows()]
        
        selecao_label = st.selectbox("Selecione o item para excluir:", options=labels)
        
        if st.button("Excluir", type="primary"):
            try:
                id_selecionado = int(selecao_label.split(" - ")[0])
                excluir_item(id_selecionado)
                st.success("Item excluído com sucesso!")
                st.rerun() 
            except Exception as e:
                st.error(f"Erro ao excluir. Verifique se o item está em uma comanda. Erro: {e}")