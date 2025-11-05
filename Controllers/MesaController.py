# Controllers/MesaController.py
import sqlite3
from Controllers.db_connection import conecta_bd, get_db_connection
from Models.Mesa import Mesa

def incluir_mesa(mesa):
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO mesa (status, capacidade) VALUES (?, ?)
        """, (mesa.get_status(), mesa.get_capacidade()))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir mesa: {e}")
    finally:
        conexao.close()

def consultar_mesas():
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM mesa ORDER BY id_mesa")
        # (id, status, capacidade)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar mesas: {e}")
        return []
    finally:
        conexao.close()

def consultar_mesas_com_comanda():
    """Consulta mesas e, se estiver ocupada, a comanda associada."""
    conn = get_db_connection()
    try:
        query = """
            SELECT 
                m.id_mesa, 
                m.status, 
                m.capacidade,
                c.id_comanda
            FROM mesa m
            LEFT JOIN comanda c ON m.id_mesa = c.mesa_id AND c.horario_fechamento IS NULL
            ORDER BY m.id_mesa
        """
        return conn.execute(query).fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar mesas com comanda: {e}")
        return []
    finally:
        conn.close()

def excluir_mesa(id_mesa):
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM mesa WHERE id_mesa = ?", (id_mesa,))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao excluir mesa: {e}")
    finally:
        conexao.close()

def alterar_mesa(mesa):
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            UPDATE mesa SET status = ?, capacidade = ? WHERE id_mesa = ?
        """, (
            mesa.get_status(),
            mesa.get_capacidade(),
            mesa.get_id_mesa()
        ))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao alterar mesa: {e}")
    finally:
        conexao.close()

def alterar_status_mesa(id_mesa, novo_status):
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE mesa SET status = ? WHERE id_mesa = ?", 
            (novo_status, id_mesa)
        )
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao alterar status da mesa: {e}")
    finally:
        conexao.close()