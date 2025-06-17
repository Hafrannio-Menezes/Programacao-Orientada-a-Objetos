from classe_veiculo import Veiculo

class Bicicleta(Veiculo):
    def __init__(self, marca, modelo, tipo):
        super().__init__(marca, modelo)
        self.tipo = tipo

    def exibir_informacoes(self):
        return f'{super().exibir_informacoes()}, Tipo: {self.tipo}'
