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

    def __init__(self):
        FinanceFacade.__init__(self)
        Subject.__init__(self)

        self.transacoes_registradas = []
        self.arquivo_dados = "movimentacoes.json"

        self._carregar_movimentacoes()

        self.meta_economia = 0.0
        self._carregar_meta()

    # ---------------------------------------------------------------
    # REGISTRAR MOVIMENTAÇÃO (CORRIGIDO — APENAS UMA FUNÇÃO)
    # ---------------------------------------------------------------
    def registrar_movimentacao(self, id_conta, tipo, valor, descricao, categoria=None):
        sucesso = super().registrar_movimentacao(id_conta, tipo, valor, descricao)

        if not sucesso:
            return False

        valor = float(valor)

        nova = {
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
    # META
    # ---------------------------------------------------------------
    def configurar_meta(self, valor):
        try:
            self.meta_economia = max(float(valor), 0)
            self._salvar_meta()
            return True
        except:
            return False

    def _salvar_meta(self):
        with open("meta.json", "w", encoding="utf-8") as f:
            json.dump({"meta": self.meta_economia}, f)

    def _carregar_meta(self):
        if not os.path.exists("meta.json"):
            return
        try:
            with open("meta.json", "r", encoding="utf-8") as f:
                self.meta_economia = float(json.load(f).get("meta", 0))
        except:
            self.meta_economia = 0

    def calcular_progresso_meta(self):
        total_receitas = 0.0
        total_despesas = 0.0

        for t in self.transacoes_registradas:
            v = float(t.get("valor", 0))
            if t["tipo"] == "receita":
                total_receitas += abs(v)
            else:
                total_despesas += abs(v)

        saldo = total_receitas - total_despesas
        meta = float(self.meta_economia)

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
        else:
            app.mostrar_alerta("Erro", "Usuário ou senha incorretos.")

    def criar_conta(self):
        app = MDApp.get_running_app()
        usuario = self.ids.usuario.text.strip()
        senha = self.ids.senha.text.strip()

        if not usuario or not senha:
            app.mostrar_alerta("Erro", "Preencha usuário e senha.")
            return

        conta = app.logic.criar_nova_conta(usuario, usuario, senha)
        if conta:
            app.mostrar_alerta("Sucesso", "Conta criada.")
        else:
            app.mostrar_alerta("Erro", "Usuário já existe.")


class MenuScreen(MDScreen):
    pass

class MetaScreen(MDScreen):
    pass


class MetaScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()

        # carrega os dados salvos
        dados = app.logic.calcular_progresso_meta()

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

        transacoes = app.logic.transacoes_registradas
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
        transacoes = [t for t in app.logic.transacoes_registradas if t["tipo"] == "receita"]

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
        transacoes = [t for t in app.logic.transacoes_registradas if t["tipo"] == "despesa"]

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
        Builder.load_file("ui/meta.kv")
        Builder.load_file("ui/movimentacao.kv")
        Builder.load_file("ui/relatorio.kv")
        Builder.load_file("ui/menu.kv")

        sm = MDScreenManager()
        sm.add_widget(Factory.LoginScreen())
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
        if self.logic.configurar_meta(valor):
            dados = self.logic.calcular_progresso_meta()
            self.mostrar_alerta("Meta Atualizada", f"Meta atualizada")
        else:
            self.mostrar_alerta("Erro", "Valor inválido.")

        # Atualiza a tela meta
        try:
            screen = self.root.get_screen("meta")
            dados = self.logic.calcular_progresso_meta()

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
