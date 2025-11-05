# Controllers/ClienteController.py
import sqlite3
from Controllers.db_connection import conecta_bd
from Models.Cliente import Cliente

def incluir_cliente(cliente):
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