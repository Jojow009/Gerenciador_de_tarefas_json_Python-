import os
import json

# 1. FUNÇÕES DE BANCO DE DADOS (JSON) NO TOPO DO ARQUIVO
def ler_tarefas_do_arquivo(filename='tasks.json'):
    """Tenta ler o arquivo JSON. Se não existir, retorna uma lista vazia."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return [] # Se é a primeira vez rodando, o arquivo não existe ainda

def salvar_tarefas_no_arquivo(tasks, filename='tasks.json'):
    """Salva a lista no arquivo JSON com acentuação correta e formatado."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


# 2. FUNÇÕES DE LOGICA DO PROGRAMA
def listar_tarefas(tasks):
    if not tasks:
        print("Nenhuma tarefa encontrada.")
        return
    print("\n--- Lista de tarefas ---")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")

def undo(tasks, tasks_redo):
    if not tasks:
        print("Nenhuma tarefa encontrada para desfazer.")
        return
    task = tasks.pop()
    tasks_redo.append(task)
    salvar_tarefas_no_arquivo(tasks)  # SALVA APÓS MODIFICAR
    print(f"Tarefa removida: {task}")

def redo(tasks, tasks_redo):
    if not tasks_redo:
        print("Nenhuma tarefa para refazer.")
        return
    task = tasks_redo.pop()
    tasks.append(task)
    salvar_tarefas_no_arquivo(tasks)  # SALVA APÓS MODIFICAR
    print(f"Tarefa refeita: {task}")


# 3. INICIALIZAÇÃO DO PROGRAMA
# Em vez de começar com tasks = [], carregamos o que já estava salvo no HD!
tasks = ler_tarefas_do_arquivo()
tasks_redo = []

# Dica: No Windows o comando para limpar tela é 'cls', no Linux/Mac é 'clear'.
# Esse código abaixo funciona automaticamente em qualquer um dos dois!
comando_limpar = 'cls' if os.name == 'nt' else 'clear'

print(">>> Sistema de Tarefas Iniciado!")
listar_tarefas(tasks)

while True:
    print('\nComandos: listar (ou listener), undo, redo, exit')
    task = input('Digite um comando OU uma nova tarefa: ').strip()
    comando = task.lower()
    
    if comando in ['listener', 'listar', 'list']:
        listar_tarefas(tasks)
        continue 
    
    elif comando == 'undo':
        undo(tasks, tasks_redo)
        continue
        
    elif comando == 'redo':
        os.system(comando_limpar)  # Limpa a tela sem dar erro no Windows!
        redo(tasks, tasks_redo) 
        continue
        
    elif comando == 'exit':
        print("Saindo do programa. Até logo!")
        break
        
    else:
        if task:
            tasks.append(task)
            tasks_redo.clear()
            salvar_tarefas_no_arquivo(tasks)  # SALVA A NOVA TAREFA NA HORA
            print(f"Tarefa adicionada e salva: {task}")