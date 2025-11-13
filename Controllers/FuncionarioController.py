# Controllers/FuncionarioController.py
"""
Controller para gerenciar operações CRUD de Funcionários.
Realiza inserção, consulta, alteração e exclusão de funcionários no banco de dados.
"""

import sqlite3
from Controllers.db_connection import conecta_bd
from Models.Funcionario import Funcionario

def incluir_funcionario(funcionario):
    """
    Insere um novo funcionário no banco de dados.
    
    Args:
        funcionario (Funcionario): Objeto Funcionario com os dados a serem inseridos
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO funcionario (cpf, nome) VALUES (?, ?)
        """, (funcionario.get_cpf(), funcionario.get_nome()))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir funcionário: {e}")
    finally:
        conexao.close()

def consultar_funcionarios():
    """
    Recupera todos os funcionários cadastrados, ordenados por nome.
    
    Returns:
        list: Lista de tuplas (id, cpf, nome) ordenadas por nome
              Retorna lista vazia se houver erro
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM funcionario ORDER BY nome")
        # Retorna lista de tuplas (id, cpf, nome)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar funcionários: {e}")
        return []
    finally:
        conexao.close()

def excluir_funcionario(id_funcionario):
    """
    Remove um funcionário do banco de dados pelo ID.
    
    Args:
        id_funcionario (int): ID do funcionário a ser removido
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM funcionario WHERE id_funcionario = ?", (id_funcionario,))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao excluir funcionário: {e}")
    finally:
        conexao.close()

def alterar_funcionario(funcionario):
    """
    Atualiza os dados de um funcionário existente no banco de dados.
    
    Args:
        funcionario (Funcionario): Objeto Funcionario com os novos dados (deve conter o id_funcionario)
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            UPDATE funcionario SET cpf = ?, nome = ? WHERE id_funcionario = ?
        """, (
            funcionario.get_cpf(),
            funcionario.get_nome(),
            funcionario.get_id_funcionario()
        ))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao alterar funcionário: {e}")
    finally:
        conexao.close()