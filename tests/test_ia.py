import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from jogo import PartidaXadrez
from ia import melhor_jogada
from app import app


class XadrezMinimaxTestCase(unittest.TestCase):
    def test_ia_encontra_xeque_mate_em_um(self):
        fen_mate = "r1bqkbnr/pppp1ppp/2n5/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4"
        partida = PartidaXadrez(fen_mate)
        lance, detalhes = melhor_jogada(partida.board, dificuldade="mestre")
        self.assertEqual(lance, "h5f7")
        self.assertIn("Xeque-mate", detalhes["motivo"])

    def test_ia_captura_dama_desprotegida(self):
        fen_tatica = "4k3/8/8/3q4/8/2N5/8/4K3 w - - 0 1"
        partida = PartidaXadrez(fen_tatica)
        lance, _ = melhor_jogada(partida.board, dificuldade="mestre")
        self.assertEqual(lance, "c3d5")

    def test_rejeita_lance_ilegal(self):
        partida = PartidaXadrez()
        with self.assertRaises(ValueError):
            partida.jogar_uci("e2e5")


class XadrezWebApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_pagina_principal_carrega(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Xadrez", resp.data)

    def test_fluxo_validar_e_jogada_ia(self):
        fen_inicial = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        resp_val = self.client.post("/api/validar", json={"fen": fen_inicial, "lance": "e2e4"})
        self.assertEqual(resp_val.status_code, 200)
        novo_fen = resp_val.get_json()["estado"]["fen"]

        resp_ia = self.client.post("/api/jogada", json={"fen": novo_fen, "dificuldade": "medio"})
        self.assertEqual(resp_ia.status_code, 200)
        dados = resp_ia.get_json()
        self.assertIsNotNone(dados["lance"])
        self.assertGreater(dados["telemetria"]["nos_avaliados"], 0)


if __name__ == "__main__":
    unittest.main()
