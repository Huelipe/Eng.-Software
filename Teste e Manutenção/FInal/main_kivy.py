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
import csv
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
# LÓGICA PRINCIPAL
# ===================================================================
# No arquivo main_kivy.py

class FinanceAppLogic(FinanceFacade, Subject):

    def __init__(self):
        FinanceFacade.__init__(self)
        Subject.__init__(self)

        self.transacoes_registradas = []
        self.arquivo_dados = "movimentacoes.json"
        self._carregar_movimentacoes()

        # CORREÇÃO: Meta agora é um dicionário {id_usuario: valor}
        self.metas_db = {} 
        self._carregar_meta()

    # --- NOVO MÉTODO DE FILTRO ---
    def get_transacoes_usuario(self, id_conta):
        """Retorna apenas as transações do usuário logado"""
        return [t for t in self.transacoes_registradas if t.get("id_conta") == id_conta]

    def exportar_dados_csv(self, id_conta, nome_arquivo="extrato_financeiro.csv"):
        try:
            # 1. Filtra apenas os dados deste usuário
            transacoes = self.get_transacoes_usuario(id_conta)

            # 2. Escreve no arquivo
            with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')

                # Cabeçalho
                writer.writerow(["Data", "Tipo", "Categoria", "Descrição", "Valor"])

                # Dados Filtrados
                for t in transacoes:
                    writer.writerow([
                        t.get("data", ""),
                        t.get("tipo", "").upper(),
                        t.get("categoria", "").capitalize(),
                        t.get("descricao", ""),
                        str(t.get("valor", 0)).replace('.', ',')
                    ])

            return True
        except Exception as e:
            print(f"Erro ao exportar CSV: {e}")
            return False

    # MOVIMENTAÇÃO --------------------------------------------------
    def registrar_movimentacao(self, id_conta, tipo, valor, descricao, categoria=None):
        sucesso = super().registrar_movimentacao(id_conta, tipo, valor, descricao)

        if not sucesso:
            return False

        valor = float(valor)

        nova = {
            "id_conta": id_conta,  # <--- CORREÇÃO: Salvando o ID DO DONO
            "descricao": descricao,
            "valor": valor if tipo == "receita" else -abs(valor),
            "tipo": tipo,
            "categoria": categoria if categoria else "outros",
            "data": "2025-10-25" # (Idealmente usar datetime.now().strftime, mas mantive sua lógica)
        }

        self.transacoes_registradas.append(nova)
        self._salvar_movimentacoes()

        # Notifica passando apenas as do usuário atual seria o ideal, mas para simplificar:
        self.notificar_observers("nova_movimentacao", {"transacoes": self.transacoes_registradas})
        return True

    # META (CORRIGIDA PARA MULTI-USUÁRIO) ---------------------------
    def configurar_meta(self, id_conta, valor): # <--- Recebe ID agora
        try:
            self.metas_db[id_conta] = max(float(valor), 0)
            self._salvar_meta()
            return True
        except:
            return False

    def _salvar_meta(self):
        with open("meta.json", "w", encoding="utf-8") as f:
            json.dump(self.metas_db, f) # Salva o dicionário todo

    def _carregar_meta(self):
        if not os.path.exists("meta.json"):
            return
        try:
            with open("meta.json", "r", encoding="utf-8") as f:
                self.metas_db = json.load(f)
        except:
            self.metas_db = {}

    def calcular_progresso_meta(self, id_conta): # <--- Recebe ID
        total_receitas = 0.0
        total_despesas = 0.0

        # CORREÇÃO: Filtra só as transações DESTE usuário
        transacoes_usuario = self.get_transacoes_usuario(id_conta)

        for t in transacoes_usuario:
            v = float(t.get("valor", 0))
            if t["tipo"] == "receita":
                total_receitas += abs(v)
            else:
                total_despesas += abs(v)

        saldo = total_receitas - total_despesas
        
        # Pega a meta específica deste usuário
        meta = float(self.metas_db.get(id_conta, 0))

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

    # SALVAR / CARREGAR MOVIMENTAÇÕES ------------------------------
    def _salvar_movimentacoes(self):
        with open(self.arquivo_dados, "w", encoding="utf-8") as f:
            json.dump(self.transacoes_registradas, f, ensure_ascii=False, indent=4)

    def _carregar_movimentacoes(self):
        if not os.path.exists(self.arquivo_dados):
            return
        try:
            with open(self.arquivo_dados, "r", encoding="utf-8") as f:
                self.transacoes_registradas = json.load(f)
                # Garante tipos numéricos
                for mov in self.transacoes_registradas:
                    mov["valor"] = float(mov.get("valor", 0))
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
        app.root.current = "cadastro"


# >>> ADIÇÃO DO CADASTRO
class CadastroScreen(MDScreen):
    def cadastrar(self):
        app = MDApp.get_running_app()

        usuario = self.ids.usuario.text.strip()
        nome = self.ids.nome.text.strip()
        senha = self.ids.senha.text.strip()
        pergunta = self.ids.pergunta.text.strip()
        resposta = self.ids.resposta.text.strip()

        if not usuario or not nome or not senha or not pergunta or not resposta:
            app.mostrar_alerta("Erro", "Preencha todos os campos.")
            return

        conta = app.logic.criar_nova_conta(usuario, nome, senha, pergunta, resposta)

        if conta:
            app.mostrar_alerta("Sucesso", "Conta criada!")
            app.root.current = "login"
        else:
            app.mostrar_alerta("Erro", "Usuário já existe.")


# >>> ADIÇÃO DA RECUPERAÇÃO
class RecuperarScreen(MDScreen):
    def buscar_pergunta(self):
        app = MDApp.get_running_app()
        user = self.ids.user_input.text.strip()

        pergunta = app.logic.buscar_pergunta_seguranca(user)

        if pergunta:
            self.ids.label_pergunta.text = pergunta
            self.ids.resposta_input.disabled = False
            self.ids.nova_senha_input.disabled = False
            self.ids.btn_resetar.disabled = False
        else:
            self.ids.label_pergunta.text = "Usuário não encontrado."

    def confirmar_reset(self):
        app = MDApp.get_running_app()
        user = self.ids.user_input.text.strip()
        resp = self.ids.resposta_input.text.strip()
        nova = self.ids.nova_senha_input.text.strip()

        if app.logic.resetar_senha(user, resp, nova):
            app.mostrar_alerta("Sucesso", "Senha alterada!")
            app.root.current = "login"
        else:
            app.mostrar_alerta("Erro", "Resposta incorreta.")


class MenuScreen(MDScreen):
    pass


class MetaScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        
        # Segurança: Se ninguém estiver logado, não faz nada
        if not app.conta_atual: 
            return

        # CORREÇÃO: Passamos o ID da conta atual aqui dentro dos parênteses
        dados = app.logic.calcular_progresso_meta(app.conta_atual.id_conta)

        texto = (
            f"Meta atual: R$ {dados['meta']:.2f}\n"
            f"Total Ganhos: R$ {dados['total_receitas']:.2f}\n"
            f"Total Gastos: R$ {dados['total_despesas']:.2f}\n"
            f"Economizado: R$ {dados['saldo']:.2f}\n"
            f"Progresso: {dados['progresso']:.1f}%"
        )

        self.ids.texto_progresso.text = texto

class MovimentacaoScreen(MDScreen):
    tipo = StringProperty()

    def registrar(self):
        app = MDApp.get_running_app()

        valor = self.ids.valor.text.strip()
        descricao = self.ids.descricao.text.strip()
        categoria = self.ids.categoria.text.strip()

        if not valor or not descricao or categoria == "Selecione uma categoria":
            app.mostrar_alerta("Erro", "Preencha tudo.")
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
            app.mostrar_alerta("Sucesso", "Registrado!")
            self.ids.valor.text = ""
            self.ids.descricao.text = ""
            self.ids.categoria.text = "Selecione uma categoria"
        else:
            app.mostrar_alerta("Erro", "Falha ao registrar.")

class ReceitasScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        if not app.conta_atual: return
        
        # --- CORREÇÃO AQUI ---
        # Antes: Pegava app.logic.transacoes_registradas (TUDO MUNDO)
        # Agora: Pega app.logic.get_transacoes_usuario (SÓ O USUÁRIO LOGADO)
        todas_do_usuario = app.logic.get_transacoes_usuario(app.conta_atual.id_conta)
        transacoes = [t for t in todas_do_usuario if t["tipo"] == "receita"]
        # ---------------------

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
        app = MDApp.get_running_app()
        if not app.conta_atual: return
        todas = app.logic.get_transacoes_usuario(app.conta_atual.id_conta)

        transacoes = [t for t in todas if t["tipo"] == "receita"]

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
        if not app.conta_atual: return

        # 1. PEGA APENAS DADOS DO USUÁRIO LOGADO (O filtro correto)
        todas_do_usuario = app.logic.get_transacoes_usuario(app.conta_atual.id_conta)
        
        # 2. FILTRA APENAS AS DESPESAS
        transacoes = [t for t in todas_do_usuario if t["tipo"] == "despesa"]

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



class RelatorioScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        if not app.conta_atual: return

        self.ids.grafico_box.clear_widgets()

        # --- CORREÇÃO AQUI ---
        # Passa o ID para pegar só as transações desse usuário
        transacoes = app.logic.get_transacoes_usuario(app.conta_atual.id_conta)
        # ---------------------

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
 # ===================================================================
# APP PRINCIPAL
# ===================================================================
class FinanceAppMobile(MDApp):

    def build(self):
        Window.size = (360, 640)

        self.categorias = ["Lazer", "Boletos", "Alimentação", "Transporte", "Moradia", "Outros"]

        self.logic = FinanceAppLogic()
        self.logic.adicionar_observer(RelatorioObserver())
        self.conta_atual = None

        Builder.load_file("ui/login.kv")
        Builder.load_file("ui/cadastro.kv")
        Builder.load_file("ui/recuperar.kv")
        Builder.load_file("ui/meta.kv")
        Builder.load_file("ui/movimentacao.kv")
        Builder.load_file("ui/relatorio.kv")
        Builder.load_file("ui/menu.kv")

        sm = MDScreenManager()
        sm.add_widget(Factory.LoginScreen())
        sm.add_widget(CadastroScreen(name="cadastro"))
        sm.add_widget(RecuperarScreen(name="recuperar"))
        sm.add_widget(Factory.MenuScreen())
        sm.add_widget(Factory.MetaScreen())

        # Movimentações
        tela_r = Factory.MovimentacaoScreen(name="receita")
        tela_r.tipo = "receita"
        sm.add_widget(tela_r)

        tela_d = Factory.MovimentacaoScreen(name="despesa")
        tela_d.tipo = "despesa"
        sm.add_widget(tela_d)

        # 🔹 Telas de listagem
        sm.add_widget(RelatorioScreen(name="relatorio"))
        sm.add_widget(ReceitasScreen(name="receitas"))
        sm.add_widget(DespesasScreen(name="despesas"))

        sm.current = "login"
        return sm

    # CATEGORIAS
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

    # ALERTAS
    def mostrar_alerta(self, titulo, mensagem):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton

        dialog = MDDialog(
            title=titulo,
            text=str(mensagem),
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    # SALVAR META (VERSÃO ÚNICA E CORRETA)
    def salvar_meta(self, valor):
        # 1. Verifica se tem usuário logado
        if not self.conta_atual: 
            return

        # 2. Passamos o ID da conta PRIMEIRO
        if self.logic.configurar_meta(self.conta_atual.id_conta, valor):
            
            # 3. Passamos o ID para calcular
            dados = self.logic.calcular_progresso_meta(self.conta_atual.id_conta)
            
            self.mostrar_alerta("Meta Atualizada", "Meta salva com sucesso.")
        else:
            self.mostrar_alerta("Erro", "Valor inválido.")
            return

        # 4. Atualiza a tela visualmente
        try:
            screen = self.root.get_screen("meta")
            
            # 5. Passamos o ID novamente
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
            print(f"Erro ao atualizar tela meta: {e}")

    def exportar_csv(self):
        # Segurança: verifica se tem usuário
        if not self.conta_atual: return

        arquivo = "extrato_financeiro.csv"

        # CORREÇÃO: Passamos o ID da conta para filtrar o CSV
        if self.logic.exportar_dados_csv(self.conta_atual.id_conta, arquivo):
            self.mostrar_alerta("Sucesso", f"Arquivo '{arquivo}' gerado com sucesso!")
        else:
            self.mostrar_alerta("Erro", "Falha ao gerar CSV. Feche o arquivo se estiver aberto!")

    def build(self):
        Window.size = (360, 640)

        self.categorias = ["Lazer", "Boletos", "Alimentação", "Transporte", "Moradia", "Outros"]

        self.logic = FinanceAppLogic()
        self.logic.adicionar_observer(RelatorioObserver())
        self.conta_atual = None

        Builder.load_file("ui/login.kv")
        Builder.load_file("ui/cadastro.kv")
        Builder.load_file("ui/recuperar.kv")
        Builder.load_file("ui/meta.kv")
        Builder.load_file("ui/movimentacao.kv")
        Builder.load_file("ui/relatorio.kv")
        Builder.load_file("ui/menu.kv")

        sm = MDScreenManager()
        sm.add_widget(Factory.LoginScreen())
        sm.add_widget(CadastroScreen(name="cadastro"))
        sm.add_widget(RecuperarScreen(name="recuperar"))
        sm.add_widget(Factory.MenuScreen())
        sm.add_widget(Factory.MetaScreen())


        # Movimentações
        tela_r = Factory.MovimentacaoScreen(name="receita")
        tela_r.tipo = "receita"
        sm.add_widget(tela_r)

        tela_d = Factory.MovimentacaoScreen(name="despesa")
        tela_d.tipo = "despesa"
        sm.add_widget(tela_d)

        # 🔹 Telas de listagem (IMPORTANTE)
        sm.add_widget(RelatorioScreen(name="relatorio"))
        sm.add_widget(ReceitasScreen(name="receitas"))
        sm.add_widget(DespesasScreen(name="despesas"))


        sm.current = "login"
        return sm

    # CATEGORIAS
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

    # ALERTAS
    def mostrar_alerta(self, titulo, mensagem):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton

        dialog = MDDialog(
            title=titulo,
            text=str(mensagem),
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()


if __name__ == "__main__":
    FinanceAppMobile().run()
