# main_kivy.py
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.lang import Builder

import json
import os
import matplotlib.pyplot as plt
from kivy_garden.matplotlib import FigureCanvasKivyAgg

from Pedro.Facade import FinanceFacade
from Felipe.observer import Subject, RelatorioObserver
from Giovanna.decorator import (
    RelatorioFinanceiroBase,
    DecoratorDetalhado,
    DecoratorAnaliseCategorias,
    DecoratorRecomendacoes
)


# ===================================================================
# LÓGICA PRINCIPAL (FACADE + SUBJECT)
# ===================================================================
class FinanceAppLogic(FinanceFacade, Subject):

    def get_transacoes_usuario(self, id_conta_atual):
        # Retorna apenas as transações que pertencem ao ID informado
        return [t for t in self.transacoes_registradas if t.get("id_conta") == id_conta_atual]

    def __init__(self):
        FinanceFacade.__init__(self)
        Subject.__init__(self)

        self.transacoes_registradas = []
        self.arquivo_dados = "movimentacoes.json"

        self._carregar_movimentacoes()

        self.meta_economia = {}
        self._carregar_meta()


    def criar_nova_conta(self, usuario, nome, senha, pergunta, resposta):
        return super().criar_nova_conta(usuario, nome, senha, pergunta, resposta)
    
    def buscar_pergunta(self, username):
        return self.buscar_pergunta_seguranca(username)

    def resetar_senha(self, username, resposta, nova_senha):
        return super().resetar_senha(username, resposta, nova_senha)
    
    
    # ---------------------------------------------------------------
    # REGISTRAR MOVIMENTAÇÃO (CORRIGIDO — APENAS UMA FUNÇÃO)
    # ---------------------------------------------------------------
    def registrar_movimentacao(self, id_conta, tipo, valor, descricao, categoria=None):
        sucesso = super().registrar_movimentacao(id_conta, tipo, valor, descricao)

        if not sucesso:
            return False

        valor = float(valor)

        nova = {
            "id_conta": id_conta,
            "descricao": descricao,
            "valor": valor if tipo == "receita" else -abs(valor),
            "tipo": tipo,
            "categoria": categoria if categoria else "outros",
            "data": "2025-10-25"
        }

        self.transacoes_registradas.append(nova)
        self._salvar_movimentacoes()

        self.notificar_observers("nova_movimentacao", {"transacoes": self.transacoes_registradas})
        return True

    # ---------------------------------------------------------------
    # META (AGORA POR USUÁRIO)
    # ---------------------------------------------------------------
    def configurar_meta(self, id_conta, valor): # <--- Recebe ID agora
        try:
            # Salva no dicionário usando o ID da conta
            self.metas_db[id_conta] = max(float(valor), 0)
            self._salvar_meta()
            return True
        except:
            return False

    def _salvar_meta(self):
        # Salva todas as metas de todos os usuários
        with open("meta.json", "w", encoding="utf-8") as f:
            json.dump(self.metas_db, f)

    def _carregar_meta(self):
        if not os.path.exists("meta.json"):
            return
        try:
            with open("meta.json", "r", encoding="utf-8") as f:
                self.metas_db = json.load(f)
        except:
            self.metas_db = {}

    def calcular_progresso_meta(self, id_conta_atual):
        total_receitas = 0.0
        total_despesas = 0.0

        # Pega só as transações desse usuário
        transacoes_usuario = self.get_transacoes_usuario(id_conta_atual)

        for t in transacoes_usuario:
            v = float(t.get("valor", 0))
            if t["tipo"] == "receita":
                total_receitas += abs(v)
            else:
                total_despesas += abs(v)

        saldo = total_receitas - total_despesas
        # Pega a meta específica desse ID (se não tiver, usa 0)
        meta = float(self.metas_db.get(id_conta_atual, 0))

        progresso = 0.0
        if meta > 0:
            progresso = max(0, min(100, (saldo / meta) * 100))

        return {
            "total_receitas": total_receitas,
            "total_despesas": total_despesas,
            "saldo": saldo,
            "meta": meta,
            "progresso": progresso
        }

    # ---------------------------------------------------------------
    # SALVAR E CARREGAR MOVIMENTAÇÕES
    # ---------------------------------------------------------------
    def _salvar_movimentacoes(self):
        with open(self.arquivo_dados, "w", encoding="utf-8") as f:
            json.dump(self.transacoes_registradas, f, ensure_ascii=False, indent=4)

    def _carregar_movimentacoes(self):
        if not os.path.exists(self.arquivo_dados):
            return
        try:
            with open(self.arquivo_dados, "r", encoding="utf-8") as f:
                self.transacoes_registradas = json.load(f)

            for mov in self.transacoes_registradas:
                mov["valor"] = float(mov.get("valor", 0))
                mov["categoria"] = mov.get("categoria", "outros")
                mov["tipo"] = mov.get("tipo", "receita" if mov["valor"] >= 0 else "despesa")

        except:
            self.transacoes_registradas = []


# ===================================================================
# TELAS
# ===================================================================
class LoginScreen(MDScreen):
    def login(self):
        app = MDApp.get_running_app()
        usuario = self.ids.usuario.text.strip()
        senha = self.ids.senha.text.strip()

        conta = app.logic.autenticar_usuario(usuario, senha)
        if conta:
            app.conta_atual = conta
            app.root.current = "menu"
            # Limpa senha por segurança
            self.ids.senha.text = ""
        else:
            app.mostrar_alerta("Erro", "Usuário ou senha incorretos.")
    

class CadastroScreen(MDScreen):
    def cadastrar(self):
        app = MDApp.get_running_app()
        
        # Pega os dados dos campos
        usuario = self.ids.usuario.text.strip()
        nome = self.ids.nome.text.strip()
        senha = self.ids.senha.text.strip()
        pergunta = self.ids.pergunta.text.strip()
        resposta = self.ids.resposta.text.strip()

        # Validação básica
        if not usuario or not nome or not senha or not pergunta or not resposta:
            app.mostrar_alerta("Erro", "Por favor, preencha TODOS os campos.")
            return

        # Chama o Facade para criar a conta
        conta = app.logic.criar_nova_conta(usuario, nome, senha, pergunta, resposta)
        
        if conta:
            app.mostrar_alerta("Sucesso", "Conta criada com sucesso! Faça login agora.")
            # Limpa os campos
            self.ids.usuario.text = ""
            self.ids.nome.text = ""
            self.ids.senha.text = ""
            self.ids.pergunta.text = ""
            self.ids.resposta.text = ""
            # Manda o usuário de volta para o login
            app.root.current = "login"
        else:
            app.mostrar_alerta("Erro", "Este nome de usuário já existe.")

class RecuperarScreen(MDScreen):
    def buscar_pergunta(self):
        app = MDApp.get_running_app()
        user = self.ids.user_input.text.strip()
        
        pergunta = app.logic.buscar_pergunta(user)
        
        if pergunta:
            self.ids.label_pergunta.text = f"Pergunta: {pergunta}"
            self.ids.resposta_input.disabled = False
            self.ids.nova_senha_input.disabled = False
            self.ids.btn_resetar.disabled = False
        else:
            self.ids.label_pergunta.text = "Usuário não encontrado."

    def confirmar_reset(self):
        app = MDApp.get_running_app()
        user = self.ids.user_input.text.strip()
        resp = self.ids.resposta_input.text.strip()
        nova_senha = self.ids.nova_senha_input.text.strip()

        if app.logic.resetar_senha(user, resp, nova_senha):
            app.mostrar_alerta("Sucesso", "Senha alterada! Faça login.")
            app.root.current = "login"
            # Limpa campos
            self.ids.user_input.text = ""
            self.ids.resposta_input.text = ""
            self.ids.nova_senha_input.text = ""
            self.ids.label_pergunta.text = "Pergunta aparecerá aqui..."
        else:
            app.mostrar_alerta("Erro", "Resposta incorreta.")


class MenuScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        if app.conta_atual:
            # Pega o primeiro nome para não ficar gigante
            primeiro_nome = app.conta_atual.nome_completo.split()[0]
            self.ids.label_boasvindas.text = f"Olá, {primeiro_nome}!"

class MetaScreen(MDScreen):
    pass


class MetaScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        if not app.conta_atual: return # Segurança

        # carrega os dados salvos
        dados = app.logic.calcular_progresso_meta(app.conta_atual.id_conta)

        texto = (
            f"Meta atual: R$ {dados['meta']:.2f}\n"
            f"Total Ganhos: R$ {dados['total_receitas']:.2f}\n"
            f"Total Gastos: R$ {dados['total_despesas']:.2f}\n"
            f"Economizado: R$ {dados['saldo']:.2f}\n"
            f"Progresso: {dados['progresso']:.1f}%"
        )

        # atualiza o label do KV
        try:
            self.ids.texto_progresso.text = texto
        except:
            print("ID texto_progresso não encontrado no meta.kv")



class MovimentacaoScreen(MDScreen):
    tipo = StringProperty()

    def registrar(self):
        app = MDApp.get_running_app()

        valor = self.ids.valor.text.strip()
        descricao = self.ids.descricao.text.strip()
        categoria = self.ids.categoria.text.strip()

        if not valor or not descricao or categoria == "Selecione uma categoria":
            app.mostrar_alerta("Erro", "Preencha todos os campos.")
            return

        try:
            valor = float(valor)
        except:
            app.mostrar_alerta("Erro", "Valor inválido.")
            return

        sucesso = app.logic.registrar_movimentacao(
            app.conta_atual.id_conta,
            self.tipo,
            valor,
            descricao,
            categoria
        )

        if sucesso:
            app.mostrar_alerta("Sucesso", "Movimentação registrada.")
            self.ids.valor.text = ""
            self.ids.descricao.text = ""
            self.ids.categoria.text = "Selecione uma categoria"
        else:
            app.mostrar_alerta("Erro", "Falha ao registrar.")


class RelatorioScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        self.ids.grafico_box.clear_widgets()

        transacoes = app.logic.get_transacoes_usuario(app.conta_atual.id_conta)
        if not transacoes:
            self.ids.resultado.text = "Nenhuma movimentação registrada."
            return

        relatorio = DecoratorRecomendacoes(
            DecoratorAnaliseCategorias(
                DecoratorDetalhado(
                    RelatorioFinanceiroBase(transacoes)
                )
            )
        )

        dados = relatorio.gerar()

        texto = (
            f"Total Ganhos: R$ {dados['total_ganhos']:.2f}\n"
            f"Total Gastos: R$ {dados['total_gastos']:.2f}\n"
            f"Saldo Final: R$ {dados['saldo_final']:.2f}\n\n"
            "Recomendações:\n"
        )
        for r in dados["recomendacoes"]:
            texto += f"- {r}\n"

        self.ids.resultado.text = texto

        # Gráfico
        fig, ax = plt.subplots(figsize=(3, 2.2))
        categorias = ["Ganhos", "Gastos"]
        valores = [dados["total_ganhos"], abs(dados["total_gastos"])]

        ax.pie(valores, labels=categorias, autopct="%1.1f%%", startangle=90)
        self.ids.grafico_box.add_widget(FigureCanvasKivyAgg(fig))


class ReceitasScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        todas_do_usuario = app.logic.get_transacoes_usuario(app.conta_atual.id_conta)
        transacoes = [t for t in todas_do_usuario if t["tipo"] == "receita"] # (ou "despesa")
        
        self.ids.grafico_box.clear_widgets()

        if not transacoes:
            self.ids.receitas_text.text = "Nenhuma receita registrada."
            return

        texto = "Receitas:\n\n"
        total = 0
        categorias = {}

        for t in transacoes:
            cat = t["categoria"].capitalize()
            val = abs(t["valor"])
            desc = t["descricao"]
            texto += f"- {desc} | {cat} | R$ {val:.2f}\n"
            categorias[cat] = categorias.get(cat, 0) + val
            total += val

        texto += f"\nTotal: R$ {total:.2f}"
        self.ids.receitas_text.text = texto

        # Gráfico
        fig, ax = plt.subplots(figsize=(3, 2.2))
        ax.pie(categorias.values(), labels=categorias.keys(), autopct="%1.1f%%")
        self.ids.grafico_box.add_widget(FigureCanvasKivyAgg(fig))


class DespesasScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        todas_do_usuario = app.logic.get_transacoes_usuario(app.conta_atual.id_conta)
        transacoes = [t for t in todas_do_usuario if t["tipo"] == "receita"] # (ou "despesa")
        self.ids.grafico_box.clear_widgets()

        if not transacoes:
            self.ids.despesas_text.text = "Nenhuma despesa registrada."
            return

        texto = "Despesas:\n\n"
        total = 0
        categorias = {}

        for t in transacoes:
            cat = t["categoria"].capitalize()
            val = abs(t["valor"])
            desc = t["descricao"]
            texto += f"- {desc} | {cat} | R$ {val:.2f}\n"
            categorias[cat] = categorias.get(cat, 0) + val
            total += val

        texto += f"\nTotal: R$ {total:.2f}"
        self.ids.despesas_text.text = texto

        fig, ax = plt.subplots(figsize=(3, 2.2))
        ax.pie(categorias.values(), labels=categorias.keys(), autopct="%1.1f%%")
        self.ids.grafico_box.add_widget(FigureCanvasKivyAgg(fig))


# ===================================================================
# APP PRINCIPAL
# ===================================================================
class FinanceAppMobile(MDApp):

    def build(self):
        Window.size = (360, 640)

        self.categorias = [
            "Lazer", "Boletos", "Alimentação", "Transporte", "Moradia", "Outros"
        ]

        self.logic = FinanceAppLogic()
        self.logic.adicionar_observer(RelatorioObserver())
        self.conta_atual = None

        Builder.load_file("ui/login.kv")
        Builder.load_file("ui/recuperar.kv")
        Builder.load_file("ui/cadastro.kv")
        Builder.load_file("ui/meta.kv")
        Builder.load_file("ui/movimentacao.kv")
        Builder.load_file("ui/relatorio.kv")
        Builder.load_file("ui/menu.kv")

        sm = MDScreenManager()
        sm.add_widget(Factory.LoginScreen())
        sm.add_widget(RecuperarScreen(name="recuperar"))
        sm.add_widget(CadastroScreen(name="cadastro"))
        sm.add_widget(Factory.MenuScreen())
        sm.add_widget(Factory.MetaScreen())

        # Movimentação
        tela_r = Factory.MovimentacaoScreen(name="receita")
        tela_r.tipo = "receita"
        sm.add_widget(tela_r)

        tela_d = Factory.MovimentacaoScreen(name="despesa")
        tela_d.tipo = "despesa"
        sm.add_widget(tela_d)

        sm.add_widget(RelatorioScreen(name="relatorio"))
        sm.add_widget(ReceitasScreen(name="receitas"))
        sm.add_widget(DespesasScreen(name="despesas"))

        sm.current = "login"
        return sm

    # Menu de categorias
    def abrir_menu_categorias(self, caller):
        from kivymd.uix.menu import MDDropdownMenu

        itens = [
            {
                "text": c,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=c: self.selecionar_categoria(caller, x)
            }
            for c in self.categorias
        ]

        self.menu = MDDropdownMenu(caller=caller, items=itens, width_mult=4)
        self.menu.open()

    def selecionar_categoria(self, caller, categoria):
        caller.text = categoria
        self.menu.dismiss()

    # Alertas
    def mostrar_alerta(self, titulo, mensagem):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton

        dialog = MDDialog(
            title=titulo,
            text=str(mensagem),
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    # ------- SALVAR META (AGORA ESTÁ DENTRO DA CLASSE E FUNCIONA) -------
    def salvar_meta(self, valor):
        if self.logic.configurar_meta(self.conta_atual.id_conta, valor):
            dados = self.logic.calcular_progresso_meta(self.conta_atual.id_conta)
            self.mostrar_alerta("Meta Atualizada", f"Meta atualizada")
        else:
            self.mostrar_alerta("Erro", "Valor inválido.")

        # Atualiza a tela meta
        try:
            screen = self.root.get_screen("meta")
            dados = self.logic.calcular_progresso_meta(self.conta_atual.id_conta)

            texto = (
                f"Meta atual: R$ {dados['meta']:.2f}\n"
                f"Total Ganhos: R$ {dados['total_receitas']:.2f}\n"
                f"Total Gastos: R$ {dados['total_despesas']:.2f}\n"
                f"Economizado: R$ {dados['saldo']:.2f}\n"
                f"Progresso: {dados['progresso']:.1f}%"
            )

            screen.ids.texto_progresso.text = texto

        except Exception as e:
            print("Falha ao atualizar tela meta:", e)


if __name__ == "__main__":
    FinanceAppMobile().run()
