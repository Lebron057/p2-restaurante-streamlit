# Controllers/db_connection.py
import sqlite3
from pathlib import Path

# Constrói o caminho para o BD de forma robusta.
# Path(__file__) -> é o caminho deste arquivo (db_connection.py)
# .parent -> /.../projeto/Controllers
# .parent -> /.../projeto/ (esta é a raiz)
# / "restaurante.db" -> /.../projeto/restaurante.db
ROOT_DIR = Path(__file__).parent.parent
DB_NAME = ROOT_DIR / 'restaurante.db'

def conecta_bd():
    """Conecta ao banco de dados SQLite no caminho correto."""
    try:
        return sqlite3.connect(DB_NAME)
    except sqlite3.OperationalError as e:
        print(f"Erro ao conectar ao banco de dados em {DB_NAME}: {e}")
        # Isso pode indicar um problema de permissão ou caminho
        raise

def get_db_connection():
    """Conecta ao banco e ativa o modo de dicionário."""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.OperationalError as e:
        print(f"Erro ao obter conexão (row_factory) ao banco {DB_NAME}: {e}")
        raise