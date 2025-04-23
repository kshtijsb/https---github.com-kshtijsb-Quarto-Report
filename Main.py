import pandas as pd
import geopandas as gpd
from plotnine import (
    ggplot, aes, geom_line, geom_point, geom_histogram, geom_boxplot, geom_map,
    labs, theme_minimal, scale_x_log10, scale_y_log10, scale_color_discrete,
    theme, element_text, scale_fill_gradient, theme_void, geom_smooth
)
from mizani.formatters import currency_format, percent_format
import warnings


METADATA_CSV_PATH = "UNICEF Metadata.csv"
INDICATOR_CSV_PATH = "UNICEF_Indicator_1_cleaned.csv"

SHAPEFILE_PATH = 'Natural Earth Countries 10m' 

warnings.filterwarnings('ignore', message='The figure layout has changed to tight')

try:
    metadata_df = pd.read_csv(METADATA_CSV_PATH)
    indicator_df = pd.read_csv(INDICATOR_CSV_PATH)

   
    cols_to_numeric_meta = [
        'year', 'Population, total', 'GDP per capita (constant 2015 US$)',
        'Life expectancy at birth, total (years)', 'Birth rate, crude (per 1,000 people)'
    ]
    for col in cols_to_numeric_meta:
        metadata_df[col] = pd.to_numeric(metadata_df[col], errors='coerce')

    
    cols_to_numeric_indicator = ['year', 'obs_value']
    for col in cols_to_numeric_indicator:
        indicator_df[col] = pd.to_numeric(indicator_df[col], errors='coerce')


except FileNotFoundError as e:
    print(f"Error loading initial CSV files: {e}")
    print("Please ensure '{METADATA_CSV_PATH}' and '{INDICATOR_CSV_PATH}' are present.")
    exit() # Exit if essential data isn't found
except Exception as e:
    print(f"An error occurred during data loading: {e}")
    exit()

# Plot 1: Life Expectancy Trend for Top 5 Countries by Population in 2021
try:
    
    top_5_countries = metadata_df[metadata_df['year'] == 2021].nlargest(5, 'Population, total')['country'].tolist()
    plot1_df = metadata_df[
        (metadata_df['country'].isin(top_5_countries)) &
        (metadata_df['year'] >= 1960) & (metadata_df['year'] <= 2022)
    ].dropna(subset=['year', 'Life expectancy at birth, total (years)', 'country'])

    plot1 = (
        ggplot(plot1_df, aes(x='year', y='Life expectancy at birth, total (years)', color='country')) +
        geom_line(size=1) +
        labs(title="Life Expectancy Trend (1960-2022)", subtitle="For the 5 most populous countries in 2021",
             x="Year", y="Life Expectancy at Birth (Years)", color="Country") +
        theme_minimal() + theme(figure_size=(9, 6))
    )
    plot1.save("plot1_life_expectancy_trend.png", dpi=300)
    plot1.show()
except Exception as e:
    print(f"Error generating Plot 1: {e}")

# Plot 2: GDP vs Life Expectancy with Regression Line
try:
    print("\nGenerating Plot 2: GDP vs Life Expectancy with Regression Line...")
    plot2_df = metadata_df[metadata_df['year'] == 2021].dropna(
        subset=['GDP per capita (constant 2015 US$)', 'Life expectancy at birth, total (years)', 'Population, total']
    )

    if not plot2_df.empty:
        plot2 = (
            ggplot(plot2_df, aes(x='GDP per capita (constant 2015 US$)', y='Life expectancy at birth, total (years)')) +
            # Scatter points (color removed, size retained)
            geom_point(aes(size='Population, total', color='country'), alpha=1, na_rm=True) +
            # Add the smoothing line (linear model 'lm' in this case)
            geom_smooth(method='lm', se=True, color='blue', linetype='dashed') + # <- Added this line
            # Log scale for X axis
            scale_x_log10(labels=currency_format(prefix="$")) +
            labs(
                title="GDP per Capita vs. Life Expectancy (2021)",
                subtitle="with Linear Regression Line", # Added subtitle detail
                x="GDP per Capita (constant 2015 US$, log scale)",
                y="Life Expectancy at Birth (Years)",
                size="Population" # Legend for size
            ) +
            theme_minimal() +
            theme(figure_size=(9, 6))
        )
        
        plot2.show() # Use print(plot2) in Quarto/Jupyter
        
        print("Plot 2 (with regression) saved as plot2_gdp_vs_life_expectancy_regression.png")
    else:
        print("No data available for Plot 2.")

except Exception as e:
    print(f"Error generating Plot 2: {e}")

# Plot 3: Healthcare Facilities with No Sanitation Service
try:
    
    plot3_countries = ['Bangladesh', 'Benin', 'Burkina Faso', 'Cambodia']
    plot3_df = indicator_df[indicator_df['country'].isin(plot3_countries)].dropna(subset=['year', 'obs_value'])
    plot3 = (
        ggplot(plot3_df, aes(x='year', y='obs_value', color='country')) +
        geom_line(size=1) + geom_point(size=2) +
        labs(title="Healthcare Facilities with No Sanitation Service", subtitle="Trend for selected countries",
             x="Year", y="Proportion (%)", color="Country") +
        scale_y_log10(labels=percent_format(accuracy=1), breaks=[1, 2, 5, 10, 20]) +
        theme_minimal() + theme(figure_size=(9, 6))
    )
    plot3.save("plot3_healthcare_sanitation_trend.png", dpi=300)
    plot3.show()
except Exception as e:
    print(f"Error generating Plot 3: {e}")

# Plot 4: Distribution of Crude Birth Rates
try:
  
    plot4_df = metadata_df[metadata_df['year'] == 2021].dropna(subset=['Birth rate, crude (per 1,000 people)'])
    plot4 = (
        ggplot(plot4_df, aes(x='Birth rate, crude (per 1,000 people)')) +
        geom_histogram(binwidth=2, fill="skyblue", color="black") +
        labs(title="Distribution of Crude Birth Rates (2021)", x="Crude Birth Rate (per 1,000 people)",
             y="Number of Countries") +
        theme_minimal() + theme(figure_size=(9, 6))
    )
    plot4.save("plot4_birth_rate_distribution.png", dpi=300)
    plot4.show()
except Exception as e:
    print(f"Error generating Plot 4: {e}")
# Plot 5: Distribution of Life Expectancy by Decade
try:
    
    # Prepare data for plot 5 - requires 'decade' column
    plot5_df = metadata_df.dropna(subset=['year', 'Life expectancy at birth, total (years)']).copy()
    plot5_df['decade'] = (plot5_df['year'] // 10 * 10).astype(int).astype(str) + 's'

    plot5 = (
        ggplot(plot5_df, aes(x='decade', y='Life expectancy at birth, total (years)', fill='decade')) +
        geom_boxplot(show_legend=False) +
        labs(title="Distribution of Life Expectancy by Decade", x="Decade", y="Life Expectancy at Birth (Years)") +
        theme_minimal() + theme(figure_size=(9, 6), axis_text_x=element_text(angle=45, hjust=1))
    )
    plot5.save("plot5_life_expectancy_decades_boxplot.png", dpi=300)
    plot5.show()
except Exception as e:
    print(f"Error generating Plot 5: {e}")


YEAR_TO_PLOT_MAP = 2021
VARIABLE_TO_PLOT_MAP = 'Life expectancy at birth, total (years)'

# Plot 6: Map of Life Expectancy
try:
    
    world_map = gpd.read_file(SHAPEFILE_PATH)
    world_map = world_map[['ADMIN', 'geometry']]
    

    # 2. Prepare UNICEF Data for Map
    data_to_plot_map = metadata_df[metadata_df['year'] == YEAR_TO_PLOT_MAP].dropna(subset=[VARIABLE_TO_PLOT_MAP])
    data_to_plot_map = data_to_plot_map[['country', VARIABLE_TO_PLOT_MAP]]
    

    # 3. Merge Geospatial and UNICEF Data
    merged_map_data = world_map.merge(data_to_plot_map, left_on='ADMIN', right_on='country', how='left')
    matched_countries = merged_map_data[VARIABLE_TO_PLOT_MAP].notna().sum()
    
    if matched_countries < len(data_to_plot_map) / 2:
         print("Warning: Low merge success rate. Check country name matching between shapefile ('ADMIN') and CSV ('country').")


    # 4. Create Map Plot
    map_plot = (
        ggplot(merged_map_data) +
        geom_map(aes(fill=VARIABLE_TO_PLOT_MAP), color="gray", size=0.5) +
        scale_fill_gradient(low="lightyellow", high="darkred", na_value="lightgrey") + # Example gradient
        labs(title=f"{VARIABLE_TO_PLOT_MAP} ({YEAR_TO_PLOT_MAP})", fill=VARIABLE_TO_PLOT_MAP.replace('_', ' ').title()) +
        theme_void() +
        theme(figure_size=(12, 8)) # Adjusted size
    )

    # 5. Save Map Plot
    output_filename = f"plot6_map_{VARIABLE_TO_PLOT_MAP.replace(' ', '_').lower()}_{YEAR_TO_PLOT_MAP}.png"
    map_plot.save(output_filename, dpi=300)
    map_plot.show()

except FileNotFoundError:
    print(f"Error: Shapefile not found at '{SHAPEFILE_PATH}'.")
    print("Please download the Natural Earth Admin 0 countries shapefile, unzip it,")
    print("and update the SHAPEFILE_PATH variable in the script to the correct .shp file path.")
except ImportError:
    print("Error: Missing library. Please install geopandas: pip install geopandas")
except KeyError as e:
    print(f"Error: Column not found during map generation. Missing key: {e}")
    print("This often happens if the shapefile column name ('ADMIN' assumed here) or")
    print("the CSV column name ('country' assumed here) used for merging is incorrect.")
    print("Inspect world_map.columns and metadata_df.columns.")
except Exception as e:
    print(f"An error occurred during map generation: {e}")