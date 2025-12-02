import unittest
import os
import csv
from main_kivy import FinanceAppLogic

# classe de teste
class TestExportacaoTDD(unittest.TestCase):

    def setUp(self):
        # limpa arquivos velhos
        if os.path.exists("tdd_extrato.csv"):
            os.remove("tdd_extrato.csv")
            
        self.app = FinanceAppLogic()
        # simula dados na memoria manualmente pra nao depender de banco
        self.app.transacoes_registradas = [
            {
                "data": "2025-10-25",
                "tipo": "receita",
                "categoria": "freela",
                "descricao": "site",
                "valor": 500.00
            }
        ]

    def tearDown(self):
        # limpa a sujeira depois do teste
        if os.path.exists("tdd_extrato.csv"):
            os.remove("tdd_extrato.csv")

    def test_deve_criar_arquivo_csv_com_dados(self):
        # --- ACAO ---
        # tenta chamar a funcao (que ainda nao existe na teoria)
        sucesso = self.app.exportar_dados_csv("tdd_extrato.csv")

        # --- VERIFICACAO ---
        self.assertTrue(sucesso, "a funcao deve retornar true")
        self.assertTrue(os.path.exists("tdd_extrato.csv"), "o arquivo deve ser criado")

        # le o arquivo pra ver se gravou certo
        with open("tdd_extrato.csv", "r", encoding="utf-8") as f:
            conteudo = f.read()
            # verifica se tem o cabecalho
            self.assertIn("Data;Tipo;Categoria;Descrição;Valor", conteudo)
            # verifica se tem o valor formatado (500.0 virou 500,0)
            self.assertIn("500,0", conteudo)
            # verifica descricao
            self.assertIn("site", conteudo)

if __name__ == "__main__":
    unittest.main()