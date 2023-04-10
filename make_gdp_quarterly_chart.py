import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots

df = pd.read_csv("qgdp.csv")

filtered_data = df[df['INDICATOR'] == 'QGDP']
filtered_data = filtered_data[filtered_data['SUBJECT'] == 'TOT']
filtered_data = filtered_data[filtered_data['MEASURE'] == 'PC_CHGPP']

countries = ['FIN', 'DEU', 'GBR']
country_names = {'FIN': 'Finland', 'DEU': 'Germany', 'GBR': 'United Kingdom'}

fig = go.Figure()

for country_code in countries:
    country_data = filtered_data[filtered_data['LOCATION'] == country_code]
    fig.add_trace(go.Scatter(
        x=country_data['TIME'],
        y=country_data['Value'],
        name=country_names[country_code],
        mode='lines+markers'
    ))

fig.update_layout(
    title_text='Quarterly GDP Growth for Finland, Germany, and the UK',
    xaxis_title='Year',
    yaxis_title='GDP Growth (%)'
)


"""Export file to browser"""
import plotly.io as pio


output_file = 'time_series_chart.html'
pio.write_html(fig, file=output_file, auto_open=True)