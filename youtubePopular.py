import pandas as pd
from googleapiclient.discovery import build

# Função para salvar os dados em um arquivo CSV
def save_to_csv(data, filename):
    # Carregar arquivo CSV se já existir
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Data da Pesquisa','Video ID', 'Channel Title', 'Title', 'Published At', 'Tags', 'Thumbnails', 'Category ID', 'Duration', 'View Count', 'Like Count', 'Dislike Count', 'Comment Count'])

    # Adicionar novos dados ao DataFrame
    new_df = pd.DataFrame(data, columns=['Data da Pesquisa','Video ID', 'Channel Title', 'Title', 'Published At', 'Tags', 'Thumbnails', 'Category ID', 'Duration', 'View Count', 'Like Count', 'Dislike Count', 'Comment Count'])
    df = pd.concat([df, new_df], ignore_index=True)

    # Salvar o DataFrame atualizado no arquivo CSV
    df.to_csv(filename, index=False)

# Defina sua chave de API do YouTube
API_KEY = 'AIzaSyB4qoflIBJ_8xLCF-g6Bbp3COizMOpzY38'

# Crie um serviço da API do YouTube
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Função para pesquisar vídeos
def search_videos(max_results=50):
    # Faça a solicitação para obter os vídeos mais populares
    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        chart='mostPopular',
        maxResults=max_results  # Número máximo de resultados desejados
    )

    # Execute a solicitação e obtenha a resposta
    response = request.execute()

    # Verificar se a resposta contém os itens esperados
    if 'items' in response:
        # Extrair os dados dos itens da resposta
        data = []
        for item in response['items']:
            video_id = item['id']
            video_snippet = item['snippet']
            video_content_details = item['contentDetails']
            video_statistics = item['statistics']
            channel_title = video_snippet['channelTitle']
            title = video_snippet['title']
            published_at = video_snippet['publishedAt']
            tags = ','.join(video_snippet.get('tags', []))
            thumbnails = video_snippet['thumbnails']['default']['url']
            category_id = video_snippet['categoryId']
            duration = video_content_details['duration']
            view_count = video_statistics['viewCount']
            like_count = video_statistics.get('likeCount', 0)
            dislike_count = video_statistics.get('dislikeCount', 0)
            comment_count = video_statistics.get('commentCount', 0)
            data_pesquisa = pd.Timestamp.now().strftime('%d/%m/%Y')
            data.append([data_pesquisa,video_id, channel_title, title, published_at, tags, thumbnails, category_id, duration, view_count, like_count, dislike_count, comment_count])

        # Salvar os resultados em um arquivo CSV
        save_to_csv(data, 'videos_populares.csv')

# Executar a função de pesquisa de vídeos
search_videos()