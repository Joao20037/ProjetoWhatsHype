# %%
import pandas as pd
import numpy as np

# %%
df = pd.read_csv("../csvs/EmAltaReddit.csv")
df.head()

# %% [markdown]
# ## Top10 posts por score

# %%
top10 = df.sort_values(by="Score", ascending=False)[:10]
top10

# %% [markdown]
# ## Top10 posts por numero de comentarios

# %%
top10 = df.sort_values(by="Num_Comments", ascending=False)[:10]
top10

# %% [markdown]
# ## Top10 autores que mais aparecem

# %%
df["Author"].value_counts()[:10]

# %% [markdown]
# ## Top10 Subreddit com mais posts

# %%
df["Subreddit"].value_counts()[:10]

# %% [markdown]
# ## Quantidade de posts por mes

# %%
df['Created_Time'] = pd.to_datetime(df['Created_Time'])

df['Year_Month'] = df['Created_Time'].dt.to_period('M')

monthly_posts = df.groupby('Year_Month').size().reset_index(name='Post_Count')

print(monthly_posts)

# %% [markdown]
# ## Quantidade de posts por mes e por subreddit especifico

# %%
df['Created_Time'] = pd.to_datetime(df['Created_Time'])

df['Year_Month'] = df['Created_Time'].dt.to_period('M')

monthly_posts = df.groupby(['Year_Month', 'Subreddit']).size().reset_index(name='Post_Count')

monthly_posts[monthly_posts["Subreddit"] == "CRFla"]

# %% [markdown]
# ## Quantidade de posts por mes e por autor especifico

# %%
df['Created_Time'] = pd.to_datetime(df['Created_Time'])

df['Year_Month'] = df['Created_Time'].dt.to_period('M')

monthly_posts = df.groupby(['Year_Month', 'Author']).size().reset_index(name='Post_Count')

monthly_posts[monthly_posts["Author"] == "zek_997"]

# %% [markdown]
# ## Quantidade de Score por tempo por post

# %%
df['Created_Time'] = pd.to_datetime(df['Created_Time'])

df['Year_Month'] = df['Created_Time'].dt.to_period('M')

monthly_posts = df.groupby('Year_Month')["Score"].sum().reset_index(name='Score_Sum')

monthly_posts

# %% [markdown]
# ## Quantidade de Score por tempo por subreddit

# %%
df['Created_Time'] = pd.to_datetime(df['Created_Time'])

df['Year_Month'] = df['Created_Time'].dt.to_period('M')

monthly_posts = df.groupby(['Year_Month', 'Subreddit'])["Score"].sum().reset_index(name='Score_Sum')

monthly_posts[monthly_posts["Subreddit"] == "CRFla"]

# %% [markdown]
# ## Quantidade de Score por tempo por autor

# %%
df['Created_Time'] = pd.to_datetime(df['Created_Time'])

df['Year_Month'] = df['Created_Time'].dt.to_period('M')

monthly_posts = df.groupby(['Year_Month', 'Author'])["Score"].sum().reset_index(name='Score_Sum')

monthly_posts[monthly_posts["Author"] == "zek_997"]


