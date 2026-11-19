"""
Motor de Inteligência Artificial para Xadrez usando Minimax com Poda Alfa-Beta,
Aprofundamento Iterativo com orçamento de tempo, Tabela de Transposição (Zobrist)
e Ordenação Tática de Lances (MVV-LVA).
"""

import random
import time
import chess
import chess.polyglot

VALOR_PECAS = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

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

# Flags da Tabela de Transposição
TT_EXACT = 0
TT_ALPHA = 1
TT_BETA = 2


class BuscaTimeout(Exception):
    """Exceção interna para interromper o aprofundamento iterativo dentro do orçamento de tempo."""


def _chave_posicao_fen(fen):
    """Extrai as 4 primeiras partes do FEN (tabuleiro, turno, roque, en passant) para detectar repetições."""
    return " ".join(fen.split()[:4])


def avaliar_tabuleiro(board, cor_ia):
    """
    Avalia a posição em centipeões sob a perspectiva de `cor_ia`.
    Valores positivos favorecem a IA; negativos favorecem o oponente.
    """
    if board.is_checkmate():
        return -MATE_SCORE if board.turn == cor_ia else MATE_SCORE

    if (
        board.is_stalemate()
        or board.is_insufficient_material()
        or board.is_seventyfive_moves()
        or board.is_fivefold_repetition()
    ):
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


def _prioridade_lance(board, move, lance_tt=None):
    """Ordena lance da TT, capturas (MVV-LVA), promoções e controle central para maximizar cortes Alfa-Beta."""
    if lance_tt is not None and move == lance_tt:
        return 1_000_000

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


def _ordenar_lances(board, lance_tt=None):
    lances = list(board.legal_moves)
    lances.sort(key=lambda m: _prioridade_lance(board, m, lance_tt), reverse=True)
    return lances


def minimax(board, profundidade, alfa, beta, maximizando, cor_ia, metricas, tt, deadline):
    """Busca Minimax com Poda Alfa-Beta, Tabela de Transposição e checagem periódica de tempo."""
    metricas["nos"] += 1
    if (metricas["nos"] & 511) == 0 and time.perf_counter() >= deadline:
        raise BuscaTimeout()

    if board.is_checkmate():
        return (-MATE_SCORE - profundidade) if board.turn == cor_ia else (MATE_SCORE + profundidade)

    if (
        board.is_stalemate()
        or board.is_insufficient_material()
        or board.is_seventyfive_moves()
        or board.is_fivefold_repetition()
    ):
        return 0

    if profundidade <= 0:
        return avaliar_tabuleiro(board, cor_ia)

    alfa_orig = alfa
    beta_orig = beta
    chave = chess.polyglot.zobrist_hash(board)
    entrada_tt = tt.get(chave)
    lance_tt = None

    if entrada_tt is not None:
        tt_prof, tt_val, tt_flag, lance_tt = entrada_tt
        if tt_prof >= profundidade:
            if tt_flag == TT_EXACT:
                return tt_val
            if tt_flag == TT_ALPHA and tt_val <= alfa:
                return tt_val
            if tt_flag == TT_BETA and tt_val >= beta:
                return tt_val

    lances = _ordenar_lances(board, lance_tt)
    if not lances:
        return avaliar_tabuleiro(board, cor_ia)

    melhor_lance = None

    if maximizando:
        melhor = float("-inf")
        for move in lances:
            board.push(move)
            valor = minimax(board, profundidade - 1, alfa, beta, False, cor_ia, metricas, tt, deadline)
            board.pop()
            if valor > melhor:
                melhor = valor
                melhor_lance = move
            alfa = max(alfa, melhor)
            if beta <= alfa:
                break
    else:
        melhor = float("inf")
        for move in lances:
            board.push(move)
            valor = minimax(board, profundidade - 1, alfa, beta, True, cor_ia, metricas, tt, deadline)
            board.pop()
            if valor < melhor:
                melhor = valor
                melhor_lance = move
            beta = min(beta, melhor)
            if beta <= alfa:
                break

    if melhor <= alfa_orig:
        flag = TT_ALPHA
    elif melhor >= beta_orig:
        flag = TT_BETA
    else:
        flag = TT_EXACT

    if len(tt) < 50_000:
        tt[chave] = (profundidade, melhor, flag, melhor_lance)

    return melhor


def analisar_posicao(
    board,
    cor_referencia,
    profundidade=3,
    limite_candidatos=5,
    tempo_limite_s=2.2,
    historico_fens=None,
):
    """
    Avalia os lances legais a partir de `board` sob o ponto de vista de `cor_referencia`
    usando aprofundamento iterativo com limite de tempo (garante resposta rápida no Render).
    """
    inicio = time.perf_counter()
    deadline = inicio + max(0.15, tempo_limite_s)
    metricas = {"nos": 0}
    tt = {}

    lances_raiz = _ordenar_lances(board)
    if not lances_raiz:
        return {
            "avaliacoes": [],
            "todas_avaliacoes": [],
            "nos_avaliados": 0,
            "tempo_ms": 0,
            "profundidade": 0,
        }

    contagem_fens = {}
    if historico_fens:
        for f in historico_fens:
            if isinstance(f, str) and f.strip():
                k = _chave_posicao_fen(f)
                contagem_fens[k] = contagem_fens.get(k, 0) + 1

    melhor_mapa = {}
    profundidade_atingida = 1

    # Aprofundamento iterativo: garante que profundidade 1 sempre conclua e avança até `profundidade`
    for prof_atual in range(1, max(1, profundidade) + 1):
        mapa_iteracao = {}
        try:
            # Na profundidade 1 não aplica timeout para garantir resultado válido em qualquer CPU
            prazo_atual = float("inf") if prof_atual == 1 else deadline

            for move in lances_raiz:
                board.push(move)
                chave_pos = _chave_posicao_fen(board.fen())
                repeticoes = contagem_fens.get(chave_pos, 0)

                if repeticoes >= 2:
                    valor = 0
                else:
                    valor = minimax(
                        board,
                        profundidade=prof_atual - 1,
                        alfa=float("-inf"),
                        beta=float("inf"),
                        maximizando=False,
                        cor_ia=cor_referencia,
                        metricas=metricas,
                        tt=tt,
                        deadline=prazo_atual,
                    )
                    # Penaliza leve repetição quando está vencendo para evitar loops infinitos
                    if repeticoes == 1 and valor > 30:
                        valor -= 45

                board.pop()
                mapa_iteracao[move.uci()] = (move, valor)

            melhor_mapa = mapa_iteracao
            profundidade_atingida = prof_atual
            # Ordena lances da raiz pela avaliação da iteração anterior
            lances_raiz = [
                item[0]
                for item in sorted(melhor_mapa.values(), key=lambda x: x[1], reverse=True)
            ]
        except BuscaTimeout:
            break

    avaliacoes = []
    for uci, (move, valor) in melhor_mapa.items():
        avaliacoes.append({
            "uci": uci,
            "move": move,
            "centipawns": valor,
            "peoes": round(valor / 100.0, 2),
            "mate": abs(valor) >= MATE_SCORE - 50,
        })

    avaliacoes.sort(key=lambda item: item["centipawns"], reverse=True)

    # Calcula SAN apenas para os candidatos retornados (economiza CPU)
    top_n = max(limite_candidatos, 6)
    for item in avaliacoes[:top_n]:
        item["san"] = board.san(item["move"])

    for item in avaliacoes:
        if "san" not in item:
            item["san"] = item["uci"]
        del item["move"]

    tempo_ms = round((time.perf_counter() - inicio) * 1000, 2)

    return {
        "avaliacoes": avaliacoes[:limite_candidatos],
        "todas_avaliacoes": avaliacoes,
        "nos_avaliados": metricas["nos"],
        "tempo_ms": tempo_ms,
        "profundidade": profundidade_atingida,
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


def melhor_jogada(board, dificuldade="mestre", historico_fens=None):
    """
    Escolhe o lance da IA de acordo com o nível:
    - 'facil': profundidade 1 com chance de lances exploratórios
    - 'medio': profundidade 2 com variação tática ocasional
    - 'mestre': profundidade 3 (com orçamento de 2.2s) e Poda Alfa-Beta completa
    """
    lances_legais = list(board.legal_moves)
    if not lances_legais:
        return None, {}

    mapa_profundidade = {
        "facil": 1,
        "medio": 2,
        "mestre": 3,
    }
    mapa_tempo = {
        "facil": 0.5,
        "medio": 1.2,
        "mestre": 2.2,
    }
    profundidade = mapa_profundidade.get(dificuldade, 3)
    tempo_limite = mapa_tempo.get(dificuldade, 2.2)
    cor_ia = board.turn

    analise = analisar_posicao(
        board,
        cor_ia,
        profundidade=profundidade,
        limite_candidatos=len(lances_legais),
        tempo_limite_s=tempo_limite,
        historico_fens=historico_fens,
    )
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
        "profundidade": analise["profundidade"],
        "avaliacao_brancas_cp": eval_brancas,
        "motivo": _gerar_diagnostico(escolhido, dificuldade),
        "candidatos": analise["avaliacoes"][:3],
    }

    return escolhido["uci"], detalhes
