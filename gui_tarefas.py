import tkinter as tk
from tkinter import messagebox
import json

# --- 1. FUNÇÕES DO ARQUIVO JSON (BANCO DE DADOS) ---
def ler_tarefas():
    """Lê o arquivo ao iniciar o programa."""
    try:
        with open('tasks.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return [] # Se o arquivo não existir ainda, começa vazio

def salvar_tarefas():
    """Salva a lista atual no arquivo tasks.json."""
    with open('tasks.json', 'w', encoding='utf-8') as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)


# --- 2. NOSSA LÓGICA DE DADOS ---
# Em vez de começar vazio com [], já carregamos do HD direto no início!
tarefas = ler_tarefas()
tarefas_redo = []

def atualizar_tela():
    """Limpa a lista visual e desenha os itens de novo com a numeração."""
    lista_visual.delete(0, tk.END)
    for i, tarefa in enumerate(tarefas, start=1):
        lista_visual.insert(tk.END, f"{i}. {tarefa}")

def adicionar():
    texto = campo_entrada.get().strip()
    if texto:
        tarefas.append(texto)
        tarefas_redo.clear()
        salvar_tarefas()  # <-- SALVA NO ARQUIVO AQUI
        campo_entrada.delete(0, tk.END)
        atualizar_tela()
    else:
        messagebox.showwarning("Aviso", "Por favor, digite uma tarefa!")

def desfazer():
    if tarefas:
        removida = tarefas.pop()
        tarefas_redo.append(removida)
        salvar_tarefas()  # <-- SALVA NO ARQUIVO AQUI
        atualizar_tela()
    else:
        messagebox.showinfo("Undo", "Nenhuma tarefa para desfazer!")

def refazer():
    if tarefas_redo:
        recuperada = tarefas_redo.pop()
        tarefas.append(recuperada)
        salvar_tarefas()  # <-- SALVA NO ARQUIVO AQUI
        atualizar_tela()
    else:
        messagebox.showinfo("Redo", "Nenhuma tarefa para refazer!")

def fechar_programa():
    """Garante o salvamento uma última vez antes de fechar."""
    salvar_tarefas()
    janela.destroy()


# --- 3. CONSTRUINDO A JANELA VISUAL ---
janela = tk.Tk()
janela.title("Meu Gerenciador de Tarefas")
janela.geometry("380x450")
janela.config(padx=20, pady=20)

# Título
titulo = tk.Label(janela, text="Lista de Tarefas", font=("Arial", 16, "bold"))
titulo.pack(pady=(0, 10))

# Campo de digitação e Botão de Adicionar
frame_entrada = tk.Frame(janela)
frame_entrada.pack(fill=tk.X, pady=5)

campo_entrada = tk.Entry(frame_entrada, font=("Arial", 12))
campo_entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

btn_adicionar = tk.Button(frame_entrada, text="Adicionar", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=adicionar)
btn_adicionar.pack(side=tk.RIGHT)

# Caixa de Listagem das Tarefas
lista_visual = tk.Listbox(janela, font=("Arial", 12), height=12, selectbackground="#a6a6a6")
lista_visual.pack(fill=tk.BOTH, expand=True, pady=10)

# Frame para Undo e Redo
frame_botoes = tk.Frame(janela)
frame_botoes.pack(fill=tk.X, pady=5)

btn_undo = tk.Button(frame_botoes, text="↩ Desfazer (Undo)", command=desfazer)
btn_undo.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

btn_redo = tk.Button(frame_botoes, text="↪ Refazer (Redo)", command=refazer)
btn_redo.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=2)

# Botão para Sair (Agora usando a nossa função fechar_programa!)
btn_sair = tk.Button(janela, text="Sair do Aplicativo", fg="red", command=fechar_programa)
btn_sair.pack(fill=tk.X, pady=(10, 0))

# MÁGICA: Assim que a janela é criada, chamamos atualizar_tela() para 
# desenhar as tarefas que foram lidas do JSON logo na abertura do app!
atualizar_tela()

# Inicia o loop da janela
janela.mainloop()