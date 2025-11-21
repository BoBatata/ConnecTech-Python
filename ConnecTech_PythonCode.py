import pandas as pd

# Banco de dados
db = {
    "usuarios": pd.DataFrame(columns=["nome", "email", "senha", "pontos"]),
    "equipes": pd.DataFrame(columns=["nome", "membros"]),  
    "projetos": pd.DataFrame(columns=["nome", "time"]),    
    "entregas": pd.DataFrame(columns=["titulo", "projeto", "finalizada"]),
    "tarefas": pd.DataFrame(columns=["titulo", "projeto", "entrega", "status", "responsavel", "pontos"])
}


# Retira os espaços dos lados da mensagem recebida
def obrigatorio(msg):
    s = ""
    while s.strip() == "":
        s = input(msg).strip()
    return s

# Funções usadas para procurar informações no Banco de Dados
# e checar se já são existentes.
def procurar_usuario(nome):
    usuarios = db["usuarios"]
    if "nome" in usuarios.columns:
        for n in usuarios["nome"].values:
            if n == nome:
                return True
    return False

def procurar_email(email):
    usuarios = db["usuarios"]
    if "email" in usuarios.columns:
        for e in usuarios["email"].values:
            if e == email:
                return True
    return False

def procurar_equipe(nome_equipe):
    equipes = db["equipes"]
    for n in equipes["nome"].values:
        if n == nome_equipe:
            return True
    return False

def procurar_projeto(nome_projeto):
    projetos = db["projetos"]
    for n in projetos["nome"].values:
        if n == nome_projeto:
            return True
    return False

def procurar_entrega(titulo):
    entregas = db["entregas"]
    for t in entregas["titulo"].values:
        if t == titulo:
            return True
    return False

def procurar_tarefa(titulo):
    tarefas = db["tarefas"]
    for t in tarefas["titulo"].values:
        if t == titulo:
            return True
    return False


# Cria um usuário apartir do nome, email e senha.
# Começa com 0 pontos, quer seriam ganhados fazendo as tarefas
# no Planner Gameficado.
def criar_usuario():
    print("\n Criar Usuário: ")
    nome = obrigatorio("Nome: ")
    if procurar_usuario(nome):
        print("Nome de usuário já existe. Escolha outro.")
        return False

    email = obrigatorio("Email: ")
    if procurar_email(email):
        print("Email já cadastrado.")
        return False

    senha = obrigatorio("Senha: ")

    novo = pd.DataFrame([{
        "nome": nome,
        "email": email,
        "senha": senha,
        "pontos": 0
    }])
    db["usuarios"] = pd.concat([db["usuarios"], novo], ignore_index=True)
    print("Usuário criado:", nome)
    return True

# Lista todos os usuários salvos no banco de dados.
def listar_usuarios():
    print("\n Usuários: ")
    if db["usuarios"].empty:
        print("Nenhum usuário cadastrado.")
    else:
        print(db["usuarios"].to_string(index=False))

# Loga o usuário se a conta já estiver salva no banco de dados.
# Nesse caso é apenas uma verificação.
# Retornando se o login foi bem sucedido ou não.
def login():
    print("\n Login: ")
    email = obrigatorio("Email: ")
    senha = obrigatorio("Senha: ")
    usuarios = db["usuarios"]
    usuarioEncontrado = False
    for i in range(len(usuarios)):
        if usuarios.at[i, "email"] == email and usuarios.at[i, "senha"] == senha:
            print("Login bem-sucedido. Usuário:", usuarios.at[i, "nome"])
            usuarioEncontrado = True
    if usuarioEncontrado == False:
        print("Credenciais inválidas.")


# Cria uma Equipe, recebe o nome do criador, se ele não existir retorna um print.
# o nome da equipe, se já existir retorna um print.
def criar_equipe():
    print("\n Criar Equipe ")
    criador = obrigatorio("Nome do criador: ")
    if procurar_usuario(criador) == False:
        print("Criador não encontrado")
        return False

    nome_equipe = obrigatorio("Nome da equipe: ")
    if procurar_equipe(nome_equipe):
        print("Já existe uma equipe com esse nome")
        return False

    nova = pd.DataFrame([{"nome": nome_equipe, "membros": [criador]}])
    db["equipes"] = pd.concat([db["equipes"], nova], ignore_index=True)
    print("Equipe criada:", nome_equipe)
    return True

# Lista as equipes que certo usuário está.
def listar_minhas_equipes():
    usuario = obrigatorio("Seu nome: ")
    print("\n Minhas equipes ")
    encontrouEquipe = False
    for _, row in db["equipes"].iterrows():
        membros = row["membros"]
        for m in membros:
            if m == usuario:
                print(row["nome"])
                encontrouEquipe = True
                break
    if encontrouEquipe == False:
        print("Nenhuma equipe encontrada para esse usuário.")

# Cria um projeto com o nome do usuario e da equipe
# Checa se ambos existem e se usuario faz parte da equipe antes de criar.
# Checa se já existe um projeto com o mesmo nome.
def criar_projeto():
    print("\n-- Criar Projeto --")
    usuario = obrigatorio("Seu nome: ")
    equipe = obrigatorio("Nome da equipe: ")

    if procurar_equipe(equipe) == False:
        print("Equipe não encontrada.")
        return False

    membros = []
    for _, row in db["equipes"].iterrows():
        if row["nome"] == equipe:
            membros = row["membros"]
            break

    permitido = False
    for m in membros:
        if m == usuario:
            permitido = True
            break

    if permitido == False:
        print("Usuário não pertence à equipe.")
        return False

    nome_projeto = obrigatorio("Nome do projeto: ")
    if procurar_projeto(nome_projeto):
        print("Já existe um projeto com esse nome.")
        return False

    novo = pd.DataFrame([{"nome": nome_projeto, "time": equipe}])
    db["projetos"] = pd.concat([db["projetos"], novo], ignore_index=True)
    print("Projeto criado:", nome_projeto)
    return True


# Lista todos os projetos de uma equipe especifica.
def listar_projetos():
    equipe = obrigatorio("Nome da equipe: ")
    filtrado = db["projetos"][db["projetos"]["time"] == equipe]
    print("\n-- Projetos da equipe", equipe, "--")
    if filtrado.empty:
        print("Nenhum projeto encontrado.")
    else:
        print(filtrado.to_string(index=False))

# Cria uma entrega para ser realizada em um projeto.
# Verifica se já existe uma entrega com o mesmo nome.
def criar_entrega():
    print("\n Criar Entrega ")
    projeto = obrigatorio("Nome do projeto: ")
    if procurar_projeto(projeto) == False:
        print("Projeto não encontrado.")
        return False

    titulo = obrigatorio("Título da entrega: ")
    if procurar_entrega(titulo):
        print("Já existe uma entrega com esse título.")
        return False

    novo = pd.DataFrame([{"titulo": titulo, "projeto": projeto, "finalizada": False}])
    db["entregas"] = pd.concat([db["entregas"], novo], ignore_index=True)
    print("Entrega criada:", titulo)
    return True

# Finaliza uma entrega, recebe o título da entrega a ser finalizada.
# Retorna False caso não encontrada.
# Retorna False caso ainda existam tarefas pendetes.
def finalizar_entrega():
    titulo = obrigatorio("Título da entrega a finalizar: ")
    if procurar_entrega(titulo) == False:
        print("Entrega não encontrada.")
        return False

    for _, t in db["tarefas"].iterrows():
        if t["entrega"] == titulo and t["status"] != "done":
            print("Ainda existem tarefas pendentes vinculadas a essa entrega.")
            return False

    for i in range(len(db["entregas"])):
        if db["entregas"].at[i, "titulo"] == titulo:
            db["entregas"].at[i, "finalizada"] = True
            print("Entrega finalizada:", titulo)
            return True

    return False


# Cria uma  tarefa para um projeto.
# Verifica se responsável existe.
# Verifica se o projeto existe.
def criar_tarefa():
    print("\n Criar Tarefa ")
    responsavel = obrigatorio("Nome do responsável: ")
    if procurar_usuario(responsavel) == False:
        print("Responsável não encontrado.")
        return False

    projeto = obrigatorio("Nome do projeto: ")
    if procurar_projeto(projeto) == False:
        print("Projeto não encontrado.")
        return False

    entrega = input("Título da entrega (opcional): ").strip()
    if entrega != "" and procurar_entrega(entrega) == False:
        print("Entrega não encontrada (se deseja, deixe vazio).")
        return False

    titulo = obrigatorio("Título da tarefa (único): ")
    if procurar_tarefa(titulo):
        print("Já existe uma tarefa com esse título.")
        return False

    novo = pd.DataFrame([{
        "titulo": titulo,
        "projeto": projeto,
        "entrega": entrega if entrega != "" else None,
        "status": "open",
        "responsavel": responsavel,
        "pontos": 10
    }])
    db["tarefas"] = pd.concat([db["tarefas"], novo], ignore_index=True)
    print("Tarefa criada:", titulo)
    return True

# Muda o status de uma tarefa.
# Se a tarefa for concluida soma os pontos na conta do responsavel pela tarefa.
def mudar_status():
    print("\n Mudar Status da Tarefa ")
    usuario = obrigatorio("Seu nome: ")
    titulo = obrigatorio("Título da tarefa: ")

    if procurar_tarefa(titulo) == False:
        print("Tarefa não encontrada.")
        return False

    novo = obrigatorio("Novo status (open / doing / review / done): ")

    for i in range(len(db["tarefas"])):
        if db["tarefas"].at[i, "titulo"] == titulo:
            db["tarefas"].at[i, "status"] = novo
            responsavel = db["tarefas"].at[i, "responsavel"]
            pontos = db["tarefas"].at[i, "pontos"]
            if novo == "done" and responsavel == usuario:
                for j in range(len(db["usuarios"])):
                    if db["usuarios"].at[j, "nome"] == usuario:
                        db["usuarios"].at[j, "pontos"] = db["usuarios"].at[j, "pontos"] + pontos
                        print("Tarefa marcada como done e pontos somados ao usuário.")
                        break
            else:
                print("Status atualizado.")
            return True

    return False

# Vizualiza a tabela completa.
def visualizar_tabela():
    for nome, df in db.items():
        print(f"\n=== {nome} ===")
        if df.empty:
            print("Vazio")
        else:
            print(df.to_string(index=False))


# popula o banco com dados dados de exemplo.
def popular_exemplo():
    # apenas se estiver vazio
    if db["usuarios"].empty:
        db["usuarios"] = pd.DataFrame([
            {"nome": "Alice", "email": "alice@test.com", "senha": "123", "pontos": 120},
            {"nome": "Bruno", "email": "bruno@test.com", "senha": "123", "pontos": 80},
            {"nome": "Carla", "email": "carla@test.com", "senha": "123", "pontos": 150}
        ])
    if db["equipes"].empty:
        db["equipes"] = pd.DataFrame([
            {"nome": "Time Um", "membros": ["Alice", "Bruno"]},
            {"nome": "Time Dois",  "membros": ["Carla"]}
        ])
    if db["projetos"].empty:
        db["projetos"] = pd.DataFrame([
            {"nome": "Sistema IoT", "time": "Time Alpha"},
            {"nome": "Plataforma Web", "time": "Time Alpha"},
            {"nome": "App Mobile", "time": "Time Beta"}
        ])
    if db["entregas"].empty:
        db["entregas"] = pd.DataFrame([
            {"titulo": "Montar protótipo", "projeto": "Sistema IoT", "finalizada": False},
            {"titulo": "Dashboard MQTT", "projeto": "Sistema IoT", "finalizada": True},
            {"titulo": "Design do frontend", "projeto": "Plataforma Web", "finalizada": False},
            {"titulo": "Autenticação no app", "projeto": "App Mobile", "finalizada": True}
        ])
    if db["tarefas"].empty:
        db["tarefas"] = pd.DataFrame([
            {"titulo": "Montar circuito ESP32", "projeto": "Sistema IoT", "entrega": "Montar protótipo", "status": "done", "responsavel": "Alice", "pontos": 30},
            {"titulo": "Testar sensores", "projeto": "Sistema IoT", "entrega": "Montar protótipo", "status": "open", "responsavel": "Bruno", "pontos": 20},
            {"titulo": "Criar API MQTT", "projeto": "Sistema IoT", "entrega": "Dashboard MQTT", "status": "done", "responsavel": "Alice", "pontos": 25},
            {"titulo": "Exibir dados em tempo real", "projeto": "Sistema IoT", "entrega": "Dashboard MQTT", "status": "done", "responsavel": "Bruno", "pontos": 25},
            {"titulo": "Criar protótipo no Figma", "projeto": "Plataforma Web", "entrega": "Design do frontend", "status": "done", "responsavel": "Carla", "pontos": 40},
            {"titulo": "Construir layout responsivo", "projeto": "Plataforma Web", "entrega": "Design do frontend", "status": "open", "responsavel": "Alice", "pontos": 20},
            {"titulo": "Tela de login", "projeto": "App Mobile", "entrega": "Autenticação no app", "status": "done", "responsavel": "Carla", "pontos": 30},
            {"titulo": "Integração Firebase", "projeto": "App Mobile", "entrega": "Autenticação no app", "status": "open", "responsavel": "Carla", "pontos": 50}
        ])
    print("Banco de dados de exemplo populado.")


# Main para navegação e simulação do Planner Gameficado.
def main():
    popular_exemplo()

    while True:
        print("""
1  - Criar usuário
2  - Listar usuários
3  - Login (verificação)
4  - Criar equipe
5  - Minhas equipes
6  - Criar projeto
7  - Listar projetos da equipe
8  - Criar entrega
9  - Finalizar entrega
10 - Criar tarefa
11 - Mudar status da tarefa
12 - Exportar tabelas
0  - Sair
""")
        op = obrigatorio("Escolha uma opção: ")

        if op == "0":
            print("Saindo...")
            break
        elif op == "1":
            criar_usuario()
        elif op == "2":
            listar_usuarios()
        elif op == "3":
            login()
        elif op == "4":
            criar_equipe()
        elif op == "5":
            listar_minhas_equipes()
        elif op == "6":
            criar_projeto()
        elif op == "7":
            listar_projetos()
        elif op == "8":
            criar_entrega()
        elif op == "9":
            finalizar_entrega()
        elif op == "10":
            criar_tarefa()
        elif op == "11":
            mudar_status()
        elif op == "12":
            visualizar_tabela()
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
