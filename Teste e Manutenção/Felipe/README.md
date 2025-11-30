# 📋 Cenários de Teste

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


# Identificação e correção de Bugs

## Felipe:
### Bug 1: Cenário de teste 4

Descrição:
Quando o usuário tentava registrar uma despesa maior do que o saldo disponível, o backend retornava erro, porém a interface exibia a mensagem “Sucesso!”, causando inconsistência entre lógica e interface.

Arquivo: main.py

Classe: MovimentacaoScreen

Método: registrar()

Problema: o retorno de sucesso/erro do método registrar_movimentacao() não era verificado.

➡️ Resultado: TESTE FALHOU

#### Análise da Causa

A função da interface estava assim:

app.logic.registrar_movimentacao(...)
app.mostrar_alerta("Sucesso", ...)

Ou seja:

A lógica retornava False corretamente em caso de saldo insuficiente.

A interface ignorava o retorno.

O alerta de sucesso aparecia sempre.

Causa raiz: Ausência de verificação do retorno booleano do Facade.

#### Correção Implementada

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

#### Resultado Após Correção

Rodando o mesmo cenário novamente:

Registrar despesa de R$ 200,00 com saldo de R$ 150,00.

Resultado esperado: erro
Resultado obtido: erro (correto)

Logs:

[Facade] FALHA ao registrar 'uai': Saldo insuficiente.
Erro: Falha ao registrar movimentação! Verifique o saldo ou os dados.


➡️ Cenário 4 passou ✔


# Relatório de Testes Unitários

## Teste implementado por Felipe:
### Ambiente de Testes

Linguagem: Python 3.10+

Framework: unittest

Arquivos testados: Facade.py 

Executado por: python3 teste_financas.py

Sistema Operacional: Windows 11

### 2. Casos de Teste Implementados
ID	Descrição	Objetivo	Resultado
TU01	Registrar receita válida	Validar registro positivo	✔ Aprovado

TU02	Registrar receita com valor negativo	Impedir valores inválidos	✔ Aprovado

TU03	Registrar despesa com saldo suficiente	Validar desconto	✔ Aprovado

TU04	Registrar despesa com saldo insuficiente	Impedir operação	✔ Aprovado

TU05	Verificar histórico de receitas	Validar filtragem correta	✔ Aprovado


### Resultado Global da Execução

Comando:

python3 teste_financas.py

Saída:

Ran 5 tests in 0.012s

OK


Conclusão: Todos os testes passaram com sucesso.

### Análise dos Resultados

Os testes confirmaram que:

A regra de saldo insuficiente está funcionando.

O sistema impede valores inválidos (receitas negativas).

O histórico está corretamente filtrado por tipo.

A arquitetura em camadas (Facade + Services) está funcionando conforme o esperado.

O comportamento do backend está consistente com os cenários de teste manuais (CT01–CT04).

Nenhuma falha ou exceção foi encontrada durante a execução dos testes.

### Conclusão

O módulo financeiro atende aos requisitos funcionais validados pelos testes unitários.
Após correções realizadas na interface, a aplicação encontra-se consistente e estável para uso.


# ✨ Documentação da Funcionalidade de Meta de Economia

Esta seção detalha a implementação e a arquitetura da nova funcionalidade de Metas de Economia no aplicativo.

## Funcionalidade adicionada por Felipe

#### Salvamento de Meta no Arquivo JSON**

Foi implementado um mecanismo para persistir o valor da meta de economia, garantindo que o dado não seja perdido ao fechar o aplicativo.

* O valor da meta é salvo no arquivo `meta.json` sempre que o usuário a define ou altera.


#### Carregamento Automático da Meta ao Iniciar o Aplicativo

Ao iniciar o app, a classe FinanceAppLogic agora carrega automaticamente o valor da meta anteriormente salva, permitindo que a meta seja persistida mesmo após o fechamento do aplicativo.

Trecho Responsável:Pythonself.meta_economia = 0.0

self._carregar_meta()

#### Cálculo Completo da Meta e Progresso

A funcionalidade foi expandida para calcular o progresso da meta. 

Essa lógica está encapsulada no método calcular_progresso_meta().

Cálculos Realizados: Total de receitas, Total de despesas, Saldo acumulado e Percentual de progresso em relação à meta definida.

#### Tela de Meta (MetaScreen)

#### Criação da Classe MetaScreen

Uma nova tela dedicada (MetaScreen) foi adicionada. 

Ela exibe a Meta atual, Ganhos, Gastos, Valor economizado e Porcentagem de progresso, sendo atualizada automaticamente via on_pre_enter.

Lógica de Atualização da Tela (on_pre_enter):Pythonclass MetaScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        dados = app.logic.calcular_progresso_meta()

        texto = (
            f"Meta atual: R$ {dados['meta']:.2f}\n"
            f"Total Ganhos: R$ {dados['total_receitas']:.2f}\n"
            f"Total Gastos: R$ {dados['total_despesas']:.2f}\n"
            f"Economizado: R$ {dados['saldo']:.2f}\n"
            f"Progresso: {dados['progresso']:.1f}%"
        )

        self.ids.texto_progresso.text = texto

        
#### Registro da Tela no BuildA tela foi registrada no gerenciador de telas e o arquivo KV correspondente foi carregado:Pythonsm.add_widget(Factory.MetaScreen())

Builder.load_file("ui/meta.kv")

#### Atualização Visual da Tela Após Configurar a MetaO método salvar_meta garante o salvamento (meta.json) e o recarregamento imediato dos dados da tela para feedback visual.

