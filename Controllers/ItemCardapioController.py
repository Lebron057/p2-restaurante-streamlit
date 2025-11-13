# Controllers/ItemCardapioController.py
"""
Controller para gerenciar operações CRUD de Itens do Cardápio.
Realiza inserção, consulta, alteração e exclusão de itens no banco de dados.
"""

import sqlite3
from Controllers.db_connection import conecta_bd
from Models.ItemCardapio import ItemCardapio

def incluir_item(item):
    """
    Insere um novo item no cardápio do banco de dados.
    
    Args:
        item (ItemCardapio): Objeto ItemCardapio com os dados a serem inseridos
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO item_cardapio (descricao, sub_descricao, valor_unitario) 
            VALUES (?, ?, ?)
        """, (
            item.get_descricao(), 
            item.get_sub_descricao(), 
            item.get_valor_unitario()
        ))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir item: {e}")
    finally:
        conexao.close()

def consultar_itens():
    """
    Recupera todos os itens do cardápio, ordenados por descrição.
    
    Returns:
        list: Lista de tuplas (id, descricao, sub_descricao, valor_unitario) ordenadas por descrição
              Retorna lista vazia se houver erro
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM item_cardapio ORDER BY descricao")
        # (id, desc, sub_desc, valor)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar itens: {e}")
        return []
    finally:
        conexao.close()

def excluir_item(id_item):
    """
    Remove um item do cardápio do banco de dados pelo ID.
    
    Args:
        id_item (int): ID do item a ser removido
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM item_cardapio WHERE id_item = ?", (id_item,))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao excluir item: {e}")
    finally:
        conexao.close()

def alterar_item(item):
    """
    Atualiza os dados de um item existente no cardápio do banco de dados.
    
    Args:
        item (ItemCardapio): Objeto ItemCardapio com os novos dados (deve conter o id_item)
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            UPDATE item_cardapio 
            SET descricao = ?, sub_descricao = ?, valor_unitario = ? 
            WHERE id_item = ?
        """, (
            item.get_descricao(),
            item.get_sub_descricao(),
            item.get_valor_unitario(),
            item.get_id_item()
        ))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao alterar item: {e}")
    finally:
        conexao.close()