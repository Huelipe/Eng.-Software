# Organização de pastas:

Esse README.md contém TODA a documentação, enquanto a pasta 'Final' contém TODO o código final, refatorado e integrado.

As pastas 'Felipe', 'Giovanna' e 'Pedro' foram utilizadas para separar o que cada um fez, dentro delas, você vai encontrar as alterações e implementações que cada um fez.

Não é precisso acessar essas pastas, tudo já está nesse README.md e na pasta Final


# 📋 Cenários de Teste

Este documento lista os cenários de teste executados para validação do sistema

---

## Cenários Implementados pelo Felipe:

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


## Cenário implementado pelo Pedro:

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


## Cenário implementado pela Giovanna:

### **Resumo dos Testes**

| ID | O que foi testado | Resultado |
| :--- | :--- | :--- |
| 1 | Entrar na tela de histórico sem ter dados. | **OK** (✔) |
| 2 | Ver se receitas aparecem na tela de despesas. | **OK** (✔) |
| 3 | Ver se despesas aparecem na tela de receitas. | **OK** (✔) |
| 4 | Conferir se o valor e a data estão certos na lista. | **OK** (✔) |

-----

### **Como foram feitos os testes**

#### **1. Teste de Filtro: Só Receitas**

  * **O que eu fiz:** Adicionei um "Salário" (100 reais) e um "Lanche" (50 reais). Depois fui na tela de **Receitas**.
  * **O que tinha que acontecer:** Só podia aparecer o salário. O lanche não podia aparecer lá.
  * **Resultado:** ✔ Funcionou. O sistema filtrou certinho.

#### **2. Teste de Filtro: Só Despesas**

  * **O que eu fiz:** Usei os mesmos dados de cima, mas fui na tela de **Despesas**.
  * **O que tinha que acontecer:** Só aparecer o "Lanche".
  * **Resultado:** ✔ Funcionou. O ganho foi ignorado nessa tela.

-----

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
#### Código incorreto (Antigo)
nova = {
    "descricao": descricao,
    "valor": valor,
    "tipo": tipo
    # Faltava o ID da conta aqui
}


##### Correção Implementada
A solução envolveu vincular cada dado ao ID do usuário e criar filtros na leitura.
# Correção nas Movimentações:
Adicionamos o id_conta ao registrar e criamos um filtro para leitura:
Python
## No método registrar_movimentacao:
nova = {
    "id_conta": id_conta,  # <--- Vinculação adicionada
    "descricao": descricao,
    "valor": valor,
    # ...
}


#### Novo método auxiliar criado para filtrar:
def get_transacoes_usuario(self, id_conta_atual):
    return [t for t in self.transacoes_registradas if t.get("id_conta") == id_conta_atual]


Com essas alterações, o CT01 agora é aprovado, pois cada conta nova inicia vazia e os dados de um usuário não aparecem para outro.



## Giovanna
### Bug que encontrei: Mistura de tipos na lista

**O problema:**
Antes, quando eu clicava pra ver o histórico, o código puxava a lista completa de transações sem separar. Então, se eu entrasse na tela de "Ganhos", aparecia tudo o que eu gastei também, o que ficava confuso.

**Onde estava o erro:**
No arquivo `Facade.py`, as funções `get_historico_receitas` e `get_historico_despesas` estavam retornando a lista `self.transacoes` inteira, sem filtrar.

**Como eu arrumei:**
Mudei o código para filtrar antes de entregar pra tela. Basicamente fiz isso:

  * Para receitas: só retorna se o tipo for `receita`.
  * Para despesas: só retorna se o tipo for `despesa`.

**Teste depois de arrumar:**
Rodei o teste de novo e agora cada tela só mostra o que deve.

-----


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



## Teste implementado pelo Pedro:

### Ambiente de Testes

Linguagem: Python 3.10+

Framework: unittest

Arquivo testado: FinanceFacade (módulo de recuperação de senha)

Arquivo de teste: test_recuperacao.py

Execução via terminal:
python3 test_recuperacao.py

Sistema Operacional: Windows 11

### 2. Casos de Teste Implementados
ID	Descrição	Objetivo	Resultado
TU-P01	Resetar senha com resposta correta	Validar fluxo principal da recuperação de senha	✔ Aprovado
TU-P02	Tentar resetar com resposta incorreta	Impedir alteração indevida de senha	✔ Aprovado
TU-P03	Resetar senha para usuário inexistente	Garantir segurança e prevenção de operações inválidas	✔ Aprovado
TU-P04	Buscar pergunta de segurança corretamente	Validar associação entre usuário e pergunta cadastrada	✔ Aprovado
TU-P05	Aceitar resposta ignorando diferenças de maiúsculas	Garantir tolerância de formato na validação da resposta	✔ Aprovado
Resultado Global da Execução

Comando:

python3 test_recuperacao.py

Saída:

Ran 5 tests in 0.014s
OK

Conclusão: Todos os testes passaram com sucesso.

### Análise dos Resultados

Os testes confirmaram que:

O fluxo completo de recuperação de senha (happy path) está funcional, permitindo redefinir a senha somente mediante resposta correta.

O sistema impede qualquer tentativa de redefinir senha usando respostas incorretas, protegendo a integridade da conta.

Usuários inexistentes não provocam crashes ou exceções; o método retorna False conforme esperado.

A associação entre usuário e pergunta de segurança está correta, garantindo consistência nos dados persistidos.

A validação da resposta opera de forma case-insensitive, garantindo maior usabilidade sem comprometer a segurança.

O comportamento após redefinir senha foi verificado com autenticação real, confirmando que a alteração foi persistida corretamente.

O arquivo contas.json foi corretamente criado e destruído a cada teste, garantindo ambiente isolado.

O conjunto de testes cobre tanto caminhos felizes quanto cenários de falha e entradas inválidas, evidenciando robustez da implementação.

Nenhuma exceção inesperada ocorreu durante o processo, e o comportamento do backend corresponde integralmente aos cenários de teste documentados anteriormente (CT-P01 a CT-P05).


## Teste implementado pela Giovanna:

Criei um script chamado `teste_listagem.py` para testar isso tudo automaticamente sem precisar ficar abrindo o app toda hora.

### O que o script testa:

1.  **Listas vazias:** Se o app não quebra quando não tem nada registrado.
2.  **Filtros:** Se ele realmente separa receitas de despesas.
3.  **Dados:** Se o valor que eu salvo é o mesmo que volta na tela (pra não ter erro de arredondamento ou descrição errada).

### Resultado do teste

Rodei no terminal com o comando:
`python3 teste_listagem.py`

**Saída:**

```text
Ran 4 tests in 0.004s

OK
```

Tudo passou.

-----


# ✨ Documentação da Funcionalidade implementadas

Esta seção detalha a implementação e a arquitetura das nova funcionalidades adicionadas ao aplicativop.

## Funcionalidade adicionada por Felipe

Botão de Meta que o usuário poderá utilizar para definir uma meta

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


## Funcionalidade adicionada por Pedro

Botão 'Esqueci minha senha' para usuários

#### 1\. Persistência de Dados de Segurança (`Facade.py`)

Foi alterada a estrutura de dados ("struct") da `Conta` para suportar perguntas de segurança. Agora, além de login e senha, o sistema armazena a pergunta personalizada e o hash da resposta.

  * **Segurança:** A resposta da pergunta de segurança **não é salva em texto puro**. Ela passa pelo mesmo processo de criptografia (`SHA-256`) que a senha, garantindo que ninguém consiga ler a resposta no arquivo `contas.json`.

**Trecho Responsável (`Facade.py`):**

```python
@dataclass
class Conta:
    # ... campos anteriores ...
    pergunta_seguranca: str = ""
    resposta_seguranca_hash: str = ""
```

#### 2\. Fluxo de Cadastro Seguro (`CadastroScreen`)

Foi implementada uma nova tela dedicada ao cadastro (`ui/cadastro.kv`), separando-a do login.
Ao criar a conta, o sistema agora exige e valida dois novos campos obrigatórios:

1.  **Pergunta de Segurança** (Ex: "Nome do cachorro?")
2.  **Resposta de Segurança** (Ex: "Rex")

A lógica `criar_nova_conta` no Facade foi atualizada para receber, hashear e persistir esses novos dados.

#### 3\. Tela de Recuperação (`RecuperarScreen`)

Uma nova tela (`ui/recuperar.kv`) foi criada para gerenciar o fluxo de redefinição de senha em duas etapas:

1.  **Busca da Pergunta:** O usuário digita o login e o sistema busca a pergunta associada.
2.  **Validação e Reset:** O usuário digita a resposta e a nova senha. O sistema compara o hash da resposta digitada com o hash salvo. Se conferir, a senha é alterada.

**Lógica de Reset (`main_kivy.py`):**

```python
def confirmar_reset(self):
    # ... capturas de input ...
    sucesso = app.logic.resetar_senha(user, resp, nova_senha)
    
    if sucesso:
        app.mostrar_alerta("Sucesso", "Senha alterada! Faça login agora.")
        app.root.current = "login"
    else:
        app.mostrar_alerta("Erro", "Resposta de segurança incorreta.")
```

#### 4\. Integração Backend-Frontend (`FinanceAppLogic`)

A classe `FinanceAppLogic` foi expandida para expor os novos métodos do Facade para a interface gráfica:

  * **`buscar_pergunta(username)`**: Retorna a string da pergunta para exibir na tela.
  * **`resetar_senha(username, resposta, nova_senha)`**: Realiza a validação criptográfica e a atualização dos dados.

#### 5\. Atualização da Interface (`UI`)

  * **Login (`login.kv`):** Adicionado o botão "Esqueci minha senha" e o botão "Não tem conta? Crie aqui", melhorando a navegação.
  * **Registro no Build:** As novas telas (`CadastroScreen` e `RecuperarScreen`) foram registradas no `ScreenManager` e seus arquivos KV carregados no método `build()`.

**Trecho de Carregamento (`main_kivy.py`):**

```python
Builder.load_file("ui/cadastro.kv")
Builder.load_file("ui/recuperar.kv")

sm.add_widget(CadastroScreen(name="cadastro"))
sm.add_widget(RecuperarScreen(name="recuperar"))
```


## Funcionalidade adicionada pela Giovanna:
Explicação rápida do que eu implementei na interface e na lógica.

#### 1\. Separação de Listas (Backend)

Arrumei a lógica para o sistema saber diferenciar o que entra e o que sai na hora de ler o arquivo JSON. Isso evita que a interface mostre dados errados.

#### 2\. Telas de Receitas e Despesas (Frontend)

Criei duas telas separadas no Kivy (`ReceitasScreen` e `DespesasScreen`):

  * **Tela Receitas:** Mostra a lista de ganhos e um gráfico verde/azul só com as categorias de entrada.
  * **Tela Despesas:** Mostra onde você gastou e um gráfico separado.
  * **Tratamento de erro:** Se não tiver nada cadastrado, agora aparece uma mensagem "Nenhuma despesa registrada" em vez de ficar uma tela em branco estranha.


  ## 🆕 Novas Funcionalidades (v1.1)

### 📄 Exportação de Extrato (.csv)
Implementada a funcionalidade de exportar todo o histórico de movimentações para um arquivo `.csv`. O arquivo é gerado formatado especificamente para o padrão brasileiro (separador `;` e decimais com `,`), facilitando a importação direta no Excel ou Google Sheets.

-----

# 📄 DOCUMENTO TDD —

## TTD Felipe

Durante os testes funcionais, foi identificado um erro relacionado à funcionalidade de metas que impedia o carregamento correto dos dados e causava uma exceção ao tentar atualizar a meta.

#### **Comportamento Incorreto Observado (Bug)**

* Ao abrir a tela de metas, os valores **não eram carregados automaticamente**.
* O usuário precisava clicar em "Atualizar Meta" apenas para visualizar a meta atual.
* Ao tentar atualizar a meta, o aplicativo apresentava o erro: `AttributeError: 'FinanceAppMobile' object has no attribute 'salvar_meta'`.

#### **Causa Identificada**

* Havia **duas classes `MetaScreen`** definidas no arquivo `main_kivy.py`, gerando conflito de referência no carregamento do Kivy.
* O Kivy vinculou a versão errada da classe, impedindo que o método `app.salvar_meta()` fosse encontrado.

#### **Objetivo do TDD (Definição dos Critérios)**
Garantir que:
1.  A meta seja **sempre carregada automaticamente** ao entrar na tela.
2.  O método `salvar_meta` seja encontrado e executado corretamente pelo *Binding* do KV.
3.  A funcionalidade de progresso seja **atualizada imediatamente** após qualquer mudança na meta.

**Teste Inicial (RED)**

Criamos testes definindo o comportamento esperado antes da correção, forçando-os a falhar e, assim, confirmando a existência e a natureza do bug.

#### **Testes Desenvolvidos**

```python
def test_meta_carrega_automaticamente():
    logic = FinanceAppLogic()
    logic.meta_economia = 300
    logic._salvar_meta()
    # Carrega de novo como se o app tivesse sido reiniciado
    novo_logic = FinanceAppLogic()
    assert novo_logic.meta_economia == 300, \
        "ERRO: A meta não foi carregada automaticamente ao abrir a tela."

def test_salvar_meta_atualiza_sem_erro():
    app = FinanceAppMobile()
    app.logic = FinanceAppLogic()
    try:
        app.salvar_meta("500")
    except AttributeError:
        assert False, "ERRO: salvar_meta não estava acessível pelo KV."
```

Resultado na Fase RED
Os testes falharam conforme o esperado, confirmando os bugs:

meta não carregava automaticamente.

salvar_meta não era encontrado pelo binding do KV.

Correção Aplicada (GREEN)
Foram implementadas as correções necessárias para fazer os testes passarem.

Correção 1: Remoção da Duplicação da Classe MetaScreen
O conflito de classes foi resolvido mantendo apenas uma definição.

Antes (erro): Duas definições de classe no arquivo.

Depois (correto): Apenas uma definição contendo toda a lógica.

```python

class MetaScreen(MDScreen):
    def on_pre_enter(self):
        # Lógica de carregamento implementada abaixo
        ...
```

🟢 Correção 2: Carregar os Dados Sempre ao Entrar na Tela
A lógica de atualização foi centralizada no evento on_pre_enter para garantir que o refresh ocorra toda vez que a tela for exibida.

```python

class MetaScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        dados = app.logic.calcular_progresso_meta()
        self.ids.texto_progresso.text = (
            f"Meta atual: R$ {dados['meta']:.2f}\n"
            f"Total Ganhos: R$ {dados['total_receitas']:.2f}\n"
            f"Total Gastos: R$ {dados['total_despesas']:.2f}\n"
            f"Economizado: R$ {dados['saldo']:.2f}\n"
            f"Progresso: {dados['progresso']:.1f}%"
        )
```

Correção 3: Disponibilizar salvar_meta Corretamente no App
O método salvar_meta foi ajustado na classe principal do aplicativo (FinanceAppMobile) para ser acessível pelo KV e incluir a lógica de atualização imediata da tela.

```python

def salvar_meta(self, valor):
    if self.logic.configurar_meta(valor):
        dados = self.logic.calcular_progresso_meta()
        self.mostrar_alerta("Meta Atualizada", "Meta alterada com sucesso.")
    else:
        self.mostrar_alerta("Erro", "Valor inválido.")
        
    # Atualiza a tela imediatamente
    screen = self.root.get_screen("meta")
    screen.ids.texto_progresso.text = (
        f"Meta atual: R$ {dados['meta']:.2f}\n"
        f"Total Ganhos: R$ {dados['total_receitas']:.2f}\n"
        f"Total Gastos: R$ {dados['total_despesas']:.2f}\n"
        f"Economizado: R$ {dados['saldo']:.2f}\n"
        f"Progresso: {dados['progresso']:.1f}%"
    )
```

Teste Aprovado (GREEN)
Após as correções, os testes foram executados novamente e todos passaram com sucesso, validando a correção:

✔ A meta agora carrega automaticamente.

✔ O método salvar_meta é encontrado e executado sem exceções.

✔ O progresso é atualizado toda vez que a meta é salva.

✔ O app não apresenta mais exceções relacionadas à tela de metas.

Refatoração (REFACTOR)
Nesta fase, melhorias secundárias foram aplicadas para otimizar o código sem alterar o comportamento funcional:

Remoção de duplicação de tela e ajustes na arquitetura.

Ajuste da exibição dos valores com formatação consistente.

Garantia de valores default no carregamento do JSON.


## TDD de Pedro

### Metodologia: TDD (Test Driven Development)

A funcionalidade de recuperação de senha desenvolvida pelo Pedro seguiu rigorosamente o ciclo Red–Green–Refactor, garantindo previsibilidade, segurança e comportamento consistente em todas as etapas.

1. 🔴 RED (O Teste)

Antes de qualquer implementação, foram definidos e criados os testes no arquivo test_recuperacao.py.

Os requisitos principais definidos foram:

O sistema deve permitir redefinir a senha somente quando a resposta da pergunta de segurança estiver correta.

Respostas incorretas não devem alterar a senha cadastrada.

Usuários inexistentes não podem produzir erros nem permitir operações irregulares.

A pergunta de segurança cadastrada deve ser retornada corretamente.

A validação deve ignorar diferenças entre maiúsculas e minúsculas.

Após escrever os testes, todos falharam no primeiro ciclo — comportamento esperado — confirmando que:

Não havia lógica implementada para recuperação de senha.

A comparação de respostas ainda era literal (case-sensitive).

Pergunta de segurança não era retornada.

O sistema não validava usuário inexistente corretamente.

O estado RED validou que o teste estava funcionando como guarda de comportamento.

2. 🟢 GREEN (A Implementação)

Com os testes falhando, Pedro implementou somente o código mínimo necessário dentro da FinanceFacade para satisfazer cada assert do conjunto de testes.

As ações implementadas nesta fase incluíram:

Criação do método de redefinição de senha com validação por resposta de segurança.

Normalização das strings usando .lower() para garantir comparação case-insensitive.

Inclusão da busca da pergunta de segurança vinculada ao usuário.

Persistência da nova senha após redefinição bem-sucedida.

Garantia de que usuários inexistentes retornassem False sem lançar exceções.

Revalidação da autenticação após a troca de senha.

Após as inserções mínimas, todos os testes passaram, confirmando que a implementação atendia exatamente ao escopo definido pelos testes.

3. 🔵 REFACTOR (A Melhoria)

Com todos os testes passando, iniciou-se a fase de refatoração, focada em:

Melhoria da legibilidade dos métodos, evitando duplicação de lógica.

Normalização centralizada para comparações de respostas.

Separação clara entre acesso aos dados, validações e regras de negócio dentro da Facade.

Ajustes no fluxo de persistência, garantindo que as operações fossem consistentes mesmo após múltiplas redefinições.

Remoção de condicionais redundantes e otimização da busca por usuário.

Nenhum comportamento foi alterado — apenas a estrutura interna.
Os testes continuaram passando, garantindo que o refatoramento não afetou a lógica da funcionalidade.


## TDD de Giovanna

### Metodologia: TDD (Test Driven Development)
Esta funcionalidade foi desenvolvida utilizando rigorosamente o ciclo **Red-Green-Refactor** para garantir robustez e qualidade de código:

1.  🔴 **RED (O Teste):**
    * Primeiro, criamos o teste `test_tdd_exportacao.py` antes de qualquer lógica.
    * Definimos os requisitos: o arquivo deve ser criado, deve conter cabeçalhos corretos e respeitar a formatação de moeda brasileira.
    * O teste falhou inicialmente (erro esperado), confirmando que a funcionalidade não existia.

2.  🟢 **GREEN (A Implementação):**
    * Implementamos a lógica mínima na classe `FinanceAppLogic` usando a biblioteca nativa `csv` do Python.
    * O foco foi escrever apenas o código necessário para fazer o teste passar.

3.  🔵 **REFACTOR (A Melhoria):**
    * Refinamos o código para tratar exceções de leitura/escrita e garantimos que a separação de responsabilidades fosse mantida.

### ✅ Verificando a implementação
Para rodar o teste automatizado desta funcionalidade:

```bash
python -m unittest test_tdd_exportacao.py
```







