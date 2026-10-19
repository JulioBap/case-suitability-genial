import math


def _validar_numero_nao_negativo(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"'{campo}' deve ser um número")

    if not math.isfinite(valor):
        raise ValueError(f"'{campo}' deve ser um número finito")

    if valor < 0:
        raise ValueError(f"'{campo}' não pode ser negativo")

    return valor


def _validar_carteira(carteira):
    if not isinstance(carteira, list):
        raise ValueError("'carteira' deve ser uma lista")

    for indice, ativo in enumerate(carteira):
        if not isinstance(ativo, dict):
            raise ValueError(f"O ativo na posição {indice} deve ser um objeto")

        for campo in ("risco", "valor_investido"):
            if campo not in ativo:
                raise ValueError(
                    f"O ativo na posição {indice} precisa do campo '{campo}'"
                )
            _validar_numero_nao_negativo(ativo[campo], f"ativo[{indice}].{campo}")


def calcular_risco_atual(carteira):
    _validar_carteira(carteira)

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
    _validar_carteira(carteira)

    if not isinstance(nova_ordem, dict):
        raise ValueError("'nova_ordem' deve ser um objeto")

    for campo in ("risco", "valor_ordem"):
        if campo not in nova_ordem:
            raise ValueError(f"'nova_ordem' precisa do campo '{campo}'")
        _validar_numero_nao_negativo(nova_ordem[campo], f"nova_ordem.{campo}")

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
    if not isinstance(cliente, dict):
        raise ValueError("'cliente' deve ser um objeto")

    if "score_max_risco" not in cliente:
        raise ValueError("'cliente' precisa do campo 'score_max_risco'")

    score_maximo = _validar_numero_nao_negativo(
        cliente["score_max_risco"], "cliente.score_max_risco"
    )

    risco_atual = calcular_risco_atual(carteira)
    risco_projetado = calcular_risco_projetado(carteira, nova_ordem)
    limite_alerta = score_maximo * 1.10

    if risco_projetado > limite_alerta:
        return {
            "status": "Alerta",
            "risco_atual": risco_atual,
            "risco_projetado": risco_projetado,
            "limite_alerta": limite_alerta,
            "mensagem": (
                f"Atenção: o risco projetado ultrapassa o limite "
                f"de {limite_alerta:.2f}."
            ),
        }

    return {
        "status": "Aprovado",
        "risco_atual": risco_atual,
        "risco_projetado": risco_projetado,
        "limite_alerta": limite_alerta,
        "mensagem": "Ordem aprovada. Carteira dentro do limite de alerta.",
    }
