import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

countries=['Germany', 'Finland', 'United Kingdom']

def load_and_index_on_date(filename, date_field_name="date"):
    """
    A function that loads the data from a CSV file, converts the date 
    field to datetime format, and sets the date as the index.
    """
    data = pd.read_csv(filename)
    data[date_field_name] = pd.to_datetime(data[date_field_name], format='%Y-%m-%d')
    data.set_index(date_field_name, inplace=True)
    return data

weekly_deaths_data = load_and_index_on_date('weekly_deaths_per_million.csv')
excess_mortality_data = load_and_index_on_date('excess_mortality.csv')



""" Preprocess excess deaths data """


special_list=['Germany', 'Finland', 'United Kingdom']
excess_value="cum_excess_per_million_proj_all_ages"
selected_countries_data = excess_mortality_data[excess_mortality_data['location'].isin(special_list)].pivot_table(values=excess_value, index='date', columns='location')



"""Select data just for our country"""
"""Create a plotly plot (or graph configured how we want it)"""
countries = ['Germany', 'Finland', 'United Kingdom']

colors = ['red', 'green', 'blue']

# Find the minimum date in the data



fig = make_subplots(rows=2, cols=1,
                    specs=[[{"secondary_y": False}], [{"secondary_y": False}] ],
                    subplot_titles=("Weekly Deaths per Million", "Excess Mortality per million"))


for i, country in enumerate(countries):
    fig.add_trace(
        go.Scatter(x=weekly_deaths_data.index, y=weekly_deaths_data[f'{country}'], name=country, line=dict(color=colors[i])),
        row=1, col=1
    )

# Add traces for excess mortality
for i, country in enumerate(countries):
    fig.add_trace(
        go.Scatter(x=selected_countries_data.index, y=selected_countries_data[country], showlegend=False, line=dict(color=colors[i])),
        row=2, col=1
    )


# Update layout and subplot titles
fig.update_layout(
    title=dict(
        text='Comparing health consequences of COVID-19 between Germany, UK and Finland',
        font=dict(
            size=24,
            family='Georgia',
            color='darkblue'
        )
    ),
    showlegend=True,
    height=1000,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5
    )
)

#fig.update_yaxes(type='log', row=3, col=1)
fig.update_xaxes(range=['2020-01-01', '2023-01-01'])

"""Export file to browser"""
import plotly.io as pio


output_file = 'time_series_chart.html'
pio.write_html(fig, file=output_file, auto_open=True)