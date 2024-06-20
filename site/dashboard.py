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

# List of CSV file options
csv_files = {
    'Em Alta': "C:\\Users\\T-GAMER\\Desktop\\ProjetoWhatsHype\\videos_populares.csv",
    'Música': "C:\\Users\\T-GAMER\\Desktop\\ProjetoWhatsHype\\videos_musica.csv",
    'Esportes': "C:\\Users\\T-GAMER\\Desktop\\ProjetoWhatsHype\\videos_esportes.csv",
    'Famosos': "C:\\Users\\T-GAMER\\Desktop\\ProjetoWhatsHype\\videos_famosos.csv",
    'Filmes': "C:\\Users\\T-GAMER\\Desktop\\ProjetoWhatsHype\\videos_filmes.csv"
}

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

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Dashboard de Evolução de Métricas de Vídeos Populares", style={'textAlign': 'center', 'marginBottom': 20}),

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
        dcc.Tabs(id="tabs", children=[
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
                          labels={'x': 'Aumento no View Count', 'y': 'Título do Vídeo'}, color=view_values,
                          color_continuous_scale=px.colors.sequential.Plasma)
        view_fig.update_layout(showlegend=False, title_x=0.5, xaxis_title='Aumento no View Count', yaxis_title='Título do Vídeo')

        like_titles = [filtered_df[filtered_df['Video ID'] == video_id]['Title'].iloc[0] for video_id in like_top_10]
        like_values = [like_evolution[video_id] for video_id in like_top_10]
        like_fig = px.bar(x=like_values, y=like_titles, orientation='h', title='Top 10 vídeos em evolução de Like Count',
                          labels={'x': 'Aumento no Like Count', 'y': 'Título do Vídeo'}, color=like_values,
                          color_continuous_scale=px.colors.sequential.Plasma)
        like_fig.update_layout(showlegend=False, title_x=0.5, xaxis_title='Aumento no Like Count', yaxis_title='Título do Vídeo')

        return view_fig, like_fig
    return {}, {}

# Callback to display video evolution based on bar chart click data
@app.callback(
    [Output('video-title', 'children'),
     Output('view-evolution-chart', 'figure'),
     Output('like-evolution-chart', 'figure'),
     Output('comment-evolution-chart', 'figure')],
    [Input('view-bar-chart', 'clickData'),
     Input('like-bar-chart', 'clickData'),
     Input('csv-dropdown', 'value')],
    [State('date-range-picker', 'start_date'),
     State('date-range-picker', 'end_date')]
)
def display_video_evolution(view_click_data, like_click_data, csv_path, start_date, end_date):
    df = load_data(csv_path)  # Load the selected CSV data
    selected_video_id = None

    if view_click_data:
        clicked_title = view_click_data['points'][0]['y']
        filtered_df = df[df['Title'] == clicked_title]
        if not filtered_df.empty:
            selected_video_id = filtered_df['Video ID'].iloc[0]
    elif like_click_data:
        clicked_title = like_click_data['points'][0]['y']
        filtered_df = df[df['Title'] == clicked_title]
        if not filtered_df.empty:
            selected_video_id = filtered_df['Video ID'].iloc[0]

    if not selected_video_id:
        return "", {}, {}, {}

    video_data = df[df['Video ID'] == selected_video_id]

    view_fig = px.line(video_data, x='Data da Pesquisa', y='View Count', title=f'Evolução do View Count: {video_data["Title"].iloc[0]}',
                       labels={'x': 'Data da Pesquisa', 'y': 'View Count'}, color_discrete_sequence=['#636EFA'])
    view_fig.update_layout(title_x=0.5)

    like_fig = px.line(video_data, x='Data da Pesquisa', y='Like Count', title=f'Evolução do Like Count: {video_data["Title"].iloc[0]}',
                       labels={'x': 'Data da Pesquisa', 'y': 'Like Count'}, color_discrete_sequence=['#EF553B'])
    like_fig.update_layout(title_x=0.5)

    comment_fig = px.line(video_data, x='Data da Pesquisa', y='Comment Count', title=f'Evolução do Comment Count: {video_data["Title"].iloc[0]}',
                          labels={'x': 'Data da Pesquisa', 'y': 'Comment Count'}, color_discrete_sequence=['#00CC96'])
    comment_fig.update_layout(title_x=0.5)

    return video_data['Title'].iloc[0], view_fig, like_fig, comment_fig

if __name__ == '__main__':
    app.run_server(debug=True)