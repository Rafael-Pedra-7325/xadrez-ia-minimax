(() => {
  const FEN_INICIAL = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
  const ARQUIVOS = ["a", "b", "c", "d", "e", "f", "g", "h"];

  const PECAS_SVG = {
    wK: `<svg class="piece-svg" viewBox="0 0 45 45"><g fill="none" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M22.5 11.63V6M20 8h5" stroke-linejoin="miter"/><path d="M22.5 25s4.5-7.5 3-10.5c0 0-1-2.5-3-2.5s-3 2.5-3 2.5c-1.5 3 3 10.5 3 10.5" fill="#fff" stroke-linecap="butt" stroke-linejoin="miter"/><path d="M11.5 37c5.5 3.5 15.5 3.5 21 0v-7s9-4.5 6-10.5c-4-6.5-13.5-3.5-16 4V27v-3.5c-3.5-7.5-13-10.5-16-4-3 6 5 10 5 10V37z" fill="#fff"/><path d="M11.5 30c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0"/></g></svg>`,
    wQ: `<svg class="piece-svg" viewBox="0 0 45 45"><g fill="#fff" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M8 12a2 2 0 1 1-4 0 2 2 0 1 1 4 0zm16.5-4.5a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM41 12a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM16 8.5a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM33 9a2 2 0 1 1-4 0 2 2 0 1 1 4 0z"/><path d="M9 26c8.5-1.5 21-1.5 27 0l2-12-7 11V11l-5.5 13.5-3-15-3 15-5.5-14V25L7 14l2 12z" stroke-linecap="butt"/><path d="M9 26c0 2 1.5 2 2.5 4 1 1.5 1 1 .5 3.5-1.5 1-1.5 2.5-1.5 2.5-1.5 1.5.5 2.5.5 2.5 6.5 1 16.5 1 23 0 0 0 1.5-1 0-2.5 0 0 .5-1.5-1-2.5-.5-2.5-.5-2 .5-3.5 1-2 2.5-2 2.5-4-8.5-1.5-18.5-1.5-27 0z" stroke-linecap="butt"/><path d="M11.5 30c3.5-1 18.5-1 22 0M12 33.5c6-1 15-1 21 0" fill="none"/></g></svg>`,
    wR: `<svg class="piece-svg" viewBox="0 0 45 45"><g fill="#fff" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9 39h27v-3H9v3zm3-3v-4h21v4H12zm-1-22V9h4v2h5V9h5v2h5V9h4v5" stroke-linecap="butt"/><path d="M34 14l-3 3H14l-3-3"/><path d="M31 17v12.5H14V17" stroke-linecap="butt" stroke-linejoin="miter"/><path d="M31 29.5l1.5 2.5h-20l1.5-2.5"/><path d="M11 14h23" fill="none" stroke-linejoin="miter"/></g></svg>`,
    wB: `<svg class="piece-svg" viewBox="0 0 45 45"><g fill="none" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><g fill="#fff" stroke-linecap="butt"><path d="M9 36c3.39-.97 10.11.43 13.5-2 3.39 2.43 10.11 1.03 13.5 2 0 0 1.65.54 3 2-.68.97-1.65.99-3 .5-3.39-.97-10.11.46-13.5-1-3.39 1.46-10.11.03-13.5 1-1.35.49-2.32.47-3-.5 1.35-1.46 3-2 3-2z"/><path d="M15 32c2.5 2.5 12.5 2.5 15 0 .5-1.5 0-2 0-2 0-2.5-2.5-4-2.5-4 5.5-1.5 6-11.5-5-15.5-11 4-10.5 14-5 15.5 0 0-2.5 1.5-2.5 4 0 0-.5.5 0 2z"/><path d="M25 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 1 1 5 0z"/></g><path d="M17.5 26h10M15 30h15m-7.5-14.5v5M20 18h5" stroke-linejoin="miter"/></g></svg>`,
    wN: `<svg class="piece-svg" viewBox="0 0 45 45"><g fill="none" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10c10.5 1 16.5 8 16 29H15c0-9 10-6.5 8-21" fill="#fff"/><path d="M24 18c.38 2.91-5.55 7.37-8 9-3 2-2.82 4.34-5 4-1.042-.94 1.41-3.04 0-3-1 0 .19 1.23-1 2-1 0-4.003 1-4-4 0-2 6-12 6-12s1.89-1.9 2-3.5c-.73-.994-.5-2-.5-3 1-1 3 2.5 3 2.5h2s.78-1.992 2.5-3c1 0 1 3 1 3" fill="#fff"/><path d="M9.5 25.5a.5.5 0 1 1-1 0 .5.5 0 1 1 1 0zm5.433-9.75a.5 1.5 30 1 1-.866-.5.5 1.5 30 1 1 .866.5z" fill="#0f172a"/></g></svg>`,
    wP: `<svg class="piece-svg" viewBox="0 0 45 45"><path d="M22.5 9c-2.21 0-4 1.79-4 4 0 .89.29 1.71.78 2.38C17.33 16.5 16 18.59 16 21c0 2.03.94 3.84 2.41 5.03-3 1.06-7.41 5.55-7.41 13.47h23c0-7.92-4.41-12.41-7.41-13.47 1.47-1.19 2.41-3 2.41-5.03 0-2.41-1.33-4.5-3.28-5.62.49-.67.78-1.49.78-2.38 0-2.21-1.79-4-4-4z" fill="#fff" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round"/></svg>`,
    bK: `<svg class="piece-svg" viewBox="0 0 45 45"><g fill="none" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M22.5 11.63V6" stroke-linejoin="miter"/><path d="M22.5 25s4.5-7.5 3-10.5c0 0-1-2.5-3-2.5s-3 2.5-3 2.5c-1.5 3 3 10.5 3 10.5" fill="#1e293b" stroke-linecap="butt" stroke-linejoin="miter"/><path d="M11.5 37c5.5 3.5 15.5 3.5 21 0v-7s9-4.5 6-10.5c-4-6.5-13.5-3.5-16 4V27v-3.5c-3.5-7.5-13-10.5-16-4-3 6 5 10 5 10V37z" fill="#1e293b"/><path d="M20 8h5" stroke-linejoin="miter"/><path d="M32 29.5s8.5-4 6.03-9.65C34.15 14 25 18 22.5 24.5l.01 2.1-.01-2.1C20 18 9.906 14 6.997 19.85c-2.497 5.65 4.853 9 4.853 9" stroke="#e2e8f0"/><path d="M11.5 30c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0" stroke="#e2e8f0"/></g></svg>`,
    bQ: `<svg class="piece-svg" viewBox="0 0 45 45"><g fill="#1e293b" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><g stroke="none"><circle cx="6" cy="12" r="2.75"/><circle cx="14" cy="9" r="2.75"/><circle cx="22.5" cy="8" r="2.75"/><circle cx="31" cy="9" r="2.75"/><circle cx="39" cy="12" r="2.75"/></g><path d="M9 26c8.5-1.5 21-1.5 27 0l2.5-12.5L31 25l-.3-14.1-5.2 13.6-3-14.5-3 14.5-5.2-13.6L14 25 6.5 13.5 9 26z" stroke-linecap="butt"/><path d="M9 26c0 2 1.5 2 2.5 4 1 1.5 1 1 .5 3.5-1.5 1-1.5 2.5-1.5 2.5-1.5 1.5.5 2.5.5 2.5 6.5 1 16.5 1 23 0 0 0 1.5-1 0-2.5 0 0 .5-1.5-1-2.5-.5-2.5-.5-2 .5-3.5 1-2 2.5-2 2.5-4-8.5-1.5-18.5-1.5-27 0z" stroke-linecap="butt"/><path d="M11 38.5a35 35 1 0 0 23 0" fill="none" stroke-linecap="butt"/><path d="M11 29a35 35 1 0 1 23 0m-21.5 2.5h20m-21 3a35 35 1 0 0 22 0" fill="none" stroke="#e2e8f0"/></g></svg>`,
    bR: `<svg class="piece-svg" viewBox="0 0 45 45"><g fill="#1e293b" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9 39h27v-3H9v3zm3.5-7l1.5-2.5h17l1.5 2.5h-20zm-.5 4v-4h21v4H12z" stroke-linecap="butt"/><path d="M14 29.5v-13h17v13H14z" stroke-linecap="butt" stroke-linejoin="miter"/><path d="M14 16.5L11 14h23l-3 2.5H14zM11 14V9h4v2h5V9h5v2h5V9h4v5H11z" stroke-linecap="butt"/><path d="M12 35.5h21m-20-4h19m-18-2h17m-17-13h17M11 14h23" fill="none" stroke="#e2e8f0" stroke-width="1.1" stroke-linejoin="miter"/></g></svg>`,
    bB: `<svg class="piece-svg" viewBox="0 0 45 45"><g fill="none" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><g fill="#1e293b" stroke-linecap="butt"><path d="M9 36c3.39-.97 10.11.43 13.5-2 3.39 2.43 10.11 1.03 13.5 2 0 0 1.65.54 3 2-.68.97-1.65.99-3 .5-3.39-.97-10.11.46-13.5-1-3.39 1.46-10.11.03-13.5 1-1.35.49-2.32.47-3-.5 1.35-1.46 3-2 3-2z"/><path d="M15 32c2.5 2.5 12.5 2.5 15 0 .5-1.5 0-2 0-2 0-2.5-2.5-4-2.5-4 5.5-1.5 6-11.5-5-15.5-11 4-10.5 14-5 15.5 0 0-2.5 1.5-2.5 4 0 0-.5.5 0 2z"/><path d="M25 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 1 1 5 0z"/></g><path d="M17.5 26h10M15 30h15m-7.5-14.5v5M20 18h5" stroke="#e2e8f0" stroke-linejoin="miter"/></g></svg>`,
    bN: `<svg class="piece-svg" viewBox="0 0 45 45"><g fill="none" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10c10.5 1 16.5 8 16 29H15c0-9 10-6.5 8-21" fill="#1e293b"/><path d="M24 18c.38 2.91-5.55 7.37-8 9-3 2-2.82 4.34-5 4-1.042-.94 1.41-3.04 0-3-1 0 .19 1.23-1 2-1 0-4.003 1-4-4 0-2 6-12 6-12s1.89-1.9 2-3.5c-.73-.994-.5-2-.5-3 1-1 3 2.5 3 2.5h2s.78-1.992 2.5-3c1 0 1 3 1 3" fill="#1e293b"/><path d="M9.5 25.5a.5.5 0 1 1-1 0 .5.5 0 1 1 1 0zm5.433-9.75a.5 1.5 30 1 1-.866-.5.5 1.5 30 1 1 .866.5z" fill="#e2e8f0" stroke="#e2e8f0"/></g></svg>`,
    bP: `<svg class="piece-svg" viewBox="0 0 45 45"><path d="M22.5 9c-2.21 0-4 1.79-4 4 0 .89.29 1.71.78 2.38C17.33 16.5 16 18.59 16 21c0 2.03.94 3.84 2.41 5.03-3 1.06-7.41 5.55-7.41 13.47h23c0-7.92-4.41-12.41-7.41-13.47 1.47-1.19 2.41-3 2.41-5.03 0-2.41-1.33-4.5-3.28-5.62.49-.67.78-1.49.78-2.38 0-2.21-1.79-4-4-4z" fill="#1e293b" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round"/></svg>`,
  };

  const estado = {
    partidaId: 0, // Controla geração da partida para descartar respostas atrasadas
    fen: FEN_INICIAL,
    turno: "brancas",
    corHumano: "brancas",
    invertido: false,
    dificuldade: "mestre",
    lancesLegais: [],
    casaSelecionada: null,
    ultimoLance: null,
    casaReiXeque: null,
    evalBrancasCp: 0,
    bloqueado: false,
    terminou: false,
    modoRaioX: false,
    somAtivo: true,
    pilhaEstados: [],
    historicoSan: [],
    historicoFens: [FEN_INICIAL],
    promocaoPendente: null,
    placar: { vitorias: 0, empates: 0, derrotas: 0 },
  };

  let abortControllerAtivo = null;

  const tabuleiroEl = document.getElementById("tabuleiro");
  const setasSvg = document.getElementById("setas-svg");
  const statusBanner = document.getElementById("status-banner");
  const statusTexto = document.getElementById("status-texto");
  const evalBarFill = document.getElementById("eval-bar-fill");
  const evalBarLabel = document.getElementById("eval-bar-label");
  const placarEvalEl = document.getElementById("placar-eval");
  const telNosEl = document.getElementById("tel-nos");
  const telTempoEl = document.getElementById("tel-tempo");
  const telMotivoEl = document.getElementById("tel-motivo");
  const listaHistoricoEl = document.getElementById("lista-historico");
  const modalPromocao = document.getElementById("modal-promocao");

  let audioCtx = null;
  function tocarSom(tipo) {
    if (!estado.somAtivo) return;
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      const t = audioCtx.currentTime;

      if (tipo === "move") {
        osc.type = "triangle";
        osc.frequency.setValueAtTime(320, t);
        osc.frequency.exponentialRampToValueAtTime(180, t + 0.07);
        gain.gain.setValueAtTime(0.09, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.08);
        osc.start(t);
        osc.stop(t + 0.08);
      } else if (tipo === "capture") {
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(480, t);
        osc.frequency.exponentialRampToValueAtTime(140, t + 0.11);
        gain.gain.setValueAtTime(0.09, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.12);
        osc.start(t);
        osc.stop(t + 0.12);
      } else if (tipo === "check") {
        osc.type = "sine";
        osc.frequency.setValueAtTime(660, t);
        osc.frequency.setValueAtTime(880, t + 0.09);
        gain.gain.setValueAtTime(0.1, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.22);
        osc.start(t);
        osc.stop(t + 0.22);
      }
    } catch (_) {}
  }

  function cancelarRequisicaoAtiva() {
    if (abortControllerAtivo) {
      try {
        abortControllerAtivo.abort();
      } catch (_) {}
      abortControllerAtivo = null;
    }
  }

  function fecharModalPromocao() {
    estado.promocaoPendente = null;
    modalPromocao.classList.add("hidden");
  }

  async function fetchApiSegura(url, payload, { tentativas = 2, timeoutMs = 25000 } = {}) {
    cancelarRequisicaoAtiva();
    const controller = new AbortController();
    abortControllerAtivo = controller;

    for (let tentativa = 1; tentativa <= tentativas; tentativa++) {
      const timer = setTimeout(() => controller.abort(), timeoutMs);
      try {
        const resp = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
          signal: controller.signal,
        });
        clearTimeout(timer);

        const textoBruto = await resp.text();
        let dados = null;
        try {
          dados = textoBruto ? JSON.parse(textoBruto) : {};
        } catch (_) {
          // Resposta HTML (ex: Render acordando ou 502 temporário)
          if (tentativa < tentativas && [502, 503, 504].includes(resp.status)) {
            atualizarStatus("⏳ Servidor acordando no Render, reconectando...", "turno-ia");
            await new Promise((r) => setTimeout(r, 1500));
            continue;
          }
          throw new Error("O servidor demorou a responder. Tente novamente.");
        }

        if (!resp.ok) {
          throw new Error(dados.erro || `Erro HTTP ${resp.status}`);
        }
        return dados;
      } catch (err) {
        clearTimeout(timer);
        if (err.name === "AbortError") {
          throw err;
        }
        if (tentativa < tentativas) {
          await new Promise((r) => setTimeout(r, 1200));
          continue;
        }
        throw err;
      }
    }
  }

  function carregarPlacar() {
    try {
      const salvo = localStorage.getItem("xadrez_ia_placar");
      if (salvo) estado.placar = { ...estado.placar, ...JSON.parse(salvo) };
    } catch (_) {}
    atualizarPlacarUI();
  }

  function salvarPlacar() {
    try {
      localStorage.setItem("xadrez_ia_placar", JSON.stringify(estado.placar));
    } catch (_) {}
    atualizarPlacarUI();
  }

  function atualizarPlacarUI() {
    document.getElementById("placar-vitorias").textContent = estado.placar.vitorias;
    document.getElementById("placar-empates").textContent = estado.placar.empates;
    document.getElementById("placar-derrotas").textContent = estado.placar.derrotas;
  }

  function parseFenMapa(fen) {
    const mapa = {};
    const parteTabuleiro = fen.split(" ")[0];
    const linhas = parteTabuleiro.split("/");
    linhas.forEach((linha, rIdx) => {
      const rank = 8 - rIdx;
      let fileIdx = 0;
      for (const ch of linha) {
        if (/\d/.test(ch)) {
          fileIdx += parseInt(ch, 10);
        } else {
          const casa = `${ARQUIVOS[fileIdx]}${rank}`;
          const cor = ch === ch.toUpperCase() ? "w" : "b";
          mapa[casa] = `${cor}${ch.toUpperCase()}`;
          fileIdx += 1;
        }
      }
    });
    return mapa;
  }

  function atualizarPecasCapturadas(mapa) {
    const inicial = { P: 8, N: 2, B: 2, R: 2, Q: 1, p: 8, n: 2, b: 2, r: 2, q: 1 };
    const simbolos = { P: "♙", N: "♘", B: "♗", R: "♖", Q: "♕", p: "♟", n: "♞", b: "♝", r: "♜", q: "♛" };
    const atuais = { P: 0, N: 0, B: 0, R: 0, Q: 0, p: 0, n: 0, b: 0, r: 0, q: 0 };

    Object.values(mapa).forEach((code) => {
      const letra = code[0] === "w" ? code[1] : code[1].toLowerCase();
      if (atuais[letra] !== undefined) atuais[letra] += 1;
    });

    let brancasPerdidas = "";
    let pretasPerdidas = "";
    ["Q", "R", "B", "N", "P"].forEach((p) => {
      const diffW = Math.max(0, inicial[p] - atuais[p]);
      brancasPerdidas += simbolos[p].repeat(diffW);
      const low = p.toLowerCase();
      const diffB = Math.max(0, inicial[low] - atuais[low]);
      pretasPerdidas += simbolos[low].repeat(diffB);
    });

    const capHumano = estado.corHumano === "brancas" ? pretasPerdidas : brancasPerdidas;
    const capIA = estado.corHumano === "brancas" ? brancasPerdidas : pretasPerdidas;
    document.getElementById("cap-humano").textContent = capHumano || "—";
    document.getElementById("cap-ia").textContent = capIA || "—";
  }

  function atualizarBarraAvaliacao(cp) {
    estado.evalBrancasCp = cp;
    const peoes = (cp / 100).toFixed(2);
    placarEvalEl.textContent = cp > 0 ? `+${peoes}` : peoes;

    const clamped = Math.max(-1000, Math.min(1000, cp));
    const pctBrancas = 50 + 50 * (2 / (1 + Math.exp(-0.004 * clamped)) - 1);
    evalBarFill.style.height = `${pctBrancas.toFixed(1)}%`;
    evalBarLabel.textContent = Math.abs(cp / 100).toFixed(1);
  }

  function renderizarTabuleiro() {
    const mapaPecas = parseFenMapa(estado.fen);
    atualizarPecasCapturadas(mapaPecas);
    tabuleiroEl.innerHTML = "";
    setasSvg.innerHTML = "";

    const destinosLegais = new Set();
    if (estado.casaSelecionada) {
      estado.lancesLegais.forEach((uci) => {
        if (uci.startsWith(estado.casaSelecionada)) {
          destinosLegais.add(uci.slice(2, 4));
        }
      });
    }

    const ranks = estado.invertido ? [1, 2, 3, 4, 5, 6, 7, 8] : [8, 7, 6, 5, 4, 3, 2, 1];
    const files = estado.invertido ? [7, 6, 5, 4, 3, 2, 1, 0] : [0, 1, 2, 3, 4, 5, 6, 7];

    ranks.forEach((rank, rVis) => {
      files.forEach((fIdx, cVis) => {
        const file = ARQUIVOS[fIdx];
        const casa = `${file}${rank}`;
        const isLight = (fIdx + rank) % 2 === 1;

        const sqEl = document.createElement("div");
        sqEl.className = `square ${isLight ? "light" : "dark"}`;
        sqEl.dataset.square = casa;

        if (estado.casaSelecionada === casa) sqEl.classList.add("selected");
        if (estado.ultimoLance && (estado.ultimoLance.startsWith(casa) || estado.ultimoLance.slice(2, 4) === casa)) {
          sqEl.classList.add("last-move");
        }
        if (estado.casaReiXeque === casa) sqEl.classList.add("in-check");

        if (cVis === 0) {
          const rLabel = document.createElement("span");
          rLabel.className = "coord-rank";
          rLabel.textContent = rank;
          sqEl.appendChild(rLabel);
        }
        if (rVis === 7) {
          const fLabel = document.createElement("span");
          fLabel.className = "coord-file";
          fLabel.textContent = file;
          sqEl.appendChild(fLabel);
        }

        const pecaCode = mapaPecas[casa];
        if (pecaCode && PECAS_SVG[pecaCode]) {
          sqEl.insertAdjacentHTML("beforeend", PECAS_SVG[pecaCode]);
        }

        if (destinosLegais.has(casa)) {
          const ind = document.createElement("span");
          ind.className = pecaCode ? "legal-ring" : "legal-dot";
          sqEl.appendChild(ind);
        }

        sqEl.addEventListener("click", () => aoClicarCasa(casa, pecaCode));
        tabuleiroEl.appendChild(sqEl);
      });
    });

    if (estado.modoRaioX && !estado.terminou && !estado.bloqueado) {
      atualizarRaioX();
    }
  }

  function desenharSetas(candidatos) {
    setasSvg.innerHTML = "";
    if (!candidatos || !candidatos.length) return;

    const defs = `<defs><marker id="arrowhead" markerWidth="4" markerHeight="4" refX="2.5" refY="2" orient="auto"><polygon points="0 0, 4 2, 0 4" fill="#38bdf8" /></marker></defs>`;
    setasSvg.insertAdjacentHTML("beforeend", defs);

    candidatos.slice(0, 3).forEach((cand, idx) => {
      const origem = cand.uci.slice(0, 2);
      const destino = cand.uci.slice(2, 4);
      const [x1, y1] = centroCasaSvg(origem);
      const [x2, y2] = centroCasaSvg(destino);
      const opacidade = idx === 0 ? 0.85 : 0.42;
      const largura = idx === 0 ? 14 : 9;

      const line = document.createElementNS("[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)", "line");
      line.setAttribute("x1", x1);
      line.setAttribute("y1", y1);
      line.setAttribute("x2", x2);
      line.setAttribute("y2", y2);
      line.setAttribute("stroke", "#38bdf8");
      line.setAttribute("stroke-width", largura);
      line.setAttribute("stroke-linecap", "round");
      line.setAttribute("opacity", opacidade);
      line.setAttribute("marker-end", "url(#arrowhead)");
      setasSvg.appendChild(line);
    });
  }

  function centroCasaSvg(casa) {
    const fIdx = ARQUIVOS.indexOf(casa[0]);
    const rank = parseInt(casa[1], 10);
    const col = estado.invertido ? 7 - fIdx : fIdx;
    const row = estado.invertido ? rank - 1 : 8 - rank;
    return [col * 100 + 50, row * 100 + 50];
  }

  function aoClicarCasa(casa, pecaCode) {
    if (estado.bloqueado || estado.terminou || estado.turno !== estado.corHumano) return;

    const prefixoCor = estado.corHumano === "brancas" ? "w" : "b";

    if (estado.casaSelecionada) {
      const prefixoLance = `${estado.casaSelecionada}${casa}`;
      const correspondentes = estado.lancesLegais.filter((u) => u.startsWith(prefixoLance));

      if (correspondentes.length > 0) {
        if (correspondentes[0].length === 5) {
          estado.promocaoPendente = prefixoLance;
          modalPromocao.classList.remove("hidden");
          return;
        }
        executarLanceHumano(correspondentes[0]);
        return;
      }
    }

    if (pecaCode && pecaCode.startsWith(prefixoCor)) {
      estado.casaSelecionada = estado.casaSelecionada === casa ? null : casa;
      renderizarTabuleiro();
    } else {
      estado.casaSelecionada = null;
      renderizarTabuleiro();
    }
  }

  async function executarLanceHumano(lanceUci) {
    const partidaAtual = estado.partidaId;
    estado.bloqueado = true;
    estado.casaSelecionada = null;

    const snapshotAntesLance = {
      fen: estado.fen,
      historicoSan: [...estado.historicoSan],
      historicoFens: [...estado.historicoFens],
      ultimoLance: estado.ultimoLance,
      casaReiXeque: estado.casaReiXeque,
      evalBrancasCp: estado.evalBrancasCp,
    };

    try {
      const dados = await fetchApiSegura("/api/validar", {
        fen: estado.fen,
        lance: lanceUci,
      });

      if (partidaAtual !== estado.partidaId) return;

      estado.pilhaEstados.push(snapshotAntesLance);
      estado.historicoFens.push(dados.estado.fen);
      aplicarRespostaEstado(dados.estado, dados.lance, dados.avaliacao_brancas_cp);

      if (!estado.terminou) {
        await turnoIA(partidaAtual);
      }
    } catch (e) {
      if (e.name === "AbortError" || partidaAtual !== estado.partidaId) return;
      estado.bloqueado = false;
      renderizarTabuleiro();
      atualizarStatus(`⚠️ ${e.message}`, "xeque");
    }
  }

  async function turnoIA(partidaAtual = estado.partidaId) {
    estado.bloqueado = true;
    atualizarStatus("🤖 IA calculando variantes na árvore Minimax...", "turno-ia");

    try {
      const dados = await fetchApiSegura("/api/jogada", {
        fen: estado.fen,
        dificuldade: estado.dificuldade,
        historico_fens: estado.historicoFens.slice(-12),
      });

      if (partidaAtual !== estado.partidaId) return;

      if (dados.telemetria) {
        telNosEl.textContent = dados.telemetria.nos_avaliados.toLocaleString("pt-BR");
        telTempoEl.textContent = `${dados.telemetria.tempo_ms} ms`;
        telMotivoEl.textContent = dados.telemetria.motivo;
      }

      estado.historicoFens.push(dados.estado.fen);
      aplicarRespostaEstado(
        dados.estado,
        dados.lance,
        dados.telemetria ? dados.telemetria.avaliacao_brancas_cp : estado.evalBrancasCp
      );
    } catch (e) {
      if (e.name === "AbortError" || partidaAtual !== estado.partidaId) return;
      estado.bloqueado = false;
      renderizarTabuleiro();
      atualizarStatus(`⚠️ ${e.message} (Clique em Nova Partida ou Desfazer)`, "xeque");
    }
  }

  function aplicarRespostaEstado(novoEstado, infoLance, evalBrancasCp) {
    estado.fen = novoEstado.fen;
    estado.turno = novoEstado.turno;
    estado.lancesLegais = novoEstado.lances_legais || [];
    estado.casaReiXeque = novoEstado.casa_rei_xeque || null;
    estado.terminou = Boolean(novoEstado.terminou);
    estado.bloqueado = false;

    if (infoLance) {
      estado.ultimoLance = infoLance.uci;
      estado.historicoSan.push(infoLance.san);
      atualizarHistoricoUI();

      if (infoLance.xeque) tocarSom("check");
      else if (infoLance.captura) tocarSom("capture");
      else tocarSom("move");
    }

    if (typeof evalBrancasCp === "number") {
      atualizarBarraAvaliacao(evalBrancasCp);
    }

    renderizarTabuleiro();

    if (novoEstado.terminou) {
      if (novoEstado.vencedor === "empate") {
        estado.placar.empates += 1;
        atualizarStatus(`🤝 Empate por ${novoEstado.motivo_fim}!`, "xeque");
      } else if (novoEstado.vencedor === estado.corHumano) {
        estado.placar.vitorias += 1;
        atualizarStatus(`🎉 Vitória por ${novoEstado.motivo_fim}! Você derrotou a IA!`, "resultado-vitoria");
      } else {
        estado.placar.derrotas += 1;
        atualizarStatus(`🤖 Fim de jogo (${novoEstado.motivo_fim}) — A IA venceu.`, "resultado-derrota");
      }
      salvarPlacar();
      return;
    }

    if (novoEstado.xeque) {
      atualizarStatus("⚠️ XEQUE! Proteja seu Rei.", "xeque");
    } else if (estado.turno === estado.corHumano) {
      atualizarStatus("Sua vez! Selecione uma peça para mover.", "turno-humano");
    }
  }

  function atualizarHistoricoUI() {
    if (!estado.historicoSan.length) {
      listaHistoricoEl.innerHTML = '<li class="empty-history">Nenhum lance realizado ainda.</li>';
      return;
    }
    listaHistoricoEl.innerHTML = "";
    for (let i = 0; i < estado.historicoSan.length; i += 2) {
      const num = Math.floor(i / 2) + 1;
      const branca = estado.historicoSan[i] || "";
      const preta = estado.historicoSan[i + 1] || "";
      const li = document.createElement("li");
      li.innerHTML = `<span>${num}.</span><strong>${branca}</strong><span>${preta}</span>`;
      listaHistoricoEl.appendChild(li);
    }
    listaHistoricoEl.scrollTop = listaHistoricoEl.scrollHeight;
  }

  function atualizarStatus(texto, classe) {
    statusTexto.textContent = texto;
    statusBanner.className = `status-banner ${classe}`;
  }

  async function atualizarRaioX() {
    const fenAlvo = estado.fen;
    const partidaAtual = estado.partidaId;
    try {
      const resp = await fetch("/api/analisar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fen: fenAlvo }),
      });
      const dados = await resp.json();
      if (
        resp.ok &&
        dados.avaliacoes &&
        partidaAtual === estado.partidaId &&
        fenAlvo === estado.fen &&
        estado.modoRaioX
      ) {
        desenharSetas(dados.avaliacoes);
      }
    } catch (_) {}
  }

  async function pedirDica() {
    if (estado.bloqueado || estado.terminou) return;
    const fenAlvo = estado.fen;
    const partidaAtual = estado.partidaId;
    try {
      const resp = await fetch("/api/analisar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fen: fenAlvo }),
      });
      const dados = await resp.json();
      if (!resp.ok || !dados.melhor_lance || partidaAtual !== estado.partidaId || fenAlvo !== estado.fen) {
        return;
      }

      desenharSetas([dados.melhor_lance]);
      const origem = dados.melhor_lance.uci.slice(0, 2);
      const destino = dados.melhor_lance.uci.slice(2, 4);
      tabuleiroEl.querySelectorAll(".square").forEach((s) => {
        s.classList.remove("hint-square");
        if (s.dataset.square === origem || s.dataset.square === destino) {
          s.classList.add("hint-square");
        }
      });
      telMotivoEl.textContent = `Dica tática: jogue ${dados.melhor_lance.san} (${dados.nos_avaliados} nós analisados).`;
    } catch (_) {}
  }

  async function iniciarNovaPartida() {
    cancelarRequisicaoAtiva();
    fecharModalPromocao();
    estado.partidaId += 1;
    const partidaAtual = estado.partidaId;

    estado.fen = FEN_INICIAL;
    estado.turno = "brancas";
    estado.casaSelecionada = null;
    estado.ultimoLance = null;
    estado.casaReiXeque = null;
    estado.terminou = false;
    estado.bloqueado = false;
    estado.pilhaEstados = [];
    estado.historicoSan = [];
    estado.historicoFens = [FEN_INICIAL];
    estado.invertido = estado.corHumano === "pretas";

    estado.lancesLegais = [
      "a2a3", "a2a4", "b2b3", "b2b4", "c2c3", "c2c4", "d2d3", "d2d4",
      "e2e3", "e2e4", "f2f3", "f2f4", "g2g3", "g2g4", "h2h3", "h2h4",
      "b1a3", "b1c3", "g1f3", "g1h3",
    ];

    atualizarHistoricoUI();
    atualizarBarraAvaliacao(0);
    telNosEl.textContent = "—";
    telTempoEl.textContent = "—";
    telMotivoEl.textContent = "Nova partida iniciada.";
    renderizarTabuleiro();

    if (estado.corHumano === "pretas") {
      await turnoIA(partidaAtual);
    } else {
      atualizarStatus("Sua vez! Selecione uma peça branca para jogar.", "turno-humano");
    }
  }

  async function desfazerJogada() {
    if (estado.bloqueado || !estado.pilhaEstados.length) return;
    fecharModalPromocao();

    const anterior = estado.pilhaEstados.pop();
    const partidaAtual = estado.partidaId;
    estado.bloqueado = true;
    estado.fen = anterior.fen;
    estado.historicoSan = anterior.historicoSan;
    estado.historicoFens = anterior.historicoFens;
    estado.ultimoLance = anterior.ultimoLance;
    estado.casaReiXeque = anterior.casaReiXeque;
    estado.terminou = false;
    estado.casaSelecionada = null;
    atualizarHistoricoUI();
    atualizarBarraAvaliacao(anterior.evalBrancasCp || 0);

    try {
      const dados = await fetchApiSegura("/api/analisar", { fen: estado.fen });
      if (partidaAtual !== estado.partidaId) return;

      if (dados.lances_legais) {
        estado.lancesLegais = dados.lances_legais;
      }
      estado.turno = estado.corHumano;
      estado.bloqueado = false;
      renderizarTabuleiro();
      atualizarStatus("Jogada desfeita. Sua vez!", "turno-humano");
    } catch (e) {
      if (e.name === "AbortError" || partidaAtual !== estado.partidaId) return;
      estado.bloqueado = false;
      renderizarTabuleiro();
      atualizarStatus(`⚠️ Erro ao desfazer: ${e.message}`, "xeque");
    }
  }

  document.querySelectorAll(".promo-options button").forEach((btn) => {
    btn.addEventListener("click", () => {
      const peca = btn.dataset.piece;
      const prefixo = estado.promocaoPendente;
      fecharModalPromocao();
      if (prefixo) {
        executarLanceHumano(`${prefixo}${peca}`);
      }
    });
  });

  function configurarSegmented(id, cb) {
    const el = document.getElementById(id);
    el.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => {
        el.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        cb(btn.dataset.value);
      });
    });
  }

  configurarSegmented("grupo-dificuldade", (v) => {
    estado.dificuldade = v;
    iniciarNovaPartida();
  });

  configurarSegmented("grupo-cor", (v) => {
    estado.corHumano = v;
    iniciarNovaPartida();
  });

  document.getElementById("btn-reiniciar").addEventListener("click", iniciarNovaPartida);
  document.getElementById("btn-desfazer").addEventListener("click", desfazerJogada);
  document.getElementById("btn-zerar-placar").addEventListener("click", () => {
    estado.placar = { vitorias: 0, empates: 0, derrotas: 0 };
    salvarPlacar();
  });

  document.getElementById("btn-inverter").addEventListener("click", () => {
    estado.invertido = !estado.invertido;
    renderizarTabuleiro();
  });

  const btnRaioX = document.getElementById("btn-raiox");
  btnRaioX.addEventListener("click", () => {
    estado.modoRaioX = !estado.modoRaioX;
    btnRaioX.classList.toggle("active", estado.modoRaioX);
    renderizarTabuleiro();
  });

  document.getElementById("btn-dica").addEventListener("click", pedirDica);

  const btnSom = document.getElementById("btn-som");
  btnSom.addEventListener("click", () => {
    estado.somAtivo = !estado.somAtivo;
    btnSom.textContent = estado.somAtivo ? "🔊" : "🔇";
  });

  document.getElementById("btn-copiar-fen").addEventListener("click", () => {
    navigator.clipboard?.writeText(estado.fen);
    telMotivoEl.textContent = "Código FEN copiado para a área de transferência!";
  });

  document.addEventListener("keydown", (e) => {
    if (e.key.toLowerCase() === "r") iniciarNovaPartida();
    if (e.key.toLowerCase() === "z") desfazerJogada();
  });

  carregarPlacar();
  iniciarNovaPartida();
})();
