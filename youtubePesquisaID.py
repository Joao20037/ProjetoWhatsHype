from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pandas as pd


# Configurar suas credenciais
API_KEY = 'AIzaSyB4qoflIBJ_8xLCF-g6Bbp3COizMOpzY38'  # ou TOKEN_OAUTH2, dependendo da autenticação que você está usando

# Construir o serviço da API do YouTube
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Função para pesquisar vídeos por categoria e termo no título
def pesquisa(id_categoria, termo, max_results=100):
    # Lista de vídeos encontrados
    videos_found = []

    # Número total de resultados encontrados
    resultado_total = 0

    # Número de resultados por página
    resultados_por_pagina = 50  # Máximo de resultados por página

    # Número total de páginas que precisam ser buscadas
    total_paginas = min(max_results // resultados_por_pagina, max_results)

    request = youtube.search().list(
        part='snippet',
        q=termo,
        type='video',
        videoCategoryId=id_categoria,
        maxResults=min(resultados_por_pagina, max_results - resultado_total)  # Limitar ao máximo de resultados desejado
    )

    # Iterar sobre todas as páginas de resultados
    while request and resultado_total < max_results:
        response = request.execute()

        # Adicionar os vídeos encontrados à lista
        for item in response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            channel_title = item['snippet']['channelTitle']
            published_at = item['snippet']['publishedAt']
            description = item['snippet']['description']  # 1. Adicionando descrição
            tags = item['snippet'].get('tags', [])  # 1. Adicionando tags
            channel_id = item['snippet']['channelId']  # 1. Adicionando ID do canal
            view_count = get_contador_de_view(video_id)  # Adiciona a contagem de visualizações
            like_count, dislike_count, comment_count = get_video_stats(video_id)  # 2. Adicionando estatísticas
            region_restriction = item['snippet'].get('regionRestriction', {})  # 3. Adicionando restrições regionais
            relevant_topics = item.get('relevantTopicIds', [])  # 6. Adicionando tópicos relevantes
            live_streaming_details = item.get('liveStreamingDetails', {})  # 7. Adicionando detalhes de transmissão ao vivo
            videos_found.append([video_id, title, channel_title, published_at, description, tags, channel_id, view_count, like_count, dislike_count, comment_count, region_restriction, relevant_topics, live_streaming_details])
            resultado_total += 1

            # Verificar se atingiu o limite máximo de resultados
            if resultado_total >= max_results:
                break

        # Verificar se há mais páginas de resultados
        if resultado_total < max_results:
            request = youtube.search().list_next(request, response)

    return pd.Dataframe(videos_found)
    
# Função para obter a contagem de visualizações de um vídeo
def get_contador_de_view(video_id):
    request = youtube.videos().list(
        part='statistics',
        id=video_id
    )
    response = request.execute()
    if 'items' in response and response['items']:
        return int(response['items'][0]['statistics']['viewCount'])
    return 0

# Função para obter estatísticas de vídeo (curtidas, descurtidas, comentários)
def get_video_stats(video_id):
    request = youtube.videos().list(
        part='statistics',
        id=video_id
    )
    response = request.execute()
    if 'items' in response and response['items']:
        item = response['items'][0]['statistics']
        like_count = int(item.get('likeCount', 0))
        dislike_count = int(item.get('dislikeCount', 0))
        comment_count = int(item.get('commentCount', 0))
        return like_count, dislike_count, comment_count
    return 0, 0, 0

# Função para salvar os dados em um arquivo CSV
def save_to_csv(data, filename):
    # Tentar carregar o arquivo CSV se já existir, caso contrário, criar um novo DataFrame
    try:
        df = pd.read_csv(filename, encoding='utf-8')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Video ID', 'Title', 'Channel Title', 'Published At', 'Description', 'Tags', 'Channel ID', 'View Count', 'Like Count', 'Dislike Count', 'Comment Count', 'Region Restriction', 'Relevant Topics', 'Live Streaming Details'])

    # Adicionar novos dados ao DataFrame
    novos_dados = pd.DataFrame(data, columns=['Video ID', 'Title', 'Channel Title', 'Published At', 'Description', 'Tags', 'Channel ID', 'View Count', 'Like Count', 'Dislike Count', 'Comment Count', 'Region Restriction', 'Relevant Topics', 'Live Streaming Details'])
    df = pd.concat([df, novos_dados], ignore_index=True)

    # Salvar o DataFrame de volta ao arquivo CSV
    df.to_csv(filename, index=False, encoding='utf-8')


#POR ENQUANTO AS CHAMADAS DE FUNÇÕES PARA EXECUTAR AS PESQUISAS ESTÃO COMENTADAS POR MOTIVOS DE:
# PRECISO MODULARIZAR PARA PODER ESCOLHER ENTRE 2 OU + TERMOS DE PESQUISA
#   PRECISO IMPLEMENTAR A COLUNA DATA DE PESQUISA COM A DATA DD/MM/AAAA
#       PRECISO ESCOLHER MAIS IDS E TERMOS DE PESQUISA DENTRO DOS IDS JÁ USADOS



#CASO PRECISE EXECUTAR A PESQUISA, DESCOMENTAR, EXECUTAR E RECOMENTAR


#PESQUISA ID 10 - "Música"

# # ID da categoria desejada (consulte o arquivo anotacoes.txt)
# id_categoria = '10'
# termo = 'Música'

# # Pesquisar vídeos
# resultados_pesquisa = pesquisa(id_categoria, termo)

# # Salvar os resultados em um arquivo CSV
# save_to_csv(resultados_pesquisa, 'videos_musica.csv')

# # PESQUISA ID 20 - "Gaming"

# # ID da categoria desejada (você pode obter isso através da API)
# id_categoria = '20'
# termo = 'Gameplay'

# # Pesquisar vídeos
# resultados_pesquisa = search_videos_by_category_and_term(id_categoria, termo)

# # Salvar os resultados em um arquivo CSV
# save_to_csv(resultados_pesquisa, 'videos_gameplay.csv')