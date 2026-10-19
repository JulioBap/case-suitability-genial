import sys
import json

from suitability import validar_suitability


arquivo_entrada = sys.argv[1] if len(sys.argv) > 1 else "example.json"

with open(arquivo_entrada, encoding="utf-8") as arquivo:
    entrada = json.load(arquivo)

resultado = validar_suitability(
    entrada["cliente"],
    entrada["carteira_atual"],
    entrada["nova_ordem"],
)

print(json.dumps(resultado, ensure_ascii=False, indent=2))
