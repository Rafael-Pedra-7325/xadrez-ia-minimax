"""
Regras e estado do Xadrez baseados na biblioteca python-chess.
Fornece validação de lances, serialização do tabuleiro e detecção de fim de jogo.
"""

import chess


class PartidaXadrez:
    def __init__(self, fen=None):
        self.board = chess.Board(fen) if fen else chess.Board()

    def copiar(self):
        return PartidaXadrez(self.board.fen())

    def turno_cor(self):
        return "brancas" if self.board.turn == chess.WHITE else "pretas"

    def lances_legais_uci(self):
        return [move.uci() for move in self.board.legal_moves]

    def jogar_uci(self, lance_uci):
        try:
            move = chess.Move.from_uci(lance_uci)
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

    def estado_jogo(self):
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

                mapa_motivos = {
                    chess.CHECKMATE: "Xeque-mate",
                    chess.STALEMATE: "Afogamento (empate)",
                    chess.INSUFFICIENT_MATERIAL: "Material insuficiente",
                    chess.SEVENTYFIVE_MOVES: "Regra dos 75 lances",
                    chess.FIVEFOLD_REPETITION: "Repetição quíntupla",
                    chess.FIFTY_MOVES: "Regra dos 50 lances",
                    chess.THREEFOLD_REPETITION: "Repetição tripla",
                }
                motivo_fim = mapa_motivos.get(outcome.termination, "Fim de partida")

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
