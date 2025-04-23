import pandas as pd

# Read the CSV files into Pandas DataFrames
df_indicator_1 = pd.read_csv("UNICEF_Indicator_1_cleaned.csv")
df_indicator_2 = pd.read_csv("UNICEF_Indicator_2_cleaned.csv")

# Rename the 'time_period' column in df_indicator_2 to 'year' for consistency
df_indicator_2.rename(columns={'time_period': 'year'}, inplace=True)

# Merge the two DataFrames on 'country' and 'year'
merged_df = pd.merge(df_indicator_1, df_indicator_2, on=['country', 'year'], how='inner')

# Display the first 5 rows of the merged DataFrame
print("First 5 rows of merged_df:")
print(merged_df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Get information about the columns and their data types in the merged DataFrame
print("\nInformation about merged_df:")
print(merged_df.info())