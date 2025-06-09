NUM_DISCOS = 3

def desenhar_hastes(hastes_atuais):
    print("\n" + "=" * 40)
    print("TORRE DE HANÓI:")
    print("=" * 40)
    
    max_disco_len = NUM_DISCOS * 2 + 1 

    for i in range(NUM_DISCOS - 1, -1, -1): 
        linha = ""
        for haste_nome in ['A', 'B', 'C']:
            haste = hastes_atuais[haste_nome]
            
            if i < len(haste):
                disco = haste[i]
                disco_str = '#' * (disco * 2 - 1)
                linha += disco_str.center(max_disco_len) + "  "
            else:
                linha += "|".center(max_disco_len) + "  "
        print(linha)
    
    base_str = "=" * max_disco_len
    print(f"{base_str}   {base_str}   {base_str}")
    
    print(f"{'A'.center(max_disco_len)}   {'B'.center(max_disco_len)}   {'C'.center(max_disco_len)}")
    print("\n")

def movimento_valido(origem_nome, destino_nome, hastes_atuais):
    if origem_nome not in hastes_atuais or destino_nome not in hastes_atuais:
        print("Haste de origem ou destino inválida. Escolha A, B ou C.")
        return False

    origem = hastes_atuais[origem_nome]
    destino = hastes_atuais[destino_nome]

    if not origem:
        print(f"A haste '{origem_nome}' está vazia. Não há discos para mover.")
        return False

    if origem_nome == destino_nome:
        print("A haste de origem e destino são as mesmas. Mova para uma haste diferente.")
        return False

    disco_a_mover = origem[-1]

    if not destino or disco_a_mover < destino[-1]:
        return True
    else:
        print(f"Movimento inválido! Disco {disco_a_mover} não pode ser colocado sobre {destino[-1]}.")
        return False

def fazer_movimento(origem_nome, destino_nome, hastes_atuais):
    disco = hastes_atuais[origem_nome].pop()
    hastes_atuais[destino_nome].append(disco)

def jogar_hanoi():
    
    hastes_do_jogo = {
        'A': list(range(NUM_DISCOS, 0, -1)),
        'B': [],
        'C': []
    }
    
    num_movimentos = 0
    
    desenhar_hastes(hastes_do_jogo)
    print(f"Objetivo: Mover todos os {NUM_DISCOS} discos da haste A para a haste C.")
    print("Regras: 1. Mova apenas um disco por vez.")
    print("        2. Um disco maior nunca pode ser colocado sobre um disco menor.")
    print("Digite o nome da haste de origem e da haste de destino (ex: A B para mover de A para B).")
    print("Digite 'sair' a qualquer momento para encerrar o jogo.")

    while hastes_do_jogo['C'] != list(range(NUM_DISCOS, 0, -1)):
        try:
            comando = input("Seu movimento (Origem Destino) ou 'sair': ").upper().strip()
            
            if comando == 'SAIR':
                print("\nJogo encerrado. Até a próxima!")
                break

            partes = comando.split()
            if len(partes) != 2:
                print("Comando inválido. Use 'ORIGEM DESTINO' (ex: A B).")
                continue
            
            origem_nome, destino_nome = partes[0], partes[1]

            if movimento_valido(origem_nome, destino_nome, hastes_do_jogo):
                fazer_movimento(origem_nome, destino_nome, hastes_do_jogo)
                num_movimentos += 1
                desenhar_hastes(hastes_do_jogo)
                print(f"Movimentos: {num_movimentos}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}. Por favor, tente novamente com uma entrada válida.")
            
    if hastes_do_jogo['C'] == list(range(NUM_DISCOS, 0, -1)):
        print("\n" + "*" * 40)
        print(f"Parabéns! Você resolveu a Torre de Hanói em {num_movimentos} movimentos!")
        print(f"O número mínimo de movimentos para {NUM_DISCOS} discos é: {2**NUM_DISCOS - 1}")
        print("*" * 40)

if __name__ == "__main__":
    jogar_hanoi()