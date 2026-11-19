"""
Motor de Inteligência Artificial para Xadrez usando Minimax com Poda Alfa-Beta,
Ordenação Tática de Lances (MVV-LVA) e Tabelas Posicionais (Piece-Square Tables).
"""

import random
import time
import chess

VALOR_PECAS = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

# Tabelas posicionais (perspectiva das Brancas, de a8=0 até h1=63)
PST_PEAO = [
     0,   0,   0,   0,   0,   0,   0,   0,
    50,  50,  50,  50,  50,  50,  50,  50,
    10,  10,  20,  30,  30,  20,  10,  10,
     5,   5,  10,  25,  25,  10,   5,   5,
     0,   0,   0,  20,  20,   0,   0,   0,
     5,  -5, -10,   0,   0, -10,  -5,   5,
     5,  10,  10, -20, -20,  10,  10,   5,
     0,   0,   0,   0,   0,   0,   0,   0,
]

PST_CAVALO = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]

PST_BISPO = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
]

PST_TORRE = [
     0,   0,   0,   0,   0,   0,   0,   0,
     5,  10,  10,  10,  10,  10,  10,   5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
     0,   0,   0,   5,   5,   0,   0,   0,
]

PST_DAMA = [
    -20, -10, -10,  -5,  -5, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,   5,   5,   5,   0, -10,
     -5,   0,   5,   5,   5,   5,   0,  -5,
      0,   0,   5,   5,   5,   5,   0,  -5,
    -10,   5,   5,   5,   5,   5,   0, -10,
    -10,   0,   5,   0,   0,   0,   0, -10,
    -20, -10, -10,  -5,  -5, -10, -10, -20,
]

PST_REI = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
     20,  20,   0,   0,   0,   0,  20,  20,
     20,  30,  10,   0,   0,  10,  30,  20,
]

TABELAS_POSICIONAIS = {
    chess.PAWN: PST_PEAO,
    chess.KNIGHT: PST_CAVALO,
    chess.BISHOP: PST_BISPO,
    chess.ROOK: PST_TORRE,
    chess.QUEEN: PST_DAMA,
    chess.KING: PST_REI,
}

CASAS_CENTRAIS = {chess.D4, chess.E4, chess.D5, chess.E5, chess.C3, chess.F3, chess.C6, chess.F6}
MATE_SCORE = 100000


def avaliar_tabuleiro(board, cor_ia):
    """
    Avalia a posição em centipeões sob a perspectiva de `cor_ia`.
    Valores positivos favorecem a IA; negativos favorecem o oponente.
    """
    if board.is_checkmate():
        return -MATE_SCORE if board.turn == cor_ia else MATE_SCORE

    if board.is_stalemate() or board.is_insufficient_material() or board.can_claim_threefold_repetition():
        return 0

    pontuacao = 0
    for tipo_peca, valor in VALOR_PECAS.items():
        tabela = TABELAS_POSICIONAIS[tipo_peca]

        for sq in board.pieces(tipo_peca, chess.WHITE):
            idx = chess.square_mirror(sq)
            pontuacao += valor + tabela[idx]

        for sq in board.pieces(tipo_peca, chess.BLACK):
            pontuacao -= valor + tabela[sq]

    return pontuacao if cor_ia == chess.WHITE else -pontuacao


def _prioridade_lance(board, move):
    """Ordena capturas (MVV-LVA), promoções e controle central primeiro para maximizar cortes Alfa-Beta."""
    score = 0
    if move.promotion:
        score += 800 + VALOR_PECAS.get(move.promotion, 0)
    if move.to_square in CASAS_CENTRAIS:
        score += 15

    if board.is_capture(move):
        atacante = board.piece_type_at(move.from_square) or chess.PAWN
        if board.is_en_passant(move):
            vitima = chess.PAWN
        else:
            vitima = board.piece_type_at(move.to_square) or chess.PAWN
        score += 10 * VALOR_PECAS[vitima] - VALOR_PECAS[atacante]

    return score


def _ordenar_lances(board):
    lances = list(board.legal_moves)
    lances.sort(key=lambda m: _prioridade_lance(board, m), reverse=True)
    return lances


def minimax(board, profundidade, alfa, beta, maximizando, cor_ia, metricas):
    """Busca Minimax com Poda Alfa-Beta."""
    metricas["nos"] += 1

    if board.is_checkmate():
        return (-MATE_SCORE - profundidade) if board.turn == cor_ia else (MATE_SCORE + profundidade)

    if profundidade == 0 or board.is_game_over():
        return avaliar_tabuleiro(board, cor_ia)

    lances = _ordenar_lances(board)

    if maximizando:
        melhor = float("-inf")
        for move in lances:
            board.push(move)
            valor = minimax(board, profundidade - 1, alfa, beta, False, cor_ia, metricas)
            board.pop()
            melhor = max(melhor, valor)
            alfa = max(alfa, melhor)
            if beta <= alfa:
                break
        return melhor
    else:
        melhor = float("inf")
        for move in lances:
            board.push(move)
            valor = minimax(board, profundidade - 1, alfa, beta, True, cor_ia, metricas)
            board.pop()
            melhor = min(melhor, valor)
            beta = min(beta, melhor)
            if beta <= alfa:
                break
        return melhor


def analisar_posicao(board, cor_referencia, profundidade=3, limite_candidatos=5):
    """
    Avalia os lances legais a partir de `board` sob o ponto de vista de `cor_referencia`.
    Retorna lista ordenada dos melhores lances, nós avaliados e tempo de cálculo.
    """
    inicio = time.perf_counter()
    metricas = {"nos": 0}
    avaliacoes = []

    lances = _ordenar_lances(board)
    alfa = float("-inf")
    beta = float("inf")

    for move in lances:
        san = board.san(move)
        board.push(move)
        valor = minimax(
            board,
            profundidade=max(0, profundidade - 1),
            alfa=alfa,
            beta=beta,
            maximizando=False,
            cor_ia=cor_referencia,
            metricas=metricas,
        )
        board.pop()

        avaliacoes.append({
            "uci": move.uci(),
            "san": san,
            "centipawns": valor,
            "peoes": round(valor / 100.0, 2),
            "mate": abs(valor) >= MATE_SCORE - 50,
        })

        if valor > alfa:
            alfa = valor

    avaliacoes.sort(key=lambda item: item["centipawns"], reverse=True)
    tempo_ms = round((time.perf_counter() - inicio) * 1000, 2)

    return {
        "avaliacoes": avaliacoes[:limite_candidatos],
        "todas_avaliacoes": avaliacoes,
        "nos_avaliados": metricas["nos"],
        "tempo_ms": tempo_ms,
        "profundidade": profundidade,
    }


def _gerar_diagnostico(avaliacao_escolhida, dificuldade):
    cp = avaliacao_escolhida["centipawns"]
    san = avaliacao_escolhida["san"]

    if cp >= MATE_SCORE - 50:
        return f"Xeque-mate forçado detectado com {san}!"
    if cp <= -MATE_SCORE + 50:
        return f"Defesa crítica ({san}): oponente ameaça mate."

    prefixo = {
        "facil": "Modo Aprendiz",
        "medio": "Modo Desafiante",
        "mestre": "Modo Mestre",
    }.get(dificuldade, "Motor IA")

    if cp >= 300:
        return f"{prefixo}: vantagem decisiva ({san}, +{cp / 100:.2f})."
    if cp >= 80:
        return f"{prefixo}: leve vantagem posicional/material ({san}, +{cp / 100:.2f})."
    if cp <= -300:
        return f"{prefixo}: posição difícil, buscando contra-jogo ({san}, {cp / 100:.2f})."
    if cp <= -80:
        return f"{prefixo}: oponente pressiona ({san}, {cp / 100:.2f})."
    return f"{prefixo}: equilíbrio dinâmico no tabuleiro ({san}, {cp / 100:+.2f})."


def melhor_jogada(board, dificuldade="mestre"):
    """
    Escolhe o lance da IA de acordo com o nível:
    - 'facil': profundidade 1 com chance de lances exploratórios
    - 'medio': profundidade 2 com variação tática ocasional
    - 'mestre': profundidade 3 com Poda Alfa-Beta completa
    """
    lances_legais = list(board.legal_moves)
    if not lances_legais:
        return None, {}

    mapa_profundidade = {
        "facil": 1,
        "medio": 2,
        "mestre": 3,
    }
    profundidade = mapa_profundidade.get(dificuldade, 3)
    cor_ia = board.turn

    analise = analisar_posicao(board, cor_ia, profundidade=profundidade, limite_candidatos=len(lances_legais))
    todas = analise["todas_avaliacoes"]

    if dificuldade == "facil" and len(todas) > 1 and random.random() < 0.65:
        escolhido = random.choice(todas[:min(6, len(todas))])
    elif dificuldade == "medio" and len(todas) > 1 and random.random() < 0.30:
        escolhido = random.choice(todas[:min(3, len(todas))])
    else:
        melhor_cp = todas[0]["centipawns"]
        empatados = [a for a in todas if a["centipawns"] == melhor_cp]
        escolhido = random.choice(empatados)

    eval_brancas = escolhido["centipawns"] if cor_ia == chess.WHITE else -escolhido["centipawns"]

    detalhes = {
        "uci": escolhido["uci"],
        "san": escolhido["san"],
        "nos_avaliados": analise["nos_avaliados"],
        "tempo_ms": analise["tempo_ms"],
        "profundidade": profundidade,
        "avaliacao_brancas_cp": eval_brancas,
        "motivo": _gerar_diagnostico(escolhido, dificuldade),
        "candidatos": analise["avaliacoes"][:3],
    }

    return escolhido["uci"], detalhes
