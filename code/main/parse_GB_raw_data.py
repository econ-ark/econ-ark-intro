import pandas as pd

# Load the Excel file
excel_file = pd.ExcelFile('data/raw/GBweb_Row_Format.xlsx') 

# First for unemployment; note, we want from 1981, Q1 onward to align with SPF data
df = excel_file.parse('UNEMP')
date = df['DATE'][178:]
unemp_f0 = df['UNEMPF0'][178:]
unemp_f4 = df['UNEMPF4'][178:]

# Lastly for real expenditures
df = excel_file.parse('gRPCE')
cons_f0 = df['gRPCEF0'][35:]
cons_f1 = df['gRPCEF1'][35:]
cons_f2 = df['gRPCEF2'][35:]
cons_f3 = df['gRPCEF3'][35:]

# Create DataFrames for each data source and reset the index
date_df = pd.DataFrame({'DATE': date}).reset_index(drop=True)
unemp_df0 = pd.DataFrame({'GB_UNEMPF0': unemp_f0 }).reset_index(drop=True)
unemp_df4 = pd.DataFrame({'GB_UNEMPF4': unemp_f4}).reset_index(drop=True)

cons_df0 = pd.DataFrame({'GB_gRPCEF0': cons_f0}).reset_index(drop=True)
cons_df1 = pd.DataFrame({'GB_gRPCEF1': cons_f1}).reset_index(drop=True)
cons_df2 = pd.DataFrame({'GB_gRPCEF2': cons_f2}).reset_index(drop=True)
cons_df3 = pd.DataFrame({'GB_gRPCEF3': cons_f3}).reset_index(drop=True)

# Define the columns to be concatenated
columns = [
    'GB_UNEMPF0',
    'GB_UNEMPF4',
    'GB_gRPCEF0',
    'GB_gRPCEF1',
    'GB_gRPCEF2',
    'GB_gRPCEF3'
]

# Define the corresponding DataFrames
dfs = [
    unemp_df0,
    unemp_df4,
    cons_df0,
    cons_df1,
    cons_df2,
    cons_df3
]

# Concatenate the columns into results_df using list comprehension
results_df = pd.concat([df for col, df in zip(columns, dfs)], axis=1)

# Add the 'DATE' column to results_df
results_df['DATE'] = date_df

# Rearrange the columns with 'DATE' as the first column
results_df = results_df[['DATE'] + columns]

# Reset the index
results_df = results_df.reset_index(drop=True)

# Print the final result
print(results_df)

# Now, since Greenbook has two forecast per quarter, we extract the final forecast for a given
# quarter, since this gives us the best chance at getting the FED's forecast *after* the SPF
# forecast is made.

# Extract odd-numbered rows (1, 3, ..., 43)
GB_df = results_df.iloc[1::2]

# Reset the index for the modified DataFrame
GB_df.reset_index(drop=True, inplace=True)

# Continue working with the 'odd_rows_df' DataFrame
print(GB_df)

decimal = False # Set to the desired number of decimal places or False to disable formatting

if decimal is not False:
    for column in GB_df.columns[1:]:
        GB_df[column] = GB_df[column].apply(lambda x: f"{x:.{decimal}f}")

# Uncomment these final lines to get the output of your choice
GB_df.to_csv('data/output/GB.csv')
# GB_df.to_excel('data/output/GB_parsed.xlsx', index=False)
