# Models/Mesa.py
class Mesa:
    def __init__(self, id_mesa, status, capacidade):
        self._id_mesa = id_mesa
        self._status = status
        self._capacidade = capacidade

    # Getters
    def get_id_mesa(self):
        return self._id_mesa

    def get_status(self):
        return self._status

    def get_capacidade(self):
        return self._capacidade

    # Setters
    def set_id_mesa(self, id_mesa):
        self._id_mesa = id_mesa

    def set_status(self, status):
        if status not in ['livre', 'ocupada', 'reservada']:
            raise ValueError("Status inválido")
        self._status = status

    def set_capacidade(self, capacidade):
        self._capacidade = capacidade