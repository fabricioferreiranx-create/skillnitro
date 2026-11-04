# skillnitro

Skills do Claude Code para montagens de imagens da Nitro.

## montagem-resultado-campo

Monta o story "Resultado de campo" (antes e depois de uma aplicação em lavoura, 1080×1920)
a partir de um modelo aprovado: fotos de campo com divisão diagonal e horizonte visível,
faixas de produto com 3 benefícios, dados da área, faixa de chamada ("Fale com seu RTV"),
RTV e logos Nitro + Vale.

Conteúdo: `.claude/skills/montagem-resultado-campo/`
- `SKILL.md`: passo a passo e regras de design
- `templates/resultado-story.dc.html`: modelo do layout
- `scripts/prepare_assets.py`: recorte de fotos, logos em branco com fundo transparente, remoção de fundo de embalagens (precisa de `pillow` e `numpy`)

### Instalar em qualquer projeto ou no seu computador

```bash
cp -r .claude/skills/montagem-resultado-campo ~/.claude/skills/
```

Depois é só pedir: "monta um resultado de campo" e enviar as fotos.
