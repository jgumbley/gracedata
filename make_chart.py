import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots


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
countries = ['Germany', 'Finland', 'United Kingdom']

colors = ['red', 'green', 'blue']


fig = make_subplots(rows=2, cols=1, 
                    specs=[[{"secondary_y": False}], [{"secondary_y": False}]],
                    subplot_titles=("Weekly Cases per Million", "Weekly Deaths per Million"))

# Add traces for weekly cases per million
for i, country in enumerate(countries):
    fig.add_trace(
        go.Scatter(x=merged_data.index, y=merged_data[f'{country}_cases'], name=f'{country} - Weekly Cases per Million', line=dict(color=colors[i])),
        row=1, col=1
    )

# Add traces for weekly deaths per million
for i, country in enumerate(countries):
    fig.add_trace(
        go.Scatter(x=merged_data.index, y=merged_data[f'{country}_deaths'], name=f'{country} - Weekly Deaths per Million', line=dict(color=colors[i])),
        row=2, col=1
    )

# Update layout and subplot titles
fig.update_layout(title='Time Series Comparison', showlegend=True, height=800)


"""Export file to browser"""
import plotly.io as pio


output_file = 'time_series_chart.html'
pio.write_html(fig, file=output_file, auto_open=True)