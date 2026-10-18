import json

from suitability import validar_suitability


with open("example.json", encoding="utf-8") as arquivo:
    entrada = json.load(arquivo)

resultado = validar_suitability(
    entrada["cliente"],
    entrada["carteira_atual"],
    entrada["nova_ordem"],
)

print(json.dumps(resultado, ensure_ascii=False, indent=2))
