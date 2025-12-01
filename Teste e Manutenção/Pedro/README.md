# 📋 Cenários de Teste

Este documento lista os cenários de teste executados para validação do sistema de controle financeiro.

#### **1. CT01 — Integridade dos Dados**

* **Objetivo:** Garantir que o sistema está registrando as informações das contas corretamente.
* **Responsável:** Pedro Miguel Lorin
* **Pré-condições:** Um usuário autenticado com receita de 10$ e despesa de 5$.

**Procedimento:**
1. Abrir o sistema
2. Adicionar uma nova conta.
3. Verificar se a nova conta tem algum dado salvo.

**Critérios de Aceitação:**
*Conta nova deve estar sem qualquer dado salvo.

**Resultado:** ❌ **Reprovado** (Esperado: Conta vazia)
> **Detalhe da Falha (Bug):** O sistema está criando as contas mas salvando seus dados em um arquivo geral que não está endereçando cada receita ou saldo para uma conta específica, o que está causando que todas as contas tenham os mesmos dados.

# Identificação e Correção de Bugs

## Pedro:
### Bug 1: Cenário de teste CT01 — Integridade dos Dados

Descrição: Ao criar uma nova conta e acessar o sistema, o usuário visualizava movimentações financeiras e metas de economia pertencentes a outros usuários. O sistema não estava isolando os dados, resultando em um compartilhamento indevido de informações entre todas as contas.

Arquivo: main_kivy.py

Classe: FinanceAppLogic

Métodos: registrar_movimentacao(), calcular_progresso_meta(), configurar_meta()

Problema: Os dados eram salvos em listas e variáveis globais sem associação com o id_conta do usuário logado.

➡️ Resultado: ❌ TESTE FALHOU (Reprovado)

#### Análise da Causa

O código anterior tratava o banco de dados como uma lista única para todos os usuários:
Movimentações: A função salvava apenas os dados da transação, sem identificar o dono:
Python
# Código incorreto (Antigo)
nova = {
    "descricao": descricao,
    "valor": valor,
    "tipo": tipo
    # Faltava o ID da conta aqui
}


##### Correção Implementada
A solução envolveu vincular cada dado ao ID do usuário e criar filtros na leitura.
1. Correção nas Movimentações:
Adicionamos o id_conta ao registrar e criamos um filtro para leitura:
Python
# No método registrar_movimentacao:
nova = {
    "id_conta": id_conta,  # <--- Vinculação adicionada
    "descricao": descricao,
    "valor": valor,
    # ...
}


# Novo método auxiliar criado para filtrar:
def get_transacoes_usuario(self, id_conta_atual):
    return [t for t in self.transacoes_registradas if t.get("id_conta") == id_conta_atual]


Com essas alterações, o CT01 agora é aprovado, pois cada conta nova inicia vazia e os dados de um usuário não aparecem para outro.






