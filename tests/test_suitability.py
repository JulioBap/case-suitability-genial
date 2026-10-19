import unittest

from suitability import validar_suitability


class TestSuitability(unittest.TestCase):
    def setUp(self):
        self.cliente = {"perfil": "Moderado", "score_max_risco": 2.5}

    def test_aprova_compra_abaixo_do_limite(self):
        carteira = [
            {"ativo": "CDB XPTO", "risco": 1.2, "valor_investido": 50000},
            {"ativo": "Ação ABC", "risco": 4.0, "valor_investido": 10000},
        ]
        ordem = {"ativo": "FII YYY", "risco": 3.5, "valor_ordem": 5000}

        resultado = validar_suitability(self.cliente, carteira, ordem)

        self.assertEqual(resultado["status"], "Aprovado")
        self.assertAlmostEqual(resultado["risco_atual"], 1.6666666667)
        self.assertAlmostEqual(resultado["risco_projetado"], 1.8076923077)
        self.assertEqual(resultado["limite_alerta"], 2.75)

    def test_emite_alerta_acima_de_110_porcento(self):
        ordem = {"ativo": "Ativo de risco", "risco": 3.0, "valor_ordem": 100}

        resultado = validar_suitability(self.cliente, [], ordem)

        self.assertEqual(resultado["status"], "Alerta")
        self.assertEqual(resultado["risco_atual"], 0)
        self.assertEqual(resultado["risco_projetado"], 3.0)
        self.assertEqual(resultado["limite_alerta"], 2.75)

    def test_aprova_quando_risco_igual_ao_limite(self):
        ordem = {"ativo": "Ativo no limite", "risco": 2.75, "valor_ordem": 100}

        resultado = validar_suitability(self.cliente, [], ordem)

        self.assertEqual(resultado["status"], "Aprovado")
        self.assertEqual(resultado["risco_projetado"], 2.75)

    def test_rejeita_valor_negativo(self):
        ordem = {"ativo": "Ativo inválido", "risco": 3.0, "valor_ordem": -100}

        with self.assertRaisesRegex(ValueError, "não pode ser negativo"):
            validar_suitability(self.cliente, [], ordem)

    def test_informa_campo_obrigatorio_ausente(self):
        ordem = {"ativo": "Ativo incompleto", "valor_ordem": 100}

        with self.assertRaisesRegex(ValueError, "risco"):
            validar_suitability(self.cliente, [], ordem)

    def test_rejeita_risco_que_nao_seja_numero(self):
        ordem = {"ativo": "Ativo inválido", "risco": "alto", "valor_ordem": 100}

        with self.assertRaisesRegex(ValueError, "deve ser um número"):
            validar_suitability(self.cliente, [], ordem)


if __name__ == "__main__":
    unittest.main()
