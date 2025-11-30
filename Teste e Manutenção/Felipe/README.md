CT01 — Registrar Receita com Valor Válido

Responsável: Felipe Ferrer
Objetivo: Garantir que o sistema registre uma receita válida e atualize o saldo.
Pré-condições: Usuário autenticado e conta com saldo inicial igual a R$ 0,00.

Entradas:

Tipo: Receita

Valor: 100

Descrição: "Salário"

Procedimento:

Acessar o menu principal.

Selecionar Adicionar Receita.

Informar valor 100.

Informar descrição.

Confirmar.

Critérios de Aceitação:

Receita salva.

Saldo atualizado.

Registro aparece no histórico.

Resultado Esperado: Receita registrada corretamente.
Resultado Obtido: aprovado

CT02 — Registrar Receita com Valor Inválido

Responsável: Felipe Ferrer
Objetivo: Garantir que valores inválidos não sejam aceitos.
Pré-condições: Usuário autenticado.

Entradas:

Tipo: Receita

Valor: -50

Procedimento:

Selecionar Adicionar Receita.

Digitar valor inválido -50.

Confirmar.

Critérios de Aceitação:

Mensagem de erro exibida.

Nada salvo no sistema.

Resultado Esperado: Registro rejeitado.
Resultado Obtido: aprovado

CT03 — Registrar Despesa com Saldo Suficiente

Responsável: Felipe Ferrer
Objetivo: Validar registro de despesa com saldo suficiente.
Pré-condições: Saldo ≥ 100.

Entradas:

Tipo: Despesa

Valor: 50

Procedimento:

Selecionar Adicionar Despesa.

Digitar valor 50.

Confirmar.

Critérios de Aceitação:

Despesa salva.

Saldo reduzido corretamente.

Resultado Esperado: Despesa registrada.
Resultado Obtido: aprovado

CT04 — Registrar Despesa com Saldo Insuficiente

Responsável: Felipe Ferrer
Objetivo: Garantir bloqueio de despesa maior que o saldo.
Pré-condições: Saldo < 200.

Entradas:

Tipo: Despesa

Valor: 200

Procedimento:

Selecionar Adicionar Despesa.

Informar valor maior que o saldo.

Confirmar.

Critérios de Aceitação:

Sistema exibe erro.

Nada é salvo.

Resultado Esperado: Operação bloqueada.
Resultado Obtido: sistema não aceitou, exibiu o alerta no terminal mas na interface exibiu como "Sucesso". Teste falhou.


Todas as despesas são exibidas.

Total correto apresentado.

Resultado Esperado: Histórico exibido corretamente.
Resultado Obtido: preencher após teste
