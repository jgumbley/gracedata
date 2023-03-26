import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def load_and_index_on_date(filename, date_field_name="date"):
    """
    A function that loads the data from a CSV file, converts the date 
    field to datetime format, and sets the date as the index.
    """
    data = pd.read_csv(filename)
    data[date_field_name] = pd.to_datetime(data[date_field_name], format='%Y-%m-%d')
    data.set_index(date_field_name, inplace=True)
    return data

weekly_cases_data = load_and_index_on_date('weekly_cases_per_million.csv')
weekly_deaths_data = load_and_index_on_date('weekly_deaths_per_million.csv')
excess_mortality_data = load_and_index_on_date('excess_mortality.csv')
icu_occupancy_data = load_and_index_on_date('covid-hospitalizations.csv')
tests_performed_data = load_and_index_on_date('covid-testing-all-observations.csv', 
        date_field_name="Date")
vaccinations_data = load_and_index_on_date('vaccinations.csv')


""" Preprocess excess deaths data """


special_list=['Germany', 'Finland', 'United Kingdom']
excess_value="cum_excess_per_million_proj_all_ages"
selected_countries_data = excess_mortality_data[excess_mortality_data['location'].isin(special_list)].pivot_table(values=excess_value, index='date', columns='location')

""" Preprocess excess deaths data """

# Filter the data for the required countries and the indicator "Daily ICU occupancy per million"
selected_icu_occupancy_data = icu_occupancy_data[
    (icu_occupancy_data['entity'].isin(countries)) & 
    (icu_occupancy_data['indicator'] == 'Daily ICU occupancy per million')
].pivot_table(values='value', index='date', columns='entity')


"""Preprocess excess testing data"""

# Filter the data for the required countries and the indicator "7-day smoothed daily change per thousand"
selected_tests_performed_data = tests_performed_data[
    (tests_performed_data['Entity'].isin([f'{country} - tests performed' for country in countries])) 
].pivot_table(values='7-day smoothed daily change per thousand', index='Date', columns='Entity')

selected_tests_performed_data.columns = [col.split(' - ')[0] for col in selected_tests_performed_data.columns]


"""Preprocess vaccination datas"""

# Filter the data for the required countries and the indicator "daily_vaccinations_per_million"
selected_vaccinations_data = vaccinations_data[vaccinations_data['location'].isin(countries)].pivot_table(values='daily_vaccinations_per_million', index='date', columns='location')


""" Merge deaths and cases weekly data"""

merged_data = weekly_cases_data.merge(weekly_deaths_data, left_index=True, right_index=True, suffixes=('_cases', '_deaths'))



"""Select data just for our country"""
"""Create a plotly plot (or graph configured how we want it)"""
countries = ['Germany', 'Finland', 'United Kingdom']

colors = ['red', 'green', 'blue']

# Find the minimum date in the data



fig = make_subplots(rows=6, cols=1,
                    specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]],
                    subplot_titles=("Weekly Cases per Million", "Weekly Deaths per Million", "Excess Mortality per million", "Daily ICU Occupancy per Million", "Tests performed per 1000", "Vaccinations"))

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

# Plot the ICU occupancy data as a time series
for i, country in enumerate(countries):
    fig.add_trace(
        go.Scatter(x=selected_icu_occupancy_data.index, y=selected_icu_occupancy_data[country], showlegend=False, line=dict(color=colors[i])),
        row=4, col=1
    )

# Plot the tests performed data as a time series
for i, country in enumerate(countries):
    fig.add_trace(
        go.Scatter(x=selected_tests_performed_data.index, y=selected_tests_performed_data[country], showlegend=False, line=dict(color=colors[i])),
        row=5, col=1
    )

# Step 4: Plot the vaccination data as a time series
for i, country in enumerate(countries):
    fig.add_trace(
        go.Scatter(x=selected_vaccinations_data.index, y=selected_vaccinations_data[country], showlegend=False, line=dict(color=colors[i])),
        row=6, col=1
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