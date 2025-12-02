# Felipe/observer.py
from typing import List, Protocol
from Giovanna.decorator import (
    RelatorioFinanceiroBase,
    DecoratorDetalhado,
    DecoratorAnaliseCategorias,
    DecoratorRecomendacoes
)

# ==================== INTERFACES ====================

class Observer(Protocol):
    def update(self, evento: str, dados: dict):
        pass

class Subject:
    #Classe base para o 'sujeito observado' (ex: FinanceFacade).
    def __init__(self):
        self._observers: List[Observer] = []

    def adicionar_observer(self, observer: Observer):
        self._observers.append(observer)

    def notificar_observers(self, evento: str, dados: dict):
        for obs in self._observers:
            obs.update(evento, dados)

# ==================== OBSERVADOR CONCRETO ====================

class RelatorioObserver(Observer):
    #Gera automaticamente relatórios quando há movimentações.
    def update(self, evento: str, dados: dict):
        if evento == "nova_movimentacao":
            print("\n📊 [Observer] Nova movimentação detectada. Gerando relatório...")

            transacoes = dados.get("transacoes", [])
            relatorio_base = RelatorioFinanceiroBase(transacoes)

            # Adiciona camadas de decoradores
            relatorio_completo = DecoratorRecomendacoes(
                DecoratorAnaliseCategorias(
                    DecoratorDetalhado(relatorio_base)
                )
            )

            relatorio = relatorio_completo.gerar()
            print(f"Saldo Atual: R$ {relatorio['saldo_final']:.2f}")
            print("Recomendações:")
            for r in relatorio['recomendacoes']:
                print(f" - {r}")
