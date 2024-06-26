import redditwarp.SYNC
import pandas as pd 


client = redditwarp.SYNC.Client()

def main():
    print("Codigo ira pesquisar por um tema, pegar os subrredits relacionados ao tema")
    print("Fazer a chamada dos 1000 top posts do ano e salvar em um csv")
    theme =  input("Tema a ser escolhido: ")
    file_path = input("Nome do csv a ser salvo: ")
    file_path += ".csv"
    data = []
    lista_de_maps_subReddit = [i.name for i in client.p.subreddit.search(theme)]
    for sub in lista_de_maps_subReddit:
        # Pega top 1000 posts do ano
        sub_reddit_posts = client.p.subreddit.pull.top(sub, 1000, time="year")
        for post in subreddit_posts:
            post_data = {
                'Title': post.title,
                'Score': post.score,
                'Num_Comments': post.num_comments,
                'Author': post.author.name if post.author else None,
                'Subreddit': post.subreddit.name,
                'Created_Time': post.created_utc,
                'URL': post.permalink,
                'Post_Type': post.post_hint,
                'Content': post.selftext if hasattr(post, 'selftext') else None,
                'Flair': post.link_flair_text if hasattr(post, 'link_flair_text') else None
            }
            data.append(post_data)
    
    df = pd.DataFrame(data)
    df.to_csv(file_path)
    
if "__main__" == __name__:
    main()