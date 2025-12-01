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


## Novo método auxiliar criado para filtrar:
def get_transacoes_usuario(self, id_conta_atual):
    return [t for t in self.transacoes_registradas if t.get("id_conta") == id_conta_atual]


Com essas alterações, o CT01 agora é aprovado, pois cada conta nova inicia vazia e os dados de um usuário não aparecem para outro.


Aqui está a documentação técnica da sua funcionalidade, seguindo o mesmo padrão do exemplo que você enviou.

-----

# ✨ Documentação da Funcionalidade de Recuperação de Senha (Esqueci minha Senha)

Esta seção detalha a implementação e a arquitetura da nova funcionalidade de segurança e recuperação de contas no aplicativo.
## Funcionalidade adicionada por Pedro

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



