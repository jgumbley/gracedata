import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp



df = pd.read_csv("data_template.csv")

# Create a subplot with each indicator in its own row
indicators = df['Indicator'].unique()
fig = sp.make_subplots(rows=len(indicators), cols=1, shared_xaxes=True, subplot_titles=indicators)

years = ['2018', '2019', '2020', '2021']
countries = df['Country'].unique()

for i, indicator in enumerate(indicators):
    for country in countries:
        country_data = df[(df['Indicator'] == indicator) & (df['Country'] == country)]
        y_values = country_data[years].values[0]

        fig.add_trace(
            go.Scatter(
                x=years,
                y=y_values,
                mode='lines+markers',
                name=f"{country} - {indicator}",
                legendgroup=country,
                marker=dict(
                    size=8,
                    line=dict(width=1)
                ),
                line=dict(width=2),
            ),
            row=i + 1,
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
    xaxis_title="Year",
    legend_title="Countries",
    height=1000,
    showlegend=True
)

# Update y-axis titles for each row
for i, indicator in enumerate(indicators):
    fig.update_yaxes(title_text=indicator, row=i + 1, col=1)

# Show the figure
fig.show()


"""Export file to browser"""
import plotly.io as pio


output_file = 'time_series_chart.html'
pio.write_html(fig, file=output_file, auto_open=True)