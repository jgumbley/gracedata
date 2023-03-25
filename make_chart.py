import pandas as pd

"""Load the data from the file into a variable called 'data'"""

file_path = 'new_cases_per_million.csv'
data = pd.read_csv(file_path)




"""Take the timestamp of data, and convert it into a pandas timestamp """

date_field_name = "date"

data[date_field_name] = pd.to_datetime(data[date_field_name], format='%Y-%m-%d')


"""Select data just for our country
   set index and print """

data.set_index(date_field_name, inplace=True)
selected_data = data[['Finland', 'Germany', 'United Kingdom']]
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

fig.update_layout(title='COVID-19 Cases', showlegend=True)



"""Export file to browser"""
import plotly.io as pio


output_file = 'time_series_chart.html'
pio.write_html(fig, file=output_file, auto_open=True)