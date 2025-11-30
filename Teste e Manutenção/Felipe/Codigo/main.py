# main.py
from Pedro.Facade import FinanceFacade
from Felipe.observer import Subject, RelatorioObserver
from Giovanna.decorator import (
    RelatorioFinanceiroBase,
    DecoratorDetalhado,
    DecoratorAnaliseCategorias,
    DecoratorRecomendacoes
)

from decimal import Decimal
import getpass

# ========================================================
# CLASSE PRINCIPAL (UNE FACADE + SUBJECT)
# ========================================================
class FinanceApp(FinanceFacade, Subject):
    def __init__(self):
        FinanceFacade.__init__(self)
        Subject.__init__(self)
        self.transacoes_registradas = []
        self.arquivo_dados = "movimentacoes.json"


    def registrar_movimentacao(self, id_conta, tipo, valor, descricao):
        sucesso = super().registrar_movimentacao(id_conta, tipo, valor, descricao)
        if sucesso:
            self.transacoes_registradas.append({
                "descricao": descricao,
                "valor": float(valor) if tipo == "receita" else -float(valor),
                "categoria": tipo,
                "data": "2025-10-21"
            })
            # Notifica observers
            self.notificar_observers("nova_movimentacao", {"transacoes": self.transacoes_registradas})
        return sucesso

# ========================================================
# FUNÇÕES AUXILIARES
# ========================================================
def gerar_relatorio(app):
    print("\n📊 Gerando Relatório Financeiro Completo...")
    if not app.transacoes_registradas:
        print("Ainda não há movimentações registradas.")
        return

    relatorio_base = RelatorioFinanceiroBase(app.transacoes_registradas)
    relatorio_completo = DecoratorRecomendacoes(
        DecoratorAnaliseCategorias(
            DecoratorDetalhado(relatorio_base)
        )
    )
    dados = relatorio_completo.gerar()
    print("\n==== RELATÓRIO ATUAL ====")
    print(f"Total Ganhos: R$ {dados['total_ganhos']:.2f}")
    print(f"Total Gastos: R$ {dados['total_gastos']:.2f}")
    print(f"Saldo Final:  R$ {dados['saldo_final']:.2f}")
    print("Recomendações:")
    for r in dados["recomendacoes"]:
        print(f" - {r}")

# ========================================================
# MENU DE LOGIN
# ========================================================
def menu_login(app):
    print("\n--- LOGIN / CRIAÇÃO DE CONTA ---")
    print("1. Fazer Login")
    print("2. Criar Nova Conta")
    print("3. Sair")
    escolha = input("Escolha: ")

    if escolha == '1':
        usuario = input("Usuário: ")
        senha = getpass.getpass("Senha: ")
        conta = app.autenticar_usuario(usuario, senha)
        if conta:
            return conta
        else:
            print("[ERRO] Usuário ou senha incorretos.")
            return None

    elif escolha == '2':
        usuario = input("Usuário: ")
        nome = input("Nome completo: ")
        senha = getpass.getpass("Senha: ")
        # saldo inicial removido — começa sempre com 0,00
        conta = app.criar_nova_conta(usuario, nome, senha)
        if conta:
            print("✅ Conta criada com sucesso! Seu saldo inicial é R$ 0,00.")
            return conta
        else:
            print("[ERRO] Não foi possível criar a conta (talvez o nome de usuário já exista).")
            return None

    elif escolha == '3':
        print("Saindo...")
        quit()

    else:
        print("Opção inválida.")
        return None

# ========================================================
# MENU PRINCIPAL (APÓS LOGIN)
# ========================================================
def menu_principal(app, conta):
    id_conta = conta.id_conta
    while True:
        saldo_atual = app.get_saldo(id_conta)
        print("\n" + "=" * 45)
        print(f"Conta: {conta.nome_completo} | Saldo: R$ {saldo_atual}")
        print("=" * 45)
        print("1. Adicionar Receita")
        print("2. Adicionar Despesa")
        print("3. Ver Histórico de Receitas")
        print("4. Ver Histórico de Despesas")
        print("5. Gerar Relatório Financeiro")
        print("6. Logout")
        opc = input("Escolha: ")

        if opc == "1" or opc == "2":
            tipo = "receita" if opc == "1" else "despesa"
            valor = input(f"Valor da {tipo}: ")
            desc = input(f"Descrição da {tipo}: ")
            app.registrar_movimentacao(id_conta, tipo, valor, desc)

        elif opc == "3":
            historico = app.get_historico_receitas(id_conta)
            total = sum((mov.valor for mov in historico), Decimal('0.0'))
            print("\n--- HISTÓRICO DE RECEITAS ---")
            if not historico:
                print("Nenhuma receita registrada.")
            else:
                for mov in historico:
                    data = mov.data.strftime("%d/%m/%Y às %H:%M")
                    print(f"{data} | R$ {mov.valor:>8.2f} | {mov.descricao}")
            print(f"TOTAL: R$ {total:>8.2f}")

        elif opc == "4":
            historico = app.get_historico_despesas(id_conta)
            total = sum((mov.valor for mov in historico), Decimal('0.0'))
            print("\n--- HISTÓRICO DE DESPESAS ---")
            if not historico:
                print("Nenhuma despesa registrada.")
            else:
                for mov in historico:
                    data = mov.data.strftime("%d/%m/%Y às %H:%M")
                    print(f"{data} | R$ {mov.valor:>8.2f} | {mov.descricao}")
            print(f"TOTAL: R$ {total:>8.2f}")

        elif opc == "5":
            gerar_relatorio(app)

        elif opc == "6":
            print(f"Logout concluído. Até logo, {conta.nome_completo}!")
            break

        else:
            print("Opção inválida.")


# ========================================================
# EXECUÇÃO
# ========================================================
if __name__ == "__main__":
    app = FinanceApp()
    observer = RelatorioObserver()
    app.adicionar_observer(observer)

    conta = menu_login(app)
    menu_principal(app, conta)
