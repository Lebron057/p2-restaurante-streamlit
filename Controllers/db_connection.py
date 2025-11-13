# Controllers/db_connection.py
"""
Módulo de conexão com banco de dados SQLite.
Fornece funções para estabelecer conexões com o banco de dados do restaurante.
"""

import sqlite3
from pathlib import Path

# ===== CONFIGURAÇÃO DO CAMINHO DO BANCO DE DADOS =====
# Constrói o caminho para o BD de forma robusta.
# Path(__file__) -> é o caminho deste arquivo (db_connection.py)
# .parent -> /.../projeto/Controllers
# .parent -> /.../projeto/ (esta é a raiz do projeto)
# / "restaurante.db" -> /.../projeto/restaurante.db
ROOT_DIR = Path(__file__).parent.parent
DB_NAME = ROOT_DIR / 'restaurante.db'

def conecta_bd():
    """
    Conecta ao banco de dados SQLite no caminho correto.
    
    Returns:
        sqlite3.Connection: Conexão com o banco de dados
        
    Raises:
        sqlite3.OperationalError: Se houver erro ao conectar ao banco
    """
    try:
        return sqlite3.connect(DB_NAME)
    except sqlite3.OperationalError as e:
        print(f"Erro ao conectar ao banco de dados em {DB_NAME}: {e}")
        # Isto pode indicar um problema de permissão ou caminho inválido
        raise

def get_db_connection():
    """
    Conecta ao banco de dados com modo dicionário ativado.
    O modo dicionário permite acessar as colunas pelo nome em vez de índice.
    
    Returns:
        sqlite3.Connection: Conexão com row_factory configurada
        
    Raises:
        sqlite3.OperationalError: Se houver erro ao obter a conexão
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        # row_factory transforma as linhas em objetos que permitem acesso por nome de coluna
        # Ex: row["id_cliente"] em vez de row[0]
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.OperationalError as e:
        print(f"Erro ao obter conexão (row_factory) ao banco {DB_NAME}: {e}")
        raise