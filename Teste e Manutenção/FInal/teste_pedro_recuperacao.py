# test_recuperacao.py
import unittest
import os
from Pedro.Facade import FinanceFacade

class TestRecuperacaoSenha(unittest.TestCase):

    def setUp(self):
        """
        Este método roda ANTES de cada teste.
        Ele prepara um ambiente limpo (apaga dados antigos e cria um app novo).
        """
        if os.path.exists("contas.json"):
            os.remove("contas.json")
        
        self.app = FinanceFacade()
        
        # Cria uma conta padrão para usarmos nos testes
        # Usuário: pedro | Senha: 123 | Pergunta: Cor? | Resposta: azul
        self.app.criar_nova_conta(
            "pedro", "Pedro Silva", "123", "Qual a cor do ceu?", "azul"
        )

    def tearDown(self):
        """Roda DEPOIS de cada teste para limpar a sujeira."""
        if os.path.exists("contas.json"):
            os.remove("contas.json")

    # --- TESTE 1: CAMINHO FELIZ (HAPPY PATH) ---
    def test_deve_resetar_senha_com_resposta_correta(self):
        # Ação: Tenta resetar com a resposta certa ("azul")
        resultado = self.app.resetar_senha("pedro", "azul", "nova_senha_456")
        
        # Verificação 1: A função retornou True?
        self.assertTrue(resultado, "Deveria retornar True para resposta correta")
        
        # Verificação 2: A senha nova funciona?
        usuario_logado = self.app.autenticar_usuario("pedro", "nova_senha_456")
        self.assertIsNotNone(usuario_logado, "O login deveria funcionar com a NOVA senha")

    # --- TESTE 2: RESPOSTA ERRADA ---
    def test_nao_deve_resetar_senha_com_resposta_errada(self):
        # Ação: Tenta resetar com resposta errada ("verde")
        resultado = self.app.resetar_senha("pedro", "verde", "senha_hacker")
        
        # Verificação 1: A função retornou False?
        self.assertFalse(resultado, "Deveria retornar False para resposta errada")
        
        # Verificação 2: A senha ANTIGA ainda deve funcionar?
        login_antigo = self.app.autenticar_usuario("pedro", "123")
        self.assertIsNotNone(login_antigo, "A senha antiga deveria continuar valendo")
        
        # Verificação 3: A senha NOVA NÃO pode funcionar
        login_novo = self.app.autenticar_usuario("pedro", "senha_hacker")
        self.assertIsNone(login_novo, "Não deveria logar com a senha nova pois a resposta estava errada")

    # --- TESTE 3: USUÁRIO INEXISTENTE ---
    def test_nao_deve_resetar_usuario_inexistente(self):
        resultado = self.app.resetar_senha("fantasma", "azul", "123")
        self.assertFalse(resultado)

    # --- TESTE 4: BUSCAR PERGUNTA ---
    def test_deve_retornar_pergunta_correta(self):
        pergunta = self.app.buscar_pergunta_seguranca("pedro")
        self.assertEqual(pergunta, "Qual a cor do ceu?")

    # --- TESTE 5: MAIÚSCULAS E MINÚSCULAS ---
    def test_deve_ignorar_maiusculas_na_resposta(self):
        # O usuário cadastrou "azul", mas respondeu "AZUL"
        resultado = self.app.resetar_senha("pedro", "AZUL", "nova_senha")
        self.assertTrue(resultado, "O sistema deve aceitar respostas em maiúsculo/minúsculo")

if __name__ == '__main__':
    unittest.main()