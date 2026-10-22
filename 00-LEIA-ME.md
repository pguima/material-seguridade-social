# SEGURIDADE SOCIAL — PREPARAÇÃO COMPLETA PARA O INSS
## Técnico do Seguro Social

> **Como usar este material.** Leia esta página uma única vez, com calma. Ela define o método.
> Todo o resto do material foi construído para funcionar dentro deste método.

---

## 1. O que é este material

Não é um resumo. Não é uma apostila para ler passivamente.

É um **curso em quatro camadas**, desenhado para o ciclo de estudo com revisão espaçada (Anki):

| Camada | Objetivo | Onde está no material |
|---|---|---|
| **1 — Entender** | Formar a intuição do instituto | Seções *Conceito*, *Explicação detalhada*, *Exemplo prático* |
| **2 — Decorar** | Fixar lei seca, prazos, requisitos | Seções *Fundamento legal*, *Memorização*, tabelas, mapas |
| **3 — Prova** | Reconhecer a armadilha antes de cair nela | Seções *Atenção!*, *Pegadinhas*, *Como a banca cobra*, *Questões* |
| **4 — Revisar** | Manter o conteúdo vivo até a prova | *Revisão de 5 min*, *Revisão de 15 min*, flashcards, simulados |

---

## 2. Estrutura de arquivos

```
00-LEIA-ME.md                  ← você está aqui (método)
01-MATRIZ-DE-ESTUDOS.md        ← mapa completo do conteúdo, com prioridades
02-PEGADINHAS-VOLUME-1.md      ← as diferenças que a banca quer que você confunda
03-PEGADINHAS-VOLUME-2.md

modulos/
  ── VOLUME 1 — FUNDAMENTOS ──
  M01-conceito-e-estrutura-da-seguridade-social.md
  M02-principios-e-objetivos-art-194.md
  M03-financiamento-e-orcamento-art-195.md
  M04-saude.md
  M05-assistencia-social-loas-bpc.md
  M06-previdencia-social-rgps-art-201.md
  ── VOLUME 2 — RGPS ──
  M07-rgps-estrutura-e-beneficiarios.md
  M08-segurados-empregado-domestico-avulso.md
  M09-contribuinte-individual-e-segurado-especial.md
  M10-facultativo-excluidos-e-quem-e-quem.md
  M11-dependentes.md
  M12-filiacao-e-inscricao.md
  M13-qualidade-de-segurado-e-periodo-de-graca.md
  M14-carencia.md
  ── VOLUME 3 — BENEFÍCIOS ──
  M15-salario-de-beneficio-e-rmi.md
  M16-beneficios-por-incapacidade.md
  M17-aposentadoria-programada-e-por-idade.md
  M18-aposentadoria-especial-e-da-pessoa-com-deficiencia.md
  M19-ec-103-transicao-e-direito-adquirido.md
  M20-pensao-por-morte-e-auxilio-reclusao.md
  M21-salario-familia-e-salario-maternidade.md
  M22-servicos-acumulacao-e-tabela-geral.md
  ── VOLUME 4 — CUSTEIO ──
  M23-empresa-equiparados-e-empregador-domestico.md
  M24-salario-de-contribuicao-conceito-e-limites.md
  M25-parcelas-integrantes-e-nao-integrantes.md
  M26-contribuicao-dos-segurados.md
  M27-contribuicao-das-empresas.md
  M28-contribuicoes-sobre-producao-rural-e-outras-fontes.md
  M29-arrecadacao-recolhimento-e-obrigacoes-acessorias.md
  M30-decadencia-prescricao-restituicao-e-crimes.md
  M31-processo-administrativo-previdenciario.md
  ── VOLUME 5 — RPPS E ESPECIAIS ──
  M32-rpps-regime-proprio-de-previdencia-social.md
  M33-contagem-reciproca-ctc-e-previdencia-complementar.md
  M34-beneficios-de-legislacoes-especiais.md
  M35-conteudo-complementar-do-edital.md
  ── VOLUME 6 — REVISÃO FINAL ──
  M36-mapas-mentais-e-quadros-consolidados.md
  M37-lei-seca-comentada.md
  M38-100-pontos-essenciais.md
  M39-sistema-de-revisao-final.md

caderno-de-erros.md            ← seu material mais valioso (preencher!)

flashcards/
  anki-volume-1.tsv            ← importar direto no Anki
  anki-volume-2.tsv
  anki-volume-3.tsv
  anki-volume-4.tsv
  anki-volume-5.tsv
  anki-volume-6-revisao.tsv    ← baralho de emergência

simulados/
  simulado-01-fundamentos.md
  simulado-02-rgps.md
  simulado-03-beneficios.md
  simulado-04-custeio.md
  simulado-05-rpps-e-especiais.md
  simulado-06-nivel-prova.md
  simulado-07-nivel-dificil.md

apostila/
  apostila-seguridade-social.html   ← versão A4 para imprimir / salvar em PDF

tools/
  gerar_apostila.py            ← regera a apostila a partir dos .md
```

### Os .md são a FONTE; a apostila é derivada

Sempre edite os arquivos `.md`. Depois rode o gerador para atualizar a apostila A4:

```powershell
python tools/gerar_apostila.py                  # apostila completa
python tools/gerar_apostila.py --vol 3          # só o Volume 3
python tools/gerar_apostila.py --vol 2 --vol 3  # Volumes 2 e 3
```

**Para gerar o PDF:** abra o HTML no Chrome ou Edge → **Ctrl+P** → Destino **Salvar como PDF**
→ papel **A4**, margens **Padrão**, escala **100%** → marque **"Gráficos de segundo plano"**
(sem isso as caixas coloridas somem) e **"Cabeçalhos e rodapés"** (para numerar as páginas).

Cada módulo segue **sempre a mesma ordem interna**, para você criar automatismo de leitura:

```
1. Conceito              7. Pegadinhas de prova
2. Definição para a prova 8. Como a banca pode cobrar
3. Fundamento legal       9. Resumo
4. Explicação detalhada  10. Memorização
5. Exemplo prático       11. Questões comentadas
6. Atenção!              12. Revisão 5 min / 15 min / Flashcards
```

---

## 3. Legenda de prioridade

Usada em toda a matriz e no cabeçalho de cada tópico.

| Marca | Nível | Significado prático |
|---|---|---|
| 🔴 | **5 — Essencial** | Domínio profundo. Você tem que acertar de olhos fechados. |
| 🟠 | **4 — Muito importante** | Domínio forte. Erro aqui custa vaga. |
| 🟡 | **3 — Importante** | Saber bem, sem obsessão. |
| 🟢 | **2 — Complementar** | Estudar depois dos principais. |
| ⚪ | **1 — Residual** | Leitura + flashcard. Não gastar horas. |

E o **tipo de estudo** exigido:

| Código | Significa |
|---|---|
| **E** | Entender (raciocínio, lógica do instituto) |
| **D** | Decorar (prazo, rol, requisito, número) |
| **L** | Lei seca (ler o dispositivo na fonte) |
| **Q** | Questões (obrigatoriamente resolver) |
| **A** | Anki (vira flashcard) |

---

## 4. O ciclo de estudo (siga isto para cada módulo)

```
① TEORIA        30–60 min   Ler o módulo inteiro, sem parar para decorar.
        ↓
② LEI SECA      15–30 min   Abrir o dispositivo citado e ler o texto original.
        ↓
③ EXEMPLO         5 min     Reescrever o exemplo com seus próprios dados.
        ↓
④ PEGADINHA      10 min     Ler a seção de pegadinhas e marcar as que te pegariam.
        ↓
⑤ QUESTÕES       20 min     Resolver as questões SEM olhar o gabarito.
        ↓
⑥ ERROS          10 min     Todo erro vira card no Caderno de Erros (item 6 abaixo).
        ↓
⑦ FLASHCARDS      5 min     Importar o .tsv do módulo no Anki.
        ↓
⑧ REVISÃO       Anki: 1d → 3d → 7d → 15d → 30d
```

> **Regra de ouro:** você não terminou um módulo quando leu. Você terminou quando
> errou, corrigiu e transformou o erro em flashcard.

---

## 5. Como importar os flashcards no Anki

1. Abra o Anki → **Arquivo → Importar**.
2. Selecione `flashcards/anki-volume-1.tsv` (e, depois, `anki-volume-2.tsv`).
3. Tipo de nota: **Básico** (Frente / Verso).
4. Separador: **Tabulação** (o arquivo já declara `#separator:tab`).
5. Marque **"Permitir HTML nos campos"**.

Cada arquivo já traz `#deck` e `#tags` nas linhas iniciais — o Anki cria os baralhos
`INSS::Seguridade Social::Volume 1` e `::Volume 2` sozinho, e etiqueta cada card com o
módulo de origem (`m01`, `m08`…) e com marcadores temáticos (`pegadinha`, `mnemonico`,
`carencia`…).

> 🎯 **Use as etiquetas.** Antes da prova, um baralho filtrado só com `tag:pegadinha`
> vale mais que reler a apostila inteira.

**Configuração de revisão sugerida:** novos cards/dia = 20; revisões/dia = 200;
intervalo máximo = 180 dias (a prova não está a 5 anos de distância).

---

## 6. Caderno de Erros (o material mais poderoso que você vai ter)

Crie um arquivo `caderno-de-erros.md` e registre **todo** erro neste formato:

```
### ERRO #001
**Assunto:** Filiação × Inscrição
**Data:** 10/08/2026
**O que eu pensei:** que a inscrição é que gera o vínculo com a Previdência.
**O correto:** o vínculo nasce da FILIAÇÃO (exercício de atividade remunerada).
              A inscrição é apenas o ato formal de cadastro.
**Por que errei:** confundi ato formal com efeito jurídico.
**Como a banca me engana:** troca as duas palavras na assertiva.
**Vira flashcard?** SIM
```

Revise o caderno de erros **toda sexta-feira**. Em 60 dias ele vale mais que a apostila.

---

## 7. Aviso metodológico obrigatório (leia)

**Este material usa o Edital nº 1/2022 (Cebraspe) como matriz de conteúdo, mas explica
a legislação VIGENTE.** Edital é mapa de assuntos; não é fotografia da lei.

Regras que segui na produção:

1. **Não invento artigo, inciso, parágrafo, prazo ou requisito.**
2. Onde o texto legal é decisivo, ele aparece **entre aspas e com o dispositivo indicado**.
3. Onde há divergência, separo explicitamente:
   `TEXTO LEGAL` × `JURISPRUDÊNCIA` × `DOUTRINA` × `ENTENDIMENTO DE CONCURSO`.
4. Todo ponto que dependa de norma alterada recentemente, de valor monetário anual
   ou de detalhe regulamentar leva a marca:

   > ⚠️ **CONFERIR NA FONTE OFICIAL** — ponto sujeito a alteração/atualização.

   Quando ver essa marca, **abra o Planalto ou o gov.br/inss antes de decorar**.

**Fontes primárias para conferência:**

| Norma | Onde |
|---|---|
| CF/88, arts. 194 a 204 | planalto.gov.br → Constituição |
| Lei 8.212/1991 (Custeio) | planalto.gov.br |
| Lei 8.213/1991 (Benefícios) | planalto.gov.br |
| Decreto 3.048/1999 (RPS) | planalto.gov.br |
| Lei 8.742/1993 (LOAS) | planalto.gov.br |
| EC 103/2019 | planalto.gov.br |
| IN PRES/INSS nº 128/2022 | gov.br/inss → Legislação → Instrução Normativa |

> A IN 128/2022 **continua vigente e já sofreu diversas alterações**. Nunca estude
> IN por print antigo: sempre a versão compilada no site do INSS.

---

## 8. O que já está pronto e o que vem depois

**PRONTO — VOLUME 1: FUNDAMENTOS DA SEGURIDADE SOCIAL**
- M01 Conceito e estrutura · M02 Princípios e objetivos (art. 194)
- M03 Financiamento e orçamento (art. 195) · M04 Saúde
- M05 Assistência Social / LOAS / BPC / Auxílio-Inclusão
- M06 Previdência Social e RGPS (art. 201)
- Pegadinhas do Volume 1, flashcards e Simulado 1

**PRONTO — VOLUME 2: REGIME GERAL DE PREVIDÊNCIA SOCIAL**
- M07 Estrutura do RGPS, beneficiários e prestações
- M08 Empregado · Empregado doméstico · Trabalhador avulso
- M09 Contribuinte individual · Segurado especial
- M10 Facultativo, excluídos e a tabela **"Quem é quem no RGPS"**
- M11 Dependentes · M12 Filiação e inscrição
- M13 Qualidade de segurado e período de graça · M14 Carência
- Pegadinhas do Volume 2, flashcards e Simulado 2

**PRONTO — VOLUME 3: BENEFÍCIOS E SERVIÇOS DO RGPS**
- M15 Salário de benefício e RMI (cálculo pós-EC 103)
- M16 Benefícios por incapacidade e auxílio-acidente
- M17 Aposentadoria programada, por idade, rural e híbrida
- M18 Aposentadoria especial e da pessoa com deficiência
- M19 EC 103/2019: as cinco transições e o direito adquirido
- M20 Pensão por morte e auxílio-reclusão
- M21 Salário-família e salário-maternidade
- M22 Serviços, acumulação e **tabela geral dos benefícios**
- Pegadinhas do Volume 3, flashcards e Simulado 3

**PRONTO — VOLUME 4: CUSTEIO DA SEGURIDADE SOCIAL**
- M23 Empresa, equiparados e empregador doméstico
- M24 Salário de contribuição: conceito e limites
- M25 Parcelas integrantes e não integrantes (art. 28, §9º)
- M26 Contribuição dos segurados
- M27 Contribuição das empresas (patronal, RAT, FAP, terceiros)
- M28 Produção rural, agroindústria, prognósticos e outras fontes
- M29 Arrecadação, recolhimento e obrigações acessórias
- M30 Decadência, prescrição, restituição e crimes
- M31 Processo administrativo previdenciário
- Pegadinhas do Volume 4, flashcards e Simulado 4

> ⚠️ **O Volume 4 é o que mais envelhece.** Todo valor em reais (teto, faixas de alíquota,
> cota do salário-família, limite de baixa renda) muda **todo ano**. Uma semana antes da
> prova, confira no Planalto e no gov.br **todos os pontos marcados com ⚠️** nesse volume.

**PRONTO — VOLUME 5: RPPS, LEGISLAÇÕES ESPECIAIS E COMPLEMENTAR**
- M32 RPPS — conceito, comparação com o RGPS e regras da EC 103
- M33 Contagem recíproca, CTC, compensação e previdência complementar
- M34 Benefícios de legislações especiais e seguro-defeso
- M35 Conteúdo complementar do edital
- Pegadinhas do Volume 5, flashcards e Simulado 5

> 🎓 **Com o Volume 5, TODO O CONTEÚDO PROGRAMÁTICO está coberto.** Os 13 blocos da
> `01-MATRIZ-DE-ESTUDOS.md` têm material correspondente.

**PRONTO — VOLUME 6: REVISÃO FINAL**
- M36 Mapas mentais e quadros consolidados (todos os volumes)
- M37 Lei seca comentada — os dispositivos que caem literalmente
- M38 **100 pontos que você precisa saber sobre Seguridade Social**
- M39 Sistema de revisão final — 30 dias / 7 dias / 24 horas / emergência
- Simulado 6 (nível prova, 50 questões) e Simulado 7 (nível difícil, 40 questões)
- `caderno-de-erros.md` — modelo pronto para preencher
- Baralho de emergência (`anki-volume-6-revisao.tsv`)

---

## 🎓 CURSO COMPLETO

**39 módulos · 7 simulados · 6 arquivos de pegadinhas · 420+ flashcards.**
Todos os 13 blocos do conteúdo programático cobertos.

**Se você está começando agora:** siga o cronograma do item 9.
**Se já estudou tudo:** vá direto ao `M39` e execute a revisão de 30 dias.
**Se a prova é amanhã:** leia o `M38` (100 pontos) e o painel de números do `M39`.
- **Volume 6 — Revisão final:** mapas mentais, lei seca comentada, "100 pontos",
  simulados 3 a 6, revisão de 24h / 7 dias / 30 dias

---

## 9. Ordem de ataque recomendada (30 semanas)

### Volume 1 — Fundamentos

| Semana | Módulos | Meta |
|---|---|---|
| 1 | M01 + M02 | Dominar art. 194 e os 7 objetivos com palavras-chave |
| 2 | M03 + M04 | Dominar art. 195 (fontes) e diferenciar Saúde das demais |
| 3 | M05 + M06 | BPC × benefício previdenciário; caráter contributivo |
| 4 | Pegadinhas Vol. 1 + **Simulado 1** | Fechar o Volume 1 com ≥ 80% |

### Volume 2 — RGPS

| Semana | Módulos | Meta |
|---|---|---|
| 5 | M07 + M08 | Enquadrar empregado, doméstico e avulso sem hesitar |
| 6 | M09 + M10 | Números do segurado especial; tabela "Quem é quem no RGPS" |
| 7 | M11 + M12 | Casos práticos de dependentes; filiação × inscrição |
| 8 | M13 + M14 | Prazos ∞·12·12·12·3·6 e carências 12·180·10·24 na ponta da língua |
| 9 | Pegadinhas Vol. 2 + **Simulado 2** | Fechar o Volume 2 com ≥ 80% |

### Volume 3 — Benefícios

| Semana | Módulos | Meta |
|---|---|---|
| 10 | M15 | Calcular a RMI de qualquer tempo de contribuição em 10 segundos |
| 11 | M16 | Dominar as transições entre os três benefícios por incapacidade |
| 12 | M17 | Aplicar o marco 13/11/2019 antes de escolher os números |
| 13 | M18 | Tabelas 15/20/25 → 55/58/60 → 66/76/86 e a da PcD |
| 14 | M19 | Reproduzir a tabela-mestra das cinco transições |
| 15 | M20 | Valor e duração da pensão; contraste com o auxílio-reclusão |
| 16 | M21 + M22 | Rols restritos, acumulação e tabela geral dos benefícios |
| 17 | Pegadinhas Vol. 3 + **Simulado 3** | Fechar o Volume 3 com ≥ 80% |

### Volume 4 — Custeio

| Semana | Módulos | Meta |
|---|---|---|
| 18 | M23 + M24 | Conceito de empresa (C-O-C-A-M) e salário de contribuição por categoria |
| 19 | M25 | Critério-mestre, as três chaves e o C-P-A da totalidade |
| 20 | M26 + M27 | Alíquotas: 7,5/9/12/14 · 20/11/5 · 20/RAT/20 · FAP |
| 21 | M28 + M29 | Produção rural, sub-rogação e os prazos 7 · 15 · 20 |
| 22 | M30 + M31 | "5 e 5 / 10 e 5", crimes e instâncias do CRPS |
| 23 | Pegadinhas Vol. 4 + **Simulado 4** | Fechar o Volume 4 com ≥ 80% |

### Volume 5 — RPPS e especiais

| Semana | Módulos | Meta |
|---|---|---|
| 24 | M32 + M33 | Quadro RGPS × RPPS; D-C-U-I e C-A-F-R |
| 25 | M34 + M35 | Palavras-âncora e a tabela de natureza jurídica |
| 26 | Pegadinhas Vol. 5 + **Simulado 5** | Fechar o Volume 5 com ≥ 80% |

### Volume 6 — Revisão final (as últimas 4 semanas antes da prova)

| Semana | Foco | Meta |
|---|---|---|
| 27 | `M36` + `M37` · refazer Simulados 1 e 2 | Reproduzir os mapas e recitar a lei seca |
| 28 | `M38` · refazer Simulados 3 e 4 | Explicar 90 dos 100 pontos |
| 29 | Refazer Simulado 5 + **Simulado 6** (nível prova) | **≥ 85%** |
| 30 | **Simulado 7** (nível difícil) + roteiro de 7 dias do `M39` | **≥ 75%** |

> A partir da semana 27, **o cronograma detalhado está no `M39`** — inclusive os roteiros de
> 30 dias, 7 dias, 24 horas e a revisão de emergência de 20 minutos.

> Se acertar menos de 70% em um simulado, **não avance**. Refaça o ciclo dos módulos
> com pior desempenho — o próprio simulado indica quais no diagnóstico final.

### As peças que se carregam de um volume para o outro

**Do Volume 2 para o 3:**
1. a tabela **"Quem é quem no RGPS"** (M10);
2. os prazos do **período de graça** e a escada **12 → 24 → 36** (M13);
3. as **carências** do art. 25 e o rol de dispensas do art. 26 (M14).

**Do Volume 3 para o 4:**
1. a **tabela geral dos benefícios** (M22, item 3);
2. a fórmula **60% + 2 p.p.** e os coeficientes **60 · 91 · 50 · 100** (M15);
3. a noção de **salário de contribuição**, que abre o Custeio.

**Do Volume 4 para o 5:**
1. o painel de alíquotas (M26 e M27);
2. os prazos **7 · 15 · 20** e **5 e 5 / 10 e 5** (M29 e M30);
3. a distinção **RGPS × RPPS**, que abre o Volume 5.

Sem essas peças, o volume seguinte vira decoreba solta.
