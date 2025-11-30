CT01 — Registrar Receita com Valor Válido

Responsável: Felipe Ferrer
Objetivo: Garantir que o sistema registre uma receita válida e atualize o saldo.
Pré-condições: Usuário autenticado e saldo inicial = R$ 0,00.

Entradas

Tipo: Receita

Valor: 100

Descrição: "Salário"

Procedimento

Acessar o menu principal.

Selecionar Adicionar Receita.

Informar valor 100.

Informar descrição "Salário".

Confirmar.

Critérios de Aceitação

Receita salva.

Saldo atualizado corretamente.

Registro aparece no histórico.

Resultado

Esperado: Receita registrada corretamente.

Obtido: ✔ Aprovado

❗ CT02 — Registrar Receita com Valor Inválido

Responsável: Felipe Ferrer
Objetivo: Garantir que o sistema rejeite valores inválidos.
Pré-condições: Usuário autenticado.

Entradas

Tipo: Receita

Valor: -50

Procedimento

Selecionar Adicionar Receita.

Digitar valor inválido -50.

Confirmar.

Critérios de Aceitação

Mensagem de erro exibida.

Nada salvo no sistema.

Resultado

Esperado: Registro rejeitado.

Obtido: ✔ Aprovado

✅ CT03 — Registrar Despesa com Saldo Suficiente

Responsável: Felipe Ferrer
Objetivo: Validar o registro de despesa com saldo suficiente.
Pré-condições: Saldo ≥ 100.

Entradas

Tipo: Despesa

Valor: 50

Procedimento

Selecionar Adicionar Despesa.

Digitar valor 50.

Confirmar.

Critérios de Aceitação

Despesa registrada.

Saldo atualizado corretamente.

Resultado

Esperado: Despesa registrada com sucesso.

Obtido: ✔ Aprovado

❌ CT04 — Registrar Despesa com Saldo Insuficiente

Responsável: Felipe Ferrer
Objetivo: Garantir bloqueio ao registrar uma despesa maior que o saldo.
Pré-condições: Saldo < 200.

Entradas

Tipo: Despesa

Valor: 200

Procedimento

Selecionar Adicionar Despesa.

Informar valor maior que o saldo.

Confirmar.

Critérios de Aceitação

Sistema exibe erro.

Nada é salvo.

Resultado

Esperado: Operação bloqueada.

Obtido: ❌ Falhou

Terminal exibiu o erro corretamente.

Interface exibiu mensagem de “Sucesso” (bug detectado).


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
