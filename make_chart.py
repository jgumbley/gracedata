import pandas as pd

"""Load the data from the file into a variable called 'data'"""

file_path = 'your_data_file.csv'
data = pd.read_csv(file_path)




"""Take the timestamp of data, and convert it into a pandas timestamp """

data['timestamp'] = pd.to_datetime(data['timestamp'], format='%Y')



"""Create a pandas 'pivot' with index timestamp and columns needed """

pivot_data = data.pivot(index='timestamp', columns='country', values='value')


import plotly.graph_objs as go
from plotly.subplots import make_subplots


"""Create a plotly plot (or graph configured how we want it)"""
fig = make_subplots(specs=[[{'secondary_y': True}]])
countries = pivot_data.columns

for country in countries:
    fig.add_trace(
        go.Scatter(x=pivot_data.index, y=pivot_data[country], name=country),
        secondary_y=False
    )

fig.update_layout(title='Time Series Comparison', showlegend=True)

import plotly.io as pio


"""Export file to browser"""
output_file = 'time_series_chart.html'
pio.write_html(fig, file=output_file, auto_open=True)