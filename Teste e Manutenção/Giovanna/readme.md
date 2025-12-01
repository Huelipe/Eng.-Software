-----

# 📋 Testes da Minha Parte (Listagem e Histórico)

Aqui eu explico como testei as telas de histórico e a separação entre o que é gasto e o que é ganho.

-----

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

# Correção de Bugs

## Bug que encontrei: Mistura de tipos na lista

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

# Testes Automatizados (Unitários)

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

# ✨ O que eu adicionei no App

Explicação rápida do que eu implementei na interface e na lógica.

#### 1\. Separação de Listas (Backend)

Arrumei a lógica para o sistema saber diferenciar o que entra e o que sai na hora de ler o arquivo JSON. Isso evita que a interface mostre dados errados.

#### 2\. Telas de Receitas e Despesas (Frontend)

Criei duas telas separadas no Kivy (`ReceitasScreen` e `DespesasScreen`):

  * **Tela Receitas:** Mostra a lista de ganhos e um gráfico verde/azul só com as categorias de entrada.
  * **Tela Despesas:** Mostra onde você gastou e um gráfico separado.
  * **Tratamento de erro:** Se não tiver nada cadastrado, agora aparece uma mensagem "Nenhuma despesa registrada" em vez de ficar uma tela em branco estranha.

