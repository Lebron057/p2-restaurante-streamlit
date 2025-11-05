# Services/database.py
import sqlite3
from pathlib import Path

# Constrói o caminho para o BD no diretório raiz (um nível acima de 'Services')
ROOT_DIR = Path(__file__).parent.parent
DB_PATH = ROOT_DIR / 'restaurante.db'

def create_database():
    """
    Cria o banco de dados 'restaurante.db' na raiz do projeto
    e todas as tabelas.
    """
    try:
        # Conecta ao BD no caminho correto
        conexao = sqlite3.connect(DB_PATH) 
        cursor = conexao.cursor()
        
        # Tabela funcionario
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionario (
            id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf VARCHAR(11) NOT NULL,
            nome VARCHAR(255) NOT NULL
        );
        """)

        # Tabela cliente
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf VARCHAR(11) NOT NULL,
            nome VARCHAR(255),
            telefone VARCHAR(14)
        );
        """)

        # Tabela item_cardapio
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS item_cardapio (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao VARCHAR(100) NOT NULL,
            sub_descricao VARCHAR(255),
            valor_unitario REAL NOT NULL CHECK (valor_unitario >= 0)
        );
        """)

        # Tabela mesa
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS mesa (
            id_mesa INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL DEFAULT 'livre' CHECK(status IN ('livre', 'ocupada', 'reservada')),
            capacidade INTEGER
        );
        """)

        # Tabela comanda (com a correção DATETIME)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comanda (
            id_comanda INTEGER PRIMARY KEY AUTOINCREMENT,
            taxa_servico REAL,
            horario_fechamento DATETIME,
            horario_abertura DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            valor_total REAL,
            funcionario_id INT NOT NULL,
            mesa_id INT NOT NULL,
            FOREIGN KEY (funcionario_id) REFERENCES funcionario(id_funcionario),
            FOREIGN KEY (mesa_id) REFERENCES mesa(id_mesa)
        );
        """)

        # Tabela comanda_item_cardapio (Tabela de Junção)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comanda_item_cardapio (
            id_comanda_item_cardapio INTEGER PRIMARY KEY AUTOINCREMENT,
            horario_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
            valor_unitario_momento REAL NOT NULL,
            quantidade_item INT NOT NULL,
            comanda_id INT NOT NULL,
            item_cardapio_id INT NOT NULL,
            FOREIGN KEY (comanda_id) REFERENCES comanda(id_comanda),
            FOREIGN KEY (item_cardapio_id) REFERENCES item_cardapio(id_item)
        );
        """)

        # Tabela comanda_cliente (Tabela de Junção)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comanda_cliente (
            id_comanda_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            valor_pago REAL NOT NULL,
            cliente_id INT NOT NULL,
            comanda_id INT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES cliente(id_cliente),
            FOREIGN KEY (comanda_id) REFERENCES comanda(id_comanda)
        );
        """)

        conexao.commit()
        print(f"Banco de dados '{DB_PATH}' e tabelas criados com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
        if conexao:
            conexao.close()

if __name__ == "__main__":
    create_database()