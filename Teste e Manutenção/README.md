# Organização de pastas:

As pastas estão organizadas de modo a dividir exatamente o que cada um fez

Esse README.md tem toda a documentação reunida. Mas como cada um fez um pouco diferente, é recomendável ver o README.md de cada um para mais detalhes.

## Final
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

# 📘 README — Documentação Consolidada do Projeto

Este documento serve como a documentação consolidada do projeto de controle financeiro, abrangendo cenários de teste, correção de bugs, relatórios de testes unitários e detalhes das funcionalidades implementadas.

---

# 1. 📝 Cenários de Teste Manual (CTs)

## 🧑‍💻 Felipe Ferrer (Movimentação)

| ID | Objetivo | Resultado |
| :--- | :--- | :--- |
| CT01 | Validar registro e atualização do saldo (Receita Válida). | ✔ Aprovado |
| CT02 | Impedir valores negativos (Receita Inválido). | ✔ Aprovado |
| CT03 | Validar desconto do saldo (Despesa Suficiente). | ✔ Aprovado |
| CT04 | Bloquear Despesa (Saldo Insuficiente). | ❌ Falhou (Corrigido posteriormente) |

## 🎨 Giovanna (Histórico e Listagem)

| ID | Objetivo | Resultado |
| :--- | :--- | :--- |
| CTG01 | Verificar comportamento do Histórico vazio. | ✔ Aprovado |
| CTG02 | Filtrar somente Receitas visíveis na tela correta. | ✔ Aprovado |
| CTG03 | Filtrar somente Despesas visíveis na tela correta. | ✔ Aprovado |
| CTG04 | Conferência de dados (valor e data) para garantir consistência. | ✔ Aprovado |

## 🔒 Pedro Miguel Lorin (Contas)

| ID | Objetivo | Pré-condição | Resultado |
| :--- | :--- | :--- | :--- |
| CTP01 | Garantir que nova conta inicie vazia (Integridade dos Dados). | Sistema armazena dados globalmente. | ❌ Reprovado (Corrigido depois) |

---

# 2. 🐛 Identificação e Correção de Bugs

## 🧑‍💻 Felipe Ferrer

### Bug — Cenário CT04 (Inconsistência UI/Lógica)
* **Erro:** Lógica retornava erro corretamente, mas a interface exibia “Sucesso!”.
* **Causa:** Falta de verificação do retorno booleano do método `registrar_movimentacao()`.
* **Correção:** Checagem explícita do retorno e exibição de mensagens adequadas ("Sucesso" ou "Erro").
* **Resultado:** ✔ Cenário corrigido.

## 🎨 Giovanna

### Bug — Mistura de Tipos na Lista de Histórico
* **Erro:** Funções `get_historico_receitas` e `get_historico_despesas` retornavam todas as movimentações.
* **Causa:** Falta de filtro por tipo (`"receita"` ou `"despesa"`) no Facade.
* **Correção:** Alteração no Facade para retornar apenas transações correspondentes ao tipo solicitado.
* **Resultado:** ✔ Telas agora mostram apenas dados corretos.

## 🔒 Pedro Miguel Lorin

### Bug — Integridade dos Dados entre Contas
* **Erro:** Todas as contas compartilhavam o mesmo histórico.
* **Causa:** Dados não eram vinculados ao `id_conta` do usuário.
* **Correção:** Inclusão de `id_conta` nos registros de movimentação e criação de métodos de filtro dedicados para a leitura.
* **Resultado:** ✔ Cada conta agora possui seu próprio histórico isolado.

---

# 3. 🧪 Relatório de Testes Unitários (TUs)

## 🧑‍💻 Felipe Ferrer (Testes no `Facade.py`)

| ID | Descrição | Objetivo | Resultado |
| :--- | :--- | :--- | :--- |
| TU01 | Receita válida | Registro correto | ✔ |
| TU02 | Receita negativa | Bloquear | ✔ |
| TU03 | Despesa válida | Descontar saldo | ✔ |
| TU04 | Despesa inválida | Bloquear | ✔ |
| TU05 | Histórico | Filtragem | ✔ |

**Conclusão:** Todos os testes passaram (**OK**). O *backend* está consistente com os cenários manuais.

## 🎨 Giovanna (Testes Automatizados - `teste_listagem.py`)
* **Casos Testados:** Listas vazias, Filtragem de receitas, Filtragem de despesas, Validação de dados (valor e descrição).
* **Resultado:** Ran 4 tests in 0.004s OK

## 🔒 Pedro Miguel Lorin
* (Sem testes unitários específicos apresentados, porém validou correções no CT01).

---

# 4. ✨ Documentação da Funcionalidade Implementada

## 🧑‍💻 Felipe — Meta de Economia

### Visão Geral
Permite ao usuário definir uma meta de economia, persistir o valor, e visualizar progresso (saldo vs. meta). Acompanha métricas (total receitas, total despesas, saldo e % de progresso).

### Arquivos Principais
* Facade.py / FinanceAppLogic: Métodos de negócio relativos à meta.
* meta.json: Arquivo onde a meta é persistida (JSON simples).
* main_kivy.py: Registro da tela e integração app <-> lógica.
* ui/meta.kv: Layout da MetaScreen.

### Métodos e Trechos Relevantes
* FinanceAppLogic._salvar_meta(): Recebe o valor (float) e escreve meta.json.
* FinanceAppLogic._carregar_meta(): Tenta ler meta.json no startup; se não existir, define meta_economia = 0.0.
* FinanceAppLogic.configurar_meta(valor_str): Valida entrada, converte para float, salva e retorna True/False.
* FinanceAppLogic.calcular_progresso_meta(): Retorna um dicionário com:
  { "meta": float, "total_receitas": float, "total_despesas": float, "saldo": float, "progresso": float }

### Tela: MetaScreen
* **Evento chave:** on_pre_enter chama app.logic.calcular_progresso_meta() e atualiza ids.texto_progresso.
* **Exemplos de Código (Pseudocódigo):**
  # FinanceAppLogicdef configurar_meta(self, valor_str): try: valor = float(valor_str.replace(",", ".")) if valor < 0: return False self.meta_economia = valor self._salvar_meta() return True except ValueError: return False
  # MetaScreen.on_pre_enter
  dados = app.logic.calcular_progresso_meta()
  self.ids.texto_progresso.text = ( f"Meta: R$ {dados['meta']:.2f}\n" f"Receitas: R$ {dados['total_receitas']:.2f}\n" f"Gastos: R$ {dados['total_despesas']:.2f}\n" f"Saldo: R$ {dados['saldo']:.2f}\n" f"Progresso: {dados['progresso']:.1f}%")

### Critérios de Aceitação (CA)
* Ao abrir a tela de metas, os valores carregam automaticamente (sem clique extra).
* Salvar nova meta persiste em meta.json.
* calcular_progresso_meta() deve retornar números consistentes com o histórico.

## 🎨 Giovanna — Listagem/Histórico e Exportação (.csv)

### Visão Geral
Melhoria nas telas de histórico (separação entre receitas/despesas, tratamento de listas vazias) e adição de exportação de extrato para **.csv com padrão BR**.

### Arquivos Principais
* Facade.py / FinanceAppLogic: Métodos para obter históricos filtrados e exportar CSV.
* ui/receitas.kv, ui/despesas.kv: Telas separadas para listagem.
* exportacao.py (ou método em FinanceAppLogic): Lógica de exportação CSV.

### Métodos e Trechos Relevantes
* FinanceAppLogic.get_historico_receitas(id_conta=None): Retorna lista filtrada com tipo == "receita".
* FinanceAppLogic.exportar_extrato_csv(caminho, id_conta=None): Gera CSV formatado no **padrão brasileiro** (separador `;`, decimais com `,`).
* **Formato CSV gerado (exemplo):** Data;Tipo;Descrição;Valor;Categoria 01/12/2025;Receita;Salário;1000,00;Trabalho 02/12/2025;Despesa;Supermercado;150,50;Alimentação

### Comportamento da UI
* **Tela de Receitas/Despesas:** Chamam o respectivo `get_historico_...()` e exibem mensagem "Nenhuma despesa/receita registrada" se vazia.
* **Ação Exportar:** Chama `exportar_extrato_csv()` e mostra alerta de sucesso/erro.

### Critérios de Aceitação (CA)
* As telas de Receitas/Despesas não devem exibir items do outro tipo.
* O CSV gerado deve abrir no Excel/Sheets sem ajustes (uso de `;` e `,`).

## 🔒 Pedro — Cadastro e Recuperação de Senha (Esqueci a senha)

### Visão Geral
Implementação de fluxo seguro para recuperação de senha usando pergunta de segurança + hash (SHA-256).

### Arquivos Principais
* Facade.py: Atualizações da Conta (dataclass) e métodos de reset de senha.
* contas.json: Armazenamento das contas; agora com campos extras de segurança.
* ui/cadastro.kv, ui/recuperar.kv: Telas adicionadas.

### Estrutura de Conta (exemplo)
@dataclassclass Conta: id_conta: str username: str senha_hash: str pergunta_seguranca: str = "" resposta_seguranca_hash: str = "" # ... outros campos ...

### Métodos e Trechos Relevantes
* Facade.criar_nova_conta(username, senha, pergunta, resposta): Aplica sha256 na senha e na resposta e salva.
* Facade.buscar_pergunta(username): Retorna pergunta_seguranca.
* Facade.resetar_senha(username, resposta_texto, nova_senha): Compara hash(resposta_texto) com resposta_seguranca_hash; se ok, altera senha_hash para hash(nova_senha) e persiste.

### Fluxo de Recuperação (UI)
* Usuário entra em Recuperar Senha e informa username.
* Tela mostra a pergunta de segurança obtida via buscar_pergunta().
* App chama resetar_senha(). Se sucesso, alerta e redireciona para login; senão, mostra erro.
* **Segurança:** A resposta de segurança **NUNCA** é armazenada em texto puro — apenas hash SHA-256.

### Critérios de Aceitação (CA)
* Cadastro salva pergunta e hash da resposta.
* resetar_senha() altera senha apenas quando a resposta bate com o hash.
* Operações inválidas retornam false e apresentam mensagem clara.

---

# 5. 📖 Documentação TDD

## 🧑‍💻 Felipe — TDD da Tela de Metas
* **Ciclo:** RED (Falha ao carregar meta, salvar_meta inacessível) -> GREEN (Remoção de classe duplicada, on_pre_enter atualiza, salvar_meta funcional) -> REFACTOR (Padronização, garantia de defaults).

## 🎨 Giovanna — TDD Exportação CSV
* **Ciclo:** RED (teste test_tdd_exportacao.py criado antes da implementação) -> GREEN (implementação mínima usando biblioteca csv) -> REFACTOR (tratamento de exceções e limpeza da lógica).

## 🔒 Pedro
* (Não apresentou TDD específico). Implementação funcional e correções validadas manualmente.




