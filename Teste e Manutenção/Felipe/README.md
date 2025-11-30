## 📋 Cenários de Teste

Este documento lista os cenários de teste executados para validação do sistema de controle financeiro.

---

### **Sumário Executivo**

| ID | Objetivo | Responsável | Resultado | Observações |
| :--- | :--- | :--- | :--- | :--- |
| CT01 | Registrar Receita com Valor Válido e atualizar saldo. | Felipe Ferrer | **Aprovado** (✔) | |
| CT02 | Rejeitar Receita com Valor Inválido (Negativo). | Felipe Ferrer | **Aprovado** (✔) | |
| CT03 | Registrar Despesa com Saldo Suficiente. | Felipe Ferrer | **Aprovado** (✔) | |
| CT04 | Bloquear Despesa com Saldo Insuficiente. | Felipe Ferrer | **Falhou** (❌) | Bug de interface detectado. |

---

### **Detalhes dos Cenários de Teste**

#### **1. CT01 — Registrar Receita com Valor Válido**

* **Objetivo:** Garantir que o sistema registre uma receita válida e atualize o saldo.
* **Responsável:** Felipe Ferrer
* **Pré-condições:** Usuário autenticado e saldo inicial = R$ 0,00.

| Campo | Entrada |
| :--- | :--- |
| Tipo | Receita |
| Valor | 100 |
| Descrição | "Salário" |

**Procedimento:**
1. Acessar o menu principal.
2. Selecionar Adicionar Receita.
3. Informar valor **100**.
4. Informar descrição **"Salário"**.
5. Confirmar.

**Critérios de Aceitação:**
* Receita salva.
* Saldo atualizado corretamente.
* Registro aparece no histórico.

**Resultado:** ✔ **Aprovado** (Esperado: Receita registrada corretamente.)

---

#### **2. CT02 — Registrar Receita com Valor Inválido**

* **Objetivo:** Garantir que o sistema rejeite valores inválidos (negativos).
* **Responsável:** Felipe Ferrer
* **Pré-condições:** Usuário autenticado.

| Campo | Entrada |
| :--- | :--- |
| Tipo | Receita |
| Valor | -50 |

**Procedimento:**
1. Selecionar Adicionar Receita.
2. Digitar valor inválido **-50**.
3. Confirmar.

**Critérios de Aceitação:**
* Mensagem de erro exibida.
* Nada salvo no sistema.

**Resultado:** ✔ **Aprovado** (Esperado: Registro rejeitado.)

---

#### **3. CT03 — Registrar Despesa com Saldo Suficiente**

* **Objetivo:** Validar o registro de despesa quando há saldo suficiente.
* **Responsável:** Felipe Ferrer
* **Pré-condições:** Saldo $\ge$ R$ 100,00$.

| Campo | Entrada |
| :--- | :--- |
| Tipo | Despesa |
| Valor | 50 |

**Procedimento:**
1. Selecionar Adicionar Despesa.
2. Digitar valor **50**.
3. Confirmar.

**Critérios de Aceitação:**
* Despesa registrada.
* Saldo atualizado corretamente.

**Resultado:** ✔ **Aprovado** (Esperado: Despesa registrada com sucesso.)

---

#### **4. CT04 — Registrar Despesa com Saldo Insuficiente**

* **Objetivo:** Garantir o bloqueio ao registrar uma despesa maior que o saldo atual.
* **Responsável:** Felipe Ferrer
* **Pré-condições:** Saldo $\lt$ R$ 200,00$.

| Campo | Entrada |
| :--- | :--- |
| Tipo | Despesa |
| Valor | 200 |

**Procedimento:**
1. Selecionar Adicionar Despesa.
2. Informar valor maior que o saldo.
3. Confirmar.

**Critérios de Aceitação:**
* Sistema exibe erro.
* Nada é salvo.

**Resultado:** ❌ **Falhou** (Esperado: Operação bloqueada.)

> **Detalhe da Falha (Bug):** O terminal exibiu o erro corretamente, mas a **Interface exibiu a mensagem de “Sucesso”** ao invés de uma mensagem de erro, indicando um problema de *feedback* para o usuário.


% ------------------------------------------------------------------------------
## 1. Identificação do Bug

Nome: Feedback incorreto ao registrar despesas maiores que o saldo
Descrição:
Quando o usuário tentava registrar uma despesa maior do que o saldo disponível, o backend retornava erro, porém a interface exibia a mensagem “Sucesso!”, causando inconsistência entre lógica e interface.

## 2. Onde o Bug foi Encontrado

Arquivo: main.py

Classe: MovimentacaoScreen

Método: registrar()

Problema: o retorno de sucesso/erro do método registrar_movimentacao() não era verificado.

## 3. Cenário de Teste que Detectou o Problema

Cenário 4 – Registrar despesa maior que o saldo disponível

Item	Valor
Saldo inicial	R$ 150,00
Tipo	despesa
Valor inserido	200.00
Resultado esperado	Mensagem de ERRO
Resultado obtido (antes)	Mensagem de SUCESSO

➡️ Resultado: TESTE FALHOU

## 4. Análise da Causa

A função da interface estava assim:

app.logic.registrar_movimentacao(...)
app.mostrar_alerta("Sucesso", ...)


Ou seja:

A lógica retornava False corretamente em caso de saldo insuficiente.

A interface ignorava o retorno.

O alerta de sucesso aparecia sempre.

Causa raiz: Ausência de verificação do retorno booleano do Facade.

## 5. Correção Implementada

A solução foi verificar o retorno (True ou False) da operação:

resultado = app.logic.registrar_movimentacao(
    app.conta_atual.id_conta,
    self.tipo,
    valor,
    descricao,
    categoria
)

if resultado:
    app.mostrar_alerta("Sucesso", f"{self.tipo.capitalize()} registrada com sucesso!")
    self.ids.valor.text = ""
    self.ids.descricao.text = ""
    self.ids.categoria.text = "Selecione uma categoria"
else:
    app.mostrar_alerta("Erro", "Falha ao registrar movimentação! Verifique o saldo ou os dados.")

## 6. Resultado Após Correção

Rodando o mesmo cenário novamente:

Registrar despesa de R$ 200,00 com saldo de R$ 150,00.

Resultado esperado: erro
Resultado obtido: erro (correto)

Logs:

[Facade] FALHA ao registrar 'uai': Saldo insuficiente.
Erro: Falha ao registrar movimentação! Verifique o saldo ou os dados.


➡️ Cenário 4 passou ✔
