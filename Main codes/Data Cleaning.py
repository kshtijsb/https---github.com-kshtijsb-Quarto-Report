import pandas as pd
import numpy as np

df_indicator1 = pd.read_csv("UNICEF Indicator 1 copy.csv")
df_indicator2 = pd.read_csv("UNICEF Indicator 2 copy.csv")
df_metadata = pd.read_csv("UNICEF Metadata Tableau Assignment copy.csv")
print("First 5 rows of Indicator 1:")
print(df_indicator1.head().to_markdown(index=False, numalign="left", stralign="left"))

print("\nFirst 5 rows of Metadata:")
print(df_metadata.head().to_markdown(index=False, numalign="left", stralign="left"))

print("\nIndicator 1 DataFrame Info:")
print(df_indicator1.info())

print("\nIndicator 2 DataFrame Info:")
print(df_indicator2.info())

print("\nMetadata DataFrame Info:")
print(df_metadata.info())

df_indicator1 = df_indicator1.drop(columns=['unit_multiplier', 'observation_status', 'observation_confidentaility', 'time_period_activity_related_to_when_the_data_are_collected', 'alpha_2_code', 'alpha_3_code'])

df_indicator2 = df_indicator2.drop(columns=['unit_multiplier', 'observation_status', 'observation_confidentaility', 'time_period_activity_related_to_when_the_data_are_collected', 'alpha_2_code', 'alpha_3_code'])

df_metadata = df_metadata.drop(columns=['alpha_2_code', 'alpha_3_code'])

print("First 5 rows of Indicator 1:")
print(df_indicator1.head().to_markdown(index=False, numalign="left", stralign="left"))

print("\nFirst 5 rows of Indicator 2:")
print(df_indicator2.head().to_markdown(index=False, numalign="left", stralign="left"))

print("\nFirst 5 rows of Metadata:")
print(df_metadata.head().to_markdown(index=False, numalign="left", stralign="left"))

print("\nIndicator 1 DataFrame Info:")
print(df_indicator1.info())

print("\nIndicator 2 DataFrame Info:")
print(df_indicator2.info())

print("\nMetadata DataFrame Info:")
print(df_metadata.info())

print("Duplicates in df_indicator1:")
print(df_indicator1.duplicated(subset=['country', 'numeric_code', 'time_period', 'indicator', 'sex', 'current_age']).any())

df_indicator1.drop_duplicates(subset=['country', 'numeric_code', 'time_period', 'indicator', 'sex', 'current_age'], inplace=True)

print("\nDuplicates in df_indicator2:")
print(df_indicator2.duplicated(subset=['country', 'numeric_code', 'time_period', 'indicator', 'sex', 'current_age']).any())

df_indicator2.drop_duplicates(subset=['country', 'numeric_code', 'time_period', 'indicator', 'sex', 'current_age'], inplace=True)

unique_values_indicator1 = {col: df_indicator1[col].unique() for col in ['country', 'indicator', 'sex', 'current_age']}

print("\nUnique values in df_indicator1:")
for col, values in unique_values_indicator1.items():
    print(f"\nColumn: {col}")
    print(values)

unique_values_indicator2 = {col: df_indicator2[col].unique() for col in ['country', 'indicator', 'sex', 'current_age']}

print("\nUnique values in df_indicator2:")
for col, values in unique_values_indicator2.items():
    print(f"\nColumn: {col}")
    print(values)


df_metadata['year'] = pd.to_datetime(df_metadata['year'], format='%Y')

print("\nDuplicates in df_metadata:")
print(df_metadata.duplicated().any())

df_metadata.drop_duplicates(inplace=True)
df_indicator1.to_csv("UNICEF_Indicator_1_cleaned.csv", index=False)
df_indicator2.to_csv("UNICEF_Indicator_2_cleaned.csv", index=False)
df_metadata.to_csv("UNICEF_Metadata_cleaned.csv", index=False)

