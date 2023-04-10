import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots

df = pd.read_csv("unemployment_monthly.csv")

unemployment_data = df[df['INDICATOR'] == 'HUR']
unemployment_data = unemployment_data[unemployment_data['SUBJECT'] == 'TOT']

countries = {'FIN': 'Finland', 'DEU': 'Germany', 'GBR': 'United Kingdom'}
colors = {'FIN': 'blue', 'DEU': 'red', 'GBR': 'green'}

fig = go.Figure()

for country_code, country_name in countries.items():
    country_data = unemployment_data[unemployment_data['LOCATION'] == country_code]
    fig.add_trace(
        go.Scatter(x=country_data['TIME'], y=country_data['Value'], name=country_name, marker_color=colors[country_code])
    )

fig.update_xaxes(title_text="Time")
fig.update_yaxes(title_text="Unemployment Rate")
fig.update_layout(height=600, width=800, title_text='Monthly Unemployment Rates in Germany, UK, and Finland')



"""Export file to browser"""
import plotly.io as pio


output_file = 'time_series_chart.html'
pio.write_html(fig, file=output_file, auto_open=True)