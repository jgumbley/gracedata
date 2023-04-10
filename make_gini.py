import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots

df = pd.read_csv("DP_LIVE_10042023100113754.csv")
# Assuming df is the DataFrame containing the data
filtered_data = df[df['INDICATOR'] == 'INCOMEINEQ']
filtered_data = filtered_data[filtered_data['TIME'].astype(int).between(2018, 2022)]

countries = ['FIN', 'DEU', 'GBR']
years = filtered_data['TIME'].unique()
years.sort()

fig = go.Figure()

for country_code in countries:
    country_data = filtered_data[filtered_data['LOCATION'] == country_code]
    fig.add_trace(go.Bar(
        x=years,
        y=country_data['Value'],
        name=country_code,
    ))

fig.update_layout(
    barmode='group',
    title_text='GINI Co-efficient for Finland, Germany, and the UK (2018-2022)',
    xaxis_title='Year',
    yaxis_title='GINI Co-efficient'
)

"""Export file to browser"""
import plotly.io as pio


output_file = 'time_series_chart.html'
pio.write_html(fig, file=output_file, auto_open=True)