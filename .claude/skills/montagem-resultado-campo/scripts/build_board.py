#!/usr/bin/env python3
"""Gera o .dc.html de um quadro "Resultado de campo" (story 1080x1920).

Uso: build_board.py spec.json SAIDA.dc.html

spec.json:
{
  "title": "Resultado Canarana",
  "layout": "stacked" | "side",          # stacked = antes/depois empilhado; side = controle x tratado lado a lado (fotos em pé)
  "number": "5",                        # número grande do topo (dias após a aplicação)
  "photo_a": "<id do asset>", "photo_b": "<id do asset>",
  "label_a": "Dia da aplicação", "label_b": "5 dias após aplicação",
  "alt_a": "...", "alt_b": "...",
  "city": "Canarana – MT", "crop": "Soja", "eval": "5 dias A.A.",
  "rtv": "Fabricio F Fagundes", "rtv_label": "RTV" (opcional, ex.: "Consultor"), "cta_button": "Fale com seu RTV" (opcional),
  "logos": ["<id nitro branco>", "<id vale branco>"],
  "photo_h": 736,                      # (opcional) altura do bloco de fotos stacked; padrão 880
  "details": {"photo_a":"<id>","photo_b":"<id>","label_a":"...","label_b":"...","alt_a":"...","alt_b":"...","h":190},  # (opcional) faixa de fotos de detalhe (936x380); reduz número do topo e espaços
  "compact_rows": true,                # (opcional) faixas de produto mais baixas (use com 2 benefícios por produto)
  "tight": true,                       # (opcional) número do topo 130px e espaços 18px (último recurso)
  "products": [ {"name":"Revita","tag":"","dose":"1 L/ha","img":"<id>","img_h":172,"alt":"...","benefits":["...","...","..."]} ]
}
Fotos: layout stacked -> foto A com proporção 952:500 e foto B 952:480 (horizonte ~25-40% da altura);
layout side -> cada foto com proporção 540:880; ou lista de 2 fotos por lado (cada uma 540:440).
"""
import json, sys

BUL = '<div style="display: flex; align-items: flex-start; gap: 12px"><div style="flex: none; width: 9px; height: 9px; margin-top: 9px; background: {{accent}}"></div><div>%s</div></div>'
LAB = "position: absolute; font-weight: 800; font-size: 34px; letter-spacing: 3px; text-transform: uppercase; padding: 14px 24px; "
FIELD = '<div style="display: flex; flex-direction: column; gap: 2px"><div style="font-size: 20px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: #B9D9C2">%s</div><div style="font-size: 30px; font-weight: 800">%s</div></div>'


def row(p, compact=False):
    nm, ds, mh, pd = (52, 34, 132, 14) if compact else (58, 38, 160, 18)
    tag = ('<div style="font-weight: 800; font-size: 22px; letter-spacing: 3px; text-transform: uppercase; color: #B9D9C2">%s</div>' % p["tag"]) if p.get("tag") else ""
    bl = "\n".join(BUL % b for b in p["benefits"])
    return f'''<div style="position: relative; min-height: {mh}px; box-sizing: border-box; background: rgba(244,250,241,0.09); border: 2px solid rgba(244,250,241,0.28); padding: {pd}px 180px {pd}px 28px; display: flex; align-items: center; gap: 28px">
<img src="/_blob/{p["img"]}" alt="{p["alt"]}" style="position: absolute; right: 22px; bottom: 10px; height: {p.get("img_h", 165)}px; width: auto; filter: drop-shadow(0 12px 18px rgba(0,0,0,0.45))">
<div style="flex: none; width: 210px; display: flex; flex-direction: column; gap: 4px">
<div style="font-family: 'Anton', Impact, sans-serif; font-size: {nm}px; line-height: 1; letter-spacing: 3px; text-transform: uppercase">{p["name"]}</div>
{tag}<div style="font-weight: 800; font-size: {ds}px; color: {{{{accent}}}}">{p["dose"]}</div>
</div>
<div style="flex: 1; display: flex; flex-direction: column; gap: 9px; font-size: 22px; font-weight: 700; line-height: 1.25; color: #E3F1E7">
{bl}
</div>
</div>'''


def im(ph, alt):
    """Uma foto ocupando o painel, ou duas empilhadas (lista de 2 ids)."""
    one = 'style="width: 100%; height: 100%; object-fit: cover; display: block"'
    if isinstance(ph, list):
        return ('<div style="width: 100%; height: 100%; display: grid; grid-template-rows: 1fr 1fr; gap: 4px">'
                + "".join(f'<img src="/_blob/{p}" alt="{alt}" {one}>' for p in ph) + '</div>')
    return f'<img src="/_blob/{ph}" alt="{alt}" {one}>'


def photos(s):
    if s["layout"] == "side":
        return f'''<div style="position: relative; height: 880px; flex: none; background: #052E1B">
<div style="position: absolute; left: 0; top: 0; width: 540px; height: 880px; clip-path: polygon(0 0, 100% 0, 88.9% 100%, 0 100%)">
{im(s["photo_a"], s["alt_a"])}
<div style="{LAB}left: 28px; top: 28px; background: #F4FAF1; color: #052E1B">{s["label_a"]}</div>
</div>
<div style="position: absolute; left: 412px; top: 0; width: 540px; height: 880px; clip-path: polygon(25.9% 0, 100% 0, 100% 100%, 14.8% 100%)">
{im(s["photo_b"], s["alt_b"])}
<div style="{LAB}right: 28px; bottom: 28px; background: {{{{accent}}}}; color: #052E1B">{s["label_b"]}</div>
</div>
</div>'''
    k = s.get("photo_h", 880) / 880
    H, A, T, B = round(880 * k), round(500 * k), round(400 * k), round(480 * k)
    return f'''<div style="position: relative; height: {H}px; flex: none; background: #052E1B">
<div style="position: absolute; left: 0; top: 0; width: 952px; height: {A}px; clip-path: polygon(0 0, 100% 0, 100% 90%, 0 100%)">
<img src="/_blob/{s["photo_a"]}" alt="{s["alt_a"]}" style="width: 100%; height: 100%; object-fit: cover; display: block">
<div style="{LAB}left: 28px; top: 28px; background: #F4FAF1; color: #052E1B">{s["label_a"]}</div>
</div>
<div style="position: absolute; left: 0; top: {T}px; width: 952px; height: {B}px; clip-path: polygon(0 23.3%, 100% 12.9%, 100% 100%, 0 100%)">
<img src="/_blob/{s["photo_b"]}" alt="{s["alt_b"]}" style="width: 100%; height: 100%; object-fit: cover; display: block">
<div style="{LAB}left: 28px; bottom: 28px; background: {{{{accent}}}}; color: #052E1B">{s["label_b"]}</div>
</div>
</div>'''


def details(s):
    """Faixa de fotos de detalhe (2 fotos lado a lado) logo abaixo das fotos principais."""
    d = s.get("details")
    if not d:
        return ""
    h = d.get("h", 190)
    tile = lambda ph, alt, lab, bg, fg: (
        f'<div style="position: relative; height: {h}px; overflow: hidden; background: #052E1B">'
        f'<img src="/_blob/{ph}" alt="{alt}" style="width: 100%; height: 100%; object-fit: cover; display: block">'
        f'<div style="position: absolute; left: 14px; bottom: 14px; background: {bg}; color: {fg}; font-weight: 800; font-size: 20px; letter-spacing: 2px; text-transform: uppercase; padding: 8px 14px">{lab}</div></div>')
    return ('<div style="flex: none; display: grid; grid-template-columns: 1fr 1fr; gap: 16px">'
            + tile(d["photo_a"], d["alt_a"], d["label_a"], "#F4FAF1", "#052E1B")
            + tile(d["photo_b"], d["alt_b"], d["label_b"], "{{accent}}", "#052E1B") + '</div>')


def build(s):
    rows = "\n".join(row(p, s.get("compact_rows", False)) for p in s["products"])
    plus = ('<div style="position: absolute; left: 118px; top: 50%; width: 52px; height: 52px; margin-left: -26px; margin-top: -26px; border-radius: 50%; background: {{accent}}; color: #052E1B; display: flex; align-items: center; justify-content: center; font-family: \'Anton\', Impact, sans-serif; font-size: 38px; line-height: 1">+</div>'
            if len(s["products"]) > 1 else "")
    l1, l2 = s["logos"]
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{s["title"]}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Archivo:wght@500;700;800&amp;display=swap">
<style>
body{{margin:0}}
</style>
</helmet>
<div style="position: relative; width: 1080px; height: 1920px; box-sizing: border-box; padding: 48px 64px 48px; background: radial-gradient(120% 60% at 100% 0%, #0E6B3C 0%, #08472A 45%, #052E1B 100%); color: #F4FAF1; font-family: 'Archivo', system-ui, sans-serif; display: flex; flex-direction: column; gap: {18 if s.get("tight") else 22}px; overflow: hidden">

<div style="display: flex; flex-direction: column; gap: 12px">
<div style="align-self: flex-start; background: {{{{accent}}}}; color: #052E1B; font-weight: 800; font-size: 28px; letter-spacing: 6px; text-transform: uppercase; padding: 10px 22px">Resultado de campo</div>
<div style="display: flex; align-items: flex-end; gap: 28px">
<div style="font-family: 'Anton', Impact, sans-serif; font-size: {130 if s.get("tight") else 170}px; line-height: 0.82; color: {{{{accent}}}}; letter-spacing: -4px">{s["number"]}</div>
<div style="font-family: 'Anton', Impact, sans-serif; font-size: {44 if s.get("tight") else 56}px; line-height: 0.98; text-transform: uppercase; padding-bottom: 4px">Dias<br>após a<br>aplicação</div>
</div>
</div>

{photos(s)}

{details(s)}

<div style="display: flex; flex-direction: column; gap: 12px">
<div style="font-weight: 800; font-size: 24px; letter-spacing: 6px; text-transform: uppercase; color: {{{{accent}}}}">Manejo Nitro</div>
<div style="position: relative; display: flex; flex-direction: column; gap: 14px">
{rows}
{plus}
</div>
</div>

<div style="display: grid; grid-template-columns: 1.5fr 0.8fr 1fr; gap: 24px; border-top: 2px solid rgba(244,250,241,0.28); padding-top: 14px">
{FIELD % ("Cidade", s["city"])}
{FIELD % ("Cultura", s["crop"])}
{FIELD % ("Avaliação", s["eval"])}
</div>

<div style="flex: none; display: flex; align-items: center; justify-content: space-between; gap: 24px; box-sizing: border-box; height: 72px; padding: 0 14px 0 28px; background: rgba(244,250,241,0.09); border: 2px solid rgba(244,250,241,0.28); border-radius: 999px">
<div style="font-size: 28px; font-weight: 800; line-height: 1.1">Garanta esse resultado na sua lavoura</div>
<div style="flex: none; background: {{{{accent}}}}; color: #052E1B; border-radius: 999px; font-size: 25px; font-weight: 800; line-height: 1; padding: 14px 28px">{s.get("cta_button", "Fale com seu RTV")}</div>
</div>

<div style="display: flex; align-items: center; justify-content: space-between; gap: 24px; margin-top: auto">
<div style="display: flex; flex-direction: column; gap: 2px"><div style="font-size: 20px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: #B9D9C2">{s.get("rtv_label", "RTV")}</div><div style="font-size: 34px; font-weight: 800">{s["rtv"]}</div></div>
<div style="display: flex; align-items: center; gap: 26px">
<img src="/_blob/{l1}" alt="Logo Nitro" style="height: 56px; width: auto; display: block">
<div style="width: 2px; height: 48px; background: rgba(244,250,241,0.45)"></div>
<img src="/_blob/{l2}" alt="Logo Vale Produtos Agrícolas" style="height: 66px; width: auto; display: block">
</div>
</div>

</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"accent":{{"editor":"color","default":"#8BE04E","options":["#8BE04E","#F5D547","#5BC8FF","#FF8A5B"]}},"$preview":{{"width":1080,"height":1920}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{ accent: this.props.accent ?? '#8BE04E' }};
  }}
}}
</script>
</body>
</html>
'''


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    open(sys.argv[2], "w").write(build(spec))
