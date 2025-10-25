# --- 1. IMPORTAÇÕES E "STRUCTS" (MODELOS DE DADOS) ---

# --- Importações de Bibliotecas Nativas ---
from dataclasses import dataclass, field # Ferramenta para criar "structs" (classes de dados)
from decimal import Decimal           # Para matemática de dinheiro 
from datetime import datetime, date     # Para lidar com datas e horas
import uuid                             # Para criar IDs únicos (ex: conta-34a2c1)
import json                             # Para ler e escrever arquivos de texto no formato JSON
import os                               # Para interagir com o sistema (ex: verificar se um arquivo existe)
import hashlib                          # Para "embaralhar" (hash) senhas de forma segura
import getpass                          # Para pedir a senha sem mostrá-la na tela (invisível)

# --- "Struct" (Modelo) da Conta ---
@dataclass # O "decorador" @dataclass cria o construtor (__init__) automaticamente
class Conta:
    """
    Define a estrutura de dados de uma Conta.
    É como um formulário em branco.
    """
    id_conta: str      # O ID único no sistema (ex: conta-a4f32c)
    username: str      # O nome de login (único, ex: 'pedro95')
    nome_completo: str # O nome real da pessoa (pode ser repetido, ex: 'Pedro Silva')
    saldo_atual: Decimal   # O saldo, usando Decimal para precisão
    password_hash: str # Onde guardamos a senha *embaralhada* (hash)

# --- "Struct" (Modelo) da Movimentação ---
@dataclass
class Movimentacao:
    """
    Define a estrutura de dados de uma Transação (receita ou despesa).
    """
    id_movimentacao: str     # O ID único da transação
    id_conta_associada: str  # A qual conta esta movimentação pertence
    tipo: str                # 'receita' ou 'despesa'
    valor: Decimal           # O valor da transação
    data: datetime           # A data E HORA exata da transação
    descricao: str           # O que foi (ex: "Compra no mercado")


# --- 2. OS SUBSISTEMAS ---


class ContaService:
    """
    O "Cofre". É a única classe que sabe como CRIAR, LER e ATUALIZAR contas.
    Ela também cuida da persistência (salvar/carregar) no arquivo 'contas.json'.
    """
    
    def __init__(self):
        """Construtor. É executado quando um 'ContaService' é criado."""
        self._FILE_NAME = "contas.json"  # Nome do arquivo de "banco de dados"
        self._contas_db = {}             # Banco de dados "em memória" (um dicionário)
        self._load_data()                # Tenta carregar dados do arquivo assim que é criado

    def _hash_password(self, password):
        """Método interno para embaralhar uma senha de forma segura (Hashing)."""
        # 'password.encode('utf-8')' transforma a string em bytes (padrão de "alfabeto")
        # 'hashlib.sha256(...)' aplica o algoritmo de hash 
        # '.hexdigest()' retorna o hash como uma string de texto
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def _get_conta_por_username(self, username):
        """Método interno para buscar uma conta pelo seu username (login)."""
        # Itera por todas as contas no banco de dados em memória
        for conta in self._contas_db.values():
            # Compara usando .lower() para não diferenciar maiúsculas/minúsculas
            if conta.username.lower() == username.lower():
                return conta # Retorna o objeto 'Conta' se encontrar
        return None # Retorna 'None' (nada) se não encontrar

    def _load_data(self):
        """Método interno para carregar os dados de 'contas.json'."""
        # 'os.path.exists' verifica se o arquivo já existe
        if not os.path.exists(self._FILE_NAME):
            print("[Sistema] 'contas.json' não encontrado. Começando do zero.")
            return # Sai da função se não há o que carregar
        
        # 'try...except' tenta executar um código que pode falhar
        try:
            # 'with open(...) as f:' abre o arquivo (modo 'r' = read/leitura)
            with open(self._FILE_NAME, 'r') as f:
                dados_salvos = json.load(f) # Converte o texto JSON em um dicionário Python
                
                # Itera pelo dicionário carregado e recria os objetos 'Conta'
                for conta_id, dados_conta in dados_salvos.items():
                    # Lógica de compatibilidade (para arquivos antigos que usavam 'nome_titular')
                    username = dados_conta.get('username') or dados_conta.get('nome_titular')
                    nome_completo = dados_conta.get('nome_completo') or username
                    
                    self._contas_db[conta_id] = Conta(
                        id_conta=conta_id,
                        username=username,
                        nome_completo=nome_completo,
                        saldo_atual=Decimal(dados_conta['saldo_atual']), # Converte str de volta para Decimal
                        password_hash=dados_conta.get('password_hash', None) # .get() evita erro se o campo não existir
                    )
            print(f"[Sistema] {len(self._contas_db)} contas carregadas de 'contas.json'.")
        except Exception as e:
            # Se o arquivo JSON estiver corrompido ou algo der errado
            print(f"[Sistema] ERRO ao carregar 'contas.json': {e}. Começando do zero.")
            self._contas_db = {}

    def _save_data(self):
        """Método interno para salvar o estado atual de _contas_db em 'contas.json'."""
        dados_para_salvar = {}
        # Converte os objetos 'Conta' de volta para um dicionário simples
        for conta_id, conta_obj in self._contas_db.items():
            dados_para_salvar[conta_id] = {
                'username': conta_obj.username,
                'nome_completo': conta_obj.nome_completo,
                'saldo_atual': str(conta_obj.saldo_atual), # Converte Decimal para str (JSON não entende Decimal)
                'password_hash': conta_obj.password_hash
            }
        
        # 'with open('w'...) abre o arquivo em modo 'w' = write/escrita (apaga o antigo)
        with open(self._FILE_NAME, 'w') as f:
            # 'json.dump' escreve o dicionário no arquivo
            # 'indent=4' formata o JSON para ficar legível
            json.dump(dados_para_salvar, f, indent=4) 
        print(f"[Sistema] Dados salvos em 'contas.json'.")

    def criar_conta(self, id_conta, username, nome_completo, saldo_inicial, senha_plana):
        """Cria uma nova conta, com validação de username único."""
        
        # Validação de regra de negócio (login único)
        if self._get_conta_por_username(username):
            # 'raise ValueError' é como o Python "grita um erro"
            # Isso será capturado pelo Facade
            raise ValueError(f"Nome de usuário '{username}' já está em uso.")
            
        # Pega a senha (ex: "123") e transforma no hash (ex: "a665a...")
        hash_da_senha = self._hash_password(senha_plana)
        
        # Cria o novo objeto 'Conta'
        nova_conta = Conta(
            id_conta=id_conta,
            username=username,
            nome_completo=nome_completo,
            saldo_atual=Decimal(str(saldo_inicial)), # Garante que o saldo é Decimal
            password_hash=hash_da_senha
        )
        
        # Salva no banco de dados em memória e no arquivo
        self._contas_db[id_conta] = nova_conta
        self._save_data()
        return nova_conta
        
    def _get_conta(self, id_conta):
        """Busca uma conta pelo seu ID único de sistema."""
        conta = self._contas_db.get(id_conta)
        if not conta: 
            raise ValueError(f"Conta {id_conta} não encontrada.")
        return conta
        
    def autenticar(self, username, senha_plana):
        """Verifica se o login (username) e a senha estão corretos."""
        # 1. Encontra a conta pelo username
        conta = self._get_conta_por_username(username)
        
        # 2. Se a conta não existe ou não tem senha (conta antiga), falha.
        if not conta or not conta.password_hash:
            return None 
            
        # 3. Embaralha a senha que o usuário DIGITOU
        hash_da_tentativa = self._hash_password(senha_plana)
        
        # 4. Compara o hash da tentativa com o hash que estava SALVO
        if hash_da_tentativa == conta.password_hash:
            return conta # Sucesso! Retorna o objeto da conta
            
        return None # Falha (senha incorreta)

    def atualizar_saldo_conta(self, id_conta, valor, tipo):
        """A lógica principal de negócio: alterar o saldo."""
        conta = self._get_conta(id_conta) # Pega a conta
        
        if tipo == 'receita':
            conta.saldo_atual += valor # Soma o valor
        elif tipo == 'despesa':
            # Validação de regra de negócio (não pode gastar o que não tem)
            if conta.saldo_atual < valor: 
                raise ValueError("Saldo insuficiente.")
            conta.saldo_atual -= valor # Subtrai o valor
        else: 
            raise ValueError(f"Tipo '{tipo}' inválido.")
        
        # Salva o novo estado da conta no arquivo
        self._save_data()
        return conta

class MovimentacaoService:
    """
    O "Livro-Razão". É a única classe que sabe como LER e SALVAR o histórico 
    de movimentações no arquivo 'movimentacoes.json'.
    """
    def __init__(self):
        self._FILE_NAME = "movimentacoes.json"
        self._movimentacoes_db = [] # Banco de dados em memória (uma lista)
        self._load_data()

    def _load_data(self):
        """Carrega o histórico de 'movimentacoes.json'."""
        if not os.path.exists(self._FILE_NAME):
            print("[Sistema] 'movimentacoes.json' não encontrado.")
            return
        try:
            with open(self._FILE_NAME, 'r') as f:
                dados_salvos = json.load(f) # Converte JSON em uma lista Python
                
                # Itera pela lista e reconstrói os objetos 'Movimentacao'
                for item in dados_salvos:
                    data_str = item['data']
                    data_obj = None
                    
                    # Lógica de compatibilidade (para dados antigos só com data)
                    try:
                        # Tenta carregar como 'datetime' completo (com hora)
                        data_obj = datetime.fromisoformat(data_str)
                    except ValueError:
                        # Se falhar, é formato antigo (só 'date')
                        # Converte 'date' para 'datetime' com hora 00:00:00
                        data_obj = datetime.combine(date.fromisoformat(data_str), datetime.min.time())
                        
                    self._movimentacoes_db.append(Movimentacao(
                        id_movimentacao=item['id_movimentacao'],
                        id_conta_associada=item['id_conta_associada'],
                        tipo=item['tipo'],
                        valor=Decimal(item['valor']), # Converte str para Decimal
                        data=data_obj, # Salva o objeto datetime
                        descricao=item['descricao']
                    ))
            print(f"[Sistema] {len(self._movimentacoes_db)} movimentações carregadas.")
        except Exception as e:
            print(f"[Sistema] ERRO ao carregar 'movimentacoes.json': {e}.")
            self._movimentacoes_db = []
            
    def _save_data(self):
        """Salva o histórico atual em 'movimentacoes.json'."""
        dados_para_salvar = []
        # Converte os objetos 'Movimentacao' em uma lista de dicionários
        for mov_obj in self._movimentacoes_db:
            dados_para_salvar.append({
                'id_movimentacao': mov_obj.id_movimentacao,
                'id_conta_associada': mov_obj.id_conta_associada,
                'tipo': mov_obj.tipo,
                'valor': str(mov_obj.valor), # Converte Decimal para str
                'data': mov_obj.data.isoformat(), # Converte datetime para str (ex: 2025-10-25T10:30:00)
                'descricao': mov_obj.descricao
            })
        with open(self._FILE_NAME, 'w') as f:
            json.dump(dados_para_salvar, f, indent=4)
        # Não imprimimos aqui para não poluir o log a cada transação

    def salvar_movimentacao(self, movimentacao: Movimentacao):
        """Adiciona uma nova movimentação ao banco de dados."""
        self._movimentacoes_db.append(movimentacao)
        self._save_data() # Salva no arquivo
        return True

    def get_historico_por_tipo(self, id_conta, tipo_movimentacao):
        """Filtra o histórico para uma conta e tipo específicos."""
        historico_filtrado = []
        for mov in self._movimentacoes_db:
            # Filtra a lista
            if mov.id_conta_associada == id_conta and mov.tipo == tipo_movimentacao:
                historico_filtrado.append(mov)
        return historico_filtrado

# --- 3. FACADE  ---

class FinanceFacade:
    """
    A Fachada. Esta é a ÚNICA classe com a qual o Cliente (menu) vai falar.
    Ele é o "Garçom" que coordena a "Cozinha" (ContaService) e o "Caixa" (MovimentacaoService).
    """
    def __init__(self):
        """Construtor. O Facade "cria" e "guarda" os subsistemas."""
        # O Facade inicializa os subsistemas (que carregam os dados sozinhos)
        self._conta_service = ContaService()
        self._mov_service = MovimentacaoService()

    def criar_nova_conta(self, username, nome_completo, senha):
        """
        Método simples para o cliente criar uma conta.
        Agora, todas as contas começam com saldo 0,00 automaticamente.
        """
        print(f"[Facade] Tentando criar conta para {username}...")
        novo_id = f"conta-{uuid.uuid4().hex[:6]}"  # Gera um ID de sistema

        try:
            # Cria a conta com saldo inicial fixo em 0,00
            conta = self._conta_service.criar_conta(
                id_conta=novo_id,
                username=username,
                nome_completo=nome_completo,
                saldo_inicial=0,  # saldo inicial automático
                senha_plana=senha
            )
            print(f"[Facade] Conta para {username} criada com ID {novo_id}. Saldo inicial: R$ 0,00.")
            return conta
        except ValueError as e:
            print(f"[Facade] FALHA ao criar conta: {e}")
            return None

        
    def autenticar_usuario(self, username, senha):
        """Método simples para o cliente fazer login."""
        print(f"[Facade] Tentando autenticar {username}...")
        # Apenas delega a chamada para o subsistema
        conta = self._conta_service.autenticar(username, senha)
        
        if conta:
            print(f"[Facade] Autenticação de {username} bem-sucedida.")
            return conta
        else:
            print(f"[Facade] Autenticação de {username} falhou (usuário ou senha inválidos).")
            return None
        
    def get_saldo(self, id_conta):
        """Método simples para o cliente buscar o saldo."""
        # Apenas delega a chamada
        return self._conta_service._get_conta(id_conta).saldo_atual

    def registrar_movimentacao(self, id_conta, tipo, valor, descricao):
        """
        O método mais importante do Facade.
        Ele orquestra MÚLTIPLOS subsistemas (atualiza saldo E salva histórico).
        """
        print(f"\n[Facade] Recebida nova movimentação: {descricao} (R$ {valor})")
        try:
            # Garante que o valor é um Decimal e positivo
            valor_decimal = Decimal(str(valor))
            if valor_decimal <= 0:
                print("[Facade] FALHA: O valor deve ser positivo.")
                return False

            # --- ORQUESTRAÇÃO ---
            # 1. Chama o primeiro subsistema (Conta)
            self._conta_service.atualizar_saldo_conta(id_conta, valor_decimal, tipo)
            
            # 2. Se o passo 1 deu certo, cria o objeto da movimentação
            nova_mov = Movimentacao(
                id_movimentacao=f"mov-{uuid.uuid4().hex[:6]}",
                id_conta_associada=id_conta,
                tipo=tipo,
                valor=valor_decimal,
                data=datetime.now(), # Pega a data E hora exatas
                descricao=descricao
            )
            
            # 3. Chama o segundo subsistema (Movimentacao)
            self._mov_service.salvar_movimentacao(nova_mov)
            # --------------------
            
            print(f"[Facade] Movimentação '{descricao}' registrada com sucesso.")
            return True # Sucesso
        
        except ValueError as e:
            # Captura erros de 'atualizar_saldo_conta' (ex: saldo insuficiente)
            print(f"[Facade] FALHA ao registrar '{descricao}': {e}")
            return False # Falha
        except Exception as e:
            # Captura outros erros (ex: digitar 'abc' no valor)
            print(f"[Facade] FALHA: Erro inesperado. Verifique os valores. ({e})")
            return False

    def get_historico_receitas(self, id_conta):
        """Método simples para o cliente pedir o histórico de receitas."""
        # Apenas delega
        return self._mov_service.get_historico_por_tipo(id_conta, 'receita')

    def get_historico_despesas(self, id_conta):
        """Método simples para o cliente pedir o histórico de despesas."""
        # Apenas delega
        return self._mov_service.get_historico_por_tipo(id_conta, 'despesa')

# --- 4. MENU INTERATIVO ---


# --- 4. MENU INTERATIVO ---

if __name__ == "__main__":
    print("--- BEM-VINDO AO SEU APP DE FINANÇAS ---")

    # 1. Inicializa o Facade 
    app_financeiro = FinanceFacade()

    # 2. Loop de Autenticação (Login / Criação)
    minha_conta_logada = None # Começa deslogado
    while minha_conta_logada is None: # Loop continua ENQUANTO o usuário não logar
        print("\n" + "="*30)
        print("--- LOGIN / CRIAÇÃO DE CONTA ---")
        print("1. Fazer Login")
        print("2. Criar Nova Conta")
        print("3. Sair do Programa")
        escolha_auth = input("Digite sua opção: ")
        
        if escolha_auth == '1':
            # --- LOGIN ---
            print("\n--- Fazer Login ---")
            username = input("Nome de usuário: ")
            senha_usuario = getpass.getpass("Senha: ") 
            minha_conta_logada = app_financeiro.autenticar_usuario(username, senha_usuario)
            if minha_conta_logada is None:
                print("\n[ERRO] Nome de usuário ou senha incorretos.")
                
        elif escolha_auth == '2':
            print("\n--- Criar Nova Conta ---")
            username = input("Nome de usuário (para login, ex: pedro123): ")
            nome_completo = input("Seu nome completo (ex: Pedro da Silva): ")
            senha_usuario = getpass.getpass("Digite sua nova senha: ")

            minha_conta_logada = app_financeiro.criar_nova_conta(
                username=username,
                nome_completo=nome_completo,
                senha=senha_usuario
            )

            if minha_conta_logada:
                print("✅ Conta criada com sucesso! Seu saldo inicial é R$ 0,00.")
            else:
                print("\n[ERRO] Não foi possível criar a conta (talvez o nome de usuário já exista?).")


        elif escolha_auth == '3':
            print("Saindo...")
            quit()
                
        else:
            print("Opção inválida.")

    # --- SUCESSO NO LOGIN ---
    print("\n" + "="*30)
    print(f"Bem-vindo(a), {minha_conta_logada.nome_completo}!")
    print(f"(Login: {minha_conta_logada.username})")
    print("="*30)

    id_da_minha_conta = minha_conta_logada.id_conta

    # 3. Loop do Menu Principal
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print(f"Conta: {minha_conta_logada.nome_completo} | Saldo atual: R$ {app_financeiro.get_saldo(id_da_minha_conta)}")
        print("1. Adicionar Receita")
        print("2. Adicionar Despesa")
        print("3. Ver Histórico de Receitas")
        print("4. Ver Histórico de Despesas")
        print("5. Sair (Logout)")
        print("="*30)
        
        escolha = input("Digite o número da opção: ")

        if escolha == '1' or escolha == '2':
            tipo_mov = "receita" if escolha == '1' else "despesa"
            valor_mov = input(f"Digite o valor da {tipo_mov} (ex: 50.75): ")
            desc_mov = input(f"Digite a descrição da {tipo_mov}: ")
            
            app_financeiro.registrar_movimentacao(
                id_conta=id_da_minha_conta,
                tipo=tipo_mov,
                valor=valor_mov,
                descricao=desc_mov
            )

        elif escolha == '3':
            print("\n--- Histórico de Receitas ---")
            historico = app_financeiro.get_historico_receitas(id_da_minha_conta)
            total_receitas = sum((mov.valor for mov in historico), Decimal('0.0'))
            if not historico:
                print("Nenhuma receita encontrada.")
            else:
                for mov in historico:
                    data_formatada = mov.data.strftime("%d/%m/%Y às %H:%M")
                    print(f"  - Data: {data_formatada} | Valor: R$ {mov.valor:>10.2f} | Descrição: {mov.descricao}")
            print("-" * 30)
            print(f"TOTAL DE RECEITAS: R$ {total_receitas:>10.2f}")

        elif escolha == '4':
            print("\n--- Histórico de Despesas ---")
            historico = app_financeiro.get_historico_despesas(id_da_minha_conta)
            total_despesas = sum((mov.valor for mov in historico), Decimal('0.0'))
            if not historico:
                print("Nenhuma despesa encontrada.")
            else:
                for mov in historico:
                    data_formatada = mov.data.strftime("%d/%m/%Y às %H:%M")
                    print(f"  - Data: {data_formatada} | Valor: R$ {mov.valor:>10.2f} | Descrição: {mov.descricao}")
            print("-" * 30)
            print(f"TOTAL DE DESPESAS: R$ {total_despesas:>10.2f}")

        elif escolha == '5':
            print(f"Fazendo logout, {minha_conta_logada.nome_completo}. Seus dados estão salvos.")
            break
        
        else:
            print("Opção inválida.")

