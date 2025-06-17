from classe_veiculo import Veiculo

class Carro(Veiculo):
    def __init__(self, marca, modelo, portas):
        super().__init__(marca, modelo)
        self.portas = portas

    def exibir_informacoes(self):
        return f'{super().exibir_informacoes()}, Portas: {self.portas}'
