import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots

df = pd.read_csv("GENDER_EMP_10042023100555755.csv")
# Assuming df is the DataFrame containing the data
filtered_data = df[df['AGE'] == 'TOTAL']
filtered_data = filtered_data[filtered_data['COU'].isin(['FIN', 'DEU', 'GER', 'GBR'])]
filtered_data = filtered_data[filtered_data['TIME'].astype(int).between(2018, 2022)]

countries = {'FIN': 'Finland', 'DEU': 'Germany', 'GER': 'Germany', 'GBR': 'United Kingdom'}
colors = {'FIN': 'blue', 'DEU': 'red', 'GER': 'red', 'GBR': 'green'}
sex_categories = {'MEN': 'Male', 'WOMEN': 'Female'}

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=('Male', 'Female'))

for sex_code, sex_label in sex_categories.items():
    for country_code, country_name in countries.items():
        country_data = filtered_data[(filtered_data['COU'] == country_code) & (filtered_data['SEX'] == sex_code)]
        row = 1 if sex_code == 'MEN' else 2
        fig.add_trace(
            go.Scatter(x=country_data['TIME'], y=country_data['Value'], name=country_name, legendgroup=country_name, marker_color=colors[country_code], showlegend=(row == 1)),
            row=row, col=1
        )

fig.update_xaxes(title_text="Time")
fig.update_yaxes(title_text="Unemployment Rate", row=1, col=1)
fig.update_yaxes(title_text="Unemployment Rate", row=2, col=1)
fig.update_layout(height=800, width=800, title_text='Unemployment Rates by Sex and Age Group in Germany, UK, and Finland (2018-2022)')

"""Export file to browser"""
import plotly.io as pio


output_file = 'time_series_chart.html'
pio.write_html(fig, file=output_file, auto_open=True)