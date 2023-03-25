import pandas as pd

"""Load the data from the file into a variable called 'data'"""

weekly_cases_file = 'weekly_cases_per_million.csv'
weekly_deaths_file = 'weekly_deaths_per_million.csv'

weekly_cases_data = pd.read_csv(weekly_cases_file)
weekly_deaths_data = pd.read_csv(weekly_deaths_file)




"""Take the timestamp of data, and convert it into a pandas timestamp """

date_field_name = "date"
date_format = '%Y-%m-%d'

weekly_cases_data[date_field_name] = pd.to_datetime(weekly_cases_data[date_field_name], format=date_format)
weekly_deaths_data[date_field_name] = pd.to_datetime(weekly_deaths_data[date_field_name], format=date_format)

weekly_cases_data.set_index(date_field_name, inplace=True)
weekly_deaths_data.set_index(date_field_name, inplace=True)

""" Merge deaths and cases weekly data"""

merged_data = weekly_cases_data.merge(weekly_deaths_data, left_index=True, right_index=True, suffixes=('_cases', '_deaths'))

print(merged_data)

"""Select data just for our country"""
"""Create a plotly plot (or graph configured how we want it)"""
countries = ['Germany', 'Finland', 'United_Kingdom']

import plotly.graph_objs as go

fig = go.Figure()

# Add traces for weekly cases per million (left y-axis)
for country in countries:
    fig.add_trace(
        go.Scatter(x=merged_data.index, y=merged_data[f'{country}_cases'], name=f'{country} - Weekly Cases per Million', yaxis='y1')
    )

# Add traces for weekly deaths per million (right y-axis)
for country in countries:
    fig.add_trace(
        go.Scatter(x=merged_data.index, y=merged_data[f'{country}_deaths'], name=f'{country} - Weekly Deaths per Million', yaxis='y2')
    )

# Update layout
fig.update_layout(
    title='Time Series Comparison',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Weekly Cases per Million', side='left', showgrid=False),
    yaxis2=dict(title='Weekly Deaths per Million', side='right', overlaying='y', showgrid=False),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)

"""Export file to browser"""
import plotly.io as pio


output_file = 'time_series_chart.html'
pio.write_html(fig, file=output_file, auto_open=True)