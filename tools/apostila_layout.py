# -*- coding: utf-8 -*-
"""Identidade visual e montagem do HTML da apostila."""

import html as _html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apostila_config import TITULO, SUBTITULO, CARGO, PARTES
from apostila_html import (BASE, EMBLEMA, ILUSTRACOES, converter, extrair_secoes,
                           limpar, slug, texto_puro)

# ===========================================================================
# CSS
# ===========================================================================

CSS = """
@page { size: A4 portrait; margin: 21mm 19mm 24mm 19mm; }
@page capa { margin: 0; }
@page divisoria { margin: 0; }

:root{
  --tinta:#16202B; --fraca:#55636F; --linha:#DCE3EA;
  --azul:#0E2A47; --azul2:#1B4F82; --azulc:#EAF2FA;
  --ouro:#A67C00; --ouro2:#C79A2E; --ouroc:#FDF6E7;
  --verm:#9B2226; --vermc:#FCEEEE;
  --verde:#1B6B4A; --verdec:#EBF5F0;
  --roxo:#59418C; --roxoc:#F3EFFA;
  --papel:#FFFFFF; --cinza:#F5F7F9;
}
*{ box-sizing:border-box; }

html,body{ background:var(--papel); }
body{
  font-family:"Segoe UI",Calibri,"Helvetica Neue",Arial,sans-serif;
  font-size:10.2pt; line-height:1.55; color:var(--tinta);
  margin:0; padding:0; text-rendering:optimizeLegibility;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
p{ margin:0 0 2.4mm; text-align:justify; hyphens:auto; }
strong{ color:#0A1520; font-weight:650; }
em{ font-style:italic; }
a{ color:inherit; text-decoration:none; }

/* ---------------- CAPA ---------------- */
.capa{
  page:capa; break-after:page; position:relative; width:100%; height:297mm;
  background:linear-gradient(160deg,#0B2440 0%,#123255 46%,#0A1E36 100%);
  color:#fff; overflow:hidden;
}
.capa .moldura{
  position:absolute; inset:11mm; border:0.7mm solid rgba(243,201,105,.55);
}
.capa .moldura:before{
  content:""; position:absolute; inset:2.4mm; border:0.22mm solid rgba(243,201,105,.35);
}
.capa .conteudo{
  position:absolute; inset:11mm; display:flex; flex-direction:column;
  align-items:center; justify-content:center; text-align:center;
  padding:18mm 16mm 26mm;
}
.capa .selo{
  font-size:8.4pt; letter-spacing:.36em; text-transform:uppercase;
  color:#F3C969; border:0.3mm solid rgba(243,201,105,.6);
  padding:2.1mm 6mm; border-radius:1mm; margin-bottom:9mm;
}
.emblema{ width:40mm; height:auto; margin-bottom:7mm; }
.capa h1{
  break-before:auto; break-after:auto;
  font-family:Georgia,"Times New Roman",serif; font-size:37pt; line-height:1.02;
  letter-spacing:.035em; margin:0; color:#fff; border:0; padding:0;
  text-shadow:0 1px 0 rgba(0,0,0,.25);
}
.capa h1:before{ display:none; }
.capa .filete{ width:46mm; height:1.1mm; background:#C79A2E; margin:6mm 0 5mm; }
.capa .sub{ font-size:13.4pt; color:#DCE7F2; font-weight:300; letter-spacing:.02em; }
.capa .cargo{
  margin-top:3mm; font-size:9.6pt; letter-spacing:.24em; text-transform:uppercase;
  color:#F3C969;
}
.capa .pilares{ display:flex; gap:4mm; margin-top:11mm; width:100%; }
.capa .pilar{
  flex:1 1 0; min-width:0; border:0.28mm solid rgba(255,255,255,.28); border-top:1mm solid #C79A2E;
  padding:4.5mm 3mm; background:rgba(255,255,255,.05); border-radius:.8mm;
}
.capa .pilar b{ display:block; font-size:9.4pt; letter-spacing:.1em; color:#fff; }
.capa .pilar span{ font-size:7.4pt; color:#B9CBDD; letter-spacing:.04em; }
.capa .rodape{
  position:absolute; left:16mm; right:16mm; bottom:12mm; text-align:center;
  font-size:7.8pt; color:#A9BED2; line-height:1.75; letter-spacing:.03em;
}
.capa .rodape b{ color:#F3C969; font-weight:600; }

/* ---------------- FOLHA DE ROSTO ---------------- */
.rosto{ break-after:page; padding-top:14mm; }
.rosto h1{
  font-family:Georgia,serif; font-size:22pt; color:var(--azul); border:0;
  margin:0 0 2mm; padding:0; break-before:auto; letter-spacing:.02em;
}
.rosto .sub{ font-size:11.6pt; color:var(--fraca); margin-bottom:8mm; }
.rosto .linha-ouro{ width:34mm; height:.9mm; background:var(--ouro2); margin-bottom:8mm; }
.ficha{
  border:0.3mm solid var(--linha); background:#fff; border-radius:1.4mm;
  padding:6mm 7mm; margin-bottom:7mm;
}
.ficha dl{ margin:0; display:grid; grid-template-columns:34mm 1fr; gap:2.2mm 4mm; }
.ficha dt{ font-size:8pt; letter-spacing:.14em; text-transform:uppercase; color:var(--ouro); }
.ficha dd{ margin:0; font-size:9.8pt; }
.aviso{
  border-left:1.1mm solid var(--verm); background:var(--vermc);
  padding:5mm 6mm; border-radius:0 1.4mm 1.4mm 0; font-size:9.5pt;
}
.aviso b{ color:var(--verm); }

/* ---------------- SUMÁRIO ---------------- */
.sumario{ break-before:page; }
.sumario h1{
  font-family:Georgia,serif; font-size:20pt; color:var(--azul);
  border-bottom:.8mm solid var(--azul); padding-bottom:2.6mm; margin:0 0 6mm;
  break-before:auto; letter-spacing:.06em;
}
.sumario ol{ list-style:none; margin:0; padding:0; }
.sumario li{ margin:0; padding:0; }
.sumario .s-parte{
  margin:6mm 0 2mm; font-family:Georgia,serif; font-size:10.6pt; color:var(--azul);
  border-bottom:.25mm solid var(--linha); padding-bottom:1.4mm; font-weight:bold;
}
.sumario .s-parte i{
  font-style:normal; color:var(--ouro); letter-spacing:.16em; font-size:8pt;
  display:inline-block; min-width:24mm; margin-right:2.5mm; text-transform:uppercase;
}
.sumario .s-item a{ display:flex; align-items:baseline; gap:1.6mm; padding:.85mm 0; font-size:9.5pt; }
.sumario .s-item .s-t{ color:var(--tinta); }
.sumario .s-item .s-d{
  flex:1; border-bottom:.22mm dotted #AEB9C4; transform:translateY(-.6mm); min-width:8mm;
}
.sumario .s-item .s-p{
  color:var(--azul2); font-variant-numeric:tabular-nums; font-weight:600;
  min-width:8mm; text-align:right;
}
.sumario .s-item.oculto .s-p{ visibility:hidden; }
.sumario .s-sub{ padding-left:6mm; }
.sumario .s-sub .s-t{ color:var(--fraca); font-size:9pt; }

/* ---------------- DIVISÓRIA DE PARTE ---------------- */
.divisoria{
  page:divisoria; break-before:page; break-after:page;
  width:100%; height:297mm; position:relative; background:#fff; overflow:hidden;
}
.divisoria .faixa{
  position:absolute; top:0; left:0; right:0; height:96mm;
  background:linear-gradient(150deg,#0B2440,#164172);
}
.divisoria .faixa:after{
  content:""; position:absolute; left:0; right:0; bottom:0; height:1.4mm; background:#C79A2E;
}
.divisoria .num{
  position:absolute; top:22mm; left:0; right:0; text-align:center;
  font-family:Georgia,serif; font-size:12pt; letter-spacing:.42em; color:#F3C969;
}
.divisoria h2{
  position:absolute; top:40mm; left:22mm; right:22mm; text-align:center;
  font-family:Georgia,serif; font-size:25pt; line-height:1.16; color:#fff;
  margin:0; padding:0; border:0;
}
.divisoria .sub{
  position:absolute; top:76mm; left:26mm; right:26mm; text-align:center;
  font-size:9.6pt; color:#BBCEE0; letter-spacing:.02em;
}
.divisoria .ilu{
  position:absolute; top:112mm; left:26mm; right:26mm; bottom:40mm;
  display:flex; align-items:center; justify-content:center;
}
.divisoria .ilu svg{ width:100%; height:auto; max-height:110mm; }
.divisoria .rodape{
  position:absolute; left:24mm; right:24mm; bottom:26mm; text-align:center;
  font-size:8pt; letter-spacing:.24em; text-transform:uppercase; color:var(--fraca);
  border-top:.25mm solid var(--linha); padding-top:3.4mm;
}

/* ---------------- TÍTULOS DO MIOLO ---------------- */
h1{
  break-before:page; break-after:avoid;
  font-family:Georgia,serif; font-size:17.4pt; line-height:1.2; color:var(--azul);
  margin:0 0 4.4mm; padding:0 0 3mm 0; border-bottom:.7mm solid var(--azul);
  letter-spacing:.01em; position:relative;
}
h1:before{
  content:""; position:absolute; left:0; bottom:-.7mm; width:26mm; height:.7mm; background:var(--ouro2);
}
h1.primeiro{ break-before:auto; }
h2{
  break-after:avoid; font-family:Georgia,serif; font-size:13pt; color:var(--azul);
  margin:7.5mm 0 2.8mm; padding-left:3.4mm; border-left:1.1mm solid var(--ouro2);
  line-height:1.3;
}
h3{
  break-after:avoid; font-size:11pt; color:#122C46; margin:5.4mm 0 2mm;
  font-weight:650; letter-spacing:.005em;
}
h4,h5,h6{ break-after:avoid; font-size:10.1pt; color:var(--fraca); margin:4mm 0 1.6mm; font-weight:650; }

hr.regua{ border:0; border-top:.25mm solid var(--linha); margin:6mm 0; }

/* ---------------- LISTAS ---------------- */
ul,ol{ margin:0 0 3mm; padding-left:6.4mm; }
li{ margin:0 0 1.1mm; }
li::marker{ color:var(--azul2); }
ul.check,ol.check{ list-style:none; padding-left:0; }
ul.check li{ padding-left:0; }
.cx{
  display:inline-block; width:3.1mm; height:3.1mm; border:.35mm solid var(--azul2);
  border-radius:.5mm; margin-right:1.8mm; vertical-align:-.4mm; background:#fff;
  text-align:center; line-height:2.9mm; font-size:8pt; color:var(--verde);
}
.cx.on{ background:var(--verdec); border-color:var(--verde); }

/* ---------------- MARCADORES ---------------- */
.pri{
  display:inline-block; width:2.6mm; height:2.6mm; border-radius:50%;
  margin-right:1.1mm; vertical-align:-.15mm; border:.2mm solid rgba(0,0,0,.12);
}
.pri.p5{ background:#C1272D; } .pri.p4{ background:#E08A1E; }
.pri.p3{ background:#D7B300; } .pri.p2{ background:#2E8B57; }
.pri.p1{ background:#C6CFD7; } .pri.pb{ background:#1B4F82; } .pri.pr{ background:#59418C; }
.mk{
  display:inline-block; min-width:3.4mm; height:3.4mm; line-height:3.4mm; text-align:center;
  border-radius:50%; font-size:7.6pt; font-weight:700; margin-right:.7mm; vertical-align:-.5mm;
  color:#fff;
}
.mk.ok{ background:var(--verde); } .mk.no{ background:var(--verm); }
.mk.wr{ background:var(--ouro); }
.emo{ font-size:9pt; }

/* ---------------- CÓDIGO / DIAGRAMAS ---------------- */
code{
  font-family:Consolas,"Cascadia Mono","Courier New",monospace; font-size:8.8pt;
  background:var(--cinza); padding:.3mm 1mm; border-radius:.7mm; border:.2mm solid var(--linha);
}
pre.diagrama{
  font-family:Consolas,"Cascadia Mono","Courier New",monospace;
  font-size:7.7pt; line-height:1.36; color:#1C2C3A;
  background:var(--cinza); border:.25mm solid var(--linha);
  border-left:1.1mm solid var(--azul2); border-radius:0 1.2mm 1.2mm 0;
  padding:3.6mm 4.4mm; margin:3.4mm 0; white-space:pre; overflow:hidden;
  break-inside:avoid;
}

/* ---------------- TABELAS ---------------- */
.tw{ margin:3.4mm 0; break-inside:avoid; }
table{ width:100%; border-collapse:collapse; font-size:8.5pt; line-height:1.4; }
thead{ display:table-header-group; }
th{
  background:var(--azul); color:#fff; font-weight:600; text-align:left;
  padding:1.7mm 2mm; border:.2mm solid var(--azul); letter-spacing:.01em;
}
td{ padding:1.5mm 2mm; border:.2mm solid var(--linha); vertical-align:top; }
tbody tr:nth-child(even){ background:var(--cinza); }
td strong{ color:#0A1520; }

/* ---------------- CAIXAS ---------------- */
.cx-box{
  margin:3.6mm 0; border-radius:1.4mm; break-inside:avoid;
  border:.25mm solid var(--linha); border-left:1.2mm solid var(--azul2);
  background:var(--azulc); overflow:hidden;
}
.cx-tag{
  display:flex; align-items:center; gap:1.6mm;
  padding:1.9mm 4mm .4mm; font-size:7.2pt; font-weight:700;
  letter-spacing:.18em; text-transform:uppercase; color:var(--azul2);
}
.cx-tag svg{ width:3.6mm; height:3.6mm; flex:none; }
.cx-body{ padding:0 4mm 2.6mm; font-size:9.7pt; }
.cx-body p{ margin:0 0 1.8mm; }
.cx-body p:last-child,.cx-body ul:last-child,.cx-body ol:last-child,
.cx-body .tw:last-child,.cx-body pre:last-child{ margin-bottom:0; }
.cx-body pre.diagrama{ background:rgba(255,255,255,.66); }

.cx-alvo{ border-left-color:var(--ouro2); background:var(--ouroc); }
.cx-alvo .cx-tag{ color:var(--ouro); }
.cx-atencao,.cx-critico,.cx-errado,.cx-bloqueio{ border-left-color:var(--verm); background:var(--vermc); }
.cx-atencao .cx-tag,.cx-critico .cx-tag,.cx-errado .cx-tag,.cx-bloqueio .cx-tag{ color:var(--verm); }
.cx-memorize,.cx-pegadinha{ border-left-color:var(--roxo); background:var(--roxoc); }
.cx-memorize .cx-tag,.cx-pegadinha .cx-tag{ color:var(--roxo); }
.cx-certo,.cx-revisao{ border-left-color:var(--verde); background:var(--verdec); }
.cx-certo .cx-tag,.cx-revisao .cx-tag{ color:var(--verde); }
.cx-nota{ border-left-color:#9AA6B2; background:var(--cinza); }
.cx-nota .cx-tag{ color:var(--fraca); }

/* ---------------- NAVEGAÇÃO DE MÓDULO ---------------- */
.prox{
  margin:7mm 0 0; padding:3mm 4mm; border:.25mm solid var(--linha);
  border-left:1.1mm solid var(--ouro2); background:var(--ouroc);
  border-radius:0 1.2mm 1.2mm 0; font-size:9.4pt; text-align:left; break-inside:avoid;
}
.prox span{
  display:block; font-size:7.2pt; letter-spacing:.2em; text-transform:uppercase;
  color:var(--ouro); margin-bottom:.8mm; font-weight:700;
}

/* ---------------- MARCA TÉCNICA DE PAGINAÇÃO (invisível) ---------------- */
.doc,.divisoria{ position:relative; }
.mkpg{ font-size:1.5pt; line-height:0; color:#FFFFFF; letter-spacing:-.2pt; }

/* ---------------- ABERTURA DE SEÇÃO EDITORIAL ---------------- */
.editorial h1{ break-before:page; }
"""

# ===========================================================================
# TEXTOS EDITORIAIS
# ===========================================================================

APRESENTACAO = """
# APRESENTAÇÃO

Esta apostila nasceu de uma decisão simples: **não produzir mais um resumo**.

Resumo é útil para quem já sabe. Quem está entrando em Seguridade Social precisa de outra
coisa — precisa entender o instituto, ver a lei, reconhecer a armadilha e resolver a questão.
Nessa ordem. Repetidas vezes.

## O que você tem em mãos

Um **curso completo em formato de apostila**, com 39 módulos, 7 simulados comentados e seis
capítulos dedicados exclusivamente às pegadinhas de prova. O conteúdo cobre todos os blocos
do programa de Seguridade Social para o cargo de Técnico do Seguro Social — dos fundamentos
constitucionais ao custeio, dos benefícios ao processo administrativo.

Cada módulo segue **sempre a mesma ordem interna**, para que você crie automatismo de leitura:

> conceito · definição para a prova · fundamento legal · explicação detalhada ·
> exemplo prático · atenção · pegadinhas · como a banca cobra · resumo · memorização ·
> questões comentadas · revisão de 5 e de 15 minutos

## O método em quatro camadas

O material foi desenhado para funcionar com **revisão espaçada**. Ele o leva por quatro
camadas sucessivas, e não por uma leitura linear:

**Entender** — a intuição do instituto, em linguagem simples.
**Decorar** — lei seca, prazos, requisitos, tabelas e mnemônicos.
**Prova** — as pegadinhas e o estilo de cobrança das bancas.
**Revisar** — resumos de 5 e 15 minutos, flashcards e simulados.

## Sobre os flashcards que acompanham esta apostila

Os baralhos que vêm no pacote **não são um brinde**: são parte do método. Cada módulo termina
indicando os cartões correspondentes, e o capítulo *Como usar os flashcards* explica a
configuração de revisão recomendada.

A regra é uma só: **você não terminou um módulo quando o leu — terminou quando errou,
corrigiu e transformou o erro em cartão.**

## Um compromisso com a honestidade jurídica

Este material não inventa artigo, prazo, requisito nem jurisprudência. Onde o texto legal é
decisivo, ele aparece entre aspas e com o dispositivo indicado. Onde há divergência, o
material separa explicitamente o que é **texto legal**, o que é **jurisprudência**, o que é
**doutrina** e o que é **entendimento predominante em concursos**.

E onde um ponto depende de valor anual, de tabela progressiva ou de norma infralegal — que
mudam —, há uma marca de **conferir na fonte oficial**. São mais de 150 marcações ao longo do
livro. Elas existem porque preferir o *"não sei ao certo"* ao *"eu acho"* é exatamente o
hábito que separa quem passa de quem quase passa.

Bons estudos — e boa prova.
"""


def _apresentacao_html(indice, pref):
    return converter(APRESENTACAO.strip(), indice, pref)


# ===========================================================================
# MONTAGEM
# ===========================================================================

def _rot(numero):
    """Rótulo da divisória: 'VOLUME 1' para números, o próprio texto para o resto."""
    return ("VOLUME " + numero) if str(numero).isdigit() else str(numero)


def _ler(rel):
    with open(os.path.join(BASE, rel.replace("/", os.sep)), "r", encoding="utf-8") as f:
        return f.read()


def gerar(paginas=None, edicao="1ª edição"):
    """Monta o HTML completo. `paginas` = {ancora: numero} (2º passe)."""
    paginas = paginas or {}
    corpo, sumario, ancoras = [], [], []
    item_idx = 0

    # ---------- CAPA ----------
    corpo.append("""
<section class="capa">
  <div class="moldura"></div>
  <div class="conteudo">
    <div class="selo">Apostila preparatória</div>
    %s
    <h1>%s</h1>
    <div class="filete"></div>
    <div class="sub">%s</div>
    <div class="cargo">%s</div>
    <div class="pilares">
      <div class="pilar"><b>SAÚDE</b><span>arts. 196 a 200</span></div>
      <div class="pilar"><b>PREVIDÊNCIA</b><span>arts. 201 e 202</span></div>
      <div class="pilar"><b>ASSISTÊNCIA</b><span>arts. 203 e 204</span></div>
    </div>
    <div class="rodape">
      <b>39 módulos &middot; 7 simulados comentados &middot; 6 capítulos de pegadinhas</b><br>
      CF/88 &middot; Lei 8.212/1991 &middot; Lei 8.213/1991 &middot; Lei 8.742/1993 &middot;
      Decreto 3.048/1999 &middot; EC 103/2019
    </div>
  </div>
</section>""" % (EMBLEMA, TITULO, SUBTITULO, CARGO.upper()))

    # ---------- FOLHA DE ROSTO ----------
    corpo.append("""
<section class="rosto">
  <h1>%s</h1>
  <div class="sub">%s</div>
  <div class="linha-ouro"></div>
  <div class="ficha"><dl>
    <dt>Cargo-alvo</dt><dd>%s — Instituto Nacional do Seguro Social</dd>
    <dt>Disciplina</dt><dd>Seguridade Social e Direito Previdenciário</dd>
    <dt>Conteúdo</dt><dd>39 módulos, 7 simulados comentados e 6 capítulos de pegadinhas</dd>
    <dt>Método</dt><dd>Entender &rarr; Decorar &rarr; Prova &rarr; Revisar, com flashcards e revisão espaçada</dd>
    <dt>Matriz</dt><dd>Edital n&ordm; 1/2022 como matriz de assuntos, com a legislação vigente</dd>
    <dt>Edição</dt><dd>%s</dd>
  </dl></div>
  <div class="aviso">
    <b>Aviso importante.</b> Esta apostila usa o último edital publicado apenas como
    <b>matriz de assuntos</b> e explica a <b>legislação vigente</b>. Edital é mapa de conteúdo,
    não fotografia da lei.<br><br>
    Todo ponto sujeito a alteração legislativa, a valor monetário anual ou a detalhe
    regulamentar está sinalizado com <b>conferir na fonte oficial</b>. Quando encontrar essa
    marca, consulte o texto compilado no Planalto ou no portal do INSS <b>antes de decorar</b>.
    A responsabilidade pela conferência final é sempre do candidato.
  </div>
</section>""" % (TITULO, SUBTITULO, CARGO, edicao))

    # ---------- CONTEÚDO ----------
    for parte in PARTES:
        if parte["tipo"] == "parte":
            aid = "parte-" + slug(parte["titulo"])[:40]
            ancoras.append(aid)
            npart = len([x for x in sumario if x["tipo"] == "parte"])
            corpo.append(
                '<section class="divisoria" id="' + aid + '">'
                '<div class="faixa"></div>'
                '<div class="num">' + _rot(parte["numero"]) + '</div>'
                '<h2>' + _html.escape(parte["titulo"]) + '</h2>'
                '<div class="sub">' + _html.escape(parte.get("subtitulo", "")) + '</div>'
                '<div class="ilu">' + ILUSTRACOES.get(parte.get("svg", ""), "") + '</div>'
                '<div class="rodape"><span class="mkpg">[[P%02d]]</span>' % npart +
                TITULO + ' &middot; ' + CARGO + '</div></section>')
            sumario.append({"tipo": "parte", "numero": parte["numero"],
                            "titulo": parte["titulo"], "id": aid})
        else:
            sumario.append({"tipo": "parte", "numero": "", "titulo": parte["titulo"], "id": None})

        for idx, (arq, titulo, rotulo, secoes) in enumerate(parte["itens"]):
            pref = slug(os.path.basename(arq))[:26] or "sec"
            indice = []
            if arq == "__APRESENTACAO__":
                html_doc = _apresentacao_html(indice, pref)
            else:
                md = _ler(arq)
                if secoes:
                    md = extrair_secoes(md, secoes)
                    md = limpar(md, secoes_removidas=False)
                    md = "# " + titulo.upper() + "\n\n" + md
                    md = md.replace("\n## ", "\n## ")
                else:
                    md = limpar(md)
                html_doc = converter(md, indice, pref)

            classe = "editorial"
            marca = '<span class="mkpg">[[A%04d]]</span>' % item_idx
            pos = html_doc.find("<h1")
            fim = html_doc.find("</h1>", pos) if pos >= 0 else -1
            if fim >= 0:
                html_doc = html_doc[:fim] + marca + html_doc[fim:]
            else:
                html_doc = marca + html_doc
            corpo.append('<section class="doc %s">%s</section>' % (classe, html_doc))

            # âncora principal do item = primeiro h1
            h1s = [x for x in indice if x["nivel"] == 1]
            aid = h1s[0]["id"] if h1s else (pref + "-top")
            if not h1s:
                corpo[-1] = corpo[-1].replace('<section class="doc',
                                              '<section id="%s" class="doc' % aid, 1)
            ancoras.append(aid)
            sumario.append({"tipo": "item", "titulo": titulo, "id": aid, "rotulo": rotulo})
            item_idx += 1

    # ---------- SUMÁRIO ----------
    li = []
    for e in sumario:
        if e["tipo"] == "parte":
            rot = ("<i>%s</i>" % _rot(e["numero"])) if e["numero"] else ""
            li.append('<li class="s-parte">%s%s</li>' % (rot, _html.escape(e["titulo"])))
        else:
            num = paginas.get(e["id"])
            oculto = "" if num else " oculto"
            li.append('<li class="s-item%s"><a href="#%s"><span class="s-t">%s</span>'
                      '<span class="s-d"></span><span class="s-p">%s</span></a></li>'
                      % (oculto, e["id"], _html.escape(e["titulo"]), num or "000"))
    sumario_html = ('<section class="sumario"><h1>SUMÁRIO</h1><ol>%s</ol></section>'
                    % "".join(li))

    doc = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>%s — %s</title><style>%s</style></head><body>
%s
%s
%s
</body></html>""" % (TITULO, CARGO, CSS, corpo[0] + corpo[1], sumario_html,
                     "\n".join(corpo[2:]))

    ordem = [e["id"] for e in sumario if e["tipo"] == "item"]
    titulos = {e["id"]: e["titulo"] for e in sumario if e["tipo"] == "item"}
    partes_ord = [(e["numero"], e["titulo"], e["id"]) for e in sumario
                  if e["tipo"] == "parte" and e["id"]]
    return doc, ordem, titulos, partes_ord
