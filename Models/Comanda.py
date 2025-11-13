# Models/Comanda.py
"""
Modelo da entidade Comanda.
Representa uma conta/pedido de um cliente no restaurante.
Nota: Os itens da comanda são gerenciados através de uma tabela de junção (comanda_item_cardapio).
"""

class Comanda:
    """
    Classe que modela uma Comanda do sistema.
    Uma comanda representa o pedido de um cliente em uma mesa específica.
    
    Atributos:
        _id_comanda: Identificador único da comanda (chave primária)
        _funcionario_id: ID do funcionário que atende (chave estrangeira)
        _mesa_id: ID da mesa onde o cliente está (chave estrangeira)
        _horario_abertura: Data/hora de quando a comanda foi aberta
        _horario_fechamento: Data/hora de quando a comanda foi fechada/paga
        _taxa_servico: Taxa de serviço em percentual (ex: 10.0 = 10%)
        _valor_total: Valor final da comanda (incluindo taxa)
    """
    
    def __init__(self, id_comanda, funcionario_id, mesa_id, horario_abertura=None, 
                 horario_fechamento=None, taxa_servico=0.0, valor_total=0.0):
        """Inicializa uma nova comanda com seus dados."""
        self._id_comanda = id_comanda
        self._funcionario_id = funcionario_id
        self._mesa_id = mesa_id
        self._horario_abertura = horario_abertura
        self._horario_fechamento = horario_fechamento
        self._taxa_servico = taxa_servico
        self._valor_total = valor_total
        # Nota: Os itens da comanda são armazenados em uma tabela de junção
        # (comanda_item_cardapio) e gerenciados pelo ComandaController

    # ===== GETTERS (Métodos para obter valores) =====
    
    def get_id_comanda(self):
        """Retorna o ID único da comanda."""
        return self._id_comanda
    
    def get_funcionario_id(self):
        """Retorna o ID do funcionário que atende esta comanda."""
        return self._funcionario_id
    
    def get_mesa_id(self):
        """Retorna o ID da mesa onde a comanda está."""
        return self._mesa_id
    
    def get_horario_abertura(self):
        """Retorna o horário de abertura da comanda (data/hora)."""
        return self._horario_abertura
    
    def get_horario_fechamento(self):
        """Retorna o horário de fechamento da comanda (data/hora)."""
        return self._horario_fechamento
    
    def get_taxa_servico(self):
        """Retorna a taxa de serviço em percentual (ex: 10.0 para 10%)."""
        return self._taxa_servico
    
    def get_valor_total(self):
        """Retorna o valor total final da comanda (com taxa incluída)."""
        return self._valor_total

    # ===== SETTERS (Métodos para atribuir/modificar valores) =====
    
    def set_id_comanda(self, id_comanda):
        """Define um novo ID para a comanda."""
        self._id_comanda = id_comanda
    
    def set_funcionario_id(self, fid):
        """Define um novo funcionário para atender esta comanda."""
        self._funcionario_id = fid
    
    def set_mesa_id(self, mid):
        """Define uma nova mesa para esta comanda."""
        self._mesa_id = mid
    
    def set_horario_fechamento(self, hf):
        """Define o horário de fechamento da comanda."""
        self._horario_fechamento = hf
    
    def set_taxa_servico(self, taxa):
        """Define a taxa de serviço em percentual."""
        self._taxa_servico = taxa
    
    def set_valor_total(self, total):
        """Define o valor total final da comanda."""
        self._valor_total = total