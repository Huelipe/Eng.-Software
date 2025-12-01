import unittest
import os
import csv

# importa a classe logica onde criamos a funcao nova
# se seu arquivo chamar outro nome, mude o 'main_kivy' aqui
from main_kivy import FinanceAppLogic 

def reset_files():
    with open("contas.json", "w") as f:
        f.write("{}")
    
    with open("movimentacoes.json", "w") as f:
        f.write("[]")
    
    # garante que nao tem lixo de csv antigo
    if os.path.exists("teste_extrato.csv"):
        os.remove("teste_extrato.csv")

class TestExportacaoCSV(unittest.TestCase):

    def setUp(self):
        reset_files()
        # instancia a logica do app (que tem a lista transacoes_registradas)
        self.app = FinanceAppLogic()

        # cria uma conta pra poder lançar movimentacoes
        conta = self.app.criar_nova_conta(
            username="csv_tester",
            nome_completo="testador csv",
            senha="123"
        )
        self.id_conta = conta.id_conta

    def tearDown(self):
        # apaga o arquivo gerado depois de cada teste pra nao sujar a pasta
        if os.path.exists("teste_extrato.csv"):
            os.remove("teste_extrato.csv")

    # teste principal: ver se gera o arquivo e se os dados tao la
    def test_exportar_com_dados(self):
        # adiciona uma receita e uma despesa
        self.app.registrar_movimentacao(self.id_conta, "receita", 150.50, "freela")
        self.app.registrar_movimentacao(self.id_conta, "despesa", 20.00, "cafe")

        # chama a funcao de exportar
        sucesso = self.app.exportar_dados_csv("teste_extrato.csv")

        # verifica se retornou true e se o arquivo existe
        self.assertTrue(sucesso, "a funcao devia retornar true")
        self.assertTrue(os.path.exists("teste_extrato.csv"), "o arquivo csv devia existir")

        # abre o arquivo pra conferir o conteudo
        with open("teste_extrato.csv", "r", encoding="utf-8") as f:
            leitor = list(csv.reader(f, delimiter=";"))

            # verifica o cabecalho (linha 0)
            cabecalho = leitor[0]
            self.assertEqual(cabecalho, ["Data", "Tipo", "Categoria", "Descrição", "Valor"])

            # verifica a primeira transacao (linha 1 - freela)
            # nota: a funcao exportar converte ponto pra virgula (150.5 -> 150,5)
            linha_receita = leitor[1]
            self.assertIn("freela", linha_receita)
            self.assertIn("150,5", linha_receita[4]) 

            # verifica a segunda transacao (linha 2 - cafe)
            linha_despesa = leitor[2]
            self.assertIn("cafe", linha_despesa)
            self.assertIn("-20,0", linha_despesa[4]) # despesa fica negativo

    # teste pra ver se funciona mesmo sem dados (gera so o cabecalho)
    def test_exportar_vazio(self):
        sucesso = self.app.exportar_dados_csv("teste_extrato.csv")
        
        self.assertTrue(sucesso)
        
        with open("teste_extrato.csv", "r", encoding="utf-8") as f:
            leitor = list(csv.reader(f, delimiter=";"))
            
            # deve ter apenas 1 linha (o cabecalho)
            self.assertEqual(len(leitor), 1)
            self.assertEqual(leitor[0], ["Data", "Tipo", "Categoria", "Descrição", "Valor"])

if __name__ == "__main__":
    unittest.main()