# main.py
import streamlit as st
import sys
from pathlib import Path
import importlib

# 1. Configuração da Página (Deve ser a primeira chamada do Streamlit)
st.set_page_config(
    page_title="Sistema de Restaurante", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# 2. Adicionar o diretório raiz ao path do Python
# Isso permite que os módulos (Views, Controllers, Models) se encontrem
sys.path.append(str(Path(__file__).parent))

# 3. Dicionário de páginas disponíveis
# A chave é o nome no menu, o valor é o caminho do módulo
PAGES = {
    "Gestão de Comandas": "Views.PageComanda",
    "Cadastro de Funcionários": "Views.PageFuncionario",
    "Cadastro de Clientes": "Views.PageCliente",
    "Gerenciar Cardápio": "Views.PageCardapio",
    "Gerenciar Mesas": "Views.PageMesas",
}

# 4. Função para carregar a página
def load_page(page_name):
    """
    Carrega um módulo de página dinamicamente com base na seleção.
    A função da view DEVE se chamar 'show_<nome_da_pagina>_page'
    Ex: 'Views.PageCliente' -> 'show_cliente_page()'
    """
    try:
        # Tira o 'Views.' do nome do módulo
        module_name_simple = PAGES[page_name].split('.')[-1]
        
        # Converte o nome do módulo (ex: PageCliente) 
        # para o nome da função (ex: show_cliente_page)
        page_func_name = f"show_{module_name_simple.replace('Page', '').lower()}_page"
        
        module = importlib.import_module(PAGES[page_name])
        
        # Obtém a função do módulo carregado
        return getattr(module, page_func_name)
    
    except (ImportError, AttributeError) as e:
        st.error(f"Erro ao carregar a página '{page_name}': {e}")
        st.warning("Verifique o nome do arquivo da View e da função 'show_..._page'.")
        return None

# 5. Função principal (main)
def main():
    st.title('Sistema de Gerenciamento de Restaurante')
    
    with st.sidebar:
        st.title("Menu de Navegação")
        page_selection = st.radio("Selecione uma Página", list(PAGES.keys()))
    
    st.divider() # Linha horizontal
    
    # Carrega e exibe a página selecionada
    show_page = load_page(page_selection)
    if show_page:
        show_page()

# 6. Ponto de entrada do script
if __name__ == "__main__":
    main()