import random

def jogar_ppt():
    opcoes = ["PEDRA", "PAPEL", "TESOURA"]
    
    escolha_computador = random.choice(opcoes)

    escolha_usuario = ""
    while escolha_usuario not in opcoes:
        print("\nEscolha uma opção:")
        print("- Pedra")
        print("- Papel")
        print("- Tesoura")
        entrada = input("Sua jogada (Pedra, Papel ou Tesoura): ").upper().strip()
        
        if entrada in opcoes:
            escolha_usuario = entrada
        else:
            print("Opção inválida! Por favor, escolha Pedra, Papel ou Tesoura.")

    print(f"\nVocê escolheu: {escolha_usuario}")
    print(f"O computador escolheu: {escolha_computador}")

    if escolha_usuario == escolha_computador:
        print("Empate!")
        return "empate"
    elif (escolha_usuario == "PEDRA" and escolha_computador == "TESOURA") or \
         (escolha_usuario == "PAPEL" and escolha_computador == "PEDRA") or \
         (escolha_usuario == "TESOURA" and escolha_computador == "PAPEL"):
        print("Você venceu!")
        return "usuario"
    else:
        print("O computador venceu!")
        return "computador"

def main():
    placar_usuario = 0
    placar_computador = 0
    
    print("=" * 30)
    print("Pedra, Papel e Tesoura!")
    print("=" * 30)

    while True:
        resultado_rodada = jogar_ppt()
        
        if resultado_rodada == "usuario":
            placar_usuario += 1
        elif resultado_rodada == "computador":
            placar_computador += 1

        print(f"\n--- PLACAR ---")
        print(f"Você: {placar_usuario} | Computador: {placar_computador}")
        print("--------------")

        jogar_novamente = input("Jogar novamente? (s/n): ").lower().strip()
        if jogar_novamente != 's':
            break
    
    print("\nJogo encerrado!")
    print("=" * 30)


if __name__ == "__main__":
    main()