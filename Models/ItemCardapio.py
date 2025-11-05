# Models/ItemCardapio.py
class ItemCardapio:
    def __init__(self, id_item, descricao, sub_descricao, valor_unitario):
        self._id_item = id_item
        self._descricao = descricao
        self._sub_descricao = sub_descricao
        self._valor_unitario = valor_unitario

    # Getters
    def get_id_item(self):
        return self._id_item

    def get_descricao(self):
        return self._descricao

    def get_sub_descricao(self):
        return self._sub_descricao

    def get_valor_unitario(self):
        return self._valor_unitario

    # Setters
    def set_id_item(self, id_item):
        self._id_item = id_item

    def set_descricao(self, descricao):
        self._descricao = descricao

    def set_sub_descricao(self, sub_descricao):
        self._sub_descricao = sub_descricao

    def set_valor_unitario(self, valor):
        if valor < 0:
            raise ValueError("Valor unitário não pode ser negativo")
        self._valor_unitario = valor