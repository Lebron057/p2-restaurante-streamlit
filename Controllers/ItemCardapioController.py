# Controllers/ItemCardapioController.py
import sqlite3
from Controllers.db_connection import conecta_bd
from Models.ItemCardapio import ItemCardapio

def incluir_item(item):
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