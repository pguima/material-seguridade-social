# -*- coding: utf-8 -*-
"""
Gerador do HTML da apostila premium (A4, pronto para PDF).

Uso interno: chamado por build_pdf.py.
    gerar(paginas=None) -> str (html)

`paginas` é um dicionário {ancora: numero_de_pagina} usado no segundo passe
para preencher o sumário com os números reais.
"""

import html as _html
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apostila_config import (TITULO, SUBTITULO, CARGO, PARTES,
                             SECOES_REMOVIDAS, SUBSTITUICOES)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===========================================================================
# ILUSTRAÇÕES (SVG)
# ===========================================================================

EMBLEMA = """
<svg class="emblema" viewBox="0 0 200 210" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Emblema da Seguridade Social">
  <defs>
    <linearGradient id="gEsc" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F3C969"/><stop offset="1" stop-color="#C79A2E"/>
    </linearGradient>
  </defs>
  <path d="M100 6 L186 34 V104c0 48-34 82-86 100C48 186 14 152 14 104V34Z"
        fill="none" stroke="url(#gEsc)" stroke-width="3.2"/>
  <path d="M100 18 L174 42 V104c0 41-29 71-74 87-45-16-74-46-74-87V42Z"
        fill="rgba(255,255,255,.05)" stroke="rgba(243,201,105,.35)" stroke-width="1"/>
  <path d="M46 78 L100 50 L154 78" fill="none" stroke="url(#gEsc)" stroke-width="3"
        stroke-linecap="round" stroke-linejoin="round"/>
  <g stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity=".92">
    <line x1="66" y1="90" x2="66" y2="140"/>
    <line x1="100" y1="90" x2="100" y2="140"/>
    <line x1="134" y1="90" x2="134" y2="140"/>
  </g>
  <g fill="url(#gEsc)">
    <rect x="59" y="84" width="14" height="6" rx="1.6"/>
    <rect x="93" y="84" width="14" height="6" rx="1.6"/>
    <rect x="127" y="84" width="14" height="6" rx="1.6"/>
  </g>
  <rect x="52" y="140" width="96" height="6" rx="2" fill="url(#gEsc)"/>
  <rect x="44" y="150" width="112" height="5" rx="2" fill="rgba(243,201,105,.55)"/>
</svg>
"""

ILUSTRACOES = {
"tripe": """
<svg viewBox="0 0 420 200" xmlns="http://www.w3.org/2000/svg">
  <path d="M40 62 Q210 6 380 62" fill="none" stroke="#C79A2E" stroke-width="2.5"/>
  <g stroke="#0E2A47" stroke-width="2.4" fill="none">
    <rect x="66" y="72" width="52" height="86" rx="3"/>
    <rect x="184" y="72" width="52" height="86" rx="3"/>
    <rect x="302" y="72" width="52" height="86" rx="3"/>
  </g>
  <g fill="#EAF2FA" stroke="#1B4F82" stroke-width="1.2">
    <circle cx="92" cy="104" r="13"/><circle cx="210" cy="104" r="13"/><circle cx="328" cy="104" r="13"/>
  </g>
  <g stroke="#1B4F82" stroke-width="2" stroke-linecap="round" fill="none">
    <path d="M86 104h12M92 98v12"/>
    <path d="M204 108c4-6 8-6 12 0M210 98v4"/>
    <path d="M204 104h12"/>
  </g>
  <g fill="#0E2A47" opacity=".82" font-family="Segoe UI,Arial" font-size="11" text-anchor="middle">
    <text x="92" y="146">SAÚDE</text><text x="210" y="146">PREVID.</text><text x="328" y="146">ASSIST.</text>
  </g>
  <rect x="44" y="164" width="332" height="7" rx="3" fill="#C79A2E"/>
  <rect x="30" y="176" width="360" height="5" rx="2.5" fill="#0E2A47" opacity=".25"/>
</svg>""",

"matriz": """
<svg viewBox="0 0 420 200" xmlns="http://www.w3.org/2000/svg">
  <rect x="46" y="26" width="250" height="152" rx="6" fill="#FFFFFF" stroke="#0E2A47" stroke-width="2.2"/>
  <rect x="46" y="26" width="250" height="26" rx="6" fill="#0E2A47"/>
  <rect x="46" y="44" width="250" height="8" fill="#0E2A47"/>
  <g stroke="#D9E0E7" stroke-width="1.2">
    <line x1="46" y1="78" x2="296" y2="78"/><line x1="46" y1="104" x2="296" y2="104"/>
    <line x1="46" y1="130" x2="296" y2="130"/><line x1="46" y1="156" x2="296" y2="156"/>
    <line x1="120" y1="52" x2="120" y2="178"/><line x1="238" y1="52" x2="238" y2="178"/>
  </g>
  <g fill="#55636F" opacity=".45">
    <rect x="58" y="62" width="50" height="6" rx="3"/><rect x="58" y="88" width="46" height="6" rx="3"/>
    <rect x="58" y="114" width="52" height="6" rx="3"/><rect x="58" y="140" width="42" height="6" rx="3"/>
    <rect x="132" y="62" width="88" height="6" rx="3"/><rect x="132" y="88" width="74" height="6" rx="3"/>
    <rect x="132" y="114" width="92" height="6" rx="3"/><rect x="132" y="140" width="68" height="6" rx="3"/>
  </g>
  <g>
    <circle cx="266" cy="65" r="7" fill="#9B2226"/><circle cx="266" cy="91" r="7" fill="#9B2226"/>
    <circle cx="266" cy="117" r="7" fill="#C77B14"/><circle cx="266" cy="143" r="7" fill="#B99400"/>
  </g>
  <circle cx="336" cy="92" r="40" fill="none" stroke="#C79A2E" stroke-width="4"/>
  <line x1="365" y1="121" x2="392" y2="150" stroke="#C79A2E" stroke-width="6" stroke-linecap="round"/>
  <path d="M320 92l11 12 21-24" fill="none" stroke="#0E2A47" stroke-width="4"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

"rgps": """
<svg viewBox="0 0 420 200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="210" cy="100" r="34" fill="#0E2A47"/>
  <text x="210" y="105" fill="#F3C969" font-family="Georgia,serif" font-size="17"
        text-anchor="middle" font-weight="bold">RGPS</text>
  <g stroke="#C79A2E" stroke-width="2" stroke-dasharray="5 4">
    <line x1="176" y1="100" x2="96" y2="52"/><line x1="176" y1="100" x2="88" y2="100"/>
    <line x1="176" y1="100" x2="96" y2="148"/><line x1="244" y1="100" x2="324" y2="52"/>
    <line x1="244" y1="100" x2="332" y2="100"/><line x1="244" y1="100" x2="324" y2="148"/>
  </g>
  <g fill="#EAF2FA" stroke="#1B4F82" stroke-width="2">
    <circle cx="76" cy="46" r="17"/><circle cx="68" cy="100" r="17"/><circle cx="76" cy="154" r="17"/>
    <circle cx="344" cy="46" r="17"/><circle cx="352" cy="100" r="17"/><circle cx="344" cy="154" r="17"/>
  </g>
  <g fill="#1B4F82">
    <circle cx="76" cy="41" r="5"/><path d="M66 56c0-6 20-6 20 0z"/>
    <circle cx="68" cy="95" r="5"/><path d="M58 110c0-6 20-6 20 0z"/>
    <circle cx="76" cy="149" r="5"/><path d="M66 164c0-6 20-6 20 0z"/>
    <circle cx="344" cy="41" r="5"/><path d="M334 56c0-6 20-6 20 0z"/>
    <circle cx="352" cy="95" r="5"/><path d="M342 110c0-6 20-6 20 0z"/>
    <circle cx="344" cy="149" r="5"/><path d="M334 164c0-6 20-6 20 0z"/>
  </g>
</svg>""",

"beneficios": """
<svg viewBox="0 0 420 200" xmlns="http://www.w3.org/2000/svg">
  <rect x="58" y="24" width="148" height="156" rx="7" fill="#FFFFFF" stroke="#0E2A47" stroke-width="2.4"/>
  <rect x="58" y="24" width="148" height="12" rx="7" fill="#0E2A47"/>
  <rect x="58" y="30" width="148" height="6" fill="#0E2A47"/>
  <g fill="#55636F" opacity=".38">
    <rect x="76" y="56" width="112" height="7" rx="3.5"/><rect x="76" y="76" width="92" height="7" rx="3.5"/>
    <rect x="76" y="96" width="104" height="7" rx="3.5"/><rect x="76" y="116" width="72" height="7" rx="3.5"/>
    <rect x="76" y="136" width="96" height="7" rx="3.5"/>
  </g>
  <g fill="none" stroke="#C79A2E" stroke-width="2.6">
    <ellipse cx="286" cy="152" rx="42" ry="13"/><ellipse cx="286" cy="132" rx="42" ry="13"/>
    <ellipse cx="286" cy="112" rx="42" ry="13"/>
    <path d="M244 112v40M328 112v40"/>
  </g>
  <path d="M286 22l38 14v30c0 21-15 36-38 44-23-8-38-23-38-44V36Z"
        fill="#EAF2FA" stroke="#0E2A47" stroke-width="2.4"/>
  <path d="M270 62l11 12 22-24" fill="none" stroke="#1B6B4A" stroke-width="4.5"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

"custeio": """
<svg viewBox="0 0 420 200" xmlns="http://www.w3.org/2000/svg">
  <g fill="none" stroke="#C79A2E" stroke-width="2.6" stroke-linecap="round">
    <path d="M46 40h72c14 0 22 8 22 22v22"/><path d="M46 100h94"/>
    <path d="M46 160h72c14 0 22-8 22-22v-22"/>
  </g>
  <g fill="#C79A2E"><path d="M138 92l14 8-14 8z"/><path d="M138 92l14 8-14 8z" opacity="0"/></g>
  <polygon points="140,100 128,93 128,107" fill="#C79A2E"/>
  <g fill="#EAF2FA" stroke="#1B4F82" stroke-width="2">
    <circle cx="40" cy="40" r="16"/><circle cx="40" cy="100" r="16"/><circle cx="40" cy="160" r="16"/>
  </g>
  <g fill="#1B4F82" font-family="Segoe UI,Arial" font-size="12" text-anchor="middle" font-weight="600">
    <text x="40" y="45">E</text><text x="40" y="105">T</text><text x="40" y="165">C</text>
  </g>
  <rect x="176" y="44" width="164" height="112" rx="8" fill="#0E2A47"/>
  <rect x="188" y="56" width="140" height="88" rx="5" fill="none" stroke="#F3C969" stroke-width="2"/>
  <circle cx="258" cy="100" r="26" fill="none" stroke="#F3C969" stroke-width="3"/>
  <circle cx="258" cy="100" r="8" fill="#F3C969"/>
  <g stroke="#F3C969" stroke-width="3" stroke-linecap="round">
    <line x1="258" y1="66" x2="258" y2="76"/><line x1="258" y1="124" x2="258" y2="134"/>
    <line x1="224" y1="100" x2="234" y2="100"/><line x1="282" y1="100" x2="292" y2="100"/>
  </g>
  <g fill="none" stroke="#C79A2E" stroke-width="2.6" stroke-linecap="round">
    <path d="M340 100h34"/>
  </g>
  <polygon points="384,100 370,93 370,107" fill="#C79A2E"/>
</svg>""",

"rpps": """
<svg viewBox="0 0 420 200" xmlns="http://www.w3.org/2000/svg">
  <g stroke="#0E2A47" stroke-width="2.4" fill="#FFFFFF">
    <path d="M34 78 L94 46 L154 78 V162 H34 Z"/>
    <path d="M266 78 L326 46 L386 78 V162 H266 Z"/>
  </g>
  <g fill="#EAF2FA" stroke="#1B4F82" stroke-width="1.4">
    <rect x="54" y="96" width="20" height="26" rx="2"/><rect x="84" y="96" width="20" height="26" rx="2"/>
    <rect x="114" y="96" width="20" height="26" rx="2"/>
    <rect x="286" y="96" width="20" height="26" rx="2"/><rect x="316" y="96" width="20" height="26" rx="2"/>
    <rect x="346" y="96" width="20" height="26" rx="2"/>
  </g>
  <g fill="#0E2A47" font-family="Georgia,serif" font-size="14" text-anchor="middle" font-weight="bold">
    <text x="94" y="152">RGPS</text><text x="326" y="152">RPPS</text>
  </g>
  <path d="M158 108 Q210 74 262 108" fill="none" stroke="#C79A2E" stroke-width="3"/>
  <path d="M262 128 Q210 162 158 128" fill="none" stroke="#C79A2E" stroke-width="3"/>
  <polygon points="266,108 250,102 252,114" fill="#C79A2E"/>
  <polygon points="154,128 170,122 168,134" fill="#C79A2E"/>
  <text x="210" y="96" fill="#55636F" font-family="Segoe UI,Arial" font-size="10"
        text-anchor="middle">contagem recíproca</text>
</svg>""",

"revisao": """
<svg viewBox="0 0 420 200" xmlns="http://www.w3.org/2000/svg">
  <rect x="52" y="22" width="176" height="158" rx="8" fill="#FFFFFF" stroke="#0E2A47" stroke-width="2.4"/>
  <rect x="52" y="22" width="176" height="30" rx="8" fill="#0E2A47"/>
  <rect x="52" y="42" width="176" height="10" fill="#0E2A47"/>
  <g>
    <rect x="70" y="70" width="16" height="16" rx="3" fill="none" stroke="#1B6B4A" stroke-width="2.2"/>
    <path d="M73 78l4 5 8-9" fill="none" stroke="#1B6B4A" stroke-width="2.6" stroke-linecap="round"/>
    <rect x="70" y="102" width="16" height="16" rx="3" fill="none" stroke="#1B6B4A" stroke-width="2.2"/>
    <path d="M73 110l4 5 8-9" fill="none" stroke="#1B6B4A" stroke-width="2.6" stroke-linecap="round"/>
    <rect x="70" y="134" width="16" height="16" rx="3" fill="none" stroke="#9AA6B2" stroke-width="2.2"/>
  </g>
  <g fill="#55636F" opacity=".38">
    <rect x="98" y="74" width="106" height="7" rx="3.5"/><rect x="98" y="106" width="92" height="7" rx="3.5"/>
    <rect x="98" y="138" width="80" height="7" rx="3.5"/>
  </g>
  <circle cx="322" cy="100" r="52" fill="none" stroke="#C79A2E" stroke-width="3"/>
  <circle cx="322" cy="100" r="43" fill="#FDF6E3"/>
  <g stroke="#0E2A47" stroke-width="3.4" stroke-linecap="round">
    <line x1="322" y1="100" x2="322" y2="72"/><line x1="322" y1="100" x2="344" y2="112"/>
  </g>
  <circle cx="322" cy="100" r="4.5" fill="#C79A2E"/>
  <g stroke="#0E2A47" stroke-width="2.4" stroke-linecap="round" opacity=".55">
    <line x1="322" y1="52" x2="322" y2="60"/><line x1="370" y1="100" x2="362" y2="100"/>
    <line x1="322" y1="148" x2="322" y2="140"/><line x1="274" y1="100" x2="282" y2="100"/>
  </g>
</svg>""",

"caderno": """
<svg viewBox="0 0 420 200" xmlns="http://www.w3.org/2000/svg">
  <rect x="92" y="22" width="200" height="158" rx="8" fill="#FFFFFF" stroke="#0E2A47" stroke-width="2.4"/>
  <rect x="92" y="22" width="26" height="158" rx="8" fill="#0E2A47"/>
  <rect x="112" y="22" width="8" height="158" fill="#0E2A47"/>
  <g fill="#F3C969"><circle cx="105" cy="52" r="4"/><circle cx="105" cy="86" r="4"/>
    <circle cx="105" cy="120" r="4"/><circle cx="105" cy="154" r="4"/></g>
  <g fill="#9B2226"><circle cx="140" cy="60" r="6"/><circle cx="140" cy="96" r="6"/></g>
  <g fill="#1B6B4A"><circle cx="140" cy="132" r="6"/></g>
  <g fill="#55636F" opacity=".38">
    <rect x="158" y="56" width="112" height="7" rx="3.5"/><rect x="158" y="76" width="88" height="6" rx="3"/>
    <rect x="158" y="92" width="112" height="7" rx="3.5"/><rect x="158" y="112" width="76" height="6" rx="3"/>
    <rect x="158" y="128" width="112" height="7" rx="3.5"/><rect x="158" y="148" width="96" height="6" rx="3"/>
  </g>
  <g transform="rotate(38 330 108)">
    <rect x="318" y="34" width="22" height="112" rx="4" fill="#C79A2E"/>
    <rect x="318" y="34" width="22" height="18" rx="4" fill="#0E2A47"/>
    <polygon points="318,146 340,146 329,172" fill="#F3C969"/>
    <polygon points="325,162 333,162 329,172" fill="#16202B"/>
  </g>
</svg>""",
}

ICONES = {
"alvo": '<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="10" cy="10" r="3.4" fill="currentColor"/></svg>',
"atencao": '<svg viewBox="0 0 20 20"><path d="M10 2.4 19 17.6H1Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M10 7.6v4.6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="10" cy="15" r="1.2" fill="currentColor"/></svg>',
"memorize": '<svg viewBox="0 0 20 20"><path d="M7 3.2c-2.4 0-4 1.7-4 3.6 0 .9.3 1.5.7 2.1-.6.6-.9 1.4-.9 2.3 0 2 1.7 3.6 3.9 3.6.4 1.3 1.6 2 3.3 2s2.9-.7 3.3-2c2.2 0 3.9-1.6 3.9-3.6 0-.9-.3-1.7-.9-2.3.4-.6.7-1.2.7-2.1 0-1.9-1.6-3.6-4-3.6-1 0-1.9.3-2.5.9-.6-.6-1.5-.9-2.5-.9Z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M10 4.1v11.7" stroke="currentColor" stroke-width="1.4"/></svg>',
"pegadinha": '<svg viewBox="0 0 20 20"><path d="M10 2.6v6.2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M10 8.8c3.2 0 5.4 2.1 5.4 4.5S13.2 17.6 10 17.6 4.6 15.6 4.6 13.3 6.8 8.8 10 8.8Z" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="10" cy="3" r="1.6" fill="currentColor"/></svg>',
"certo": '<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="8.2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M6 10.3 8.8 13 14 7.4" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
"errado": '<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="8.2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M6.8 6.8 13.2 13.2M13.2 6.8 6.8 13.2" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
"revisao": '<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M10 5.4V10l3.2 2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
"critico": '<svg viewBox="0 0 20 20"><path d="M10 1.8 18 6v8l-8 4.2L2 14V6Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M10 6.4v5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="10" cy="14" r="1.2" fill="currentColor"/></svg>',
"bloqueio": '<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="8.2" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M4.6 4.6 15.4 15.4" stroke="currentColor" stroke-width="1.9"/></svg>',
"nota": '<svg viewBox="0 0 20 20"><path d="M4 3.4h12v13.2H4Z" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M7 7.4h6M7 10.4h6M7 13.4h4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
}

CALLOUTS = [
    ("\U0001F3AF", "alvo",      "Como cai na prova", "alvo"),
    ("⚠",     "atencao",   "Atenção",           "atencao"),
    ("\U0001F9E0", "memorize",  "Memorize",          "memorize"),
    ("\U0001F3A3", "pegadinha", "Pegadinha",         "pegadinha"),
    ("❌",     "errado",    "Assertiva errada",  "errado"),
    ("✅",     "certo",     "Assertiva certa",   "certo"),
    ("\U0001F534", "critico",   "Prioridade máxima", "critico"),
    ("⏱",     "revisao",   "Revisão",           "revisao"),
    ("⛔",     "bloqueio",  "Pare",              "bloqueio"),
]

# ===========================================================================
# LIMPEZA DO MARKDOWN
# ===========================================================================

TITULOS_ARQUIVO = {}
for _p in PARTES:
    for _a, _t, _r, _s in _p["itens"]:
        TITULOS_ARQUIVO[os.path.basename(_a)] = _t

RE_LINK_MD = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
RE_ARQ_MD = re.compile(r"`?([A-Za-z0-9_./-]+\.md)`?")
RE_PROX = re.compile(r"^\*\*Próximo módulo:\*\*\s*(.+?)\s*$", re.M)


def _titulo_de(arquivo):
    base = os.path.basename(arquivo).strip("`")
    if base in TITULOS_ARQUIVO:
        return TITULOS_ARQUIVO[base]
    nome = re.sub(r"\.md$", "", base)
    nome = re.sub(r"^M(\d+)-", r"Módulo \1 — ", nome)
    return nome.replace("-", " ")


def limpar(md, secoes_removidas=True):
    """Remove referências de infraestrutura e adapta o texto ao produto impresso."""
    # blocos de comando (powershell / shell)
    md = re.sub(r"```(?:powershell|bash|sh)\n.*?```\n?", "", md, flags=re.S)

    # seções inteiras que não fazem sentido no PDF
    if secoes_removidas:
        for titulo in SECOES_REMOVIDAS:
            md = re.sub(r"^##\s+" + re.escape(titulo) + r"\s*$.*?(?=^##\s|\Z)",
                        "", md, flags=re.S | re.M)

    # bloco sobre o gerador
    md = re.sub(r"^### Os \.md são a FONTE.*?(?=^##\s|\Z)", "", md, flags=re.S | re.M)
    md = re.sub(r"^\*\*Para gerar o PDF:\*\*.*?$", "", md, flags=re.M)
    md = re.sub(r"^## Como imprimir\s*$.*?(?=^##\s|\Z)", "", md, flags=re.S | re.M)

    # substituições literais configuradas
    for de, para in SUBSTITUICOES:
        md = md.replace(de, para)

    # "Próximo módulo: `arquivo.md` 🔴"  ->  chip com o título real
    # navegacao "Proximo modulo" nao faz sentido em livro unico com sumario
    md = RE_PROX.sub("", md)

    # links markdown -> só o texto
    md = RE_LINK_MD.sub(lambda m: m.group(1), md)

    # qualquer arquivo .md remanescente -> título legível
    md = RE_ARQ_MD.sub(lambda m: _titulo_de(m.group(1)), md)

    # arquivos .tsv remanescentes
    md = re.sub(r"`?[A-Za-z0-9_./-]*anki-volume-(\d)[A-Za-z0-9_.-]*\.tsv`?",
                lambda m: "baralho do Volume %s" % m.group(1), md)

    # linhas órfãs de navegação/execução
    md = re.sub(r"^\s*python tools.*$", "", md, flags=re.M)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


# ===========================================================================
# EMOJI -> MARCADORES TIPOGRÁFICOS
# ===========================================================================

EMOJI_HTML = {
    "\U0001F534": '<span class="pri p5"></span>',
    "\U0001F7E0": '<span class="pri p4"></span>',
    "\U0001F7E1": '<span class="pri p3"></span>',
    "\U0001F7E2": '<span class="pri p2"></span>',
    "⚪":     '<span class="pri p1"></span>',
    "\U0001F535": '<span class="pri pb"></span>',
    "\U0001F7E3": '<span class="pri pr"></span>',
    "\U0001F7E5": '<span class="pri p5"></span>',
    "\U0001F7E7": '<span class="pri p4"></span>',
    "\U0001F7E8": '<span class="pri p3"></span>',
    "✅":     '<span class="mk ok">&#10003;</span>',
    "✔️": '<span class="mk ok">&#10003;</span>',
    "✔":     '<span class="mk ok">&#10003;</span>',
    "❌":     '<span class="mk no">&#10007;</span>',
    "✘":     '<span class="mk no">&#10007;</span>',
    "⚠️": '<span class="mk wr">!</span>',
    "⚠":     '<span class="mk wr">!</span>',
    "☑":     '<span class="mk ok">&#10003;</span>',
    "☐":     '<span class="cx"></span>',
}

RE_EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF←-⇿⌀-➿⬀-⯿️⃣]+")


def emojis(txt):
    for k, v in EMOJI_HTML.items():
        txt = txt.replace(k, v)
    return RE_EMOJI.sub(lambda m: '<span class="emo">%s</span>' % m.group(0), txt)


# ===========================================================================
# CONVERSOR MARKDOWN -> HTML
# ===========================================================================

_ENT = re.compile(r"&(#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);")


def escapar(t):
    marcas = []

    def guarda(m):
        marcas.append(m.group(0))
        return "\x00E%d\x00" % (len(marcas) - 1)

    t = _ENT.sub(guarda, t)
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for i, mk in enumerate(marcas):
        t = t.replace("\x00E%d\x00" % i, mk)
    return t


def inline(t):
    cods = []

    def guarda(m):
        cods.append(m.group(1))
        return "\x00C%d\x00" % (len(cods) - 1)

    t = re.sub(r"`([^`]+)`", guarda, t)
    t = escapar(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", t)
    t = emojis(t)
    for i, c in enumerate(cods):
        t = t.replace("\x00C%d\x00" % i, "<code>%s</code>" % escapar(c))
    return t


def texto_puro(t):
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = t.replace("**", "")
    t = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"\1", t)
    t = RE_EMOJI.sub("", t)
    return re.sub(r"\s+", " ", t).strip()


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^\w\s-]", "", t).strip().lower()
    return re.sub(r"[\s_]+", "-", t) or "s"


def classificar(txt):
    limpo = txt.lstrip()
    for marc, classe, rotulo, icone in CALLOUTS:
        if limpo.startswith(marc):
            return classe, rotulo, icone
    return None, None, None


def converter(md, indice, pref, nivel_base=0):
    linhas = md.split("\n")
    out, i, n = [], 0, len(linhas)
    while i < n:
        ln = linhas[i]

        if ln.startswith("<!--PROX-->"):
            out.append('<p class="prox"><span>Próximo módulo</span>%s</p>'
                       % inline(ln.replace("<!--PROX-->", "")))
            i += 1
            continue

        if ln.startswith("```"):
            i += 1
            buf = []
            while i < n and not linhas[i].startswith("```"):
                buf.append(linhas[i]); i += 1
            i += 1
            bloco = chr(10).join(buf)
            if "**" in bloco:          # modelos de formulario: limpa a sintaxe markdown
                limpas = []
                for lb in bloco.replace("**", "").split(chr(10)):
                    if lb.lstrip().startswith("#"):
                        lb = lb.lstrip().lstrip("#").lstrip()
                    limpas.append(lb)
                bloco = chr(10).join(limpas)
            out.append('<pre class="diagrama">%s</pre>' % escapar(bloco))
            continue

        if re.match(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$", ln):
            out.append('<hr class="regua">'); i += 1; continue

        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            niv = min(6, len(m.group(1)) + nivel_base)
            txt = m.group(2).strip()
            ident = "%s-%s" % (pref, slug(txt)[:52])
            if niv <= 2:
                indice.append({"nivel": niv, "texto": texto_puro(txt), "id": ident})
            out.append('<h%d id="%s">%s</h%d>' % (niv, ident, inline(txt), niv))
            i += 1
            continue

        if "|" in ln and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", linhas[i + 1]):
            cab = [c.strip() for c in ln.strip().strip("|").split("|")]
            al = []
            for c in linhas[i + 1].strip().strip("|").split("|"):
                c = c.strip()
                al.append("center" if c.startswith(":") and c.endswith(":")
                          else "right" if c.endswith(":") else "left")
            i += 2
            corpo = []
            while i < n and "|" in linhas[i] and linhas[i].strip():
                corpo.append([c.strip() for c in linhas[i].strip().strip("|").split("|")])
                i += 1
            p = ['<div class="tw"><table><thead><tr>']
            for j, c in enumerate(cab):
                p.append('<th style="text-align:%s">%s</th>'
                         % (al[j] if j < len(al) else "left", inline(c)))
            p.append("</tr></thead><tbody>")
            for lc in corpo:
                p.append("<tr>")
                for j, c in enumerate(lc):
                    p.append('<td style="text-align:%s">%s</td>'
                             % (al[j] if j < len(al) else "left", inline(c)))
                p.append("</tr>")
            p.append("</tbody></table></div>")
            out.append("".join(p))
            continue

        if ln.lstrip().startswith(">"):
            buf = []
            while i < n and linhas[i].lstrip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", linhas[i])); i += 1
            interno = "\n".join(buf)
            classe, rotulo, icone = classificar(interno)
            corpo = converter(interno, [], pref, nivel_base)
            if classe:
                out.append('<aside class="cx-box cx-%s"><div class="cx-tag">%s<span>%s</span>'
                           '</div><div class="cx-body">%s</div></aside>'
                           % (classe, ICONES[icone], rotulo, corpo))
            else:
                out.append('<aside class="cx-box cx-nota"><div class="cx-tag">%s<span>Nota</span>'
                           '</div><div class="cx-body">%s</div></aside>'
                           % (ICONES["nota"], corpo))
            continue

        if re.match(r"^\s*[-*+]\s+", ln) or re.match(r"^\s*\d+[.)]\s+", ln):
            ordenada = bool(re.match(r"^\s*\d+[.)]\s+", ln))
            itens = []
            while i < n:
                a = linhas[i]
                if re.match(r"^\s*[-*+]\s+", a) or re.match(r"^\s*\d+[.)]\s+", a):
                    itens.append(re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", a))
                    i += 1
                elif itens and a.startswith("  ") and a.strip():
                    itens[-1] += " " + a.strip()
                    i += 1
                elif not a.strip():
                    j = i + 1
                    while j < n and not linhas[j].strip():
                        j += 1
                    seguinte_lista = j < n and (re.match(r"^\s*[-*+]\s+", linhas[j])
                                                or re.match(r"^\s*\d+[.)]\s+", linhas[j]))
                    mesmo_tipo = (seguinte_lista and
                                  bool(re.match(r"^\s*\d+[.)]\s+", linhas[j])) == ordenada)
                    if mesmo_tipo:
                        i = j
                        continue
                    break
                else:
                    break
            tag = "ol" if ordenada else "ul"
            cls = ""
            p = []
            for it in itens:
                mm = re.match(r"^\[( |x|X)\]\s*(.*)$", it)
                if mm:
                    cls = ' class="check"'
                    marc = ('<span class="cx on">&#10003;</span>'
                            if mm.group(1).lower() == "x" else '<span class="cx"></span>')
                    p.append("<li>%s%s</li>" % (marc, inline(mm.group(2))))
                else:
                    p.append("<li>%s</li>" % inline(it))
            out.append("<%s%s>%s</%s>" % (tag, cls, "".join(p), tag))
            continue

        if not ln.strip():
            i += 1; continue

        buf = []
        while i < n and linhas[i].strip() and not re.match(
                r"^\s*(#{1,6}\s|>|```|[-*+]\s|\d+[.)]\s|<!--PROX-->|(-{3,}|\*{3,}|_{3,})\s*$)",
                linhas[i]):
            if "|" in linhas[i] and i + 1 < n and re.match(
                    r"^\s*\|?[\s:|-]+\|[\s:|-]*$", linhas[i + 1]):
                break
            buf.append(linhas[i].strip()); i += 1
        if buf:
            out.append("<p>%s</p>" % inline(" ".join(buf)))
        else:
            i += 1
    return "\n".join(out)


def extrair_secoes(md, titulos):
    """Extrai apenas as seções de nível 2 pedidas, na ordem dada."""
    blocos = {}
    partes = re.split(r"^(##\s+.*)$", md, flags=re.M)
    atual = None
    for p in partes:
        if p.startswith("## "):
            atual = p[3:].strip()
            blocos[atual] = [p]
        elif atual:
            blocos[atual].append(p)
    saida = []
    for t in titulos:
        for chave in blocos:
            if texto_puro(chave).lower().startswith(texto_puro(t).lower()[:40]):
                saida.append("".join(blocos[chave]).strip())
                break
    return "\n\n".join(saida)
