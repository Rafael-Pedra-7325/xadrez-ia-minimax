"""
IA de Xadrez — Interface de Terminal (CLI).
Permite jogar contra o motor Minimax + Poda Alfa-Beta diretamente no console.
"""

from jogo import PartidaXadrez
from ia import melhor_jogada

SIMBOLOS_UNICODE = {
    "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔",
    "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚",
}


def exibir_tabuleiro(board):
    print("\n    a b c d e f g h")
    print("  ┌─────────────────┐")
    for rank in range(7, -1, -1):
        linha = []
        for file in range(8):
            peca = board.piece_at(rank * 8 + file)
            linha.append(SIMBOLOS_UNICODE[peca.symbol()] if peca else "·")
        print(f"{rank + 1} │ {' '.join(linha)} │ {rank + 1}")
    print("  └─────────────────┘")
    print("    a b c d e f g h\n")


def jogar():
    print("╔════════════════════════════════════════╗")
    print("║      ♟️  IA DE XADREZ MINIMAX          ║")
    print("╚════════════════════════════════════════╝")
    print("Nível: [1] Fácil  [2] Médio  [3] Mestre")
    dif = {"1": "facil", "2": "medio", "3": "mestre"}.get(input("Opção [3]: ").strip(), "mestre")

    cor = input("Jogar com [B]rancas ou [P]retas? [B]: ").strip().upper()
    ia_joga_brancas = cor == "P"

    partida = PartidaXadrez()

    while not partida.estado_jogo()["terminou"]:
        exibir_tabuleiro(partida.board)
        turno_ia = (partida.board.turn and ia_joga_brancas) or (not partida.board.turn and not ia_joga_brancas)

        if turno_ia:
            lance_uci, detalhes = melhor_jogada(partida.board, dificuldade=dif)
            info = partida.jogar_uci(lance_uci)
            print(f"🤖 IA jogou: {info['san']} ({lance_uci}) — {detalhes['nos_avaliados']} nós em {detalhes['tempo_ms']}ms")
        else:
            while True:
                entrada = input("Seu lance em UCI (ex: e2e4, g1f3, e7e8q): ").strip().lower()
                try:
                    partida.jogar_uci(entrada)
                    break
                except ValueError as e:
                    print(f"Erro: {e}")

    exibir_tabuleiro(partida.board)
    estado = partida.estado_jogo()
    print(f"Fim de jogo ({estado['motivo_fim']}) — Vencedor: {estado['vencedor']}")


if __name__ == "__main__":
    jogar()
