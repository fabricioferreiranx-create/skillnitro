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
  "rtv": "Fabricio F Fagundes",
  "logos": ["<id nitro branco>", "<id vale branco>"],
  "products": [ {"name":"Revita","tag":"","dose":"1 L/ha","img":"<id>","img_h":172,"alt":"...","benefits":["...","...","..."]} ]
}
Fotos: layout stacked -> foto A com proporção 952:500 e foto B 952:480 (horizonte ~25-40% da altura);
layout side -> cada foto com proporção 540:880.
"""
import json, sys

BUL = '<div style="display: flex; align-items: flex-start; gap: 12px"><div style="flex: none; width: 9px; height: 9px; margin-top: 9px; background: {{accent}}"></div><div>%s</div></div>'
LAB = "position: absolute; font-weight: 800; font-size: 34px; letter-spacing: 3px; text-transform: uppercase; padding: 14px 24px; "
FIELD = '<div style="display: flex; flex-direction: column; gap: 2px"><div style="font-size: 20px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: #B9D9C2">%s</div><div style="font-size: 30px; font-weight: 800">%s</div></div>'


def row(p):
    tag = ('<div style="font-weight: 800; font-size: 22px; letter-spacing: 3px; text-transform: uppercase; color: #B9D9C2">%s</div>' % p["tag"]) if p.get("tag") else ""
    bl = "\n".join(BUL % b for b in p["benefits"])
    return f'''<div style="position: relative; min-height: 160px; box-sizing: border-box; background: rgba(244,250,241,0.09); border: 2px solid rgba(244,250,241,0.28); padding: 18px 180px 18px 28px; display: flex; align-items: center; gap: 28px">
<img src="/_blob/{p["img"]}" alt="{p["alt"]}" style="position: absolute; right: 22px; bottom: 10px; height: {p.get("img_h", 165)}px; width: auto; filter: drop-shadow(0 12px 18px rgba(0,0,0,0.45))">
<div style="flex: none; width: 210px; display: flex; flex-direction: column; gap: 4px">
<div style="font-family: 'Anton', Impact, sans-serif; font-size: 58px; line-height: 1; letter-spacing: 3px; text-transform: uppercase">{p["name"]}</div>
{tag}<div style="font-weight: 800; font-size: 38px; color: {{{{accent}}}}">{p["dose"]}</div>
</div>
<div style="flex: 1; display: flex; flex-direction: column; gap: 9px; font-size: 22px; font-weight: 700; line-height: 1.25; color: #E3F1E7">
{bl}
</div>
</div>'''


def photos(s):
    if s["layout"] == "side":
        return f'''<div style="position: relative; height: 880px; flex: none; background: #052E1B">
<div style="position: absolute; left: 0; top: 0; width: 540px; height: 880px; clip-path: polygon(0 0, 100% 0, 88.9% 100%, 0 100%)">
<img src="/_blob/{s["photo_a"]}" alt="{s["alt_a"]}" style="width: 100%; height: 100%; object-fit: cover; display: block">
<div style="{LAB}left: 28px; top: 28px; background: #F4FAF1; color: #052E1B">{s["label_a"]}</div>
</div>
<div style="position: absolute; left: 412px; top: 0; width: 540px; height: 880px; clip-path: polygon(25.9% 0, 100% 0, 100% 100%, 14.8% 100%)">
<img src="/_blob/{s["photo_b"]}" alt="{s["alt_b"]}" style="width: 100%; height: 100%; object-fit: cover; display: block">
<div style="{LAB}right: 28px; bottom: 28px; background: {{{{accent}}}}; color: #052E1B">{s["label_b"]}</div>
</div>
</div>'''
    return f'''<div style="position: relative; height: 880px; flex: none; background: #052E1B">
<div style="position: absolute; left: 0; top: 0; width: 952px; height: 500px; clip-path: polygon(0 0, 100% 0, 100% 90%, 0 100%)">
<img src="/_blob/{s["photo_a"]}" alt="{s["alt_a"]}" style="width: 100%; height: 100%; object-fit: cover; display: block">
<div style="{LAB}left: 28px; top: 28px; background: #F4FAF1; color: #052E1B">{s["label_a"]}</div>
</div>
<div style="position: absolute; left: 0; top: 400px; width: 952px; height: 480px; clip-path: polygon(0 23.3%, 100% 12.9%, 100% 100%, 0 100%)">
<img src="/_blob/{s["photo_b"]}" alt="{s["alt_b"]}" style="width: 100%; height: 100%; object-fit: cover; display: block">
<div style="{LAB}left: 28px; bottom: 28px; background: {{{{accent}}}}; color: #052E1B">{s["label_b"]}</div>
</div>
</div>'''


def build(s):
    rows = "\n".join(row(p) for p in s["products"])
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
<div style="position: relative; width: 1080px; height: 1920px; box-sizing: border-box; padding: 48px 64px 48px; background: radial-gradient(120% 60% at 100% 0%, #0E6B3C 0%, #08472A 45%, #052E1B 100%); color: #F4FAF1; font-family: 'Archivo', system-ui, sans-serif; display: flex; flex-direction: column; gap: 22px; overflow: hidden">

<div style="display: flex; flex-direction: column; gap: 12px">
<div style="align-self: flex-start; background: {{{{accent}}}}; color: #052E1B; font-weight: 800; font-size: 28px; letter-spacing: 6px; text-transform: uppercase; padding: 10px 22px">Resultado de campo</div>
<div style="display: flex; align-items: flex-end; gap: 28px">
<div style="font-family: 'Anton', Impact, sans-serif; font-size: 170px; line-height: 0.82; color: {{{{accent}}}}; letter-spacing: -4px">{s["number"]}</div>
<div style="font-family: 'Anton', Impact, sans-serif; font-size: 56px; line-height: 0.98; text-transform: uppercase; padding-bottom: 4px">Dias<br>após a<br>aplicação</div>
</div>
</div>

{photos(s)}

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
<div style="flex: none; background: {{{{accent}}}}; color: #052E1B; border-radius: 999px; font-size: 25px; font-weight: 800; line-height: 1; padding: 14px 28px">Fale com seu RTV</div>
</div>

<div style="display: flex; align-items: center; justify-content: space-between; gap: 24px; margin-top: auto">
<div style="display: flex; flex-direction: column; gap: 2px"><div style="font-size: 20px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: #B9D9C2">RTV</div><div style="font-size: 34px; font-weight: 800">{s["rtv"]}</div></div>
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
