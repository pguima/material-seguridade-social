#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline de produção do PDF da apostila.

  1) gera o HTML (passe 1, sumário sem números)
  2) renderiza em PDF com o Chrome headless
  3) lê os links internos do sumário para descobrir a página de cada capítulo
  4) regera o HTML já com os números de página reais
  5) renderiza o PDF definitivo
  6) acrescenta rodapés numerados, marcadores (bookmarks) e metadados

Uso:  python tools/build_pdf.py
"""

import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fitz  # PyMuPDF
from apostila_config import CARGO, SUBTITULO, TITULO
from apostila_layout import gerar

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA_DIR = os.path.join(BASE, "pdf")
NOME = "Seguridade-Social-Apostila-Completa-INSS"

NAVEGADORES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

COR_OURO = (0.65, 0.48, 0.05)
COR_AZUL = (0.055, 0.165, 0.278)
COR_CINZA = (0.42, 0.47, 0.52)


def navegador():
    for c in NAVEGADORES:
        if os.path.exists(c):
            return c
    raise SystemExit("Chrome ou Edge não encontrado.")


def html_para_pdf(html_path, pdf_path, exe):
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    url = "file:///" + html_path.replace("\\", "/").replace(" ", "%20")
    base_args = [
        exe, "--disable-gpu", "--no-sandbox", "--disable-extensions",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=120000",
        "--print-to-pdf=" + pdf_path, url,
    ]
    for modo in ("--headless=new", "--headless"):
        try:
            subprocess.run([base_args[0], modo] + base_args[1:],
                           timeout=900, capture_output=True)
        except subprocess.TimeoutExpired:
            pass
        for _ in range(30):
            if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 50_000:
                return
            time.sleep(1)
    raise SystemExit("Falha ao gerar %s" % pdf_path)


def mapear_paginas(pdf_path, ordem):
    """Localiza as marcas técnicas [[Annnn]] e devolve {ancora: pagina}."""
    import re as _re
    doc = fitz.open(pdf_path)
    achados = {}
    for i in range(doc.page_count):
        for m in _re.finditer(r"\[\[A(\d{4})\]\]", doc[i].get_text("text")):
            k = int(m.group(1))
            achados.setdefault(k, i)
    doc.close()
    if len(achados) < len(ordem):
        print("  ! marcas encontradas: %d de %d" % (len(achados), len(ordem)))
    return {anc: achados[i] for i, anc in enumerate(ordem) if i in achados}


def limpar_marcas(doc):
    """Remove do PDF as marcas técnicas usadas na paginação."""
    import re as _re
    n = 0
    for page in doc:
        if not _re.search(r"\[\[[AP]\d+\]\]", page.get_text("text")):
            continue
        for padrao in _re.findall(r"\[\[[AP]\d+\]\]", page.get_text("text")):
            for r in page.search_for(padrao):
                page.add_redact_annot(r)
                n += 1
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                              graphics=fitz.PDF_REDACT_LINE_ART_NONE)
    return n


def acabamento(pdf_path, final_path, ordem, titulos, partes_ord, mapa):
    doc = fitz.open(pdf_path)
    total = doc.page_count

    # primeira página de conteúdo (Apresentação) -> passa a ser a página 1
    offset = mapa.get(ordem[0], 0) if ordem else 0

    # faixas de cada parte, para o título corrente
    faixas = []
    for numero, titulo, aid in partes_ord:
        primeiros = [mapa[a] for a in ordem if a in mapa]
        faixas.append((numero, titulo))
    # início de cada parte = página do 1º item que a compõe, menos a divisória
    inicios = []
    divisorias = set()
    from apostila_config import PARTES
    idx = 0
    for parte in PARTES:
        primeiro_item = parte["itens"][0][0]
        anc = ordem[idx] if idx < len(ordem) else None
        pg = mapa.get(anc, 0)
        rotulo = parte["titulo"] if parte["tipo"] == "parte" else "ABERTURA"
        if parte["tipo"] == "parte" and str(parte["numero"]).isdigit():
            rotulo = "VOLUME %s  ·  %s" % (parte["numero"], parte["titulo"])
        if parte["tipo"] == "parte":
            pg = max(0, pg - 1)  # inclui a divisória
            divisorias.add(pg)
        inicios.append((pg, rotulo))
        idx += len(parte["itens"])
    inicios.sort()

    def parte_da_pagina(i):
        atual = "ABERTURA"
        for pg, rot in inicios:
            if i >= pg:
                atual = rot
            else:
                break
        return atual

    marca = "%s  ·  %s" % (TITULO, CARGO)
    for i in range(total):
        page = doc[i]
        w, h = page.rect.width, page.rect.height
        if i < offset:
            continue                      # capa, folha de rosto e sumário sem rodapé
        if i in divisorias:
            continue                      # divisórias têm rodapé próprio
        num = str(i - offset + 1)
        y = h - 40
        page.draw_line(fitz.Point(54, y - 12), fitz.Point(w - 54, y - 12),
                       color=COR_OURO, width=0.6)
        recto = (i % 2 == 0)
        esq = parte_da_pagina(i)[:58] if recto else num
        dir_ = num if recto else marca
        page.insert_text(fitz.Point(54, y), esq, fontname="helv", fontsize=7.4,
                         color=COR_CINZA if recto else COR_AZUL)
        largura = fitz.get_text_length(dir_, fontname="helv", fontsize=7.4)
        page.insert_text(fitz.Point(w - 54 - largura, y), dir_, fontname="helv",
                         fontsize=7.4, color=COR_AZUL if recto else COR_CINZA)

    # marcadores
    toc = []
    idx = 0
    for parte in PARTES:
        anc = ordem[idx] if idx < len(ordem) else None
        pg = mapa.get(anc, 0)
        if parte["tipo"] == "parte":
            pg = max(0, pg - 1)
            rot = parte["numero"]
            rot = ("Volume " + rot) if str(rot).isdigit() else str(rot).title()
            toc.append([1, "%s — %s" % (rot, parte["titulo"]), pg + 1])
        else:
            toc.append([1, parte["titulo"], pg + 1])
        for arq, titulo, rot, sec in parte["itens"]:
            a = ordem[idx] if idx < len(ordem) else None
            toc.append([2, titulo, mapa.get(a, 0) + 1])
            idx += 1
    doc.set_toc(toc)

    marcas = limpar_marcas(doc)
    doc.set_metadata({
        "title": "%s — %s" % (TITULO, SUBTITULO),
        "author": "Apostila preparatória",
        "subject": "Seguridade Social e Direito Previdenciário — %s (INSS)" % CARGO,
        "keywords": "INSS, Seguridade Social, Direito Previdenciário, concurso, "
                    "Técnico do Seguro Social, RGPS, custeio, benefícios",
        "creator": "Apostila Seguridade Social",
    })
    doc.save(final_path, garbage=4, deflate=True)
    doc.close()
    return total


def main():
    os.makedirs(SAIDA_DIR, exist_ok=True)
    exe = navegador()
    print("Navegador:", os.path.basename(exe))

    h1 = os.path.join(SAIDA_DIR, "_passe1.html")
    p1 = os.path.join(SAIDA_DIR, "_passe1.pdf")
    h2 = os.path.join(SAIDA_DIR, "_passe2.html")
    p2 = os.path.join(SAIDA_DIR, "_passe2.pdf")
    final = os.path.join(SAIDA_DIR, NOME + ".pdf")

    print("[1/6] HTML — passe 1 …")
    doc1, ordem, titulos, partes_ord = gerar()
    open(h1, "w", encoding="utf-8").write(doc1)
    print("      %.1f MB · %d capítulos" % (len(doc1) / 1e6, len(ordem)))

    print("[2/6] PDF — passe 1 (Chrome) …")
    html_para_pdf(h1, p1, exe)

    print("[3/6] Mapeando páginas do sumário …")
    mapa = mapear_paginas(p1, ordem)
    offset = mapa.get(ordem[0], 0)
    exib = {a: (p - offset + 1) for a, p in mapa.items()}
    print("      %d capítulos localizados" % len(mapa))

    print("[4/6] HTML — passe 2 (sumário numerado) …")
    doc2, ordem2, titulos2, partes2 = gerar(paginas=exib)
    open(h2, "w", encoding="utf-8").write(doc2)

    print("[5/6] PDF — passe 2 …")
    html_para_pdf(h2, p2, exe)
    mapa2 = mapear_paginas(p2, ordem2)

    print("[6/6] Acabamento: rodapés, marcadores e metadados …")
    total = acabamento(p2, final, ordem2, titulos2, partes2, mapa2 or mapa)

    for tmp in (h1, p1, h2, p2):
        try:
            os.remove(tmp)
        except OSError:
            pass

    mb = os.path.getsize(final) / 1e6
    print("\nOK  →  pdf/%s.pdf" % NOME)
    print("    %d páginas · %.1f MB" % (total, mb))


if __name__ == "__main__":
    main()
