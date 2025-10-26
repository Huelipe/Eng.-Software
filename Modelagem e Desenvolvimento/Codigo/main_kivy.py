# main.py
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from Pedro.Facade import FinanceFacade
from Felipe.observer import Subject, RelatorioObserver
from Giovanna.decorator import (
    RelatorioFinanceiroBase,
    DecoratorDetalhado,
    DecoratorAnaliseCategorias,
    DecoratorRecomendacoes
)
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import json
import os
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from collections import defaultdict


# ====================================================
# LÓGICA PRINCIPAL (FACADE + SUBJECT)
# ====================================================
class FinanceAppLogic(FinanceFacade, Subject):
    def __init__(self):
        FinanceFacade.__init__(self)
        Subject.__init__(self)
        self.transacoes_registradas = []
        self.arquivo_dados = "movimentacoes.json"
        self._carregar_movimentacoes()

    def registrar_movimentacao(self, id_conta, tipo, valor, descricao, categoria=None):
        sucesso = super().registrar_movimentacao(id_conta, tipo, valor, descricao)
        if sucesso:
            self.transacoes_registradas.append({
                "descricao": descricao,
                "valor": float(valor) if tipo == "receita" else -float(valor),
                "tipo": tipo,
                "categoria": categoria if categoria else "Outros",
                "data": "2025-10-25"
            })
            self.notificar_observers("nova_movimentacao", {"transacoes": self.transacoes_registradas})
        return sucesso

    def listar_transacoes(self, tipo=None):
        """Retorna uma string formatada com as transações do tipo especificado."""
        if not self.transacoes_registradas:
            return "Nenhuma movimentação registrada."

        filtradas = (
            [t for t in self.transacoes_registradas if t["tipo"] == tipo]
            if tipo else self.transacoes_registradas
        )

        if not filtradas:
            return f"Nenhuma {tipo} registrada."

        linhas = []
        for t in filtradas:
            linhas.append(
                f"- {t['descricao']} | {t['categoria']} | R$ {abs(t['valor']):.2f}"
            )

        return "\n".join(linhas)


    # ====================================================
    # REGISTRAR MOVIMENTAÇÃO
    # ====================================================
    def registrar_movimentacao(self, id_conta, tipo, valor, descricao, categoria):
        """Registra uma movimentação e salva automaticamente no JSON."""
        sucesso = super().registrar_movimentacao(id_conta, tipo, valor, descricao)
        if sucesso:
            nova = {
                "descricao": descricao,
                "valor": float(valor) if tipo == "receita" else -float(valor),
                "categoria": categoria.lower(),
                "tipo": tipo,
                "data": "2025-10-25"
            }
            self.transacoes_registradas.append(nova)
            self._salvar_movimentacoes()
            self.notificar_observers("nova_movimentacao", {"transacoes": self.transacoes_registradas})
        return sucesso

    # ====================================================
    # SALVAR / CARREGAR
    # ====================================================
    def _salvar_movimentacoes(self):
        """Salva todas as movimentações no JSON."""
        try:
            with open(self.arquivo_dados, "w", encoding="utf-8") as f:
                json.dump(self.transacoes_registradas, f, ensure_ascii=False, indent=4)
            print(f"[Sistema] {len(self.transacoes_registradas)} movimentações salvas em '{self.arquivo_dados}'.")
        except Exception as e:
            print(f"[Sistema] ERRO ao salvar '{self.arquivo_dados}': {e}")

    def _carregar_movimentacoes(self):
        """Carrega as movimentações do JSON (se existir)."""
        if not os.path.exists(self.arquivo_dados):
            print("[Sistema] Nenhum arquivo de movimentações encontrado — iniciando novo.")
            return
        try:
            with open(self.arquivo_dados, "r", encoding="utf-8") as f:
                self.transacoes_registradas = json.load(f)

            # 🔹 Corrige dados antigos
            for mov in self.transacoes_registradas:
                # Garante que o valor seja float
                try:
                    mov["valor"] = float(mov["valor"])
                except (ValueError, TypeError):
                    mov["valor"] = 0.0

                if "categoria" not in mov:
                    mov["categoria"] = "geral"
                if "tipo" not in mov:
                    mov["tipo"] = "receita" if mov.get("valor", 0) >= 0 else "despesa"

            print(f"[Sistema] {len(self.transacoes_registradas)} movimentações carregadas.")
        except Exception as e:
            print(f"[Sistema] ERRO ao carregar '{self.arquivo_dados}': {e}")
            self.transacoes_registradas = []





# ====================================================
# TELAS
# ====================================================
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
            app.mostrar_alerta("Erro de Login", "Usuário ou senha incorretos.")

    def criar_conta(self):
        app = MDApp.get_running_app()
        usuario = self.ids.usuario.text.strip()
        senha = self.ids.senha.text.strip()

        if not usuario or not senha:
            app.mostrar_alerta("Campos Vazios", "Preencha usuário e senha para criar uma conta.")
            return

        conta = app.logic.criar_nova_conta(usuario, usuario, senha)
        if conta:
            app.mostrar_alerta("Sucesso", "Conta criada com sucesso! Faça login para continuar.")
        else:
            app.mostrar_alerta("Erro", "Usuário já existe. Escolha outro nome.")


class MenuScreen(MDScreen):
    pass


class MovimentacaoScreen(MDScreen):
    tipo = StringProperty()

    def registrar(self):
        app = MDApp.get_running_app()
        valor = self.ids.valor.text.strip()
        descricao = self.ids.descricao.text.strip()
        categoria = self.ids.categoria.text.strip()  # <-- novo campo

        if not valor or not descricao or not categoria or categoria == "Selecione uma categoria":
            app.mostrar_alerta("Campos Vazios", "Preencha todos os campos e selecione uma categoria.")
            return

        try:
            valor = float(valor)
        except ValueError:
            app.mostrar_alerta("Erro", "Valor inválido.")
            return

        app.logic.registrar_movimentacao(
            app.conta_atual.id_conta,
            self.tipo,
            valor,
            descricao,
            categoria
        )
        app.mostrar_alerta("Sucesso", f"{self.tipo.capitalize()} registrada com sucesso!")
        self.ids.valor.text = ""
        self.ids.descricao.text = ""
        self.ids.categoria.text = "Selecione uma categoria"

    def exibir_transacoes(self):
        """Mostra lista detalhada das transações e gráfico por categoria."""
        app = MDApp.get_running_app()
        transacoes = [t for t in app.logic.transacoes_registradas if t["tipo"] == self.tipo]

        # Limpa os elementos antigos
        self.ids.grafico_box.clear_widgets()
        self.ids.resultado.text = ""

        if not transacoes:
            self.ids.resultado.text = f"Nenhuma {self.tipo} registrada."
            return

        # ==== LISTA DETALHADA ====
        texto = f"💰 {self.tipo.capitalize()}s registradas:\n\n"
        total = 0
        for t in transacoes:
            cat = t.get("categoria", "Outros").capitalize()
            desc = t.get("descricao", "Sem descrição")
            val = abs(float(t.get("valor", 0)))
            texto += f"- {desc} | {cat} | R$ {val:.2f}\n"
            total += val

        texto += f"\n📊 Total de {self.tipo}s: R$ {total:.2f}\n"
        self.ids.resultado.text = texto

        # ==== GRÁFICO DE CATEGORIAS ====
        categorias = {}
        for t in transacoes:
            cat = t.get("categoria", "Outros").capitalize()
            categorias[cat] = categorias.get(cat, 0) + abs(float(t["valor"]))

        fig, ax = plt.subplots(figsize=(3.0, 2.3))
        ax.pie(
            categorias.values(),
            labels=categorias.keys(),
            autopct="%1.1f%%",
            startangle=90,
            textprops={"fontsize": 10},
        )
        ax.set_title(f"{self.tipo.capitalize()}s por Categoria", fontsize=10)
        self.ids.grafico_box.add_widget(FigureCanvasKivyAgg(fig))


class RelatorioScreen(MDScreen):
    def on_pre_enter(self):
        """Gera o relatório assim que a tela é aberta."""
        app = MDApp.get_running_app()
        self.ids.grafico_box.clear_widgets()

        transacoes = app.logic.transacoes_registradas
        if not transacoes:
            self.ids.resultado.text = "Ainda não há movimentações registradas."
            return

        # ======= TEXTO DO RELATÓRIO =======
        relatorio_base = RelatorioFinanceiroBase(transacoes)
        relatorio_completo = DecoratorRecomendacoes(
            DecoratorAnaliseCategorias(
                DecoratorDetalhado(relatorio_base)
            )
        )
        dados = relatorio_completo.gerar()

        texto = (
            f"📊 Relatório Financeiro\n\n"
            f"💰 Total Ganhos: R$ {dados['total_ganhos']:.2f}\n"
            f"💸 Total Gastos: R$ {dados['total_gastos']:.2f}\n"
            f"🧾 Saldo Final: R$ {dados['saldo_final']:.2f}\n\n"
            "💡 Recomendações:\n"
        )
        for r in dados["recomendacoes"]:
            texto += f" - {r}\n"

        self.ids.resultado.text = texto

        # ======= GRÁFICO (GANHOS vs GASTOS) =======
        ganhos = dados["total_ganhos"]
        gastos = abs(dados["total_gastos"])

        if ganhos == 0 and gastos == 0:
            return

        fig, ax = plt.subplots(figsize=(3, 2.25))  # 25% menor
        categorias = ['Ganhos', 'Gastos']
        valores = [ganhos, gastos]
        cores = ['#4CAF50', '#F44336']

        ax.pie(valores, labels=categorias, colors=cores, autopct='%1.1f%%', startangle=90)
        ax.set_title("Distribuição Financeira", fontsize=10)

        canvas = FigureCanvasKivyAgg(fig)
        self.ids.grafico_box.add_widget(canvas)



class ReceitasScreen(MDScreen):
    def on_pre_enter(self):
        """Mostra lista de receitas e gráfico por categoria."""
        app = MDApp.get_running_app()
        transacoes = [t for t in app.logic.transacoes_registradas if t["tipo"] == "receita"]

        # limpa o container
        self.ids.grafico_box.clear_widgets()

        if not transacoes:
            # usa o id que está no KV
            self.ids.receitas_text.text = "Nenhuma receita registrada."
            return

        # ====== LISTA TEXTO ======
        texto = "💰 Receitas registradas:\n\n"
        total = 0
        categorias = {}
        for t in transacoes:
            cat = t.get("categoria", "Outros").capitalize()
            val = abs(float(t["valor"]))
            desc = t.get("descricao", "Sem descrição")
            texto += f"- {desc} | {cat} | R$ {val:.2f}\n"
            categorias[cat] = categorias.get(cat, 0) + val
            total += val

        texto += f"\n📊 Total de Receitas: R$ {total:.2f}\n"
        # escreve no id existente no KV
        self.ids.receitas_text.text = texto

        # ====== GRÁFICO ======
        if categorias:
            fig, ax = plt.subplots(figsize=(15, 15))  # tamanho razoável para tela mobile
            ax.pie(
                list(categorias.values()),
                labels=list(categorias.keys()),
                autopct="%1.1f%%",
                startangle=90,
                textprops={"fontsize": 10},
            )
            ax.axis("equal")
            plt.tight_layout()

            grafico_widget = FigureCanvasKivyAgg(fig)
            # força tamanho do widget (25% menor do que antes)
            grafico_widget.size_hint_y = None
            grafico_widget.height = 195
            self.ids.grafico_box.add_widget(grafico_widget)


class DespesasScreen(MDScreen):
    def on_pre_enter(self):
        """Mostra lista de despesas e gráfico por categoria."""
        app = MDApp.get_running_app()
        transacoes = [t for t in app.logic.transacoes_registradas if t["tipo"] == "despesa"]

        self.ids.grafico_box.clear_widgets()

        if not transacoes:
            self.ids.despesas_text.text = "Nenhuma despesa registrada."
            return

        # ====== LISTA TEXTO ======
        texto = "💸 Despesas registradas:\n\n"
        total = 0
        categorias = {}
        for t in transacoes:
            cat = t.get("categoria", "Outros").capitalize()
            val = abs(float(t["valor"]))
            desc = t.get("descricao", "Sem descrição")
            texto += f"- {desc} | {cat} | R$ {val:.2f}\n"
            categorias[cat] = categorias.get(cat, 0) + val
            total += val

        texto += f"\n📊 Total de Despesas: R$ {total:.2f}\n"
        self.ids.despesas_text.text = texto

        # ====== GRÁFICO ======
        if categorias:
            fig, ax = plt.subplots(figsize=(15, 15))
            ax.pie(
                list(categorias.values()),
                labels=list(categorias.keys()),
                autopct="%1.1f%%",
                startangle=90,
                textprops={"fontsize": 10},
            )
            ax.axis("equal")
            plt.tight_layout()

            grafico_widget = FigureCanvasKivyAgg(fig)
            grafico_widget.size_hint_y = None
            grafico_widget.height = 195
            self.ids.grafico_box.add_widget(grafico_widget)



# ====================================================
# APP PRINCIPAL
# ====================================================
class FinanceAppMobile(MDApp):
    def build(self):
        from kivy.lang import Builder
        from kivy.core.window import Window
        from kivy.factory import Factory
        from kivymd.uix.screenmanager import MDScreenManager

        Window.size = (360, 640)

        # Categorias iniciais (poucas, como você pediu)
        self.categorias = [
            "Lazer",
            "Boletos",
            "Alimentação",
            "Transporte",
            "Moradia",
            "Outros"
        ]

        # Inicializa lógica e estado
        self.logic = FinanceAppLogic()
        self.logic.adicionar_observer(RelatorioObserver())
        self.conta_atual = None

        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Light"

        Builder.load_file("ui/login.kv")
        Builder.load_file("ui/menu.kv")
        Builder.load_file("ui/movimentacao.kv")
        Builder.load_file("ui/relatorio.kv")

        # Gerenciador de telas
        sm = MDScreenManager()

        sm.add_widget(Factory.LoginScreen())
        sm.add_widget(Factory.MenuScreen())

        # Cria telas de movimentação com 'tipo' como propriedade (StringProperty)
        receita_screen = Factory.MovimentacaoScreen(name="receita")
        receita_screen.tipo = "receita"
        sm.add_widget(receita_screen)

        despesa_screen = Factory.MovimentacaoScreen(name="despesa")
        despesa_screen.tipo = "despesa"
        sm.add_widget(despesa_screen)

        sm.add_widget(RelatorioScreen(name="relatorio"))
        sm.add_widget(ReceitasScreen(name="receitas"))
        sm.add_widget(DespesasScreen(name="despesas"))

        sm.current = "login"
        return sm

    # método que abre o menu de seleção de categorias (usado no .kv)
    def abrir_menu_categorias(self, caller):
        # monta os itens para o MDDropdownMenu
        menu_items = [
            {
                "text": c,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=c: self.selecionar_categoria(caller, x)
            }
            for c in self.categorias
        ]
        # cria/abre o menu (width_mult ajusta largura)
        from kivymd.uix.menu import MDDropdownMenu
        self.menu = MDDropdownMenu(caller=caller, items=menu_items, width_mult=4)
        self.menu.open()

    def selecionar_categoria(self, caller, categoria):
        caller.text = categoria
        try:
            self.menu.dismiss()
        except Exception:
            pass

    # utilitário de diálogo (assegura que app.mostrar_alerta exista)
    def mostrar_alerta(self, titulo, mensagem):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        dialog = MDDialog(
            title=titulo,
            text=str(mensagem),
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()


if __name__ == "__main__":
    FinanceAppMobile().run()
