# main.py
"""
SISTEMA DE GERENCIAMENTO DE RESTAURANTE
========================================
Aplicação web Streamlit para gerenciar todas as operações de um restaurante:
- Cadastro de clientes e funcionários
- Gerenciamento de mesas e cardápio
- Gestão completa de comandas (pedidos)

Estrutura do Projeto:
- Models/: Classes de dados (Cliente, Funcionario, Mesa, etc)
- Controllers/: Lógica de negócio e acesso ao banco de dados
- Views/: Interfaces do Streamlit (páginas da aplicação)

O aplicativo usa Streamlit para interface e SQLite para persistência de dados.
"""

import streamlit as st
import sys
from pathlib import Path
import importlib

# ===== 1. CONFIGURAÇÃO DA PÁGINA =====
# IMPORTANTE: st.set_page_config DEVE SER A PRIMEIRA CHAMADA DO STREAMLIT
st.set_page_config(
    page_title="Sistema de Restaurante",  # Título abas do navegador
    layout="wide",  # Layout amplo (não modal)
    initial_sidebar_state="auto"  # Sidebar visível por padrão
)

# ===== 2. ADICIONAR DIRETÓRIO RAIZ AO PATH DO PYTHON =====
# Isso permite que os módulos (Views, Controllers, Models) se encontrem
# sem problemas de importação relativa
sys.path.append(str(Path(__file__).parent))

# ===== 3. DICIONÁRIO DE PÁGINAS DISPONÍVEIS =====
# Mapeia o nome exibido no menu para o caminho do módulo View
# A chave é o nome no menu, o valor é o caminho do módulo
PAGES = {
    "Gestão de Comandas": "Views.PageComanda",
    "Cadastro de Funcionários": "Views.PageFuncionario",
    "Cadastro de Clientes": "Views.PageCliente",
    "Gerenciar Cardápio": "Views.PageCardapio",
    "Gerenciar Mesas": "Views.PageMesas",
}

# ===== 4. FUNÇÃO PARA CARREGAR PÁGINAS DINAMICAMENTE =====
def load_page(page_name):
    """
    Carrega um módulo de página dinamicamente com base na seleção do usuário.
    
    A função espera que cada módulo View tenha uma função nomeada como:
    'show_<nome_da_pagina>_page'
    
    Exemplos:
        'Views.PageCliente' -> procura por 'show_cliente_page()'
        'Views.PageComanda' -> procura por 'show_comanda_page()'
    
    Args:
        page_name (str): Nome da página selecionado (deve estar em PAGES)
        
    Returns:
        function: Função da página carregada, ou None se erro
    """
    try:
        # Extrai apenas o nome do módulo (última parte após 'Views.')
        module_name_simple = PAGES[page_name].split('.')[-1]
        
        # Converte o nome do módulo (ex: PageCliente) 
        # para o nome da função esperada (ex: show_cliente_page)
        # Remove 'Page' do início e converte para minúsculas
        page_func_name = f"show_{module_name_simple.replace('Page', '').lower()}_page"
        
        # Importa dinamicamente o módulo
        module = importlib.import_module(PAGES[page_name])
        
        # Obtém a função de renderização do módulo carregado
        return getattr(module, page_func_name)
    
    except (ImportError, AttributeError) as e:
        # Se houver erro, exibe mensagem ao usuário
        st.error(f"Erro ao carregar a página '{page_name}': {e}")
        st.warning("Verifique o nome do arquivo da View e da função 'show_..._page'.")
        return None

# ===== 5. FUNÇÃO PRINCIPAL (MAIN) =====
def main():
    """
    Função principal que renderiza a aplicação.
    Gerencia a navegação entre páginas e renderiza a página selecionada.
    """
    # Título principal da aplicação
    st.title('Sistema de Gerenciamento de Restaurante')
    
    # Cria sidebar com menu de navegação
    with st.sidebar:
        st.title("Menu de Navegação")
        # Selectbox com todas as páginas disponíveis
        page_selection = st.radio("Selecione uma Página", list(PAGES.keys()))
    
    # Linha horizontal para separação visual
    st.divider()
    
    # Carrega e renderiza a página selecionada
    show_page = load_page(page_selection)
    if show_page:
        show_page()  # Executa a função da página

# ===== 6. PONTO DE ENTRADA DO SCRIPT =====
# Executa a função main apenas se o arquivo for executado diretamente
# (não quando importado como módulo em outro arquivo)
if __name__ == "__main__":
    main()