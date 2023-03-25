import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots


"""Load the data from the file into a variable called 'data'"""

date_field_name = "date"
date_format = '%Y-%m-%d'
countries = ['Germany', 'Finland', 'United Kingdom']


weekly_cases_file = 'weekly_cases_per_million.csv'
weekly_deaths_file = 'weekly_deaths_per_million.csv'
excess_mortality_file = 'excess_mortality.csv'
icu_occupancy_file = 'covid-hospitalizations.csv'

weekly_cases_data = pd.read_csv(weekly_cases_file)
weekly_deaths_data = pd.read_csv(weekly_deaths_file)
excess_mortality_data = pd.read_csv(excess_mortality_file)
icu_occupancy_data = pd.read_csv(icu_occupancy_file)


"""Take the timestamp of data, and convert it into a pandas timestamp """



weekly_cases_data[date_field_name] = pd.to_datetime(weekly_cases_data[date_field_name], format=date_format)
weekly_deaths_data[date_field_name] = pd.to_datetime(weekly_deaths_data[date_field_name], format=date_format)
excess_mortality_data[date_field_name] = pd.to_datetime(excess_mortality_data[date_field_name], format=date_format)
icu_occupancy_data[date_field_name] = pd.to_datetime(icu_occupancy_data[date_field_name], format=date_format)

weekly_cases_data.set_index(date_field_name, inplace=True)
weekly_deaths_data.set_index(date_field_name, inplace=True)
excess_mortality_data.set_index(date_field_name, inplace=True)
icu_occupancy_data.set_index(date_field_name, inplace=True)

""" Take a look at excess deaths data """


special_list=['Germany', 'Finland', 'United Kingdom']
excess_value="cum_excess_per_million_proj_all_ages"
selected_countries_data = excess_mortality_data[excess_mortality_data['location'].isin(special_list)].pivot_table(values=excess_value, index='date', columns='location')

""" Take a look at ICU data"""

# Filter the data for the required countries and the indicator "Daily ICU occupancy per million"
selected_icu_occupancy_data = icu_occupancy_data[
    (icu_occupancy_data['entity'].isin(countries)) & 
    (icu_occupancy_data['indicator'] == 'Daily ICU occupancy per million')
].pivot_table(values='value', index='date', columns='entity')


""" Merge deaths and cases weekly data"""

merged_data = weekly_cases_data.merge(weekly_deaths_data, left_index=True, right_index=True, suffixes=('_cases', '_deaths'))



"""Select data just for our country"""
"""Create a plotly plot (or graph configured how we want it)"""
countries = ['Germany', 'Finland', 'United Kingdom']

colors = ['red', 'green', 'blue']

# Find the minimum date in the data



fig = make_subplots(rows=4, cols=1,
                    specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]],
                    subplot_titles=("Weekly Cases per Million", "Weekly Deaths per Million", "Excess Mortality per Million", "Daily ICU Occupancy per Million"))


# Add traces for weekly cases per million
# Add traces for weekly cases per million
for i, country in enumerate(countries):
    fig.add_trace(
        go.Scatter(x=merged_data.index, y=merged_data[f'{country}_cases'], name=country, line=dict(color=colors[i])),
        row=1, col=1
    )

# Add traces for weekly deaths per million
for i, country in enumerate(countries):
    fig.add_trace(
        go.Scatter(x=merged_data.index, y=merged_data[f'{country}_deaths'], showlegend=False, line=dict(color=colors[i])),
        row=2, col=1
    )

# Add traces for excess mortality
for i, country in enumerate(countries):
    fig.add_trace(
        go.Scatter(x=selected_countries_data.index, y=selected_countries_data[country], showlegend=False, line=dict(color=colors[i])),
        row=3, col=1
    )

# Step 4: Plot the ICU occupancy data as a time series
for i, country in enumerate(countries):
    fig.add_trace(
        go.Scatter(x=selected_icu_occupancy_data.index, y=selected_icu_occupancy_data[country], showlegend=False, line=dict(color=colors[i])),
        row=4, col=1
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