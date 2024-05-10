from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import csv

# Configurar suas credenciais
API_KEY = 'AIzaSyB4qoflIBJ_8xLCF-g6Bbp3COizMOpzY38'  # ou TOKEN_OAUTH2, dependendo da autenticação que você está usando

# Construir o serviço da API do YouTube
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Função para pesquisar vídeos por categoria e termo no título
def search_videos_by_category_and_term(category_id, search_term, max_results=100):
    # Lista de vídeos encontrados
    videos_found = []

    # Número total de resultados encontrados
    total_results = 0

    # Número de resultados por página
    results_per_page = 50  # Máximo de resultados por página

    # Número total de páginas que precisam ser buscadas
    total_pages = min(max_results // results_per_page, max_results)

    # Primeira página de resultados
    request = youtube.search().list(
        part='snippet',
        q=search_term,
        type='video',
        videoCategoryId=category_id,
        maxResults=min(results_per_page, max_results - total_results)  # Limitar ao máximo de resultados desejado
    )

    # Iterar sobre todas as páginas de resultados
    while request and total_results < max_results:
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
            view_count = get_video_view_count(video_id)  # Adiciona a contagem de visualizações
            like_count, dislike_count, comment_count = get_video_stats(video_id)  # 2. Adicionando estatísticas
            region_restriction = item['snippet'].get('regionRestriction', {})  # 3. Adicionando restrições regionais
            relevant_topics = item.get('relevantTopicIds', [])  # 6. Adicionando tópicos relevantes
            live_streaming_details = item.get('liveStreamingDetails', {})  # 7. Adicionando detalhes de transmissão ao vivo
            videos_found.append([video_id, title, channel_title, published_at, description, tags, channel_id, view_count, like_count, dislike_count, comment_count, region_restriction, relevant_topics, live_streaming_details])
            total_results += 1

            # Verificar se atingiu o limite máximo de resultados
            if total_results >= max_results:
                break

        # Verificar se há mais páginas de resultados
        if total_results < max_results:
            request = youtube.search().list_next(request, response)

    return videos_found

# Função para obter a contagem de visualizações de um vídeo
def get_video_view_count(video_id):
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
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Video ID', 'Title', 'Channel Title', 'Published At', 'Description', 'Tags', 'Channel ID', 'View Count', 'Like Count', 'Dislike Count', 'Comment Count', 'Region Restriction', 'Relevant Topics', 'Live Streaming Details'])
        writer.writerows(data)

# ID da categoria desejada (você pode obter isso através da API)
category_id = '10'  # Exemplo: Entretenimento
search_term = 'Música'  # Termo de pesquisa desejado

# Pesquisar vídeos
search_results = search_videos_by_category_and_term(category_id, search_term)

# Salvar os resultados em um arquivo CSV
save_to_csv(search_results, 'videos_found.csv')