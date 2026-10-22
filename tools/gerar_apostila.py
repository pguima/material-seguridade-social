#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador da apostila A4 — Seguridade Social / INSS
==================================================

Converte os arquivos .md do curso em um único HTML pronto para impressão em A4
(ou para "Salvar como PDF" pelo navegador), com capa, sumário e identidade visual.

Uso:
    python tools/gerar_apostila.py                 # gera tudo
    python tools/gerar_apostila.py --vol 1         # só o Volume 1
    python tools/gerar_apostila.py --vol 2         # só o Volume 2
    python tools/gerar_apostila.py --saida X.html  # nome do arquivo de saída

Sem dependências externas: usa apenas a biblioteca padrão do Python 3.
Para acrescentar novos volumes, basta editar a lista SUMARIO abaixo.
"""

import argparse
import html as _html
import os
import re
import sys
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# ESTRUTURA DA APOSTILA — edite aqui ao acrescentar novos volumes
# ---------------------------------------------------------------------------

SUMARIO = [
    {
        "volume": 0,
        "parte": "ABERTURA",
        "arquivos": [
            "00-LEIA-ME.md",
            "01-MATRIZ-DE-ESTUDOS.md",
        ],
    },
    {
        "volume": 1,
        "parte": "VOLUME 1 — FUNDAMENTOS DA SEGURIDADE SOCIAL",
        "arquivos": [
            "modulos/M01-conceito-e-estrutura-da-seguridade-social.md",
            "modulos/M02-principios-e-objetivos-art-194.md",
            "modulos/M03-financiamento-e-orcamento-art-195.md",
            "modulos/M04-saude.md",
            "modulos/M05-assistencia-social-loas-bpc.md",
            "modulos/M06-previdencia-social-rgps-art-201.md",
            "02-PEGADINHAS-VOLUME-1.md",
            "simulados/simulado-01-fundamentos.md",
        ],
    },
    {
        "volume": 2,
        "parte": "VOLUME 2 — REGIME GERAL DE PREVIDÊNCIA SOCIAL",
        "arquivos": [
            "modulos/M07-rgps-estrutura-e-beneficiarios.md",
            "modulos/M08-segurados-empregado-domestico-avulso.md",
            "modulos/M09-contribuinte-individual-e-segurado-especial.md",
            "modulos/M10-facultativo-excluidos-e-quem-e-quem.md",
            "modulos/M11-dependentes.md",
            "modulos/M12-filiacao-e-inscricao.md",
            "modulos/M13-qualidade-de-segurado-e-periodo-de-graca.md",
            "modulos/M14-carencia.md",
            "03-PEGADINHAS-VOLUME-2.md",
            "simulados/simulado-02-rgps.md",
        ],
    },
    {
        "volume": 3,
        "parte": "VOLUME 3 — BENEFÍCIOS E SERVIÇOS DO RGPS",
        "arquivos": [
            "modulos/M15-salario-de-beneficio-e-rmi.md",
            "modulos/M16-beneficios-por-incapacidade.md",
            "modulos/M17-aposentadoria-programada-e-por-idade.md",
            "modulos/M18-aposentadoria-especial-e-da-pessoa-com-deficiencia.md",
            "modulos/M19-ec-103-transicao-e-direito-adquirido.md",
            "modulos/M20-pensao-por-morte-e-auxilio-reclusao.md",
            "modulos/M21-salario-familia-e-salario-maternidade.md",
            "modulos/M22-servicos-acumulacao-e-tabela-geral.md",
            "04-PEGADINHAS-VOLUME-3.md",
            "simulados/simulado-03-beneficios.md",
        ],
    },
    {
        "volume": 4,
        "parte": "VOLUME 4 — CUSTEIO DA SEGURIDADE SOCIAL",
        "arquivos": [
            "modulos/M23-empresa-equiparados-e-empregador-domestico.md",
            "modulos/M24-salario-de-contribuicao-conceito-e-limites.md",
            "modulos/M25-parcelas-integrantes-e-nao-integrantes.md",
            "modulos/M26-contribuicao-dos-segurados.md",
            "modulos/M27-contribuicao-das-empresas.md",
            "modulos/M28-contribuicoes-sobre-producao-rural-e-outras-fontes.md",
            "modulos/M29-arrecadacao-recolhimento-e-obrigacoes-acessorias.md",
            "modulos/M30-decadencia-prescricao-restituicao-e-crimes.md",
            "modulos/M31-processo-administrativo-previdenciario.md",
            "05-PEGADINHAS-VOLUME-4.md",
            "simulados/simulado-04-custeio.md",
        ],
    },
    {
        "volume": 5,
        "parte": "VOLUME 5 — RPPS, LEGISLAÇÕES ESPECIAIS E COMPLEMENTAR",
        "arquivos": [
            "modulos/M32-rpps-regime-proprio-de-previdencia-social.md",
            "modulos/M33-contagem-reciproca-ctc-e-previdencia-complementar.md",
            "modulos/M34-beneficios-de-legislacoes-especiais.md",
            "modulos/M35-conteudo-complementar-do-edital.md",
            "06-PEGADINHAS-VOLUME-5.md",
            "simulados/simulado-05-rpps-e-especiais.md",
        ],
    },
    {
        "volume": 6,
        "parte": "VOLUME 6 — REVISÃO FINAL",
        "arquivos": [
            "modulos/M36-mapas-mentais-e-quadros-consolidados.md",
            "modulos/M37-lei-seca-comentada.md",
            "modulos/M38-100-pontos-essenciais.md",
            "modulos/M39-sistema-de-revisao-final.md",
            "simulados/simulado-06-nivel-prova.md",
            "simulados/simulado-07-nivel-dificil.md",
            "caderno-de-erros.md",
        ],
    },
]

TITULO = "SEGURIDADE SOCIAL"
SUBTITULO = "Preparação Completa para o Concurso do INSS"
CARGO = "Técnico do Seguro Social"

# ---------------------------------------------------------------------------
# CALLOUTS — blockquotes que começam com estes marcadores viram caixas
# ---------------------------------------------------------------------------

CALLOUTS = [
    ("\U0001F3AF", "alvo", "COMO CAI NA PROVA"),          # 🎯
    ("⚠", "atencao", "ATENÇÃO"),                       # ⚠
    ("\U0001F9E0", "memorize", "MEMORIZE"),                # 🧠
    ("\U0001F3A3", "pegadinha", "PEGADINHA"),              # 🎣
    ("❌", "errado", "ASSERTIVA ERRADA"),               # ❌
    ("✅", "certo", "ASSERTIVA CERTA"),                 # ✅
    ("\U0001F534", "critico", "PRIORIDADE MÁXIMA"),        # 🔴
    ("⏱", "revisao", "REVISÃO"),                       # ⏱
    ("⛔", "bloqueio", "PARE"),                         # ⛔
]


# ---------------------------------------------------------------------------
# CONVERSOR MARKDOWN -> HTML
# ---------------------------------------------------------------------------

_ENTIDADE = re.compile(r"&(#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);")


def escapar(texto):
    """Escapa HTML preservando entidades já escritas (ex.: &nbsp;)."""
    marcas = []

    def guardar(m):
        marcas.append(m.group(0))
        return "\x00E%d\x00" % (len(marcas) - 1)

    texto = _ENTIDADE.sub(guardar, texto)
    texto = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for i, marca in enumerate(marcas):
        texto = texto.replace("\x00E%d\x00" % i, marca)
    return texto


def inline(texto):
    """Converte marcação inline: `code`, **negrito**, *itálico*, [link](url)."""
    codigos = []

    def guardar_codigo(m):
        codigos.append(m.group(1))
        return "\x00C%d\x00" % (len(codigos) - 1)

    texto = re.sub(r"`([^`]+)`", guardar_codigo, texto)
    texto = escapar(texto)
    texto = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', texto)
    # não-guloso: permite itálico aninhado dentro do negrito (ex.: **art. 201, *caput*:**)
    texto = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", texto)
    texto = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", texto)
    for i, cod in enumerate(codigos):
        texto = texto.replace("\x00C%d\x00" % i, "<code>%s</code>" % escapar(cod))
    return texto


def texto_puro(texto):
    """Remove marcação inline — usado no sumário, que não aceita tags."""
    texto = re.sub(r"`([^`]+)`", r"\1", texto)
    texto = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", texto)
    texto = texto.replace("**", "")
    texto = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"\1", texto)
    return texto.strip()


def slug(texto):
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = re.sub(r"[^\w\s-]", "", texto).strip().lower()
    return re.sub(r"[\s_]+", "-", texto) or "sec"


def classificar_callout(texto):
    """Devolve (classe, rotulo) conforme o marcador inicial do blockquote."""
    limpo = texto.lstrip()
    for marcador, classe, rotulo in CALLOUTS:
        if limpo.startswith(marcador):
            return classe, rotulo
    return None, None


def converter(md, indice, prefixo):
    """Converte um documento markdown em HTML. Alimenta `indice` com os títulos."""
    linhas = md.split("\n")
    saida = []
    i = 0
    n = len(linhas)

    while i < n:
        linha = linhas[i]

        # ---------- bloco de código / diagramas ASCII ----------
        if linha.startswith("```"):
            i += 1
            buffer = []
            while i < n and not linhas[i].startswith("```"):
                buffer.append(linhas[i])
                i += 1
            i += 1
            saida.append("<pre class=\"diagrama\">%s</pre>" % escapar("\n".join(buffer)))
            continue

        # ---------- linha horizontal ----------
        if re.match(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$", linha):
            saida.append('<hr class="regua">')
            i += 1
            continue

        # ---------- títulos ----------
        m = re.match(r"^(#{1,6})\s+(.*)$", linha)
        if m:
            nivel = len(m.group(1))
            texto = m.group(2).strip()
            ident = "%s-%s" % (prefixo, slug(texto)[:60])
            if nivel <= 2:
                indice.append({"nivel": nivel, "texto": texto_puro(texto), "id": ident})
            saida.append('<h%d id="%s">%s</h%d>' % (nivel, ident, inline(texto), nivel))
            i += 1
            continue

        # ---------- tabela ----------
        if "|" in linha and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", linhas[i + 1]):
            cabecalho = [c.strip() for c in linha.strip().strip("|").split("|")]
            alinhamentos = []
            for c in linhas[i + 1].strip().strip("|").split("|"):
                c = c.strip()
                if c.startswith(":") and c.endswith(":"):
                    alinhamentos.append("center")
                elif c.endswith(":"):
                    alinhamentos.append("right")
                else:
                    alinhamentos.append("left")
            i += 2
            corpo = []
            while i < n and "|" in linhas[i] and linhas[i].strip():
                corpo.append([c.strip() for c in linhas[i].strip().strip("|").split("|")])
                i += 1
            partes = ['<div class="tabela-wrap"><table>', "<thead><tr>"]
            for j, celula in enumerate(cabecalho):
                al = alinhamentos[j] if j < len(alinhamentos) else "left"
                partes.append('<th style="text-align:%s">%s</th>' % (al, inline(celula)))
            partes.append("</tr></thead><tbody>")
            for linha_corpo in corpo:
                partes.append("<tr>")
                for j, celula in enumerate(linha_corpo):
                    al = alinhamentos[j] if j < len(alinhamentos) else "left"
                    partes.append('<td style="text-align:%s">%s</td>' % (al, inline(celula)))
                partes.append("</tr>")
            partes.append("</tbody></table></div>")
            saida.append("".join(partes))
            continue

        # ---------- blockquote / callout ----------
        if linha.lstrip().startswith(">"):
            buffer = []
            while i < n and (linhas[i].lstrip().startswith(">") or
                             (buffer and linhas[i].strip() and
                              not linhas[i].lstrip().startswith(("#", "|", "```", "- ", "* ")))):
                if linhas[i].lstrip().startswith(">"):
                    buffer.append(re.sub(r"^\s*>\s?", "", linhas[i]))
                else:
                    break
                i += 1
            interno = "\n".join(buffer)
            classe, rotulo = classificar_callout(interno)
            sub_indice = []
            corpo_html = converter(interno, sub_indice, prefixo)
            if classe:
                saida.append(
                    '<aside class="callout callout-%s">'
                    '<div class="callout-rotulo">%s</div>%s</aside>'
                    % (classe, rotulo, corpo_html)
                )
            else:
                saida.append('<blockquote class="nota">%s</blockquote>' % corpo_html)
            continue

        # ---------- listas ----------
        if re.match(r"^\s*[-*+]\s+", linha) or re.match(r"^\s*\d+[.)]\s+", linha):
            ordenada = bool(re.match(r"^\s*\d+[.)]\s+", linha))
            itens = []
            while i < n and (re.match(r"^\s*[-*+]\s+", linhas[i]) or
                             re.match(r"^\s*\d+[.)]\s+", linhas[i]) or
                             (itens and linhas[i].startswith("  ") and linhas[i].strip())):
                atual = linhas[i]
                if re.match(r"^\s*[-*+]\s+", atual) or re.match(r"^\s*\d+[.)]\s+", atual):
                    texto = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", atual)
                    itens.append(texto)
                elif itens:
                    itens[-1] += " " + atual.strip()
                i += 1
            tag = "ol" if ordenada else "ul"
            partes = ["<%s>" % tag]
            for item in itens:
                caixa = ""
                mm = re.match(r"^\[( |x|X)\]\s*(.*)$", item)
                if mm:
                    marcado = mm.group(1).lower() == "x"
                    item = mm.group(2)
                    caixa = '<span class="caixa">%s</span> ' % ("&#9745;" if marcado else "&#9744;")
                partes.append("<li>%s%s</li>" % (caixa, inline(item)))
            partes.append("</%s>" % tag)
            saida.append("".join(partes))
            continue

        # ---------- linha em branco ----------
        if not linha.strip():
            i += 1
            continue

        # ---------- parágrafo ----------
        buffer = []
        while i < n and linhas[i].strip() and not re.match(
            r"^\s*(#{1,6}\s|>|```|[-*+]\s|\d+[.)]\s|(-{3,}|\*{3,}|_{3,})\s*$)", linhas[i]
        ):
            if "|" in linhas[i] and i + 1 < n and re.match(
                r"^\s*\|?[\s:|-]+\|[\s:|-]*$", linhas[i + 1]
            ):
                break
            buffer.append(linhas[i].strip())
            i += 1
        if buffer:
            saida.append("<p>%s</p>" % inline(" ".join(buffer)))
        else:
            i += 1

    return "\n".join(saida)


# ---------------------------------------------------------------------------
# CSS DA APOSTILA
# ---------------------------------------------------------------------------

CSS = """
@page { size: A4 portrait; margin: 18mm 16mm 20mm 16mm; }

:root{
  --tinta:#15202b; --tinta-fraca:#4a5a6a; --linha:#d7dee6;
  --azul:#123a63; --azul-claro:#eaf1f8;
  --dourado:#8a6a12; --dourado-claro:#fdf6e3;
  --vermelho:#9d2323; --vermelho-claro:#fdeeee;
  --roxo:#5b3a8e; --roxo-claro:#f4efFB;
  --verde:#1d6b3f; --verde-claro:#ecf7f0;
  --cinza-claro:#f6f8fa;
}

*{ box-sizing:border-box; }

body{
  font-family:"Segoe UI","Helvetica Neue",Arial,sans-serif;
  font-size:10.4pt; line-height:1.5; color:var(--tinta);
  margin:0; padding:0; background:#fff;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}

.pagina{ max-width:186mm; margin:0 auto; padding:8mm 0; }

/* ---------- CAPA ---------- */
.capa{
  page-break-after:always; text-align:center;
  min-height:245mm; display:flex; flex-direction:column;
  justify-content:center; align-items:center;
  border:2.5pt solid var(--azul); padding:20mm 12mm;
}
.capa .selo{
  font-size:9pt; letter-spacing:.32em; text-transform:uppercase;
  color:var(--azul); border:1pt solid var(--azul);
  padding:5pt 14pt; border-radius:2pt; margin-bottom:16mm;
}
.capa h1{
  font-size:34pt; line-height:1.08; margin:0 0 6mm 0; color:var(--azul);
  border:0; padding:0; letter-spacing:.02em;
}
.capa .sub{ font-size:14pt; color:var(--tinta-fraca); margin-bottom:3mm; }
.capa .cargo{
  font-size:11pt; letter-spacing:.18em; text-transform:uppercase;
  color:var(--dourado); margin-bottom:18mm;
}
.capa .barra{ width:52mm; height:2.5pt; background:var(--dourado); margin:0 auto 18mm; }
.capa .pilares{
  display:flex; gap:6mm; justify-content:center; margin-bottom:16mm; flex-wrap:wrap;
}
.capa .pilar{
  border:1pt solid var(--linha); border-top:3pt solid var(--azul);
  padding:6mm 7mm; min-width:38mm; background:var(--cinza-claro);
}
.capa .pilar b{ display:block; font-size:10.5pt; color:var(--azul); }
.capa .pilar span{ font-size:8pt; color:var(--tinta-fraca); }
.capa .rodape{ font-size:8.5pt; color:var(--tinta-fraca); line-height:1.7; }

/* ---------- AVISO ---------- */
.aviso-legal{
  border:1pt solid var(--vermelho); background:var(--vermelho-claro);
  padding:6mm; margin:8mm 0; font-size:9pt; page-break-inside:avoid;
}
.aviso-legal b{ color:var(--vermelho); }

/* ---------- SUMÁRIO ---------- */
.sumario{ page-break-after:always; }
.sumario h1{ border-bottom:2.5pt solid var(--azul); }
.sumario .parte{
  margin-top:7mm; font-size:9pt; letter-spacing:.16em; text-transform:uppercase;
  color:var(--dourado); border-bottom:1pt solid var(--linha); padding-bottom:1.5mm;
}
.sumario ol{ list-style:none; margin:2mm 0 0 0; padding:0; }
.sumario li{ margin:0; padding:1.1mm 0; font-size:9.6pt; }
.sumario li.n1{ font-weight:600; color:var(--azul); padding-top:2.5mm; }
.sumario li.n2{ padding-left:7mm; color:var(--tinta-fraca); font-size:9pt; }
.sumario a{ color:inherit; text-decoration:none; }

/* ---------- DIVISÓRIA DE PARTE ---------- */
.divisoria{
  page-break-before:always; page-break-after:always;
  min-height:200mm; display:flex; flex-direction:column;
  justify-content:center; align-items:center; text-align:center;
}
.divisoria .num{
  font-size:64pt; font-weight:700; color:var(--azul-claro); line-height:1;
}
.divisoria h2{
  font-size:19pt; color:var(--azul); border:0; margin:4mm 0 0 0; padding:0;
  max-width:120mm;
}
.divisoria .risco{ width:38mm; height:2.5pt; background:var(--dourado); margin:6mm auto 0; }

/* ---------- TÍTULOS ---------- */
h1{
  font-size:17pt; color:var(--azul); margin:0 0 4mm 0; padding-bottom:2.5mm;
  border-bottom:2pt solid var(--azul); page-break-before:always;
  page-break-after:avoid; line-height:1.2;
}
h1.primeiro{ page-break-before:auto; }
h2{
  font-size:13pt; color:var(--azul); margin:7mm 0 3mm 0;
  padding-bottom:1.2mm; border-bottom:1pt solid var(--linha);
  page-break-after:avoid; line-height:1.25;
}
h3{ font-size:11.4pt; color:var(--tinta); margin:5mm 0 2mm 0; page-break-after:avoid; }
h4,h5,h6{ font-size:10.4pt; color:var(--tinta-fraca); margin:4mm 0 1.5mm 0; page-break-after:avoid; }

p{ margin:0 0 2.6mm 0; text-align:justify; }
strong{ color:#0b1720; }
a{ color:var(--azul); }

hr.regua{ border:0; border-top:1pt solid var(--linha); margin:5mm 0; }

/* ---------- LISTAS ---------- */
ul,ol{ margin:0 0 3mm 0; padding-left:6mm; }
li{ margin:0 0 1.1mm 0; }
.caixa{ font-size:11pt; color:var(--azul); }

/* ---------- CÓDIGO E DIAGRAMAS ---------- */
code{
  font-family:"Cascadia Mono",Consolas,"Courier New",monospace;
  font-size:8.8pt; background:var(--cinza-claro);
  padding:.4mm 1.1mm; border-radius:1.5pt; border:.5pt solid var(--linha);
}
pre.diagrama{
  font-family:"Cascadia Mono",Consolas,"Courier New",monospace;
  font-size:7.9pt; line-height:1.32; background:var(--cinza-claro);
  border:1pt solid var(--linha); border-left:3pt solid var(--azul);
  padding:3.5mm 4mm; margin:3mm 0; overflow-x:auto;
  page-break-inside:avoid; white-space:pre; color:#22303c;
}

/* ---------- TABELAS ---------- */
.tabela-wrap{ margin:3mm 0; overflow-x:auto; page-break-inside:avoid; }
table{ width:100%; border-collapse:collapse; font-size:8.6pt; line-height:1.38; }
thead{ display:table-header-group; }
th{
  background:var(--azul); color:#fff; font-weight:600;
  padding:1.7mm 2mm; border:.5pt solid var(--azul); text-align:left;
}
td{ padding:1.5mm 2mm; border:.5pt solid var(--linha); vertical-align:top; }
tbody tr:nth-child(even){ background:var(--cinza-claro); }

/* ---------- CALLOUTS ---------- */
.callout{
  margin:3.5mm 0; padding:3mm 4mm 3mm 4mm; border-left:3.5pt solid var(--azul);
  background:var(--azul-claro); page-break-inside:avoid; font-size:9.8pt;
  border-radius:0 2pt 2pt 0;
}
.callout p:last-child{ margin-bottom:0; }
.callout-rotulo{
  font-size:7.4pt; letter-spacing:.16em; text-transform:uppercase;
  font-weight:700; margin-bottom:1.5mm; color:var(--azul);
}
.callout-alvo{ border-left-color:var(--dourado); background:var(--dourado-claro); }
.callout-alvo .callout-rotulo{ color:var(--dourado); }
.callout-atencao{ border-left-color:var(--vermelho); background:var(--vermelho-claro); }
.callout-atencao .callout-rotulo{ color:var(--vermelho); }
.callout-critico{ border-left-color:var(--vermelho); background:var(--vermelho-claro); }
.callout-critico .callout-rotulo{ color:var(--vermelho); }
.callout-errado{ border-left-color:var(--vermelho); background:var(--vermelho-claro); }
.callout-errado .callout-rotulo{ color:var(--vermelho); }
.callout-memorize{ border-left-color:var(--roxo); background:var(--roxo-claro); }
.callout-memorize .callout-rotulo{ color:var(--roxo); }
.callout-pegadinha{ border-left-color:var(--roxo); background:var(--roxo-claro); }
.callout-pegadinha .callout-rotulo{ color:var(--roxo); }
.callout-certo{ border-left-color:var(--verde); background:var(--verde-claro); }
.callout-certo .callout-rotulo{ color:var(--verde); }
.callout-revisao{ border-left-color:var(--verde); background:var(--verde-claro); }
.callout-revisao .callout-rotulo{ color:var(--verde); }
.callout-bloqueio{ border-left-color:var(--vermelho); background:var(--vermelho-claro); }
.callout-bloqueio .callout-rotulo{ color:var(--vermelho); }

blockquote.nota{
  margin:3mm 0; padding:2.5mm 4mm; border-left:2.5pt solid var(--linha);
  background:var(--cinza-claro); font-size:9.8pt; page-break-inside:avoid;
  border-radius:0 2pt 2pt 0;
}
blockquote.nota p:last-child{ margin-bottom:0; }

/* ---------- TELA ---------- */
@media screen{
  body{ background:#e9edf1; padding:10mm 4mm; }
  .pagina{
    background:#fff; padding:14mm 15mm; margin:0 auto 8mm;
    box-shadow:0 2px 14px rgba(0,0,0,.13); border-radius:3px; max-width:210mm;
  }
  .barra-imprimir{
    position:sticky; top:0; z-index:99; max-width:210mm; margin:0 auto 8mm;
    background:var(--azul); color:#fff; padding:3mm 5mm; border-radius:3px;
    font-size:9.5pt; display:flex; justify-content:space-between; align-items:center;
    gap:4mm; flex-wrap:wrap;
  }
  .barra-imprimir button{
    background:#fff; color:var(--azul); border:0; padding:2mm 5mm;
    border-radius:2px; font-weight:600; cursor:pointer; font-size:9.5pt;
  }
}
@media print{ .barra-imprimir{ display:none !important; } }
"""

JS = """
document.addEventListener('click', function(e){
  if(e.target && e.target.id === 'btn-imprimir'){ window.print(); }
});
"""


# ---------------------------------------------------------------------------
# MONTAGEM
# ---------------------------------------------------------------------------

def montar(volumes, saida):
    partes_html = []
    indice_geral = []

    for grupo in SUMARIO:
        if grupo["volume"] != 0 and volumes and grupo["volume"] not in volumes:
            continue

        if grupo["volume"] != 0:
            indice_geral.append({"parte": grupo["parte"]})
            partes_html.append(
                '<section class="divisoria">'
                '<div class="num">%s</div><h2>%s</h2><div class="risco"></div></section>'
                % (grupo["volume"], _html.escape(grupo["parte"].split("—")[-1].strip()))
            )
        else:
            indice_geral.append({"parte": grupo["parte"]})

        for rel in grupo["arquivos"]:
            caminho = os.path.join(BASE, rel.replace("/", os.sep))
            if not os.path.exists(caminho):
                print("  ! ausente, ignorado: %s" % rel, file=sys.stderr)
                continue
            with open(caminho, "r", encoding="utf-8") as fh:
                md = fh.read()
            prefixo = slug(os.path.splitext(os.path.basename(rel))[0])
            indice_doc = []
            corpo = converter(md, indice_doc, prefixo)
            indice_geral.extend(indice_doc)
            partes_html.append('<section class="doc">%s</section>' % corpo)
            print("  + %s (%d KB)" % (rel, len(corpo) // 1024))

    # ---- sumário ----
    itens = []
    for item in indice_geral:
        if "parte" in item:
            itens.append('<li class="parte">%s</li>' % _html.escape(item["parte"]))
        else:
            itens.append(
                '<li class="n%d"><a href="#%s">%s</a></li>'
                % (item["nivel"], item["id"], _html.escape(item["texto"]))
            )
    sumario_html = (
        '<section class="pagina sumario"><h1 class="primeiro">SUMÁRIO</h1>'
        "<ol>%s</ol></section>" % "".join(itens)
    )

    todos = sorted(g["volume"] for g in SUMARIO if g["volume"] != 0)
    alvo = sorted(volumes) if volumes else todos
    if len(alvo) == 1:
        rotulo_vols = "Volume %d" % alvo[0]
    else:
        rotulo_vols = "Volumes %s e %d" % (", ".join(str(v) for v in alvo[:-1]), alvo[-1])

    capa = """
<section class="pagina capa">
  <div class="selo">Apostila preparatória &middot; %s</div>
  <h1>%s</h1>
  <div class="barra"></div>
  <div class="sub">%s</div>
  <div class="cargo">%s</div>
  <div class="pilares">
    <div class="pilar"><b>SAÚDE</b><span>arts. 196 a 200</span></div>
    <div class="pilar"><b>PREVIDÊNCIA</b><span>arts. 201 e 202</span></div>
    <div class="pilar"><b>ASSISTÊNCIA</b><span>arts. 203 e 204</span></div>
  </div>
  <div class="rodape">
    CF/88 &middot; Lei 8.212/1991 &middot; Lei 8.213/1991 &middot; Lei 8.742/1993<br>
    Decreto 3.048/1999 &middot; EC 103/2019<br><br>
    Matriz de conteúdo: Edital nº 1/2022 &middot; Legislação vigente
  </div>
</section>

<section class="pagina">
  <h1 class="primeiro">AVISO METODOLÓGICO</h1>
  <div class="aviso-legal">
    <b>Leia antes de estudar.</b><br><br>
    Este material usa o <b>Edital nº 1/2022</b> apenas como <b>matriz de assuntos</b> e explica a
    <b>legislação vigente</b>. Edital é mapa de conteúdo, não fotografia da lei.<br><br>
    Todo ponto sujeito a alteração legislativa, valor monetário anual ou detalhe regulamentar
    está marcado com <b>&#9888; CONFERIR NA FONTE OFICIAL</b>. Quando encontrar essa marca,
    <b>abra o Planalto ou o gov.br/inss antes de decorar</b>.<br><br>
    O material distingue explicitamente <b>texto legal</b>, <b>jurisprudência</b>,
    <b>doutrina</b> e <b>entendimento predominante em concursos</b>. Nenhum artigo, inciso,
    prazo ou requisito foi inventado.
  </div>
  <h2>Fontes primárias para conferência</h2>
  <ul>
    <li>CF/88, arts. 194 a 204 &mdash; planalto.gov.br</li>
    <li>Lei nº 8.212/1991 (Custeio) &mdash; planalto.gov.br</li>
    <li>Lei nº 8.213/1991 (Benefícios) &mdash; planalto.gov.br</li>
    <li>Decreto nº 3.048/1999 (RPS) &mdash; planalto.gov.br</li>
    <li>Lei nº 8.742/1993 (LOAS) &mdash; planalto.gov.br</li>
    <li>EC nº 103/2019 &mdash; planalto.gov.br</li>
    <li>IN PRES/INSS nº 128/2022 &mdash; gov.br/inss (texto compilado)</li>
  </ul>
  <h2>Como imprimir</h2>
  <ol>
    <li>Abra este arquivo no <b>Chrome</b> ou no <b>Edge</b>.</li>
    <li><b>Ctrl+P</b> &rarr; Destino: <b>Salvar como PDF</b>.</li>
    <li>Papel <b>A4</b>, margens <b>Padrão</b>, escala <b>100%%</b>.</li>
    <li>Marque <b>&ldquo;Gráficos de segundo plano&rdquo;</b> &mdash; sem isso as caixas
        coloridas somem.</li>
    <li>Marque <b>&ldquo;Cabeçalhos e rodapés&rdquo;</b> para numerar as páginas.</li>
  </ol>
</section>
""" % (rotulo_vols, TITULO, SUBTITULO, CARGO)

    doc = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s — %s</title>
<style>%s</style>
</head>
<body>
<div class="barra-imprimir">
  <span><b>%s</b> — %s (%s)</span>
  <button id="btn-imprimir">Imprimir / Salvar como PDF</button>
</div>
%s
%s
<div class="pagina">
%s
</div>
<script>%s</script>
</body>
</html>
""" % (
        TITULO, CARGO, CSS,
        TITULO, CARGO, rotulo_vols,
        capa, sumario_html, "\n".join(partes_html), JS,
    )

    destino = os.path.join(BASE, saida)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return destino, len(doc)


def main():
    ap = argparse.ArgumentParser(description="Gera a apostila A4 em HTML a partir dos .md")
    ap.add_argument("--vol", type=int, action="append", default=None,
                    help="volume a incluir (pode repetir: --vol 1 --vol 2)")
    ap.add_argument("--saida", default=None, help="caminho do HTML de saída")
    args = ap.parse_args()

    volumes = set(args.vol) if args.vol else set()
    if args.saida:
        saida = args.saida
    elif volumes:
        saida = "apostila/apostila-seguridade-social-vol-%s.html" % "-".join(
            str(v) for v in sorted(volumes)
        )
    else:
        saida = "apostila/apostila-seguridade-social.html"

    print("Gerando apostila...")
    destino, tamanho = montar(volumes, saida)
    print("\nOK: %s" % destino)
    print("Tamanho: %.1f KB" % (tamanho / 1024))
    print("\nAbra no Chrome/Edge e use Ctrl+P -> Salvar como PDF.")
    print("Marque 'Graficos de segundo plano' para preservar as caixas coloridas.")


if __name__ == "__main__":
    main()
