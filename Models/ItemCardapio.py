# Models/ItemCardapio.py
"""
Modelo da entidade ItemCardapio.
Representa um item disponível no cardápio do restaurante.
"""

class ItemCardapio:
    """
    Classe que modela um Item do Cardápio do sistema.
    
    Atributos:
        _id_item: Identificador único do item (chave primária)
        _descricao: Nome/descrição principal do item (ex: 'Frango Assado')
        _sub_descricao: Descrição adicional do item (ex: 'com batata frita')
        _valor_unitario: Preço do item em reais
    """
    
    def __init__(self, id_item, descricao, sub_descricao, valor_unitario):
        """Inicializa um novo item do cardápio."""
        self._id_item = id_item
        self._descricao = descricao
        self._sub_descricao = sub_descricao
        self._valor_unitario = valor_unitario

    # ===== GETTERS (Métodos para obter valores) =====
    def get_id_item(self):
        """Retorna o ID único do item."""
        return self._id_item

    def get_descricao(self):
        """Retorna a descrição principal do item."""
        return self._descricao

    def get_sub_descricao(self):
        """Retorna a sub-descrição (descrição adicional) do item."""
        return self._sub_descricao

    def get_valor_unitario(self):
        """Retorna o preço unitário do item."""
        return self._valor_unitario

    # ===== SETTERS (Métodos para atribuir/modificar valores) =====
    def set_id_item(self, id_item):
        """Define um novo ID para o item."""
        self._id_item = id_item

    def set_descricao(self, descricao):
        """Define uma nova descrição principal para o item."""
        self._descricao = descricao

    def set_sub_descricao(self, sub_descricao):
        """Define uma nova sub-descrição para o item."""
        self._sub_descricao = sub_descricao

    def set_valor_unitario(self, valor):
        """
        Define um novo preço para o item.
        Lança ValueError se o valor for negativo.
        """
        if valor < 0:
            raise ValueError("Valor unitário não pode ser negativo")
        self._valor_unitario = valor