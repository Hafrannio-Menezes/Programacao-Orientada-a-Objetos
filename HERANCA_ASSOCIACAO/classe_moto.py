from classe_veiculo import Veiculo

class Moto(Veiculo):
    def __init__(self, marca, modelo, cilindrada):
        super().__init__(marca, modelo)
        self.cilindrada = cilindrada

    def exibir_informacoes(self):
        return f'{super().exibir_informacoes()}, Cilindradas: {self.cilindrada}'
