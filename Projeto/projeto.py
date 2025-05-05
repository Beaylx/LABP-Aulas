class ItemCardapio:
    def __init__ (self, nome: str, descrição: str, preço: float):
        self.nome = nome
        self.descrição = descrição
        self.preço = preço
    
    def exibir_detalhes(self):
        print(f"Nome: {self.nome}")
        print(f"Descrição: {self.descrição}")
        print(f"Preço: R$ {self.preço:.2f}")


class cliente:
    def __init__ (self, nome: str, telefone: str) :
        self.nome = nome
        self.telefone = telefone

    def exibir_detalhes(self):
        print(f'Nome: {self.nome} - Contato: {self.telefone}')


class pedido:
    def __init__(self, cliente, itens_pedido, status: str):
        self.cliente = cliente
        self.itens_pedido = []
        self.status = "Aberto"

    def adicionar_item(item: ItemCardapio):
        item.itens_pedido.append(item)

    def calcular_total(self: float):
        total = sum(item.preço for item in self.itens_pedido)
        return total


item1 = ItemCardapio("Pão-de-queijo", 
                     "Pãozinho redondo envolvido por uma massa crocante e recheado de queijo cremoso por dentro", 
                     2.50)
item1.exibir_detalhes()  


cliente1 = cliente("Beatriz", "11838518007")
cliente1.exibir_detalhes()
  