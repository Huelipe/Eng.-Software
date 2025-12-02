from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Any



class Relatorio(ABC):
    """
    Interface comum para todos os relatórios - Componente do padrão Decorator
    Define os métodos que tanto o componente concreto quanto os decorators devem implementar
    """
    @abstractmethod
    def gerar(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_conteudo(self) -> str:
        pass

class RelatorioFinanceiroBase(Relatorio):
    """
    Componente Concreto do padrão Decorator
    Implementação básica do relatório financeiro sem funcionalidades extras
    Esta é a classe que será 'decorada' com funcionalidades adicionais
    """
    def __init__(self, transacoes: List[Dict]):
        self.transacoes = transacoes
    
    def gerar(self) -> Dict[str, Any]:
        total_gastos = sum(t['valor'] for t in self.transacoes if t['valor'] < 0)
        total_ganhos = sum(t['valor'] for t in self.transacoes if t['valor'] > 0)
        
        gastos_por_categoria = {}
        for transacao in self.transacoes:
            if transacao['valor'] < 0:
                categoria = transacao['categoria']
                valor = abs(transacao['valor'])
                gastos_por_categoria[categoria] = gastos_por_categoria.get(categoria, 0) + valor
        
        return {
            'total_gastos': abs(total_gastos),
            'total_ganhos': total_ganhos,
            'saldo_final': total_ganhos + total_gastos,
            'gastos_por_categoria': gastos_por_categoria,
            'quantidade_transacoes': len(self.transacoes)
        }
    
    def get_conteudo(self) -> str:
        dados = self.gerar()
        return f"Relatório Financeiro Básico - {dados['quantidade_transacoes']} transações"

# ==================== DECORATORS ====================

class RelatorioDecorator(Relatorio):
    """
    Decorator Base - Classe abstrata para todos os decorators concretos
    Mantém referência para o relatório que está sendo decorado e delega chamadas para ele
    Esta é a peça central do padrão Decorator
    """
    def __init__(self, relatorio: Relatorio):
        # decorator: guarda referencia para o componente que será decorado
        self._relatorio = relatorio
    
    def gerar(self) -> Dict[str, Any]:
        # decorator: delega a operação para o componente decorado
        return self._relatorio.gerar()
    
    def get_conteudo(self) -> str:
        # decorator: delega a operação para o componente decorado
        return self._relatorio.get_conteudo()

class DecoratorDetalhado(RelatorioDecorator):
    """
    Decorator Concreto - Adiciona funcionalidade de transações detalhadas
    decorator: estende o comportamento do relatório base sem modificar sua classe
    """
    def gerar(self) -> Dict[str, Any]:
        # decorator: primeiro chama o método do componente decorado
        dados_base = super().gerar()
        
        # decorator: depois adiciona nova funcionalidade
        dados_base['transacoes_detalhadas'] = [
            {
                'descricao': t['descricao'],
                'valor': t['valor'],
                'categoria': t['categoria'],
                'data': t['data']
            }
            for t in self._relatorio.transacoes
        ]
        return dados_base
    
    def get_conteudo(self) -> str:
        # decorator: estende o conteúdo do componente decorado
        return f"{super().get_conteudo()} - Versão Detalhada"

class DecoratorAnaliseCategorias(RelatorioDecorator):
    """
    Decorator Concreto - add análise estatística das categorias
    decorator: encapsula outro relatório e adiciona análise de percentuais
    """
    def gerar(self) -> Dict[str, Any]:
        # decorator: obtem dados do componente decorado
        dados_base = super().gerar()
        gastos_por_categoria = dados_base['gastos_por_categoria']
        
        if gastos_por_categoria:
            total_gastos = dados_base['total_gastos']
            
            # decorator: nova analise aos dados existentes
            percentuais = {
                categoria: (valor / total_gastos) * 100
                for categoria, valor in gastos_por_categoria.items()
            }
            
            categoria_mais_gasta = max(gastos_por_categoria.items(), key=lambda x: x[1])
            
            dados_base['analise_categorias'] = {
                'percentuais': percentuais,
                'categoria_mais_gasta': categoria_mais_gasta,
                'total_categorias': len(gastos_por_categoria)
            }
        
        return dados_base
    
    def get_conteudo(self) -> str:
        # decorator: estende a descricao do relatorio
        return f"{super().get_conteudo()} - Com Análise"

class DecoratorRecomendacoes(RelatorioDecorator):
    """
    Decorator Concreto - add recomendações inteligentes baseadas nos dados
    decorator: add comportamento inteligente sem modificar a lógica base
    """
    def gerar(self) -> Dict[str, Any]:
        # decorator: obtem dados do componente decorado
        dados_base = super().gerar()
        recomendacoes = []
        
        total_gastos = dados_base['total_gastos']
        total_ganhos = dados_base['total_ganhos']
        saldo = dados_base['saldo_final']
        
        # decorator: recomenda baseado no total gasto do saldo
        if total_gastos > total_ganhos * 0.7:
            recomendacoes.append("Atenção: Seus gastos representam mais de 70% dos seus ganhos")
        
        if saldo < 0:
            recomendacoes.append("ALERTA: Saldo negativo - revise seus gastos urgentemente!")
        elif saldo < total_ganhos * 0.1:
            recomendacoes.append("Cuidado: Pouca margem de segurança financeira")
        else:
            recomendacoes.append("Ótimo! Suas finanças estão saudáveis")
        
        if 'analise_categorias' in dados_base:
            categoria_mais_gasta = dados_base['analise_categorias']['categoria_mais_gasta']
            if categoria_mais_gasta[1] > total_gastos * 0.4:
                recomendacoes.append(f"Considere reduzir gastos com '{categoria_mais_gasta[0]}'")
        
        # decorator: add novo campo 
        dados_base['recomendacoes'] = recomendacoes
        return dados_base
    
    def get_conteudo(self) -> str:
        # decorator: estende a descricao do relatorio
        return f"{super().get_conteudo()} - Com Recomendações"



def criar_transacoes_exemplo():
    return [
        {'descricao': 'Salário', 'valor': 3000.00, 'categoria': 'renda', 'data': '2024-01-15'},
        {'descricao': 'Freelance', 'valor': 800.00, 'categoria': 'renda', 'data': '2024-01-20'},
        {'descricao': 'Supermercado', 'valor': -350.00, 'categoria': 'alimentacao', 'data': '2024-01-16'},
        {'descricao': 'Restaurante', 'valor': -120.00, 'categoria': 'alimentacao', 'data': '2024-01-18'},
        {'descricao': 'Delivery', 'valor': -85.00, 'categoria': 'alimentacao', 'data': '2024-01-22'},
        {'descricao': 'Combustível', 'valor': -200.00, 'categoria': 'transporte', 'data': '2024-01-17'},
        {'descricao': 'Manutenção Carro', 'valor': -450.00, 'categoria': 'transporte', 'data': '2024-01-25'},
        {'descricao': 'Cinema', 'valor': -60.00, 'categoria': 'lazer', 'data': '2024-01-19'},
        {'descricao': 'Assinatura Streaming', 'valor': -45.00, 'categoria': 'lazer', 'data': '2024-01-20'},
        {'descricao': 'Aluguel', 'valor': -1200.00, 'categoria': 'moradia', 'data': '2024-01-05'},
        {'descricao': 'Conta de Luz', 'valor': -150.00, 'categoria': 'moradia', 'data': '2024-01-10'},
        {'descricao': 'Internet', 'valor': -90.00, 'categoria': 'moradia', 'data': '2024-01-12'},
    ]

def testar_relatorios():
    transacoes = criar_transacoes_exemplo()
    
    print("Teste do Sistema de Relatórios Financeiros")
    
    
    print("\n1. Relatório Básico")
    relatorio_base = RelatorioFinanceiroBase(transacoes)
    dados_base = relatorio_base.gerar()
    print(f"Total Gastos: R$ {dados_base['total_gastos']:.2f}")
    print(f"Total Ganhos: R$ {dados_base['total_ganhos']:.2f}")
    print(f"Saldo Final: R$ {dados_base['saldo_final']:.2f}")
    print(f"Transações: {dados_base['quantidade_transacoes']}")
    
    # decorator: aplicando um único decorator
    print("\n2. Relatório Detalhado")
    relatorio_detalhado = DecoratorDetalhado(RelatorioFinanceiroBase(transacoes))
    print(relatorio_detalhado.get_conteudo())
    dados_detalhados = relatorio_detalhado.gerar()
    
    print("Gastos por Categoria:")
    for categoria, valor in dados_detalhados['gastos_por_categoria'].items():
        print(f"  {categoria}: R$ {valor:.2f}")
    
    # decorator: aplicando múltiplos decorators em cascata
    print("\n3. Relatório Completo")
    relatorio_completo = DecoratorRecomendacoes(
        DecoratorAnaliseCategorias(
            DecoratorDetalhado(
                RelatorioFinanceiroBase(transacoes)  # nucleo básico
            )  # mais detalhes
        )  # + Análise
    )  # + Recomendações
    
    print(relatorio_completo.get_conteudo())
    dados_completos = relatorio_completo.gerar()
    
    print("Resumo Financeiro:")
    print(f"  Ganhos: R$ {dados_completos['total_ganhos']:.2f}")
    print(f"  Gastos: R$ {dados_completos['total_gastos']:.2f}")
    print(f"  Saldo:  R$ {dados_completos['saldo_final']:.2f}")
    
    print("Análise Detalhada:")
    if 'analise_categorias' in dados_completos:
        analise = dados_completos['analise_categorias']
        print(f"  Categoria mais gasta: {analise['categoria_mais_gasta'][0]} (R$ {analise['categoria_mais_gasta'][1]:.2f})")

if __name__ == "__main__":
    testar_relatorios()