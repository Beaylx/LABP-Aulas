import random

def forca(erros):
    estagios = [
        """
        _______
        |/      |
        |       
        |       
        |       
        |       
        |
        _|_
        """,
        """
        _______
        |/      |
        |     (^-^)
        |       
        |       
        |       
        |
        _|_
        """,
        """
        _______
        |/      |
        |     (^-^)
        |       |
        |       |
        |       
        |
        _|_
        """,
        """
        _______
        |/      |
        |     (^-^)
        |      /|
        |       |
        |       
        |
        _|_
        """,
        """
        _______
        |/      |
        |     (^-^)
        |      /|\\
        |       |
        |      
        |
        _|_
        """,
        """
        _______
        |/      |
        |     (^-^)
        |      /|\\
        |       |
        |      / 
        |
        _|_
        """,
        """
        _______
        |/      |
        |     (^-^)
        |      /|\\
        |       |
        |      / \\
        |
        _|_
        """
    ]
    
    print(estagios[erros])

def jogar():
    palavras = ['Roblox', 'Pokemon', 'Minecraft', 'Super Mario', 'The last of us', 'Sonic',    
    'Free Fire', 'Genshin Impact', 'Apex Legends', 'Grand Theft Auto', 'Red Dead Redemption',    
    'The Witcher', 'Overwatch', 'Tetris', 'Halo', 'Call of Duty', 'Fifa', 'League of Legends',
    'Dota', 'Phasmophobia', 'Fortnite', 'Rocket League', 'Tomb Raider', 'Paladins', 'Brawl Stars']
    
    palavra_random = random.choice(palavras).upper()
    letras_certas = [' ' if letra == ' ' else '_' for letra in palavra_random]

    chances = 6
    erros = 0
    chutes = set()

    print('-' * 30)
    print('Forca dos games!')
    print('-' * 30)
    print(f'O jogo possui {len(palavra_random)} letras.')

    while erros < chances and '_' in letras_certas:
        forca(erros)
        print('\nPalavra: ' + ' '.join(letras_certas)) 
        print(f"Tentativas restantes: {chances - erros}")

        if chutes:
            print('Letras já tentadas: ' + ', '.join(sorted(chutes)))

        tentativa = input('Digite uma letra: ').upper().strip()

        if not tentativa.isalpha() or len(tentativa) != 1:
            print('Digite apenas uma letra válida.')
            continue

        if tentativa in chutes:
            print(f'Você já tentou a letra "{tentativa}".')
            continue

        chutes.add(tentativa)

        if tentativa in palavra_random:
            print(f'A letra "{tentativa}" faz parte do nome do jogo!')
            for i in range(len(palavra_random)):
                if palavra_random[i].lower() == tentativa.lower():
                    letras_certas[i] = palavra_random[i]
        else:
            print(f'Você errou! "{tentativa}" não faz parte do nome do jogo.')
            erros += 1
        
        print(' '.join(letras_certas))
        print('-' * 30)

    if "_" not in letras_certas:
        print("\n" + "*" * 30)
        print(f'Parabéns! Você descobriu! O jogo é: "{palavra_random}"')
        print("*" * 30)
    
    else:
        if erros == chances:
            forca(erros)
            print("\n" + "=" * 30)
            print("Você está sem tentativas! Faça um chute agora.")
            chute_final = input("Qual o nome do jogo? ").upper().strip()

            if chute_final == palavra_random:
                print("\n" + "*" * 30)
                print(f'ACERTOU NOS 45 DO SEGUNDO TEMPO! O jogo é: "{palavra_random}"')
                print("*" * 30)
            else:
                print("\n" + "X" * 30)
                print("Que pena! Você errou o chute final.")
                print("Você perdeu! Fim de jogo.")
                print(f'O jogo era: "{palavra}"')
            print("X" * 30)

if __name__ == "__main__":
    jogar()