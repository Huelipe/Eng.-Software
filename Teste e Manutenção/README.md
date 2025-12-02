# Organização de pastas:

As pastas estão organizadas de modo a dividir exatamente o que cada um fez

Ao fim desse README.md tem a documentação reunida, mas como cada um fez um pouco diferente, é recomendável ver o README.md de cada um.

## Codigo
Contém todo o código final, com todas as funcionalidades antigas, correções de bugs, testes, refatoração, revisão e novas funcionalidades

## Felipe
#### Codigo
Contém o código da parte 2 com as modificações e implementações que o Felipe fez
#### teste_felipe_financas.py
Contém o teste feito pelo Felipe para a parte de financas
#### README.md 
Contém toda a documentação escrita pelo Felipe

## Giovanna
#### Codigo
Contém o código da parte 2 com as modificações e implementações que a Giovanna fez
#### ...
#### teste_giovanna_listagem.py
#### ...
#### README.md 
## 🚀 Novas Funcionalidades (v1.1)

### 📄 Exportação de Extrato (.csv)
Foi implementada a funcionalidade de exportar todo o histórico financeiro para um arquivo `.csv`. Isso permite que o usuário analise seus gastos externamente em ferramentas como Excel ou Google Sheets.




## Pedro
#### Codigo
Contém o código da parte 2 com as modificações e implementações que o Pedro fez
#### ...
#### ...
#### ...
#### README.md 
Contém toda a documentação escrita pelo Pedro

# Junção da documentação:
# 📋 Relatório Consolidado de Testes e Implementações

Este documento consolida os cenários de teste manuais, a identificação e correção de bugs, os relatórios de testes unitários e a documentação das novas funcionalidades implementadas no sistema de controle financeiro.

---

## 📊 Sumário Executivo

| ID | Objetivo | Responsável | Resultado | Observações |
| :--- | :--- | :--- | :--- | :--- |
| CT01 | Registrar Receita (Válido). | Felipe Ferrer | **Aprovado** (✔) | |
| CT02 | Rejeitar Receita (Inválido). | Felipe Ferrer | **Aprovado** (✔) | |
| CT03 | Registrar Despesa (Saldo Suficiente). | Felipe Ferrer | **Aprovado** (✔) | |
| CT04 | Bloquear Despesa (Saldo Insuficiente). | Felipe Ferrer | **Falhou** (❌) -> **Aprovado** (✔) | Corrigido bug de *feedback* da UI. |
| CT05 | Integridade dos Dados entre contas. | Pedro Miguel Lorin | **Reprovado** (❌) -> **Aprovado** (✔) | Corrigido compartilhamento indevido de dados. |
| Filtros | Separação de Receitas e Despesas. | Giovanna | **Aprovado** (✔) | Corrigido bug de mistura de listas. |

---

# 📝 Detalhes dos Cenários de Teste Manual (CTs)

## 🧑‍💻 Felipe Ferrer

### **1. CT01 — Registrar Receita com Valor Válido**
* **Objetivo:** Garantir que o sistema registre uma receita válida e atualize o saldo.
* **Pré-condições:** Usuário autenticado e saldo inicial = R$ 0,00.
* **Entrada:**
    | Campo | Entrada |
    | :--- | :--- |
    | Tipo | Receita |
    | Valor | 100 |
    | Descrição | "Salário" |
* **Procedimento:** Acessar menu, Selecionar Adicionar Receita, Informar valor **100** e descrição **"Salário"**, Confirmar.
* **Resultado:** **Aprovado** (✔).

### **2. CT02 — Registrar Receita com Valor Inválido**
* **Objetivo:** Garantir que o sistema rejeite valores inválidos (negativos).
* **Entrada:**
    | Campo | Entrada |
    | :--- | :--- |
    | Tipo | Receita |
    | Valor | -50 |
* **Procedimento:** Selecionar Adicionar Receita, Digitar valor inválido **-50**, Confirmar.
* **Resultado:** **Aprovado** (✔).

### **3. CT03 — Registrar Despesa com Saldo Suficiente**
* **Objetivo:** Validar o registro de despesa quando há saldo suficiente.
* **Pré-condições:** Saldo $\ge$ R$ 100,00$.
* **Entrada:**
    | Campo | Entrada |
    | :--- | :--- |
    | Tipo | Despesa |
    | Valor | 50 |
* **Resultado:** **Aprovado** (✔).

### **4. CT04 — Registrar Despesa com Saldo Insuficiente**
* **Objetivo:** Garantir o bloqueio ao registrar uma despesa maior que o saldo atual.
* **Pré-condições:** Saldo $<$ R$ 200,00$.
* **Entrada:**
    | Campo | Entrada |
    | :--- | :--- |
    | Tipo | Despesa |
    | Valor | 200 |
* **Resultado Inicial:** **Falhou** (❌).
> **Detalhe da Falha (Bug):** A lógica bloqueou a operação, mas a **Interface exibiu a mensagem de “Sucesso”**.

## 🔒 Pedro Miguel Lorin

### **5. CT05 — Integridade dos Dados (Isolamento de Contas)**
* **Objetivo:** Garantir que as informações das contas sejam registradas e isoladas corretamente.
* **Pré-condições:** Um usuário autenticado com receita de R$ 10,00 e despesa de R$ 5,00.
* **Procedimento:** Adicionar nova conta e verificar se esta conta está vazia.
* **Critérios de Aceitação:** Conta nova deve estar sem qualquer dado salvo.
* **Resultado Inicial:** **Reprovado** (❌).
> **Detalhe da Falha (Bug):** O sistema estava salvando dados em um arquivo geral, causando o **compartilhamento indevido** entre todas as contas.

## 🎨 Giovanna

### **Testes de Filtro (Listagem e Histórico)**
* **Teste 1: Só Receitas:** Adicionado Salário (R$ 100) e Lanche (R$ 50). Verificado se **somente o Salário** aparecia na tela de Receitas. **Resultado:** ✔ Funcionou.
* **Teste 2: Só Despesas:** Usado os mesmos dados. Verificado se **somente o Lanche** aparecia na tela de Despesas. **Resultado:** ✔ Funcionou.

---

# 🐛 Identificação e Correção de Bugs

## 🧑‍💻 Felipe Ferrer

### Bug 1: Cenário de teste 4 (Inconsistência UI/Lógica)

* **Descrição:** Interface exibia "Sucesso!" com saldo insuficiente.
* **Causa Raiz:** O método `registrar()` (`MovimentacaoScreen`) ignorava o retorno da função `registrar_movimentacao()`.
* **Correção Implementada:** Foi adicionada a verificação do retorno booleano:
python
# Correção:
resultado = app.logic.registrar_movimentacao(...)
if resultado:
    app.mostrar_alerta("Sucesso", ...)
else:
    app.mostrar_alerta("Erro", "Falha ao registrar movimentação! Verifique o saldo ou os dados.")
* **Resultado Pós-Correção:** Cenário 4 passou (✔).

## 🔒 Pedro Miguel Lorin

### Bug 1: Cenário de teste CT05 — Falha na Integridade dos Dados

* **Descrição:** Dados como movimentações e metas estavam sendo compartilhados entre usuários.
* **Causa Raiz:** Os dados eram salvos em listas e variáveis globais sem associação com o `id_conta` do usuário.
* **Correção Implementada:**
    1.  **Registro:** O dicionário da transação recebeu o `"id_conta"` como campo obrigatório.
    2.  **Leitura:** Criado um método auxiliar `get_transacoes_usuario(self, id_conta_atual)` para filtrar a lista de transações por ID da conta.

## 🎨 Giovanna

### Bug: Mistura de Tipos na Lista de Histórico

* **Descrição:** Telas de Receitas mostravam Despesas e vice-versa.
* **Causa Raiz:** As funções `get_historico_receitas` e `get_historico_despesas` no `Facade.py` estavam retornando a lista completa `self.transacoes` sem aplicar o filtro.
* **Correção:** Alteração do código no `Facade.py` para **filtrar estritamente** as transações pelo campo `tipo` (Receita ou Despesa) antes de retornar à UI.

---

# 🧪 Relatórios de Testes Automatizados

## 🧑‍💻 Felipe Ferrer (Testes Unitários - `Facade.py`)

* **Ambiente:** Python 3.10+, Framework `unittest`.
* **Arquivos Testados:** `Facade.py`.
* **Resultado Global:** `Ran 5 tests in 0.012s OK`.

| ID | Descrição | Objetivo | Resultado |
| :--- | :--- | :--- | :--- |
| TU01 | Registrar receita válida | Validar registro positivo | ✔ Aprovado |
| TU04 | Registrar despesa com saldo insuficiente | Impedir operação | ✔ Aprovado |

## 🎨 Giovanna (Testes de Listagem - `teste_listagem.py`)

* **O que o script testa:** Listas vazias, filtros (separação Receitas/Despesas) e integridade dos dados.
* **Saída:** `Ran 4 tests in 0.004s OK`.
* **Conclusão:** Todos os testes de filtragem e consistência foram aprovados.

---

# 📄 DOCUMENTO TDD — Ajuste da Tela de Metas

## 🧑‍💻 Felipe Ferrer

* **Comportamento Incorreto:** A meta não era carregada automaticamente; Erro `AttributeError: ...salvar_meta` ao tentar atualizar.
* **Causa Identificada:** Havia **duas classes `MetaScreen`** definidas no `main_kivy.py`, gerando conflito de referência.
* **Correções Aplicadas (GREEN):**
    1.  **Remoção de Duplicação:** Mantida apenas uma definição de `MetaScreen`.
    2.  **Lógica de Carregamento:** Centralizada no evento `on_pre_enter`.
    3.  **Acessibilidade:** Ajuste do método `salvar_meta` na classe principal para ser encontrado pelo *Binding* do KV e atualizar a tela imediatamente.
* **Resultado:** Testes de carregamento e salvamento passaram (✔), validando a correção.

---

# ✨ Documentação das Funcionalidades Implementadas

## 🧑‍💻 Felipe Ferrer: Funcionalidade de Meta de Economia

* **Persistência:** O valor da meta é salvo no arquivo `meta.json`.
* **Carregamento Automático:** `self._carregar_meta()` é chamado na inicialização da `FinanceAppLogic`.
* **Cálculo de Progresso:** O método `calcular_progresso_meta()` calcula Ganhos, Gastos, Saldo e o **Percentual de Progresso** para exibir na tela.
* **Interface:** Criação da **`MetaScreen`**, que se atualiza via `on_pre_enter`.

## 🔒 Pedro Miguel Lorin: Funcionalidade de Recuperação de Senha

* **Persistência de Segurança:** A estrutura da `Conta` (no `Facade.py`) foi atualizada para armazenar a `pergunta_seguranca` e a `resposta_seguranca_hash`.
* **Segurança:** A resposta é **hasheada (criptografada com SHA-256)**, nunca salva em texto puro.
* **Fluxo de Cadastro:** O sistema agora exige Pergunta e Resposta de Segurança no `CadastroScreen`.
* **Tela de Recuperação (`RecuperarScreen`):** Gerencia a busca da pergunta e o **reset da senha** após validação correta do hash da resposta.
* **Integração UI:** As telas `CadastroScreen` e `RecuperarScreen` foram registradas no *ScreenManager* do Kivy.

## 🎨 Giovanna: Separação Visual do Histórico

* **Separação de Listas (Backend):** Lógica ajustada no Facade para diferenciar rigorosamente Receita de Despesa.
* **Telas Dedicadas (Frontend):** Criação das **`ReceitasScreen`** e **`DespesasScreen`** separadas, cada uma com gráficos e listas específicas.
* **Tratamento de Erro:** Adicionada mensagem "Nenhuma despesa registrada" para evitar telas em branco.




