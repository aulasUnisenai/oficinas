"""
# Geral
"""

# Bibliotecas
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Carregar a base
df = pd.read_excel('/content/pokedex.xlsx')
df.head(5)

# Ver colunas
df.columns

# Verificar tipo das variáveis
df.info()

# Transformar em variáveis categóricas
colunasCategoricas = ['numero', 'geracao']
for coluna in colunasCategoricas:
    df[coluna] = df[coluna].astype('object')

# Estatísticas gerais
df.describe().T.round(2)

"""# Estatísticas descritivas"""

# Quais são os tipos com mais Pokémon?
df['tipoPrincipal'].value_counts()

# Quantidade de Pokémon por geração?
df['geracao'].value_counts()

# Função para obter os cinco principais Pokémon para cada status
def top_pokemon(df, stat, top_n=5):
    return df.nlargest(top_n, stat)[["nome", stat]]

# Listar os status
stats = ["ataque", "defesa", "hp",
         "ataqueEspecial", "defesaEspecial",
         "velocidade", "total"]

# Obter os cinco principais Pokémon para cada status
top_pokemon_stats = {stat: top_pokemon(df, stat)
                      for stat in stats}

# Mostrar os resultados
for stat, top_pokemon in top_pokemon_stats.items():
    print(f"Top 5 Pokémon por {stat}:\n{top_pokemon}\n")

"""# Gráficos"""

# Tipo de Pokémon
tipo_counts = df['tipoPrincipal'].value_counts()

# Criar gráfico de barras
fig = px.bar(tipo_counts, x=tipo_counts.index, y=tipo_counts.values,
             title='Tipos de Pokémon mais Comuns',
             labels={'tipoPrincipal': 'Tipo Principal',
                     'quantidade': 'Quantidade'},
             text=tipo_counts.values)

# Ajustar layout do gráfico
fig.update_layout(
    xaxis_title='Tipo Principal',
    yaxis_title='Quantidade',
    xaxis_tickangle=-45
)

# Mostrar o gráfico
fig.show()

# Quantidade por geração
geracao_counts = df['geracao'].value_counts().sort_index()

# Criar gráfico de linhas
fig = px.line(geracao_counts, x=geracao_counts.index,
              y=geracao_counts.values,
              markers=True,
              title='Evolução dos Pokémon por Geração')

fig.update_layout(
    xaxis_title='Geração',
    yaxis_title='Quantidade de Pokémon',
    xaxis=dict(tickmode='linear')
)

fig.show()

# Gráfico de barras para um determinado status (top 5)
def plot_top_pokemon_stat(top_pokemon, stat):
    fig = px.bar(top_pokemon, x="nome",
                 y=stat, title=f"Top 5 Pokémon por {stat}")
    fig.show()

# Criar gráficos para todos os status
for stat in stats:
    plot_top_pokemon_stat(top_pokemon_stats[stat], stat)

# Função para criar boxplot por tipo
def plot_boxplot_tipo(df, stat):
    fig = px.box(df, x="tipoPrincipal",
                 y=stat,
                 color = "tipoPrincipal",
                 title=f"Distribuição de {stat} por Tipo de Pokémon")
    fig.show()

# Criar boxplots para todos os status por tipo
for stat in stats:
    plot_boxplot_tipo(df, stat)

# Função para criar boxplot por geração
def plot_boxplot_geracao(df, stat):
    fig = px.box(df, x="geracao",
                 y=stat,
                 color = "geracao",
                 title=f"Distribuição de {stat} por Geração de Pokémon")
    fig.show()

# Criar boxplots para todos os status por geração
for stat in stats:
    plot_boxplot_geracao(df, stat)

# Gráfico de radar para verificar os status
def plot_radar_pokemon(df, pokemon_nome):
    # Filtrar o DataFrame e selecionar a linha do Pokémon
    linha_selecionada = df[df["nome"] == pokemon_nome].iloc[0]

    # Estatísticas e valores
    stats = ['hp', 'ataque', 'defesa', 'ataqueEspecial',
             'defesaEspecial', 'velocidade']
    values = [linha_selecionada.get(stat, 0) for stat in stats]

    # Fechar o gráfico de radar
    values += values[:1]
    stats += stats[:1]

    # Criar o gráfico de radar
    fig = go.Figure(go.Scatterpolar(
        r=values,
        theta=stats,
        fill='toself'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(values)])
        ),
        title=f'Estatísticas do Pokémon: {pokemon_nome}'
    )

    fig.show()

# Exemplo de uso
plot_radar_pokemon(df, "Charmander")