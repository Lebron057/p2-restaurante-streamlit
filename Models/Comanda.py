# Models/Comanda.py
# Nota: Este modelo é mais complexo, pois representa a transação principal.
# Os itens da comanda (comanda_item_cardapio) serão gerenciados pelo Controller.

class Comanda:
    def __init__(self, id_comanda, funcionario_id, mesa_id, horario_abertura=None, 
                 horario_fechamento=None, taxa_servico=0.0, valor_total=0.0):
        
        self._id_comanda = id_comanda
        self._funcionario_id = funcionario_id
        self._mesa_id = mesa_id
        self._horario_abertura = horario_abertura
        self._horario_fechamento = horario_fechamento
        self._taxa_servico = taxa_servico
        self._valor_total = valor_total
        # self._itens = [] # Itens serão gerenciados no controller

    # Getters
    def get_id_comanda(self): return self._id_comanda
    def get_funcionario_id(self): return self._funcionario_id
    def get_mesa_id(self): return self._mesa_id
    def get_horario_abertura(self): return self._horario_abertura
    def get_horario_fechamento(self): return self._horario_fechamento
    def get_taxa_servico(self): return self._taxa_servico
    def get_valor_total(self): return self._valor_total

    # Setters
    def set_id_comanda(self, id_comanda): self._id_comanda = id_comanda
    def set_funcionario_id(self, fid): self._funcionario_id = fid
    def set_mesa_id(self, mid): self._mesa_id = mid
    def set_horario_fechamento(self, hf): self._horario_fechamento = hf
    def set_taxa_servico(self, taxa): self._taxa_servico = taxa
    def set_valor_total(self, total): self._valor_total = total