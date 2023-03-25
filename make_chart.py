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

"""Select data just for our country
   set index and print """


selected_data = merged_data[['Finland_cases', 'Germany_cases', 'United Kingdom_cases',
                             'Finland_deaths', 'Germany_deaths', 'United Kingdom_deaths',
                             ]]
print(selected_data)

"""Create a plotly plot (or graph configured how we want it)"""


import plotly.graph_objs as go
from plotly.subplots import make_subplots

fig = make_subplots(specs=[[{'secondary_y': True}]])
countries = selected_data.columns

for country in countries:
    fig.add_trace(
        go.Scatter(x=selected_data.index, y=selected_data[country], name=country),
        secondary_y=False
    )

fig.update_layout(title='Weekly COVID-19 Cases per million', showlegend=True)



"""Export file to browser"""
import plotly.io as pio


output_file = 'time_series_chart.html'
pio.write_html(fig, file=output_file, auto_open=True)