import os
import sys
import time
import unittest
import chess

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

    def test_rejeita_lance_ilegal_e_entradas_invalidas(self):
        partida = PartidaXadrez()
        with self.assertRaises(ValueError):
            partida.jogar_uci("e2e5")
        with self.assertRaises(ValueError):
            partida.jogar_uci(None)
        with self.assertRaises(ValueError):
            PartidaXadrez("")
        with self.assertRaises(ValueError):
            PartidaXadrez("8/8/8/8/8/8/8/8 w - - 0 1")  # Sem reis

    def test_detecta_empate_repeticao_tripla_por_historico(self):
        partida = PartidaXadrez()
        fen_inicial = partida.board.fen()
        estado = partida.estado_jogo(historico_fens=[fen_inicial, fen_inicial, fen_inicial])
        self.assertTrue(estado["terminou"])
        self.assertEqual(estado["vencedor"], "empate")
        self.assertEqual(estado["motivo_fim"], "Repetição tripla")

    def test_orcamento_tempo_meio_jogo_complexo(self):
        fen_complexo = "r1bq1rk1/pp2ppbp/2np1np1/8/2BNP3/2N1BP2/PPPQ2PP/R3K2R w KQ - 3 9"
        partida = PartidaXadrez(fen_complexo)
        inicio = time.perf_counter()
        lance, detalhes = melhor_jogada(partida.board, dificuldade="mestre")
        duracao = time.perf_counter() - inicio
        self.assertIsNotNone(lance)
        self.assertEqual(partida.board.fen(), fen_complexo)
        self.assertLess(duracao, 3.5)
        self.assertGreater(detalhes["nos_avaliados"], 0)


class XadrezWebApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_pagina_principal_e_health(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        resp_health = self.client.get("/health")
        self.assertEqual(resp_health.status_code, 200)

    def test_fluxo_validar_e_jogada_ia(self):
        fen_inicial = chess.STARTING_FEN
        resp_val = self.client.post("/api/validar", json={"fen": fen_inicial, "lance": "e2e4"})
        self.assertEqual(resp_val.status_code, 200)
        novo_fen = resp_val.get_json()["estado"]["fen"]

        resp_ia = self.client.post(
            "/api/jogada",
            json={"fen": novo_fen, "dificuldade": "medio", "historico_fens": [fen_inicial, novo_fen]},
        )
        self.assertEqual(resp_ia.status_code, 200)
        dados = resp_ia.get_json()
        self.assertIsNotNone(dados["lance"])
        self.assertGreater(dados["telemetria"]["nos_avaliados"], 0)

    def test_fluxo_dois_jogadores_local(self):
        fen0 = chess.STARTING_FEN
        r1 = self.client.post("/api/validar", json={"fen": fen0, "lance": "e2e4", "historico_fens": [fen0]})
        self.assertEqual(r1.status_code, 200)
        fen1 = r1.get_json()["estado"]["fen"]
        self.assertEqual(r1.get_json()["estado"]["turno"], "pretas")

        r2 = self.client.post("/api/validar", json={"fen": fen1, "lance": "e7e5", "historico_fens": [fen0, fen1]})
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r2.get_json()["estado"]["turno"], "brancas")

    def test_api_resiste_a_payloads_malformados(self):
        casos_invalidos = [
            ("/api/validar", {"fen": chess.STARTING_FEN}),  # sem lance
            ("/api/validar", {"fen": "", "lance": "e2e4"}),
            ("/api/validar", {"fen": 123, "lance": "e2e4"}),
            ("/api/jogada", {"fen": "8/8/8/8/8/8/8/8 w - - 0 1"}),
            ("/api/analisar", {"fen": None}),
        ]
        for rota, payload in casos_invalidos:
            resp = self.client.post(rota, json=payload)
            self.assertEqual(resp.status_code, 400, f"Falhou em {rota} com {payload}")
            self.assertIn("erro", resp.get_json())


if __name__ == "__main__":
    unittest.main()
