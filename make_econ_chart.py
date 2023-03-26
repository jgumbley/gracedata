import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots




df = pd.read_csv("data_template.csv")

# Create a subplot with each indicator in its own row
df = df.pivot_table(index='Indicator', columns='Country')
df.columns = df.columns.droplevel(0)
years = ['2018', '2019', '2020', '2021']

fig = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=df.index)

colors = {
    'Finland': 'blue',
    'Germany': 'red',
    'United Kingdom': 'green'
}

for idx, (indicator, row) in enumerate(df.iterrows()):
    for country, color in colors.items():
        fig.add_trace(
            go.Scatter(x=years, y=row[country], name=country, legendgroup=country, showlegend=(idx == 0), line=dict(color=color)),
            row=idx + 1,
            col=1
        )

fig.update_layout(
    title=dict(
        text="Comparing Economic Consequences of COVID-19 between Germany, UK, and Finland",
        font=dict(
            size=24,
            family='Georgia',
            color='darkblue'
        )
    ),
    legend_title="Countries",
    height=1000,
    showlegend=True
)


# Show the figure
fig.show()


"""Export file to browser"""
import plotly.io as pio


output_file = 'time_series_chart.html'
pio.write_html(fig, file=output_file, auto_open=True)