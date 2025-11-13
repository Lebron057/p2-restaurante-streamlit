# Controllers/MesaController.py
"""
Controller para gerenciar operações CRUD de Mesas.
Realiza inserção, consulta, alteração e exclusão de mesas no banco de dados.
Também gerencia o status (livre/ocupada/reservada) das mesas.
"""

import sqlite3
from Controllers.db_connection import conecta_bd, get_db_connection
from Models.Mesa import Mesa

def incluir_mesa(mesa):
    """
    Insere uma nova mesa no banco de dados.
    
    Args:
        mesa (Mesa): Objeto Mesa com os dados a serem inseridos
    """
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
    """
    Recupera todas as mesas cadastradas, ordenadas por ID.
    
    Returns:
        list: Lista de tuplas (id, status, capacidade) ordenadas por id
              Retorna lista vazia se houver erro
    """
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
    """
    Consulta mesas e, se estiverem ocupadas, a comanda aberta associada.
    Usa LEFT JOIN para trazer também as mesas sem comanda ativa.
    
    Returns:
        list: Lista de dicts com {id_mesa, status, capacidade, id_comanda}
              Retorna lista vazia se houver erro
    """
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
    """
    Remove uma mesa do banco de dados pelo ID.
    
    Args:
        id_mesa (int): ID da mesa a ser removida
    """
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
    """
    Atualiza os dados de uma mesa existente no banco de dados.
    
    Args:
        mesa (Mesa): Objeto Mesa com os novos dados (deve conter o id_mesa)
    """
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
    """
    Altera apenas o status de uma mesa (sem modificar capacidade).
    Usado principalmente para mudanças de status (livre -> ocupada -> livre).
    
    Args:
        id_mesa (int): ID da mesa a ser atualizada
        novo_status (str): Novo status ('livre', 'ocupada' ou 'reservada')
    """
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