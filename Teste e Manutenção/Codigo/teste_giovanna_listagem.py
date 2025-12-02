import unittest
import os
from decimal import Decimal


from Pedro.Facade import FinanceFacade

# funcao pra limpar os arquivos json antes de rodar os testes
def reset_files():
    with open("contas.json", "w") as f:
        f.write("{}")
    
    with open("movimentacoes.json", "w") as f:
        f.write("[]")

class TestListagem(unittest.TestCase):

    def setUp(self):
        # roda antes de cada teste iniciar
        reset_files()
        self.app = FinanceFacade()

        # cria uma conta padrao pra usar nos testes
        conta = self.app.criar_nova_conta(
            username="tester",
            nome_completo="usuario teste",
            senha="123"
        )
        self.id_conta = conta.id_conta

   
    # ver se as listas começam vazias
   
    def test_listas_vazias(self):
        # busca receitas e despesas sem ter registrado nada
        receitas = self.app.get_historico_receitas(self.id_conta)
        despesas = self.app.get_historico_despesas(self.id_conta)

        self.assertEqual(len(receitas), 0, "lista de receitas devia estar vazia")
        self.assertEqual(len(despesas), 0, "lista de despesas devia estar vazia")

    # filtrar apenas receitas
 
    def test_filtro_receitas(self):
        # adiciona uma receita
        self.app.registrar_movimentacao(self.id_conta, "receita", 1000, "salario")
        
        # adiciona uma despesa pra ver se nao mistura (precisa ter saldo antes)
        self.app.registrar_movimentacao(self.id_conta, "despesa", 200, "gasolina")

        # pede so as receitas
        lista_receitas = self.app.get_historico_receitas(self.id_conta)

        # verifica se so veio 1 item e se eh o certo
        self.assertEqual(len(lista_receitas), 1)
        self.assertEqual(lista_receitas[0].descricao, "salario")
        self.assertEqual(lista_receitas[0].valor, Decimal("1000"))

  
    # filtrar apenas despesas
   
    def test_filtro_despesas(self):
        # bota saldo primeiro
        self.app.registrar_movimentacao(self.id_conta, "receita", 500, "pix recebido")

        # faz dois gastos
        self.app.registrar_movimentacao(self.id_conta, "despesa", 50, "ifood")
        self.app.registrar_movimentacao(self.id_conta, "despesa", 20, "uber")

        # pede so as despesas
        lista_despesas = self.app.get_historico_despesas(self.id_conta)

        # verifica se vieram os 2 gastos
        self.assertEqual(len(lista_despesas), 2)
        
        # garante que a receita nao apareceu na lista de gastos
        descricoes = [mov.descricao for mov in lista_despesas]
        self.assertIn("ifood", descricoes)
        self.assertIn("uber", descricoes)
        self.assertNotIn("pix recebido", descricoes)

   
    # conferir dados da listagem

    def test_dados_integros(self):
        # registra algo com valor quebrado
        valor_teste = 150.50
        desc_teste = "venda produto"
        
        self.app.registrar_movimentacao(self.id_conta, "receita", valor_teste, desc_teste)
        
        lista = self.app.get_historico_receitas(self.id_conta)
        item = lista[0]

        # confere se salvou e listou igual
        self.assertEqual(item.descricao, desc_teste)
        self.assertEqual(item.valor, Decimal("150.50"))

if __name__ == "__main__":
    unittest.main()