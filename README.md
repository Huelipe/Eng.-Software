# Eng.-Software

Alunos:
Felipe Ferrer Sorrilha,
Giovanna Sanches Reghine e
Pedro Miguel Lorin

Link Trello: https://trello.com/invite/b/68a4c55473563e97ae1399e6/ATTI4245f37f8a5842f03bf0a1a13aefe923094FC47A/eng-software

Projeto: Aplicativo de controle de finanças

Problema: pesquisas indicam que muitos brasileiros possuem dificuldades para administrar suas finanças.

Objetivos: criar um aplicativo que pode ser utilizado para ajudar a controlar finanças pessoais. Gráficos e feedbacks seriam implementados para auxiliar na administração de dinheiro.

Relevância: artigos e pesquisas indicam que adultos, principalmente mais jovens, têm dificuldade para gerenciar finanças. Um aplicativo poderia ser muito útil para auxiliar.



## Gerência de qualidade

- Padrões adotados:
  - ISO/IEC 9126: define critérios de qualidade (funcionalidade, confiabilidade, usabilidade, eficiência e manutenibilidade).
  - ISO 9001: garante rastreabilidade e melhoria contínua no processo.
  - CMM: orienta boas práticas de maturidade de processo.
  - PROCERGS: diretrizes de segurança (autenticação e criptografia).
    
- Critérios principais:
  - Segurança de dados do usuário (criptografia e login).
  - Desempenho fluido com respostas abaixo de 2 segundos.
  - Interface intuitiva e responsiva.
  - Código modular e revisado entre os integrantes.

- Ferramentas utilizadas: GitHub (controle de versão), Trello (gestão de tarefas), Figma (protótipos), Flutter (app), VS Code (IDE).

## Decisão arquiteturial

- Padrão de Arquitetura escolhido: MVVM (Model–View–ViewModel)

- O padrão MVVM foi escolhido por ser amplamente utilizado em aplicativos mobile modernos, como os desenvolvidos em Flutter e React Native.
- Ele separa claramente as responsabilidades do sistema:
  - Model: representa os dados e regras de negócio (transações, contas, relatórios).
  - View: cuida da interface e interação com o usuário.
  - ViewModel: faz a ponte entre o Model e a View, processando dados e atualizando a interface de forma reativa.

- Essa separação melhora a organização, testabilidade e manutenibilidade do código, permitindo adicionar novas funcionalidades (como gráficos, relatórios e notificações) sem alterar partes principais do sistema.
- Também facilita o uso de padrões de projeto complementares, como Observer e Decorator, integrando de forma limpa as atualizações de dados com a interface.

- Fluxo:
  - 1: Usuário interage com a View (UI).
  - 2: A ViewModel processa as ações e comunica-se com o Model.
  - 3: O Model retorna dados e notifica a ViewModel, que atualiza a interface.

## Padrões de projeto

- Facade (implementado pelo Pedro)
  - Foi escolhido para simplificar a comunicação entre os diferentes módulos do sistema (como autenticação, transações e relatórios).
  - Em vez de a interface chamar várias classes diretamente, o padrão Facade fornece um ponto de acesso único — por exemplo, uma classe FinanceAppManager que centraliza as chamadas do app.
  - Isso deixa o código mais limpo e fácil de manter, reduzindo o acoplamento entre as partes do sistema.

- Decorator (implementado pela Giovanna)
  - O Decorator é usado para permitir que relatórios e gráficos financeiros recebam novas funcionalidades sem alterar a estrutura principal.
  - Por exemplo, um relatório básico pode ganhar exportação em PDF, adição de gráficos ou filtros personalizados através de decoradores.
  - Esse padrão facilita a expansão futura e evita repetição de código.

- Observer (implementado pelo Felipe)
  - O Observer foi adotado para manter a interface atualizada em tempo real.
  - Quando o usuário adiciona uma nova despesa, o sistema notifica automaticamente os componentes que exibem saldo e gráficos, sem precisar atualizar manualmente cada tela.
  - Isso torna o app mais dinâmico e reativo, melhorando a experiência do usuário.


# 🧪 Relatório de Testes Automatizados (TDD)

**Responsável:** Pedro
**Funcionalidade Testada:** Recuperação de Senha (Backend/Lógica)
**Arquivo de Teste:** `test_recuperacao.py`
**Framework Utilizado:** `unittest` (Nativo do Python)

### 1\. Objetivo dos Testes

Garantir a integridade e a segurança da lógica de redefinição de senha (`resetar_senha`), assegurando que apenas usuários com a resposta de segurança correta consigam alterar suas credenciais, independente da formatação do texto (maiúsculas/minúsculas).

### 2\. Cenários de Teste Cobertos

Foram implementados 5 casos de teste (Test Cases) cobrindo caminhos felizes e exceções:

  * **✅ CT01 - Caminho Feliz (Sucesso):** Simula um usuário fornecendo a resposta correta.
      * *Resultado Esperado:* A senha deve ser alterada no banco de dados e o login com a nova senha deve funcionar.
  * **🛡️ CT02 - Proteção contra Resposta Incorreta:** Simula uma tentativa de invasão com resposta errada.
      * *Resultado Esperado:* O sistema deve negar a alteração e a senha antiga deve permanecer válida.
  * **👻 CT03 - Usuário Inexistente:** Tenta recuperar a senha de um login que não existe.
      * *Resultado Esperado:* O sistema deve retornar `False` sem quebrar (crash).
  * **🔍 CT04 - Recuperação de Pergunta:** Verifica se o sistema busca a pergunta correta associada ao usuário.
      * *Resultado Esperado:* A string da pergunta deve corresponder exatamente à salva no cadastro.
  * **🔠 CT05 - Robustez de Input (Case Insensitive):** Tenta validar a resposta "azul" digitando "AZUL".
      * *Resultado Esperado:* O sistema deve aceitar, pois a validação deve ignorar diferenças de caixa alta/baixa.

### 3\. Aplicação da Metodologia TDD (Ciclo Red-Green)

Durante o desenvolvimento dos testes, foi aplicado o ciclo de **Test Driven Development**:

1.  **🔴 Fase RED (Falha Inicial):** Ao executar o teste `test_deve_retornar_pergunta_correta` pela primeira vez, o teste falhou acusando `AttributeError`.
      * *Causa:* O teste chamava o método `buscar_pergunta`, mas a implementação no Facade chamava-se `buscar_pergunta_seguranca`.
2.  **🟢 Fase GREEN (Correção):** O código de teste foi refatorado para utilizar a nomenclatura correta definida na arquitetura do sistema.
3.  **✅ Resultado Final:** Após a correção, todos os 5 testes passaram com sucesso em **0.026s**.

### 4\. Evidência de Execução

Abaixo, o log de execução final comprovando a estabilidade do módulo de segurança:

```text
PS C:\...\Codigo> python test_recuperacao.py
[Sistema] 'movimentacoes.json' não encontrado.
[Sistema] Dados salvos em 'contas.json'.
.
[Facade] Autenticação de pedro bem-sucedida.
.
[Facade] Autenticação de pedro falhou (usuário ou senha inválidos).
.
----------------------------------------------------------------------
Ran 5 tests in 0.026s

OK
```

-----

**Conclusão:** O módulo de recuperação de senha foi validado logicamente e está seguro contra falhas de digitação (case sensitivity) e tentativas de acesso não autorizado via resposta incorreta.
