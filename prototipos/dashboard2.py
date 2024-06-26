import dash
from dash import dcc, html, Input, Output
from dash.dependencies import State
import plotly.express as px
import pandas as pd

# Function to load and preprocess data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df['Data da Pesquisa'] = pd.to_datetime(df['Data da Pesquisa'], format='%d/%m/%Y')
        df['Published At'] = pd.to_datetime(df['Published At'])
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Function to load Reddit data
def load_reddit_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df['Created_Time'] = pd.to_datetime(df['Created_Time'])
        df['Year_Month'] = df['Created_Time'].dt.to_period('M')
        return df
    except Exception as e:
        print(f"Error loading Reddit data: {e}")
        return None

# List of CSV file options for YouTube
csv_files = {
    'Em Alta': "/home/joaolucas/Documentos/SPAD03/ProjetoWhatsHype/videos_populares.csv",
    'Música': "/home/joaolucas/Documentos/SPAD03/ProjetoWhatsHype/videos_musica.csv",
    'Esportes': "/home/joaolucas/Documentos/SPAD03/ProjetoWhatsHype/videos_esportes.csv",
    'Famosos': "/home/joaolucas/Documentos/SPAD03/ProjetoWhatsHype/videos_famosos.csv",
    'Filmes': "/home/joaolucas/Documentos/SPAD03/ProjetoWhatsHype/videos_filmes.csv"
}

reddit_file = "../csvs/EmAltaReddit.csv"

# Function to calculate the evolution of metrics
def calculate_evolution(df, metric):
    evolution = {}
    top_20_videos = df['Video ID'].value_counts().nlargest(20).index
    for video_id in top_20_videos:
        video_data = df[df['Video ID'] == video_id]
        oldest_entry = video_data[metric].iloc[0]
        newest_entry = video_data[metric].iloc[-1]
        evolution[video_id] = newest_entry - oldest_entry
    top_10_videos = sorted(evolution, key=evolution.get, reverse=True)[:10]
    return top_10_videos, evolution

# Function to create Reddit plots
def create_reddit_plots(df):
    top10_posts_by_score = df.sort_values(by="Score", ascending=False)[:10]
    top10_posts_by_comments = df.sort_values(by="Num_Comments", ascending=False)[:10]
    top10_authors = df["Author"].value_counts()[:10]
    top10_subreddits = df["Subreddit"].value_counts()[:10]
    monthly_posts = df.groupby('Year_Month').size().reset_index(name='Post_Count')
    monthly_posts_subreddit = df.groupby(['Year_Month', 'Subreddit']).size().reset_index(name='Post_Count')
    monthly_scores = df.groupby('Year_Month')["Score"].sum().reset_index(name='Score_Sum')

    fig1 = px.bar(top10_posts_by_score, x='Title', y='Score', title='Top 10 Posts by Score')
    fig2 = px.bar(top10_posts_by_comments, x='Title', y='Num_Comments', title='Top 10 Posts by Comments')
    fig3 = px.bar(top10_authors, x=top10_authors.index, y=top10_authors.values, title='Top 10 Authors')
    fig4 = px.bar(top10_subreddits, x=top10_subreddits.index, y=top10_subreddits.values, title='Top 10 Subreddits')
    fig5 = px.line(monthly_posts, x='Year_Month', y='Post_Count', title='Monthly Posts')
    fig6 = px.line(monthly_scores, x='Year_Month', y='Score_Sum', title='Monthly Score Sum')

    return fig1, fig2, fig3, fig4, fig5, fig6

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Dashboard de Evolução de Métricas de Vídeos Populares", style={'textAlign': 'center', 'marginBottom': 20}),

    dcc.Tabs(id="main-tabs", children=[
        dcc.Tab(label='YouTube', children=[
            html.Div([
                dcc.Dropdown(
                    id='csv-dropdown',
                    options=[{'label': name, 'value': path} for name, path in csv_files.items()],
                    value=list(csv_files.values())[0],  # Initial value
                    style={'marginBottom': 20}
                )
            ]),
            html.Div([
                dcc.DatePickerRange(
                    id='date-range-picker',
                    display_format='DD/MM/YYYY',
                    style={'marginBottom': 20}
                )
            ]),
            html.Div([
                dcc.Tabs(id="youtube-tabs", children=[
                    dcc.Tab(label='Top 10 vídeos em evolução de View Count', children=[
                        html.Div([
                            dcc.Graph(id='view-bar-chart', style={'marginTop': 20})
                        ])
                    ]),
                    dcc.Tab(label='Top 10 vídeos em evolução de Like Count', children=[
                        html.Div([
                            dcc.Graph(id='like-bar-chart', style={'marginTop': 20})
                        ])
                    ]),
                    dcc.Tab(label='Detalhes do Vídeo', children=[
                        html.H2(id='video-title', style={'textAlign': 'center', 'marginTop': 20}),
                        html.Div([
                            dcc.Graph(id='view-evolution-chart', style={'marginTop': 20}),
                            dcc.Graph(id='like-evolution-chart', style={'marginTop': 20}),
                            dcc.Graph(id='comment-evolution-chart', style={'marginTop': 20})
                        ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'})
                    ])
                ])
            ])
        ]),
        dcc.Tab(label='Reddit', children=[
            html.Div([
                dcc.Graph(id='reddit-top10-score', style={'marginTop': 20}),
                dcc.Graph(id='reddit-top10-comments', style={'marginTop': 20}),
                dcc.Graph(id='reddit-top10-authors', style={'marginTop': 20}),
                dcc.Graph(id='reddit-top10-subreddits', style={'marginTop': 20}),
                dcc.Graph(id='reddit-monthly-posts', style={'marginTop': 20}),
                dcc.Graph(id='reddit-monthly-scores', style={'marginTop': 20})
            ])
        ])
    ])
])

# Callback to load data based on dropdown selection and update date picker range
@app.callback(
    [Output('date-range-picker', 'min_date_allowed'),
     Output('date-range-picker', 'max_date_allowed'),
     Output('date-range-picker', 'start_date'),
     Output('date-range-picker', 'end_date')],
    [Input('csv-dropdown', 'value')]
)
def update_date_picker_range(csv_path):
    df = load_data(csv_path)
    if df is not None:
        min_date = df['Data da Pesquisa'].min().date()
        max_date = df['Data da Pesquisa'].max().date()
        return min_date, max_date, min_date, max_date
    return pd.Timestamp('2000-01-01').date(), pd.Timestamp('2100-01-01').date(), pd.Timestamp('2023-01-01').date(), pd.Timestamp('2023-12-31').date()

# Callback to update bar charts based on date range and selected CSV file
@app.callback(
    [Output('view-bar-chart', 'figure'),
     Output('like-bar-chart', 'figure')],
    [Input('csv-dropdown', 'value'),
     Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def update_bar_charts(csv_path, start_date, end_date):
    df = load_data(csv_path)
    if df is not None:
        filtered_df = df[(df['Data da Pesquisa'] >= pd.to_datetime(start_date)) & (df['Data da Pesquisa'] <= pd.to_datetime(end_date))]

        view_top_10, view_evolution = calculate_evolution(filtered_df, 'View Count')
        like_top_10, like_evolution = calculate_evolution(filtered_df, 'Like Count')

        view_titles = [filtered_df[filtered_df['Video ID'] == video_id]['Title'].iloc[0] for video_id in view_top_10]
        view_values = [view_evolution[video_id] for video_id in view_top_10]
        view_fig = px.bar(x=view_values, y=view_titles, orientation='h', title='Top 10 vídeos em evolução de View Count',
                          labels={'x': 'Aumento no View Count', 'y': 'Título do Vídeo'})

        like_titles = [filtered_df[filtered_df['Video ID'] == video_id]['Title'].iloc[0] for video_id in like_top_10]
        like_values = [like_evolution[video_id] for video_id in like_top_10]
        like_fig = px.bar(x=like_values, y=like_titles, orientation='h', title='Top 10 vídeos em evolução de Like Count',
                          labels={'x': 'Aumento no Like Count', 'y': 'Título do Vídeo'})

        return view_fig, like_fig
    return {}, {}

# Callback to update video details based on bar chart click
@app.callback(
    [Output('video-title', 'children'),
     Output('view-evolution-chart', 'figure'),
     Output('like-evolution-chart', 'figure'),
     Output('comment-evolution-chart', 'figure')],
    [Input('view-bar-chart', 'clickData'),
     Input('like-bar-chart', 'clickData')],
    [State('csv-dropdown', 'value')]
)
def update_video_details(view_click_data, like_click_data, csv_path):
    ctx = dash.callback_context
    df = load_data(csv_path)
    if not ctx.triggered or df is None:
        return "", {}, {}, {}

    clicked_video_id = None
    if ctx.triggered[0]['prop_id'].startswith('view-bar-chart') and view_click_data:
        clicked_video_id = df['Video ID'][view_click_data['points'][0]['pointIndex']]
    elif ctx.triggered[0]['prop_id'].startswith('like-bar-chart') and like_click_data:
        clicked_video_id = df['Video ID'][like_click_data['points'][0]['pointIndex']]

    if clicked_video_id:
        video_data = df[df['Video ID'] == clicked_video_id]
        video_title = video_data['Title'].iloc[0]

        view_fig = px.line(video_data, x='Data da Pesquisa', y='View Count', title='Evolução de View Count')
        like_fig = px.line(video_data, x='Data da Pesquisa', y='Like Count', title='Evolução de Like Count')
        comment_fig = px.line(video_data, x='Data da Pesquisa', y='Comment Count', title='Evolução de Comment Count')

        return video_title, view_fig, like_fig, comment_fig
    return "", {}, {}, {}

# Callback to update Reddit graphs
@app.callback(
    [Output('reddit-top10-score', 'figure'),
     Output('reddit-top10-comments', 'figure'),
     Output('reddit-top10-authors', 'figure'),
     Output('reddit-top10-subreddits', 'figure'),
     Output('reddit-monthly-posts', 'figure'),
     Output('reddit-monthly-scores', 'figure')],
    [Input('main-tabs', 'value')]
)
def update_reddit_graphs(tab):
    if tab == 'Reddit':
        reddit_df = load_reddit_data(reddit_file)
        if reddit_df is not None:
            fig1, fig2, fig3, fig4, fig5, fig6 = create_reddit_plots(reddit_df)
            return fig1, fig2, fig3, fig4, fig5, fig6
    return {}, {}, {}, {}, {}, {}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
