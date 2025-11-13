# Controllers/ComandaController.py
"""
Controller para gerenciar operações de Comandas.
Uma comanda representa o pedido de um cliente em uma mesa.
Operações principais: abrir, adicionar itens, calcular total, fechar.
"""

import sqlite3
from Controllers.db_connection import conecta_bd, get_db_connection
from Controllers.MesaController import alterar_status_mesa
from datetime import datetime

def abrir_comanda(funcionario_id, mesa_id):
    """
    Cria uma nova comanda e atualiza o status da mesa para ocupada.
    
    Args:
        funcionario_id (int): ID do funcionário que abre a comanda
        mesa_id (int): ID da mesa onde a comanda será aberta
        
    Returns:
        int: ID da comanda criada, ou None se houve erro
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        # Registra o horário atual de abertura
        horario_abertura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insere a nova comanda com taxa de serviço padrão de 10%
        cursor.execute("""
            INSERT INTO comanda (funcionario_id, mesa_id, horario_abertura, taxa_servico)
            VALUES (?, ?, ?, ?)
        """, (funcionario_id, mesa_id, horario_abertura, 10.0)) # Taxa de 10% por padrão
        
        # Obtém o ID da comanda recém-criada
        id_comanda = cursor.lastrowid
        conexao.commit()
        
        # Atualiza o status da mesa para 'ocupada'
        alterar_status_mesa(mesa_id, 'ocupada')
        
        print(f"Comanda {id_comanda} aberta para mesa {mesa_id}")
        return id_comanda
    except sqlite3.Error as e:
        print(f"Erro ao abrir comanda: {e}")
        conexao.rollback()
        return None
    finally:
        conexao.close()

def adicionar_item_comanda(comanda_id, item_cardapio_id, quantidade):
    """
    Adiciona um item do cardápio a uma comanda aberta.
    Registra o valor unitário do item no momento da adição (importante para histórico de preços).
    
    Args:
        comanda_id (int): ID da comanda à qual adicionar o item
        item_cardapio_id (int): ID do item do cardápio
        quantidade (int): Quantidade do item a adicionar
        
    Returns:
        bool: True se sucesso, False se erro
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        # 1. Buscar o valor unitário atual do item
        cursor.execute(
            "SELECT valor_unitario FROM item_cardapio WHERE id_item = ?",
            (item_cardapio_id,)
        )
        resultado = cursor.fetchone()
        if not resultado:
            raise ValueError("Item de cardápio não encontrado")
        
        valor_unitario_momento = resultado[0]
        
        # 2. Inserir na tabela de junção (comanda_item_cardapio)
        # O valor_unitario_momento é armazenado para manter o histórico de preços
        cursor.execute("""
            INSERT INTO comanda_item_cardapio 
            (comanda_id, item_cardapio_id, quantidade_item, valor_unitario_momento)
            VALUES (?, ?, ?, ?)
        """, (comanda_id, item_cardapio_id, quantidade, valor_unitario_momento))
        
        conexao.commit()
        print(f"Item {item_cardapio_id} adicionado à comanda {comanda_id}")
        return True
    except (sqlite3.Error, ValueError) as e:
        print(f"Erro ao adicionar item à comanda: {e}")
        conexao.rollback()
        return False
    finally:
        conexao.close()

def consultar_itens_comanda(comanda_id):
    """
    Consulta todos os itens de uma comanda com seus detalhes completos.
    Faz JOIN com a tabela de item_cardapio para obter descrições.
    
    Args:
        comanda_id (int): ID da comanda
        
    Returns:
        list: Lista de dicts com: id_comanda_item_cardapio, descricao, quantidade_item, 
              valor_unitario_momento, valor_total_item
              Retorna lista vazia se erro
    """
    conn = get_db_connection()
    try:
        query = """
            SELECT 
                cic.id_comanda_item_cardapio,
                ic.descricao,
                cic.quantidade_item,
                cic.valor_unitario_momento,
                (cic.quantidade_item * cic.valor_unitario_momento) AS valor_total_item
            FROM comanda_item_cardapio cic
            JOIN item_cardapio ic ON cic.item_cardapio_id = ic.id_item
            WHERE cic.comanda_id = ?
        """
        return conn.execute(query, (comanda_id,)).fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar itens da comanda: {e}")
        return []
    finally:
        conn.close()

def calcular_total_comanda(comanda_id):
    """
    Calcula o subtotal dos itens, a taxa de serviço e o valor total de uma comanda.
    
    Args:
        comanda_id (int): ID da comanda
        
    Returns:
        dict: Dicionário com:
            - subtotal: soma dos (quantidade * valor_unitario) de todos os itens
            - taxa_servico_valor: valor calculado da taxa em reais
            - valor_total: subtotal + taxa_servico_valor
            - id_mesa: ID da mesa associada à comanda
              Retorna None se erro
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 1. Calcular subtotal dos itens (soma de quantidade * valor)
        cursor.execute("""
            SELECT SUM(quantidade_item * valor_unitario_momento) 
            FROM comanda_item_cardapio
            WHERE comanda_id = ?
        """, (comanda_id,))
        subtotal_result = cursor.fetchone()
        subtotal = subtotal_result[0] if subtotal_result[0] else 0.0

        # 2. Obter taxa de serviço (ex: 10.0 para 10%) e mesa_id
        cursor.execute(
            "SELECT taxa_servico, mesa_id FROM comanda WHERE id_comanda = ?", 
            (comanda_id,)
        )
        comanda_info = cursor.fetchone()
        taxa_percentual = comanda_info["taxa_servico"] if comanda_info else 0.0
        id_mesa = comanda_info["mesa_id"] if comanda_info else None

        # 3. Calcular valor da taxa e total final
        valor_taxa = (subtotal * taxa_percentual) / 100
        valor_total = subtotal + valor_taxa
        
        return {
            "subtotal": subtotal,
            "taxa_servico_valor": valor_taxa,
            "valor_total": valor_total,
            "id_mesa": id_mesa
        }

    except sqlite3.Error as e:
        print(f"Erro ao calcular total: {e}")
        return None
    finally:
        conn.close()

def fechar_comanda(comanda_id):
    """
    Fecha uma comanda aberta, calculando e registrando o valor total final.
    Também libera a mesa, marcando-a como 'livre'.
    
    Args:
        comanda_id (int): ID da comanda a fechar
        
    Returns:
        bool: True se sucesso, False se erro
    """
    conexao = conecta_bd()
    cursor = conexao.cursor()
    try:
        # 1. Calcular o total final
        totais = calcular_total_comanda(comanda_id)
        if not totais:
            raise Exception("Não foi possível calcular o total da comanda.")

        valor_total_final = totais['valor_total']
        id_mesa = totais['id_mesa']
        
        # 2. Atualizar a comanda com o total e o horário de fechamento
        horario_fechamento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            UPDATE comanda
            SET valor_total = ?, horario_fechamento = ?
            WHERE id_comanda = ?
        """, (valor_total_final, horario_fechamento, comanda_id))
        
        conexao.commit()

        # 3. Liberar a mesa
        if id_mesa:
            alterar_status_mesa(id_mesa, 'livre')
            
        print(f"Comanda {comanda_id} fechada. Mesa {id_mesa} livre.")
        return True
    except Exception as e:
        print(f"Erro ao fechar comanda: {e}")
        conexao.rollback()
        return False
    finally:
        conexao.close()