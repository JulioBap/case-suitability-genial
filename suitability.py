def calcular_risco_atual(carteira):
    valor_total = 0
    risco_ponderado_total = 0

    for ativo in carteira:
        risco = ativo["risco"]
        valor_investido = ativo["valor_investido"]

        risco_ponderado_total += risco * valor_investido
        valor_total += valor_investido

    if valor_total == 0:
        return 0

    return risco_ponderado_total / valor_total

def calcular_risco_projetado(carteira, nova_ordem):
    valor_total = sum(ativo["valor_investido"] for ativo in carteira)
    risco_ponderado_total = sum(
        ativo["risco"] * ativo["valor_investido"] for ativo in carteira
    )

    valor_ordem = nova_ordem["valor_ordem"]
    risco_ordem = nova_ordem["risco"]

    valor_total += valor_ordem
    risco_ponderado_total += risco_ordem * valor_ordem

    if valor_total == 0:
        return 0

    return risco_ponderado_total / valor_total

def validar_suitability(cliente, carteira, nova_ordem):
    risco_projetado = calcular_risco_projetado(carteira, nova_ordem)
    limite_alerta = cliente["score_max_risco"] * 1.10

    if risco_projetado > limite_alerta:
        return {
            "status": "Alerta",
            "risco_projetado": risco_projetado,
            "mensagem": (
                f"Atenção: o risco projetado ultrapassa o limite "
                f"de {limite_alerta:.2f}."
            ),
        }

    return {
        "status": "Aprovado",
        "risco_projetado": risco_projetado,
        "mensagem": "Ordem aprovada. Carteira dentro do limite de alerta.",
    }
