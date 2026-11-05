---
name: montagem-resultado-campo
description: Monta a imagem "Resultado de campo" (antes e depois de uma aplicação em lavoura) em formato story 1080×1920 como Artifact de Design. Use quando o usuário pedir para criar, montar ou refazer um post/story de resultado de campo, antes e depois, testemunha vs produto, com fotos da lavoura, produtos aplicados, benefícios, dados da área, RTV e logos (Nitro, Vale).
---

# Montagem de resultado de campo (story 1080×1920)

Gera uma imagem de antes e depois de campo, a partir do modelo aprovado pelo usuário.
O modelo está em `templates/resultado-story.dc.html`. As imagens são tratadas por
`scripts/prepare_assets.py` (precisa de `pillow` e `numpy`).

## O que pedir ao usuário (só o que faltar)

1. **Duas fotos de campo**: dia da aplicação e depois. Se as fotos vierem dentro de um
   exemplo (screenshot), recortar só a foto e **remover qualquer texto embutido**
   (etiquetas "Dia da aplicação", "11 dias após aplicação"), cortando acima/abaixo dele.
2. **Dias após a aplicação** (o número gigante do topo e a etiqueta da foto de baixo).
3. **Produtos, dose e benefícios.** Os benefícios vêm do portfólio Nitro (PDF): buscar com
   `pdftotext -layout` por nome do produto e ler a página (Read com `pages`). Nunca inventar
   benefício; se o produto não estiver no portfólio, perguntar.
4. **Dados da área**: cidade-UF, cultura, avaliação (dias A.A.).
5. **RTV** (nome).
6. **Fotos das embalagens** e **logos** (Nitro, Vale ou outros).

Perguntar apenas o que não foi dito. Texto ausente vira placeholder entre colchetes.

## Passo a passo

1. Criar o Artifact pelo tipo Design (`type_url` do Design, título, sem `file_path`), se ainda não existir um.
2. Tratar as imagens (`python3 scripts/prepare_assets.py ...`):
   - **Fotos de campo**: `crop ENTRADA SAIDA x0 y0 x1 y1`.
     Proporção alvo: foto de cima ≈ 952×500 (1,9:1), foto de baixo ≈ 952×480 (2:1).
   - **Logos**: `logo ENTRADA SAIDA` → branco, fundo transparente, 4× maior, borda afiada.
     Branco porque os logos originais são escuros e somem sobre o fundo verde. Avisar o
     usuário e oferecer versão colorida sobre faixa clara. Pedir arquivo vetorial (SVG/PDF/AI)
     quando os logos vierem pequenos.
   - **Embalagens**: `cutout-preto` (fundo preto) ou `cutout-branco` (fundo branco).
     Avisar que o recorte é automático e pode falhar em alças/bordas.
3. Subir cada imagem ao Artifact (`action: publish`, `asset: true`, `file_paths`) e
   anotar a URL `/_blob/<id>` de cada uma.
4. Copiar `templates/resultado-story.dc.html` para `project/Main.dc.html` e trocar:
   - `__FOTO_ANTES__`, `__FOTO_DEPOIS__`, `__PRODUTO1_IMG__`, `__PRODUTO2_IMG__`,
     `__LOGO_1__`, `__LOGO_2__` pelos ids dos assets;
   - os textos: número de dias (o "11", "11 dias após aplicação", "11 dias A.A."),
     nomes e doses dos produtos, listas de benefícios, cidade, cultura, RTV.
   O `project/canvas.json` usa um quadro 1080×1920 chamado `Main.dc.html`.
5. Publicar com `root` na pasta que contém `project/`, `file_path` = `project/canvas.json`
   (ou o html), e `files` com o html. Não verificar renderizando, a menos que o usuário peça.

## Regras de design já aprovadas (não mudar sem pedir)

- **Divisão das fotos**: diagonal suave. A foto de baixo começa mais acima e é recortada
  (`clip-path: polygon(0 23.3%, 100% 12.9%, ...)`) de modo que **a linha do horizonte
  (árvores ao fundo) apareça no corte**. O usuário aprovou isso. Ao trocar as fotos,
  conferir que o horizonte da foto de baixo fica abaixo da linha do corte; ajustar
  `object-position` ou os percentuais do polígono.
- Sem texto dentro das fotos além das etiquetas do layout.
- Cores: fundo verde-escuro em degradê, destaque verde-limão (prop `accent`, editável em Tweaks).
- Tipografia: Anton nos títulos, Archivo no resto.
- Cada produto é uma faixa na largura toda: nome + dose à esquerda, benefícios no meio,
  embalagem à direita. Máximo 3 benefícios por produto, os mais importantes do portfólio, uma linha cada (texto curto). Mais que isso deixa o layout apertado.
- Faixa de chamada (CTA) acima do rodapé: "Garanta esse resultado na sua lavoura" + botão "Fale com seu RTV" (pílula verde-limão).
- Rodapé: RTV à esquerda, logos brancos à direita separados por uma linha vertical.
- Espaço vertical é justo: com mais benefícios, reduzir o número do topo (hoje 170px) e os espaçamentos antes de mexer nas fotos.

## Avisos ao entregar

- Dizer que o link é privado até o usuário compartilhar pelo menu Share.
- Dizer o que foi recortado automaticamente e a resolução das fotos de origem.
- Listar placeholders que sobraram.

## Versão final aprovada (referência)

Exemplo aprovado pelo usuário: quadro "Resultado Canarana" (Soja, Canarana, 5 dias A.A., Revita 1 L/ha + Speed 1 kg/ha, RTV Fabricio F Fagundes).
Valores finais do template: padding 48px, espaçamento entre blocos 22px, número do topo 170px,
faixas de produto com min-height 160px, benefícios 22px (3 por produto), embalagens 172px (Revita) e 160px (Speed),
faixa CTA "Garanta esse resultado na sua lavoura" + botão "Fale com seu RTV" de 72px de altura.
Logos em branco (Nitro + Vale). RTV padrão: Fabricio F Fagundes (trocar só se o usuário pedir).
Benefícios aprovados — Revita: rápida recuperação da planta pós-estresses; redução de danos por fitotoxicidade;
maior desenvolvimento vegetal e vigor de plantas. Speed: balanço nutricional de macro e micronutrientes;
rápida eficiência de absorção de nutrientes; alta solubilidade e segurança de uso.

## Gerar vários quadros de uma vez (build_board.py)

`scripts/build_board.py spec.json SAIDA.dc.html` gera o quadro completo a partir de um JSON (veja o cabeçalho do script).
Dois layouts, ambos com a mesma identidade:
- `stacked`: antes/depois empilhado, fotos largas (recortar com proporção 952:500 e 952:480, horizonte a ~25-40% da altura da foto).
- `side`: controle x tratado lado a lado, para fotos em pé (proporção 540:880). Etiquetas "Controle" e nome do produto.
Produtos aceitam `tag` (ex.: "Gramíneas") e quantidade 1 ou 2 (o "+" só aparece com 2).
Dose desconhecida vira `[dose] kg/ha` e deve ser perguntada ao usuário. Cidade com UF: "Canarana – MT".

Quando o responsável não é RTV (ex.: consultor), usar `"rtv_label": "Consultor"` e `"cta_button": "Fale com seu consultor"` no spec.
Fotos em pé (celular, ~739x1600) em quadro `stacked`: recortar uma faixa horizontal 952:500 / 952:480 que inclua o horizonte; sem foto da área comparativa, o horizonte da foto de baixo fica a ~32% da altura.

Fotos de detalhe (close das plantas) abaixo das fotos principais: spec `details` + `photo_h` (ex.: 736) no `build_board.py`.
Recortar as fotos principais na nova proporção (952:`photo_h*500/880` e 952:`photo_h*480/880`) e os detalhes em 936x380. O número do topo e os espaços encolhem automaticamente.
Pedido de "4K": é ampliação por interpolação (Lanczos + realce leve), não cria detalhe; avisar o usuário e pedir a foto original.
