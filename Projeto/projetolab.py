class ItemCardapio:
    def __init__ (self, nome: str, descrição: str, preço: float):
        self.nome = nome
        self.descrição = descrição
        self.preço = preço
    
    def exibir_detalhes(self):
        print(f"Nome: {self.nome}")
        print(f"Descrição: {self.descrição}")
        print(f"Preço: R$ {self.preço:.2f}")


class Cliente:
    def __init__ (self, nome: str, telefone: str):
        self.nome = nome
        self.telefone = telefone

    def exibir_detalhes(self):
        print(f'Nome: {self.nome} - Contato: {self.telefone}')


class Pedido:
    def __init__(self, cliente: Cliente):
        self.cliente = cliente
        self.itens_pedido = []
        self.status = "Aberto"

    def adicionar_item(self, item: ItemCardapio):
        self.itens_pedido.append(item)
        print(f"Item '{item.nome}' adicionado ao pedido.")
    
    def calcular_total(self):
        total = sum(item.preço for item in self.itens_pedido)
        return total

    def exibir_resumo(self):
        print("\n--- RESUMO DO PEDIDO ---")
        self.cliente.exibir_detalhes()

        print("\nItens do Pedido:")
        if not self.itens_pedido:
            print("  Nenhum item adicionado ao pedido ainda.")
        else:
            for item in self.itens_pedido:
                print(f"- {item.nome} (R$ {item.preço:.2f})")

        total = self.calcular_total() 
        print(f"\nTotal: R$ {total:.2f}")
        print(f"Status do Pedido: {self.status}")
        print("------------------------")

    def finalizar_pedido(self):
        self.status = "Finalizado"
        print(f"\nPedido do cliente {self.cliente.nome} foi FINALIZADO.")


# Funcionamento

item1 = ItemCardapio("Fatia de bolo", "Bolo macio de sabor à sua escolha.", 10.50)
item2 = ItemCardapio("Cappuccino", "Café expresso, leite vaporizado e espuma de leite", 8.00)
item3 = ItemCardapio("Brownie", "Sabor chocolate com textura macia e sabor intenso, perfeito para quem ama chocolate puro.", 6.00)
item4 = ItemCardapio("Suco Natural", "Suco de laranja natural", 7.00)

Cardapio = [item1, item2, item3, item4]

print("\n--- CARDAPIO ---")
for i, item in enumerate(Cardapio):
    print(f"{i+1}. {item.nome} - R$ {item.preço:.2f}")
print("------------------------------")

cliente1 = Cliente("Beatriz", "11838518007")
print(f"\n--- Cliente: {cliente1.nome} ---")

pedidoBeatriz = Pedido(cliente1)

print("\n--- SIMULACAO DE PEDIDO ---")

pedidoBeatriz.adicionar_item(Cardapio[0])
pedidoBeatriz.adicionar_item(Cardapio[0])
pedidoBeatriz.adicionar_item(Cardapio[1])

pedidoBeatriz.exibir_resumo()
pedidoBeatriz.finalizar_pedido()
pedidoBeatriz.exibir_resumo()

print("\n--- SIMULACAO CONCLUIDA ---")
