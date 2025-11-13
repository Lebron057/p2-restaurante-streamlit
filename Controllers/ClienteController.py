# Controllers/ClienteController.py
"""
Controller para gerenciar operações CRUD de Clientes.
Realiza inserção, consulta, alteração e exclusão de clientes no banco de dados.
"""

import sqlite3
from Controllers.db_connection import conecta_bd
from Models.Cliente import Cliente

def incluir_cliente(cliente):
    """
    Insere um novo cliente no banco de dados.
    
    Args:
        cliente (Cliente): Objeto Cliente com os dados a serem inseridos
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO cliente (cpf, nome, telefone) VALUES (?, ?, ?)
        """, (cliente.get_cpf(), cliente.get_nome(), cliente.get_telefone()))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir cliente: {e}")
    finally:
        conexao.close()

def consultar_clientes():
    """
    Recupera todos os clientes cadastrados, ordenados por nome.
    
    Returns:
        list: Lista de tuplas (id, cpf, nome, telefone) ordenadas por nome
              Retorna lista vazia se houver erro
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM cliente ORDER BY nome")
        # Retorna lista de tuplas (id, cpf, nome, telefone)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar clientes: {e}")
        return []
    finally:
        conexao.close()

def excluir_cliente(id_cliente):
    """
    Remove um cliente do banco de dados pelo ID.
    
    Args:
        id_cliente (int): ID do cliente a ser removido
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM cliente WHERE id_cliente = ?", (id_cliente,))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao excluir cliente: {e}")
    finally:
        conexao.close()

def alterar_cliente(cliente):
    """
    Atualiza os dados de um cliente existente no banco de dados.
    
    Args:
        cliente (Cliente): Objeto Cliente com os novos dados (deve conter o id_cliente)
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            UPDATE cliente SET cpf = ?, nome = ?, telefone = ? WHERE id_cliente = ?
        """, (
            cliente.get_cpf(),
            cliente.get_nome(),
            cliente.get_telefone(),
            cliente.get_id_cliente()
        ))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao alterar cliente: {e}")
    finally:
        conexao.close()