# Views/PageComanda.py
import streamlit as st
import pandas as pd
from Controllers.MesaController import consultar_mesas_com_comanda
from Controllers.FuncionarioController import consultar_funcionarios
from Controllers.ItemCardapioController import consultar_itens
from Controllers.ComandaController import (
    abrir_comanda, 
    adicionar_item_comanda, 
    consultar_itens_comanda,
    calcular_total_comanda,
    fechar_comanda
)

def format_func_dict(options_dict):
    """Função para formatar labels de selectbox a partir de um dicionário."""
    return lambda x: options_dict[x]

def show_comanda_page():
    st.title("👨‍🍳 Gestão de Comandas")

    operacao = st.sidebar.selectbox(
        "Operações de Comanda", 
        ["Abrir Comanda", "Gerenciar Comanda Aberta", "Fechar Comanda"]
    )

    # --- ABRIR COMANDA ---
    if operacao == "Abrir Comanda":
        st.subheader("Abrir Nova Comanda")
        
        # Carregar dados
        mesas_livres = [m for m in consultar_mesas_com_comanda() if m["status"] == 'livre']
        funcionarios_data = consultar_funcionarios()

        if not mesas_livres:
            st.warning("Todas as mesas estão ocupadas. Libere uma mesa para abrir uma nova comanda.")
            return
        if not funcionarios_data:
            st.warning("Cadastre funcionários antes de abrir uma comanda.")
            return

        # Dicionários para formatar selectbox
        mesas_options = {m["id_mesa"]: f"Mesa {m['id_mesa']} (Cap: {m['capacidade']})" for m in mesas_livres}
        func_options = {f[0]: f[2] for f in funcionarios_data}

        with st.form(key="form_abrir_comanda"):
            st.write("Selecione a Mesa e o Funcionário:")
            col1, col2 = st.columns(2)
            with col1:
                id_mesa = st.selectbox("Mesa:", options=list(mesas_options.keys()), format_func=format_func_dict(mesas_options))
            with col2:
                id_func = st.selectbox("Funcionário:", options=list(func_options.keys()), format_func=format_func_dict(func_options))
            
            submit = st.form_submit_button("Abrir Comanda")
            if submit:
                try:
                    novo_id = abrir_comanda(id_func, id_mesa)
                    if novo_id:
                        st.success(f"Comanda {novo_id} aberta para a Mesa {id_mesa}!")
                        st.info("Vá para 'Gerenciar Comanda Aberta' para adicionar itens.")
                        st.rerun()
                    else:
                        st.error("Erro ao abrir comanda.")
                except Exception as e:
                    st.error(f"Erro: {e}")

    # --- GERENCIAR COMANDA ABERTA (ADICIONAR ITENS) ---
    elif operacao == "Gerenciar Comanda Aberta":
        st.subheader("Gerenciar Comanda Aberta")
        
        # 1. Selecionar a comanda aberta
        mesas_ocupadas = [m for m in consultar_mesas_com_comanda() if m["status"] == 'ocupada' and m["id_comanda"] is not None]
        if not mesas_ocupadas:
            st.info("Nenhuma comanda aberta no momento.")
            return
        
        comanda_options = {m["id_comanda"]: f"Comanda {m['id_comanda']} (Mesa {m['id_mesa']})" for m in mesas_ocupadas}
        id_comanda_selecionada = st.selectbox(
            "Selecione a Comanda:", 
            options=list(comanda_options.keys()), 
            format_func=format_func_dict(comanda_options)
        )
        
        if id_comanda_selecionada:
            st.markdown("---")
            
            # 2. Adicionar itens a essa comanda
            itens_cardapio_data = consultar_itens()
            if not itens_cardapio_data:
                st.warning("Nenhum item cadastrado no cardápio.")
                return
            
            item_options = {i[0]: f"{i[1]} - R$ {i[3]:.2f}" for i in itens_cardapio_data}
            
            with st.form(key="form_add_item"):
                st.write(f"**Adicionar Itens à Comanda {id_comanda_selecionada}**")
                col1, col2 = st.columns([3, 1])
                with col1:
                    id_item = st.selectbox("Item do Cardápio:", options=list(item_options.keys()), format_func=format_func_dict(item_options))
                with col2:
                    qtd = st.number_input("Qtd:", min_value=1, step=1)
                
                submit_item = st.form_submit_button("Adicionar Item")
                if submit_item:
                    try:
                        if adicionar_item_comanda(id_comanda_selecionada, id_item, qtd):
                            st.success(f"{qtd}x '{item_options[id_item].split(' - ')[0]}' adicionado(s).")
                        else:
                            st.error("Erro ao adicionar item.")
                    except Exception as e:
                        st.error(f"Erro: {e}")

            # 3. Mostrar itens já adicionados
            st.markdown("---")
            st.write("**Itens na Comanda:**")
            itens_na_comanda = consultar_itens_comanda(id_comanda_selecionada)
            
            if itens_na_comanda:
                df_itens = pd.DataFrame(
                    [dict(row) for row in itens_na_comanda], 
                    columns=["descricao", "quantidade_item", "valor_unitario_momento", "valor_total_item"]
                )
                df_itens.columns = ["Item", "Qtd", "Vl. Unit.", "Total Item"]
                st.dataframe(df_itens, use_container_width=True, hide_index=True)
                
                # 4. Mostrar total parcial
                totais = calcular_total_comanda(id_comanda_selecionada)
                if totais:
                    st.metric(
                        label="Total Parcial (c/ 10% serviço)", 
                        value=f"R$ {totais['valor_total']:.2f}"
                    )
            else:
                st.info("Nenhum item adicionado a esta comanda ainda.")

    # --- FECHAR COMANDA ---
    elif operacao == "Fechar Comanda":
        st.subheader("Fechar Comanda e Pagar")
        
        mesas_ocupadas = [m for m in consultar_mesas_com_comanda() if m["status"] == 'ocupada' and m["id_comanda"] is not None]
        if not mesas_ocupadas:
            st.info("Nenhuma comanda aberta para fechar.")
            return

        comanda_options = {m["id_comanda"]: f"Comanda {m['id_comanda']} (Mesa {m['id_mesa']})" for m in mesas_ocupadas}
        id_comanda_selecionada = st.selectbox(
            "Selecione a Comanda para fechar:", 
            options=list(comanda_options.keys()), 
            format_func=format_func_dict(comanda_options)
        )
        
        if id_comanda_selecionada:
            st.markdown("---")
            st.write("**Resumo da Conta:**")
            
            # Mostrar itens
            itens_na_comanda = consultar_itens_comanda(id_comanda_selecionada)
            if itens_na_comanda:
                df_itens = pd.DataFrame(
                    [dict(row) for row in itens_na_comanda], 
                    columns=["descricao", "quantidade_item", "valor_total_item"]
                )
                df_itens.columns = ["Item", "Qtd", "Total Item"]
                st.dataframe(df_itens, use_container_width=True, hide_index=True)
                
                # Calcular e mostrar totais
                totais = calcular_total_comanda(id_comanda_selecionada)
                if totais:
                    st.write(f"**Subtotal:** R$ {totais['subtotal']:.2f}")
                    st.write(f"**Taxa de Serviço (10%):** R$ {totais['taxa_servico_valor']:.2f}")
                    st.header(f"**Valor Total:** R$ {totais['valor_total']:.2f}")
                    
                    st.markdown("---")
                    
                    if st.button("Confirmar Pagamento e Fechar Comanda", type="primary"):
                        try:
                            if fechar_comanda(id_comanda_selecionada):
                                st.success(f"Comanda {id_comanda_selecionada} fechada com sucesso!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("Erro ao fechar comanda.")
                        except Exception as e:
                            st.error(f"Erro: {e}")
            else:
                st.warning("Esta comanda está vazia. Não é possível fechar.")