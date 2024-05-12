import pandas as pd
import matplotlib.pyplot as plt

# Carregar o CSV para um DataFrame
df = pd.read_csv('videos_musica.csv')

# Converter a coluna 'Data da Pesquisa' para o formato datetime
df['Data da Pesquisa'] = pd.to_datetime(df['Data da Pesquisa'])

# Selecionar os top 10 vídeos com mais visualizações
top_10 = df.groupby('Video ID').agg({'View Count': 'max', 'Title': 'first'}).nlargest(10, 'View Count')

# Criar subplots para cada um dos top 10 vídeos
fig, axs = plt.subplots(5, 2, figsize=(15, 20))

# Iterar sobre os top 10 vídeos e plotar gráficos separados
for i, (video_id, row) in enumerate(top_10.iterrows()):
    row_idx = i // 2
    col_idx = i % 2
    ax = axs[row_idx, col_idx]
    
    video_data = df[(df['Video ID'] == video_id)]
    video_data = video_data.groupby('Data da Pesquisa').agg({'View Count': 'max'}).reset_index()
    
    ax.plot(video_data['Data da Pesquisa'], video_data['View Count'])
    ax.set_title(row['Title'])
    ax.set_xlabel('Data da Pesquisa')
    ax.set_ylabel('Número de visualizações')
    ax.tick_params(axis='x', rotation=45)

# Ajustar layout
plt.tight_layout()
plt.show()