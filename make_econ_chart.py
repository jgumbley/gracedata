import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots




df = pd.read_csv("data_template.csv")

# Create a subplot with each indicator in its own row

df = df.pivot_table(index='Indicator', columns='Country')
df.columns = df.columns.droplevel(0)
years = ['2018', '2019', '2020', '2021', '2022']

fig = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=df.index)

colors = {
    'Finland': 'blue',
    'Germany': 'red',
    'United Kingdom': 'green'
}

bar_width = 0.2
positions = {
    'Finland': -bar_width,
    'Germany': 0,
    'United Kingdom': bar_width
}

labels = [
    "$",
    "$",
    '% GDP',
    "%",
    "%"

]

for idx, (indicator, row) in enumerate(df.iterrows()):
    for country, color in colors.items():
        fig.add_trace(
            go.Bar(x=years, y=row[country], name=country, legendgroup=country, showlegend=(idx == 0), marker_color=color, width=bar_width, offset=positions[country]),
            row=idx + 1,
            col=1
        )
    # Adding x-axis tick labels for each subplot
    fig.update_xaxes(tickvals=years, row=idx + 1, col=1)
    fig.update_yaxes(title_text=labels[idx], row=idx + 1, col=1)


fig.update_layout(
    title=dict(
        text='Comparing economic consequences of COVID-19 between Germany, UK, and Finland',
        font=dict(
            size=24,
            family='Georgia',
            color='darkblue'
        )
    ),
    barmode='group',
    showlegend=True,
    height=1000,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5
    )
)





"""Export file to browser"""
import plotly.io as pio


output_file = 'time_series_chart.html'
pio.write_html(fig, file=output_file, auto_open=True)