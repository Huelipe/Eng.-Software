## Testes feito pelo Felipe

import unittest
import json
import os
from decimal import Decimal

# Importa corretamente sua Facade
from Pedro.Facade import FinanceFacade


# Utilitário para RESETAR os arquivos antes de cada teste
def reset_files():
    with open("contas.json", "w") as f:
        f.write("{}")  # estrutura de dicionário vazia

    with open("movimentacoes.json", "w") as f:
        f.write("[]")  # lista vazia


class TestFinanceFacade(unittest.TestCase):

    def setUp(self):
        """Executa antes de cada teste."""
        reset_files()
        self.app = FinanceFacade()

        # Criar conta para todos os testes
        conta = self.app.criar_nova_conta(
            username="teste_user",
            nome_completo="Usuário Teste",
            senha="123"
        )
        self.id_conta = conta.id_conta

    # ============================================================
    # TESTE 1 — Registrar receita válida
    # ============================================================
    def test_registrar_receita_valida(self):
        resultado = self.app.registrar_movimentacao(
            id_conta=self.id_conta,
            tipo="receita",
            valor=100,
            descricao="Salário"
        )

        self.assertTrue(resultado, "A receita deveria ser registrada com sucesso.")
        self.assertEqual(self.app.get_saldo(self.id_conta), Decimal("100"))

    # ============================================================
    # TESTE 2 — Registrar receita inválida (valor negativo)
    # ============================================================
    def test_registrar_receita_invalida(self):
        resultado = self.app.registrar_movimentacao(
            id_conta=self.id_conta,
            tipo="receita",
            valor=-50,
            descricao="Erro"
        )

        self.assertFalse(resultado, "Receita negativa deve ser rejeitada.")
        self.assertEqual(self.app.get_saldo(self.id_conta), Decimal("0"))

    # ============================================================
    # TESTE 3 — Registrar despesa com saldo suficiente
    # ============================================================
    def test_registrar_despesa_valida(self):
        # Primeiro coloca saldo
        self.app.registrar_movimentacao(
            id_conta=self.id_conta,
            tipo="receita",
            valor=200,
            descricao="Depósito"
        )

        resultado = self.app.registrar_movimentacao(
            id_conta=self.id_conta,
            tipo="despesa",
            valor=50,
            descricao="Mercado"
        )

        self.assertTrue(resultado, "Despesa deveria ser aprovada.")
        self.assertEqual(self.app.get_saldo(self.id_conta), Decimal("150"))

    # ============================================================
    # TESTE 4 — Registrar despesa com saldo insuficiente
    # ============================================================
    def test_despesa_saldo_insuficiente(self):
        # Saldo atual = 0
        resultado = self.app.registrar_movimentacao(
            id_conta=self.id_conta,
            tipo="despesa",
            valor=100,
            descricao="Tentativa"
        )

        self.assertFalse(resultado, "Despesa além do saldo deve falhar.")
        self.assertEqual(self.app.get_saldo(self.id_conta), Decimal("0"))

    # ============================================================
    # TESTE 5 — Histórico funcionando corretamente
    # ============================================================
    def test_historico(self):
        # Receita
        self.app.registrar_movimentacao(
            id_conta=self.id_conta,
            tipo="receita",
            valor=150,
            descricao="Freela"
        )

        # Despesa
        self.app.registrar_movimentacao(
            id_conta=self.id_conta,
            tipo="despesa",
            valor=50,
            descricao="Lanche"
        )

        receitas = self.app.get_historico_receitas(self.id_conta)
        despesas = self.app.get_historico_despesas(self.id_conta)

        self.assertEqual(len(receitas), 1)
        self.assertEqual(len(despesas), 1)

        self.assertEqual(receitas[0].descricao, "Freela")
        self.assertEqual(despesas[0].descricao, "Lanche")


if __name__ == "__main__":
    unittest.main()
