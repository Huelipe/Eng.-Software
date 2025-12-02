# 📋 Relatório de Cenários de Teste, Bugs e Implementações

Este documento consolida os cenários de teste manuais, a identificação e correção de bugs, os relatórios de testes unitários e a documentação das novas funcionalidades implementadas no sistema de controle financeiro.

---

## 📊 Sumário Executivo

| ID | Objetivo | Responsável | Resultado | Observações |
| :--- | :--- | :--- | :--- | :--- |
| CT01 | Registrar Receita com Valor Válido. | Felipe Ferrer | **Aprovado** (✔) | |
| CT02 | Rejeitar Receita com Valor Inválido. | Felipe Ferrer | **Aprovado** (✔) | |
| CT03 | Registrar Despesa com Saldo Suficiente. | Felipe Ferrer | **Aprovado** (✔) | |
| CT04 | Bloquear Despesa com Saldo Insuficiente. | Felipe Ferrer | **Falhou** (❌) | Bug de *feedback* da interface corrigido. |
| CT05 | Integridade dos Dados entre contas. | Pedro Miguel Lorin | **Reprovado** (❌) | Dados estavam sendo compartilhados entre usuários. |
| Filtros | Separação correta de Receitas e Despesas. | Giovanna | **Aprovado** (✔) | Corrigido bug de mistura de listas. |

---

# 📝 Detalhes dos Cenários de Teste Manual (CTs)

## 🧑‍💻 Cenários de Teste (Felipe Ferrer)

### **1. CT01 — Registrar Receita com Valor Válido**
* **Objetivo:** Garantir que o sistema registre uma receita válida e atualize o saldo.
* **Pré-condições:** Usuário autenticado e saldo inicial = R$ 0,00.
* **Entrada:** Tipo: Receita, Valor: 100, Descrição: "Salário".
* **Critérios de Aceitação:** Receita salva, saldo atualizado, registro aparece no histórico.
* **Resultado:** **Aprovado** (✔)

### **2. CT02 — Registrar Receita com Valor Inválido**
* **Objetivo:** Garantir que o sistema rejeite valores inválidos (negativos).
* **Entrada:** Tipo: Receita, Valor: -50.
* **Critérios de Aceitação:** Mensagem de erro exibida. Nada salvo no sistema.
* **Resultado:** **Aprovado** (✔)

### **3. CT03 — Registrar Despesa com Saldo Suficiente**
* **Objetivo:** Validar o registro de despesa quando há saldo suficiente.
* **Pré-condições:** Saldo $\ge$ R$ 100,00$.
* **Entrada:** Tipo: Despesa, Valor: 50.
* **Critérios de Aceitação:** Despesa registrada, saldo atualizado corretamente.
* **Resultado:** **Aprovado** (✔)

### **4. CT04 — Registrar Despesa com Saldo Insuficiente**
* **Objetivo:** Garantir o bloqueio ao registrar uma despesa maior que o saldo atual.
* **Entrada:** Tipo: Despesa, Valor: 200 (com Saldo $<$ R$ 200,00$).
* **Resultado:** **Falhou** (❌)
> **Detalhe da Falha (Bug):** O *backend* bloqueou, mas a **Interface exibiu "Sucesso"**, indicando problema de *feedback*.

## 🔒 Cenário de Teste (Pedro Miguel Lorin)

### **5. CT05 — Integridade dos Dados (Isolamento de Contas)**
* **Objetivo:** Garantir que as informações financeiras sejam isoladas por conta.
* **Procedimento:** Adicionar nova conta após um usuário já ter movimentações. Verificar se a nova conta está vazia.
* **Critérios de Aceitação:** Conta nova deve estar sem qualquer dado salvo.
* **Resultado:** **Reprovado** (❌)
> **Detalhe da Falha (Bug):** Dados eram salvos em um arquivo geral, fazendo com que todas as contas tivessem as mesmas movimentações e metas.

---

# 🐛 Identificação e Correção de Bugs

## 🧑‍💻 Felipe Ferrer

### Bug 1: Cenário de teste 4 (Inconsistência de Interface)

* **Descrição:** Falha no *feedback* visual (UI) para o usuário quando o *backend* (lógica) rejeitava uma despesa por saldo insuficiente.
* **Causa Raiz:** Ausência de verificação do retorno do método `registrar_movimentacao()` na classe `MovimentacaoScreen`.
python
# Análise da Causa (Código Incorreto)
app.logic.registrar_movimentacao(...)
app.mostrar_alerta("Sucesso", ...) # Exibia o sucesso sempre
* **Correção Implementada:** Adicionada a verificação booleana do retorno para exibir o alerta apropriado ("Sucesso" ou "Erro").
python
# Correção Implementada
resultado = app.logic.registrar_movimentacao(...) 
if resultado:
    app.mostrar_alerta("Sucesso", ...)
else:
    app.mostrar_alerta("Erro", "Falha ao registrar movimentação! Verifique o saldo ou os dados.")
* **Resultado Pós-Correção:** Cenário 4 passou (✔). Logs: `[Facade] FALHA ao registrar: Saldo insuficiente.`

## 🔒 Pedro Miguel Lorin

### Bug 1: Cenário de teste CT05 — Integridade dos Dados

* **Descrição:** Compartilhamento indevido de movimentações e metas entre diferentes contas de usuário.
* **Causa Raiz:** Os dados eram salvos em estruturas globais sem vinculação ao `id_conta`.
* **Correção Implementada:**
    1.  **Registro:** Adição do campo `"id_conta"` ao registrar cada nova movimentação.
    2.  **Leitura:** Criação do método auxiliar `get_transacoes_usuario(self, id_conta_atual)` para filtrar todas as transações apenas pelo ID da conta logada.
* **Resultado Pós-Correção:** CT05 agora é aprovado, garantindo o isolamento dos dados.

## 🎨 Giovanna

### Bug: Mistura de Tipos na Lista de Histórico

* **Descrição:** As telas de histórico (Receitas e Despesas) mostravam transações do tipo oposto (ex: Despesas na tela de Receitas).
* **Causa Raiz:** As funções `get_historico_receitas` e `get_historico_despesas` no `Facade.py` estavam retornando a lista de transações completa (`self.transacoes`) sem aplicar o filtro.
* **Correção:** Modificação das funções no Facade para aplicar o filtro por `tipo` antes de entregar os dados para a interface.

---

# 🧪 Relatórios de Testes Automatizados

## 🧑‍💻 Felipe Ferrer (Testes Unitários - `Facade.py`)

* **Ambiente:** Python 3.10+, `unittest`.
* **Comando:** `python3 teste_financas.py`
* **Saída:** `Ran 5 tests in 0.012s OK`

| ID | Descrição | Objetivo | Resultado |
| :--- | :--- | :--- | :--- |
| TU04 | Registrar despesa com saldo insuficiente | Impedir operação | ✔ Aprovado |
| TU05 | Verificar histórico de receitas | Validar filtragem correta | ✔ Aprovado |

**Conclusão:** O *backend* atende a todos os requisitos funcionais validados.

## 🎨 Giovanna (Testes de Listagem - `teste_listagem.py`)

* **Objetivos:** Validar filtros (separação de Receitas/Despesas), e integridade de dados/listas vazias.
* **Saída:** `Ran 4 tests in 0.004s OK`
* **Conclusão:** A correção do filtro foi validada com sucesso, garantindo que as listas de histórico exibam apenas o tipo de transação esperado.

---

# ✨ Documentação das Funcionalidades Adicionadas

## 🧑‍💻 Felipe Ferrer: Funcionalidade de Meta de Economia

* **Persistência:** O valor da meta é persistido no arquivo `meta.json`.
* **Carregamento:** Implementado o `self._carregar_meta()` para carregar a meta automaticamente na inicialização.
* **Cálculo:** O método `calcular_progresso_meta()` calcula **Total Ganhos, Total Gastos, Saldo, e o Percentual de Progresso** em relação à meta.
* **Interface:** Criação da **`MetaScreen`**, com atualização garantida pelo evento `on_pre_enter`.
* **Ajuste TDD:** Após falha inicial, o TDD garantiu a unicidade da classe `MetaScreen` e a correta acessibilidade do método `salvar_meta`.

## 🔒 Pedro Miguel Lorin: Funcionalidade de Recuperação de Senha

* **Segurança:** Adicionada a persistência da `pergunta_seguranca` e `resposta_seguranca_hash` (criptografada com SHA-256) na estrutura da conta.
* **Cadastro:** O novo fluxo exige Pergunta e Resposta de Segurança.
* **Fluxo de Reset:** A **`RecuperarScreen`** gerencia o fluxo de redefinição de senha em duas etapas: buscar a pergunta e validar o hash da resposta para permitir a alteração da senha.
* **Integração:** `FinanceAppLogic` expõe os métodos `buscar_pergunta(username)` e `resetar_senha(...)`.

## 🎨 Giovanna: Telas Separadas de Histórico

* **Separação Lógica:** Implementação de filtros no *backend* para diferenciar o que é Receita e o que é Despesa.
* **Interface:** Criação de duas telas dedicadas (`ReceitasScreen` e `DespesasScreen`).
* **Usabilidade:** Adição de *feedback* visual para listas vazias (ex: "Nenhuma despesa registrada").
