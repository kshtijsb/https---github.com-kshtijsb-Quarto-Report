import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import geopandas
import pycountry
import altair as alt

def load_data():
    """Loads the CSV files into Pandas DataFrames."""
    df_indicator_1 = pd.read_csv("UNICEF_Indicator_1_cleaned.csv")
    df_indicator_2 = pd.read_csv("UNICEF_Indicator_2_cleaned.csv")
    df_metadata = pd.read_csv("UNICEF_Metadata_cleaned.csv")
    return df_indicator_1, df_indicator_2, df_metadata

def filter_indicator_data(df, country, indicator):
    """Filters data for a specific country and indicator in df_indicator_1."""
    return df[(df['country'] == country) & (df['indicator'] == indicator)]

def plot_line_chart(df, x, y, title, xlabel, ylabel, color=None, hue=None):
    """Plots a line chart."""

    plt.figure(figsize=(10, 6))
    if color:
        sns.lineplot(data=df, x=x, y=y, color=color, hue=hue)
    elif hue:
        sns.lineplot(data=df, x=x, y=y, hue=hue)
    else:
        sns.lineplot(data=df, x=x, y=y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()

def plot_bar_chart(df, x, y, title, xlabel, ylabel):
    """Plots a bar chart."""

    plt.figure(figsize=(12, 6))
    plt.bar(df[x], df[y])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)
    plt.grid(axis='y')
    plt.show()

def plot_scatter_chart(df, x, y, title, xlabel, ylabel):
    """Plots a scatter chart."""

    plt.figure(figsize=(10, 8))
    sns.regplot(x=x, y=y, data=df, scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})  # Added regression line
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()

'''def plot_scatter_chart(df, x, y, title, xlabel, ylabel):
    """Plots a scatter chart."""

    plt.figure(figsize=(10, 8))
    plt.scatter(df[x], df[y])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()'''

def plot_map_sanitation_deaths(df_sanitation, df_deaths, year=None):
    """Plots a choropleth map showing sanitation and deaths data."""

    merged_data = pd.merge(df_sanitation, df_deaths, on='country', how='inner')

    fig = px.choropleth(
        merged_data,
        locations='country',
        locationmode='country names',
        color='obs_value_x', # Sanitation
        hover_name='country',
        hover_data=['obs_value_x', 'obs_value_y'], # Sanitation and Deaths
        title=f'Sanitation and Deaths Aged 15-24 (Year {year})',
        animation_frame='year' # Add this line
    )
    fig.show()

def plot_heatmap(df, x, y, color, title, xlabel, ylabel):
    """Plots a heatmap."""
    chart = alt.Chart(df).mark_rect().encode(
        x=alt.X(x, title=xlabel),
        y=alt.Y(y, title=ylabel),
        color=alt.Color(color, title='Correlation'),  # Add a title to the color legend
        tooltip=[x, y, color]  # Add tooltip for interactivity
    ).properties(
        title=title
    ).interactive()
    chart.save(f'{title.replace(" ", "_").lower()}_heatmap.json')

if __name__ == "__main__":
    df_indicator_1, df_indicator_2, df_metadata = load_data()
    
    # 2. Bar Chart: Compare 'Proportion of health care facilities with no sanitation service' across different countries in the latest available year
    indicator_of_interest = 'Proportion of health care facilities with no sanitation service'
    latest_year = df_indicator_1['year'].max()
    latest_sanitation = df_indicator_1[(df_indicator_1['year'] == latest_year) & (df_indicator_1['indicator'] == indicator_of_interest)]
    top_n = 20
    top_countries_sanitation = latest_sanitation.nlargest(top_n, 'obs_value')
    plot_bar_chart(top_countries_sanitation, 'country', 'obs_value',
                    f'{indicator_of_interest} in {latest_year} (Top {top_n} Countries)',
                    'Country', 'Observation Value')

    # 3. Line Charts: Trends of 'GDP per capita (constant 2015 US$)' and 'Life expectancy at birth, total (years)' over the years for Afghanistan
    afg_metadata = df_metadata[df_metadata['country'] == 'Afghanistan']
    plot_line_chart(afg_metadata, 'year', 'GDP per capita (constant 2015 US$)',
                    'GDP per capita in Afghanistan Over the Years',
                    'Year', 'GDP per capita (constant 2015 US$)', color='green')
    plot_line_chart(afg_metadata, 'year', 'Life expectancy at birth, total (years)',
                    'Life Expectancy at Birth in Afghanistan Over the Years',
                    'Year', 'Life expectancy at birth, total (years)', color='red')

    # 4. Scatter Plot: Relationship between 'GDP per capita (constant 2015 US$)' and 'Life expectancy at birth, total (years)' across different countries in the latest year
    df_metadata['year'] = pd.to_datetime(df_metadata['year'], errors='coerce').dt.year
    latest_year_metadata = df_metadata['year'].max()
    latest_metadata = df_metadata[df_metadata['year'] == latest_year_metadata]
    plot_scatter_chart(latest_metadata, 'GDP per capita (constant 2015 US$)', 'Life expectancy at birth, total (years)',
                       f'Relationship between GDP per capita and Life Expectancy at Birth in {latest_year_metadata}',
                       'GDP per capita (constant 2015 US$)', 'Life expectancy at birth, total (years)')

    # 5. Line chart of female and male deaths aged 15-24 in India
    india_deaths = df_indicator_2[(df_indicator_2['country'] == 'India') & (df_indicator_2['indicator'] == 'Deaths aged 15 to 24')]
    plot_line_chart(india_deaths, 'year', 'obs_value', 'Deaths Aged 15-24 in India (1990-2020)',
                    'Year', 'Number of Deaths', hue='sex')

    # 6. Scatter plot of GDP per capita vs. number of deaths among 15-24 year-olds
    year_of_interest = 2000
    df_indicator_2['year'] = pd.to_numeric(df_indicator_2['year'], errors='coerce')
    df_metadata['year'] = pd.to_numeric(df_metadata['year'], errors='coerce')

    # Find the closest year
    available_years_indicator = df_indicator_2['year'].unique()
    closest_year_indicator = min(available_years_indicator, key=lambda x: abs(x - year_of_interest))

    available_years_metadata = df_metadata['year'].unique()
    closest_year_metadata = min(available_years_metadata, key=lambda x: abs(x - year_of_interest))

    # Filter DataFrames based on the closest years
    df_indicator_2_year = df_indicator_2[df_indicator_2['year'] == closest_year_indicator]
    df_metadata_year = df_metadata[df_metadata['year'] == closest_year_metadata]

    # Aggregate deaths data (summing over sex)
    df_indicator_2_year_agg = df_indicator_2_year.groupby('country')['obs_value'].sum().reset_index()

    # Merge the two DataFrames on 'country'
    merged_data = pd.merge(df_indicator_2_year_agg, df_metadata_year, on='country', how='inner')

    plot_scatter_chart(merged_data, 'GDP per capita (constant 2015 US$)', 'obs_value',
                        f'GDP per Capita vs. Deaths Aged 15-24 (Year {year_of_interest})',
                        'GDP per capita (constant 2015 US$)', 'Total Deaths Aged 15-24')

    # 7. Map showing deaths occurred due to poor sanitations
    # Prepare data for the map
    sanitation_data_map = df_indicator_1[
        (df_indicator_1['indicator'] == 'Proportion of health care facilities with no sanitation service')
    ]
    deaths_data_map = df_indicator_2[
        (df_indicator_2['indicator'] == 'Deaths aged 15 to 24')
    ].groupby('country')['obs_value'].sum().reset_index()

    plot_map_sanitation_deaths(sanitation_data_map, deaths_data_map)