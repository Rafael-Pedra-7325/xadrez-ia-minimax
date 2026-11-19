# ♟️ IA de Xadrez — Minimax + Poda Alfa-Beta

Aplicação Web e CLI em Python (Flask + `python-chess`) com Inteligência Artificial baseada em **Minimax com Poda Alfa-Beta**, ordenação tática de capturas (**MVV-LVA**) e avaliação posicional por **Piece-Square Tables**.

## ✨ Funcionalidades
- **Tabuleiro Interativo 8x8**: peças vetoriais SVG, indicadores de lances legais, modal de promoção de peão, inversão de lado e desfazer jogada (`Z`).
- **Barra de Avaliação em Tempo Real**: exibe a vantagem em peões (centipawns) lance a lance.
- **Cérebro da IA & Visão Raio-X**: desenha setas com as 3 melhores variantes calculadas, mostra nós analisados e tempo de resposta em milissegundos.
- **3 Níveis de Dificuldade**: Fácil (Aprendiz), Médio (Desafiante) e Mestre.

## 🚀 Como Executar Localmente
```bash
pip install -r requirements.txt
python app.py
