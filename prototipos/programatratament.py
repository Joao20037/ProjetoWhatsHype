import pandas as pd
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

# Variáveis globais para armazenar os DataFrames
df_original = None
df_filtered = None
data_view_text = None  # Defina data_view_text como uma variável global
video_titles_listbox = None  # Defina video_titles_listbox como uma variável global

# Função para carregar arquivo CSV
def load_csv():
    global df_original
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df_original = pd.read_csv(file_path)
        status_bar.config(text=f"Arquivo carregado: {file_path}")
    else:
        status_bar.config(text="Nenhum arquivo selecionado")

# Função para filtrar os dados
def filter_data(filters):
    global df_filtered
    if df_original is None:
        status_bar.config(text="Nenhum arquivo CSV carregado")
        return

    df_filtered = df_original.copy()

    # Aplicar filtros
    for col, value in filters.items():
        if callable(value):
            df_filtered = df_filtered[df_filtered[col].apply(value)]
        else:
            df_filtered = df_filtered[df_filtered[col] == value]

    status_bar.config(text="Dados filtrados")
    update_video_titles_listbox()

# Função para atualizar a lista de títulos de vídeos
def update_video_titles_listbox():
    video_titles_listbox.delete(0, tk.END)  # Limpa a lista atual
    if df_filtered is not None and not df_filtered.empty:
        video_ids = df_filtered['Video ID'].unique()
        for video_id in video_ids[:10]:  # Limita a exibição aos 10 primeiros vídeos
            title = df_filtered[df_filtered['Video ID'] == video_id]['Title'].iloc[0]
            video_titles_listbox.insert(tk.END, title)

# Função para exibir gráficos quando um título de vídeo for selecionado
def show_video_graph():
    selected_title_index = video_titles_listbox.curselection()
    if selected_title_index:
        selected_title = video_titles_listbox.get(selected_title_index)
        selected_video_df = df_original[df_original['Title'] == selected_title]
        plot_video_evolution(selected_video_df)

# Função para plotar gráficos de evolução dos likes e likes+comentários
def plot_video_evolution(df):
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))

    axes[0].plot(df['Data da Pesquisa'], df['Like Count'], marker='o', color='blue')
    axes[0].set_title('Evolução de Likes')
    axes[0].set_xlabel('Data da Pesquisa')
    axes[0].set_ylabel('Likes')
    axes[0].set_yscale('log')  # Aplicando escala logarítmica ao eixo y

    axes[1].plot(df['Data da Pesquisa'], df['Like Count'], marker='o', color='green', label='Likes')
    axes[1].plot(df['Data da Pesquisa'], df['Comment Count'], marker='s', color='red', label='Comentários')
    axes[1].set_title('Evolução de Likes e Comentários')
    axes[1].set_xlabel('Data da Pesquisa')
    axes[1].set_ylabel('Quantidade')
    axes[1].legend()
    axes[1].set_yscale('log')  # Aplicando escala logarítmica ao eixo y

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Função para criar a interface gráfica
def create_gui():
    global data_view_text, video_titles_listbox  # Declare data_view_text e video_titles_listbox como global
    # Crie a janela principal
    root = tk.Tk()
    root.title("Análise de Vídeos Musicais")

    # Barra de menu
    menu_bar = tk.Menu(root)

    # Menu Arquivo
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Carregar CSV", command=load_csv)
    file_menu.add_separator()
    file_menu.add_command(label="Sair", command=root.quit)
    menu_bar.add_cascade(label="Arquivo", menu=file_menu)

    # Menu Filtros
    filters_menu = tk.Menu(menu_bar, tearoff=0)
    filters_submenu = tk.Menu(filters_menu, tearoff=0)
    filters_submenu.add_command(label="10 Vídeos Mais Populares", command=lambda: filter_data({}))
    filters_submenu.add_command(label="Vídeos Publicados a partir de 2024", command=lambda: filter_data({'Published At': lambda x: x.year >= 2024}))
    filters_menu.add_cascade(label="Opções de Filtragem", menu=filters_submenu)
    menu_bar.add_cascade(label="Filtros", menu=filters_menu)

    root.config(menu=menu_bar)

    # Status Bar
    global status_bar
    status_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Lista de títulos de vídeos
    video_titles_listbox = tk.Listbox(root)
    video_titles_listbox.pack(side=tk.LEFT, expand=True, fill="both", padx=10, pady=10)
    video_titles_listbox.bind("<<ListboxSelect>>", lambda event: show_video_graph())

    root.mainloop()

# Inicialize a interface gráfica
create_gui()
