import json
import os
from classe_carro import Carro
from classe_bicicleta import Bicicleta
from classe_moto import Moto

ARQUIVO_JSON = "veiculos.json"

def criar_linha_tabela(colunas, tamanhos, numero=None):
    linha = "│" if numero is None else f"{numero:2d} │"
    for i, (coluna, tamanho) in enumerate(zip(colunas, tamanhos)):
        linha += f" {coluna:<{tamanho}} │"
    return linha.rstrip()

def criar_linha_separadora(tamanhos, tipo="meio", com_numero=False):
    if tipo == "topo":
        left, mid, right, sep = "┌", "┬", "┐", "─"
    elif tipo == "base":
        left, mid, right, sep = "└", "┴", "┘", "─"
    else:  #isso aqi vai no meio ( só para n esqecer pq refiz isso aqi mais de horas)
        left, mid, right, sep = "├", "┼", "┤", "─"
    #agradeço ao Tiago Caceraghi por ter ensinado isso a um tempo atrás...
    linha = ""
    if com_numero:
        linha = left + "─" * 3 + mid
    else:
        linha = left
    
    for i, tamanho in enumerate(tamanhos):
        linha += sep * (tamanho + 2)
        linha += right if i == len(tamanhos) - 1 else mid
    return linha

def criar_cabecalho(tamanhos):
    return criar_linha_separadora(tamanhos, "topo")

def obter_tamanhos_colunas(veiculos, tipo="todos"):
    tamanhos = {
        "tipo": 4,
        "marca": 5,
        "modelo": 6, 
        "detalhes": 8
    }
    
    for v in veiculos:
        tamanhos["tipo"] = max(tamanhos["tipo"], len(v["tipo"]))
        tamanhos["marca"] = max(tamanhos["marca"], len(v["marca"]))
        tamanhos["modelo"] = max(tamanhos["modelo"], len(v["modelo"]))
        if v["tipo"] == "Carro":
            detalhes = f"Portas: {v['portas']}"
        elif v["tipo"] == "Moto":
            detalhes = f"Cilindradas: {v['cilindrada']}"
        else:
            detalhes = f"Tipo: {v['tipo_bicicleta']}"
        tamanhos["detalhes"] = max(tamanhos["detalhes"], len(detalhes))
    
    return [tamanhos["tipo"], tamanhos["marca"], tamanhos["modelo"], tamanhos["detalhes"]]

def carregar_veiculos():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_veiculo(veiculo):
    veiculos = carregar_veiculos()
    veiculos.append(veiculo)
    with open(ARQUIVO_JSON, "w") as f:
        json.dump(veiculos, f, indent=4)

def salvar_todos_veiculos(veiculos):
    with open(ARQUIVO_JSON, "w") as f:
        json.dump(veiculos, f, indent=4)

def remover_veiculo():
    while True:
        veiculos = carregar_veiculos()
        if not veiculos:
            print("\nNenhum veículo cadastrado para remover.")
            input("\nPressione ENTER para voltar ao menu...")
            return
        
        print("\n Veículos cadastrados:")
        
        carros = [v for v in veiculos if v["tipo"] == "Carro"]
        motos = [v for v in veiculos if v["tipo"] == "Moto"]
        bicicletas = [v for v in veiculos if v["tipo"] == "Bicicleta"]
        veiculos_ordenados = carros + motos + bicicletas
        
        tamanhos = obter_tamanhos_colunas(veiculos)
        
        print("\n" + criar_linha_separadora(tamanhos, "topo", True))
        print(criar_linha_tabela(["Tipo", "Marca", "Modelo", "Detalhes"], tamanhos))
        print(criar_linha_separadora(tamanhos, "meio", True))
        
        for i, v in enumerate(veiculos_ordenados, 1):
            if v["tipo"] == "Carro":
                detalhes = f"Portas: {v['portas']}"
            elif v["tipo"] == "Moto":
                detalhes = f"Cilindradas: {v['cilindrada']}"
            else:
                detalhes = f"Tipo: {v['tipo_bicicleta']}"
            linha = criar_linha_tabela([v["tipo"], v["marca"], v["modelo"], detalhes], tamanhos, i)
            print(linha)
            if i < len(veiculos_ordenados):
                print(criar_linha_separadora(tamanhos, "meio", True))
        print(criar_linha_separadora(tamanhos, "base", True))
        
        print("\nOpções:")
        print("1 - Remover um veículo")
        print("2 - Voltar ao menu principal")
        print("0 - Sair do programa")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            try:
                escolha = int(input("\nDigite o número do veículo que deseja remover (0 para cancelar): "))
                
                if escolha == 0:
                    print("Operação cancelada.")
                    continue
                
                if 1 <= escolha <= len(veiculos_ordenados):

                    veiculo_para_remover = veiculos_ordenados[escolha - 1]
                    
                    indice_original = veiculos.index(veiculo_para_remover)
                    
                    veiculo_removido = veiculos.pop(indice_original)
                    salvar_todos_veiculos(veiculos)
                    print(f"\nVeículo removido com sucesso: {veiculo_removido['marca']} {veiculo_removido['modelo']}")
                    input("\nPressione ENTER para continuar...")
                else:
                    print("Número inválido. Operação cancelada.")
                    input("\nPressione ENTER para continuar...")
            
            except ValueError:
                print("Por favor, digite um número válido.")
                input("\nPressione ENTER para continuar...")
        
        elif opcao == "2":
            return
        
        elif opcao == "0":
            print("\nEncerrando o programa...")
            exit()
        
        else:
            print("\nOpção inválida!")
            input("Pressione ENTER para continuar...")

def mostrar_veiculos():
    veiculos = carregar_veiculos()
    if not veiculos:
        print("\nNenhum veículo cadastrado ainda.")
        input("\nPressione ENTER para voltar ao menu...")
        return
    
    while True:
        print("\nTodos os veículos cadastrados:")
        
        carros = [v for v in veiculos if v["tipo"] == "Carro"]
        motos = [v for v in veiculos if v["tipo"] == "Moto"]
        bicicletas = [v for v in veiculos if v["tipo"] == "Bicicleta"]
        veiculos_ordenados = carros + motos + bicicletas
        
        tamanhos = obter_tamanhos_colunas(veiculos)
        
        print("\n" + criar_linha_separadora(tamanhos, "topo", True))
        print(criar_linha_tabela(["Tipo", "Marca", "Modelo", "Detalhes"], tamanhos))
        print(criar_linha_separadora(tamanhos, "meio", True))
        
        for i, v in enumerate(veiculos_ordenados, 1):
            if v["tipo"] == "Carro":
                detalhes = f"Portas: {v['portas']}"
            elif v["tipo"] == "Moto":
                detalhes = f"Cilindradas: {v['cilindrada']}"
            else:
                detalhes = f"Tipo: {v['tipo_bicicleta']}"
            linha = criar_linha_tabela([v["tipo"], v["marca"], v["modelo"], detalhes], tamanhos, i)
            print(linha)
            if i < len(veiculos_ordenados):
                print(criar_linha_separadora(tamanhos, "meio", True))
        print(criar_linha_separadora(tamanhos, "base", True))
        
        print("\nOpções:")
        print("1 - Voltar ao menu principal")
        print("0 - Sair do programa")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            return
        elif opcao == "0":
            print("\nEncerrando o programa...")
            exit()
        else:
            print("\nOpção inválida!")
            input("Pressione ENTER para continuar...")

def listar_carros():
    veiculos = carregar_veiculos()
    carros = [v for v in veiculos if v["tipo"] == "Carro"]
    if not carros:
        print("\n Nenhum carro cadastrado.")
        input("\nPressione ENTER para voltar ao menu...")
        return
    
    while True:
        print("\n Carros cadastrados:")
        
        tamanhos = obter_tamanhos_colunas(carros)
        
        print("\n" + criar_linha_separadora(tamanhos[1:], "topo", True))
        print(criar_linha_tabela(["Marca", "Modelo", "Portas"], tamanhos[1:]))
        print(criar_linha_separadora(tamanhos[1:], "meio", True))
        
        for i, c in enumerate(carros, 1):
            linha = criar_linha_tabela([c["marca"], c["modelo"], f"Portas: {c['portas']}"], tamanhos[1:], i)
            print(linha)
            if i < len(carros):
                print(criar_linha_separadora(tamanhos[1:], "meio", True))
        print(criar_linha_separadora(tamanhos[1:], "base", True))
        
        print("\nOpções:")
        print("1 - Voltar ao menu principal")
        print("0 - Sair do programa")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            return
        elif opcao == "0":
            print("\nEncerrando o programa...")
            exit()
        else:
            print("\nOpção inválida!")
            input("Pressione ENTER para continuar...")

def listar_motos():
    veiculos = carregar_veiculos()
    motos = [v for v in veiculos if v["tipo"] == "Moto"]
    if not motos:
        print("\n Nenhuma moto cadastrada.")
        input("\nPressione ENTER para voltar ao menu...")
        return
    
    while True:
        print("\n Motos cadastradas:")
        
        tamanhos = obter_tamanhos_colunas(motos)
        
        print("\n" + criar_linha_separadora(tamanhos[1:], "topo", True))
        print(criar_linha_tabela(["Marca", "Modelo", "Cilindradas"], tamanhos[1:]))
        print(criar_linha_separadora(tamanhos[1:], "meio", True))
        
        for i, m in enumerate(motos, 1):
            linha = criar_linha_tabela([m["marca"], m["modelo"], f"Cilindradas: {m['cilindrada']}"], tamanhos[1:], i)
            print(linha)
            if i < len(motos):
                print(criar_linha_separadora(tamanhos[1:], "meio", True))
        print(criar_linha_separadora(tamanhos[1:], "base", True))
        
        print("\nOpções:")
        print("1 - Voltar ao menu principal")
        print("0 - Sair do programa")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            return
        elif opcao == "0":
            print("\nEncerrando o programa...")
            exit()
        else:
            print("\nOpção inválida!")
            input("Pressione ENTER para continuar...")

def listar_bicicletas():
    veiculos = carregar_veiculos()
    bicicletas = [v for v in veiculos if v["tipo"] == "Bicicleta"]
    if not bicicletas:
        print("\n Nenhuma bicicleta cadastrada.")
        input("\nPressione ENTER para voltar ao menu...")
        return
    
    while True:
        print("\n Bicicletas cadastradas:")
        
        tamanhos = obter_tamanhos_colunas(bicicletas)
        
        print("\n" + criar_linha_separadora(tamanhos[1:], "topo", True))
        print(criar_linha_tabela(["Marca", "Modelo", "Tipo"], tamanhos[1:]))
        print(criar_linha_separadora(tamanhos[1:], "meio", True))
        
        for i, b in enumerate(bicicletas, 1):
            linha = criar_linha_tabela([b["marca"], b["modelo"], f"Tipo: {b['tipo_bicicleta']}"], tamanhos[1:], i)
            print(linha)
            if i < len(bicicletas):
                print(criar_linha_separadora(tamanhos[1:], "meio", True))
        print(criar_linha_separadora(tamanhos[1:], "base", True))
        
        print("\nOpções:")
        print("1 - Voltar ao menu principal")
        print("0 - Sair do programa")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            return
        elif opcao == "0":
            print("\nEncerrando o programa...")
            exit()
        else:
            print("\nOpção inválida!")
            input("Pressione ENTER para continuar...")

def cadastrar_veiculo():
    print("\nEscolha o tipo de veículo para cadastrar:")
    print( )
    print("1 - Carro")
    print("2 - Moto")
    print("3 - Bicicleta")
    print( )
    opcao = input("Digite a opção desejada: ")
    print( )

    if opcao == "1":
        marca = input("Marca do carro: ")
        modelo = input("Modelo do carro: ")
        portas = int(input("Número de portas: "))
        carro = Carro(marca, modelo, portas)
        salvar_veiculo({
            "tipo": "Carro",
            "marca": marca,
            "modelo": modelo,
            "portas": portas
        })
        print("\n Carro cadastrado com sucesso!")

    elif opcao == "2":
        marca = input("Marca da moto: ")
        modelo = input("Modelo da moto: ")
        cilindrada = int(input("Cilindradas: "))
        moto = Moto(marca, modelo, cilindrada)
        salvar_veiculo({
            "tipo": "Moto",
            "marca": marca,
            "modelo": modelo,
            "cilindrada": cilindrada
        })
        print("\n Moto cadastrada com sucesso!")

    elif opcao == "3":
        marca = input("Marca da bicicleta: ")
        modelo = input("Modelo da bicicleta: ")
        tipo_bicicleta = input("Tipo (montanha, urbana, etc.): ")
        bicicleta = Bicicleta(marca, modelo, tipo_bicicleta)
        salvar_veiculo({
            "tipo": "Bicicleta",
            "marca": marca,
            "modelo": modelo,
            "tipo_bicicleta": tipo_bicicleta
        })
        print("\n Bicicleta cadastrada com sucesso!")

    else:
        print(" Opção inválida. Retornando ao menu....")

def main():
    while True:
        print("\n--------- [ MENU ] ---------")
        print("1 - Cadastrar novo veículo")
        print("2 - Listar todos os veículos")
        print("3 - Listar apenas carros")
        print("4 - Listar apenas motos")
        print("5 - Listar apenas bicicletas")
        print("6 - Remover veículo")
        print("0 - Sair")
        print( )
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            cadastrar_veiculo()
        elif escolha == "2":
            mostrar_veiculos()
        elif escolha == "3":
            listar_carros()
        elif escolha == "4":
            listar_motos()
        elif escolha == "5":
            listar_bicicletas()
        elif escolha == "6":
            remover_veiculo()
        elif escolha == "0":
            print(" Painel encerrado.")
            break
        else:
            print(" Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
