"""
Regras e estado do Xadrez baseados na biblioteca python-chess.
Fornece validação estrita de FEN/lances, serialização do tabuleiro e detecção de fim de jogo.
"""

import chess

MAPA_MOTIVOS_FIM = {
    chess.Termination.CHECKMATE: "Xeque-mate",
    chess.Termination.STALEMATE: "Afogamento (empate)",
    chess.Termination.INSUFFICIENT_MATERIAL: "Material insuficiente",
    chess.Termination.SEVENTYFIVE_MOVES: "Regra dos 75 lances",
    chess.Termination.FIVEFOLD_REPETITION: "Repetição quíntupla",
    chess.Termination.FIFTY_MOVES: "Regra dos 50 lances",
    chess.Termination.THREEFOLD_REPETITION: "Repetição tripla",
}


class PartidaXadrez:
    def __init__(self, fen=None):
        if fen is None:
            self.board = chess.Board()
        else:
            if not isinstance(fen, str) or not fen.strip():
                raise ValueError("FEN inválido: deve ser uma string não vazia.")
            self.board = chess.Board(fen.strip())

        if not self.board.is_valid():
            raise ValueError("Posição FEN ilegal pelas regras do xadrez.")

    def copiar(self):
        return PartidaXadrez(self.board.fen())

    def turno_cor(self):
        return "brancas" if self.board.turn == chess.WHITE else "pretas"

    def lances_legais_uci(self):
        return [move.uci() for move in self.board.legal_moves]

    def jogar_uci(self, lance_uci):
        if not isinstance(lance_uci, str) or not lance_uci.strip():
            raise ValueError("Lance UCI não informado ou inválido.")

        lance_limpo = lance_uci.strip().lower()
        try:
            move = chess.Move.from_uci(lance_limpo)
        except ValueError as exc:
            raise ValueError(f"Formato de lance inválido: {lance_uci}") from exc

        if move not in self.board.legal_moves:
            raise ValueError(f"Lance ilegal na posição atual: {lance_uci}")

        san = self.board.san(move)
        captura = self.board.is_capture(move)
        roque = self.board.is_castling(move)
        self.board.push(move)

        return {
            "uci": move.uci(),
            "san": san,
            "captura": captura,
            "roque": roque,
            "xeque": self.board.is_check(),
        }

    def estado_jogo(self, historico_fens=None):
        terminou = self.board.is_game_over(claim_draw=True)
        vencedor = None
        motivo_fim = None

        if terminou:
            outcome = self.board.outcome(claim_draw=True)
            if outcome:
                if outcome.winner == chess.WHITE:
                    vencedor = "brancas"
                elif outcome.winner == chess.BLACK:
                    vencedor = "pretas"
                else:
                    vencedor = "empate"

                motivo_fim = MAPA_MOTIVOS_FIM.get(outcome.termination, "Fim de partida")
        elif historico_fens:
            chave_atual = " ".join(self.board.fen().split()[:4])
            ocorrencias = sum(
                1
                for f in historico_fens
                if isinstance(f, str) and f.strip() and " ".join(f.split()[:4]) == chave_atual
            )
            if ocorrencias >= 3:
                terminou = True
                vencedor = "empate"
                motivo_fim = MAPA_MOTIVOS_FIM[chess.Termination.THREEFOLD_REPETITION]

        casa_rei_xeque = None
        if self.board.is_check():
            rei_sq = self.board.king(self.board.turn)
            if rei_sq is not None:
                casa_rei_xeque = chess.square_name(rei_sq)

        return {
            "fen": self.board.fen(),
            "turno": self.turno_cor(),
            "lances_legais": self.lances_legais_uci(),
            "xeque": self.board.is_check(),
            "casa_rei_xeque": casa_rei_xeque,
            "terminou": terminou,
            "vencedor": vencedor,
            "motivo_fim": motivo_fim,
        }
