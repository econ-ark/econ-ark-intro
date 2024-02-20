import pandas as pd

# Load the Excel file with levels first
excel_file = pd.ExcelFile('data/raw/meanLevel.xlsx') 

# Extract unemployment; starting from 2007 Q1 so that there are forecasts for every variable
df = excel_file.parse('UNEMP')
date = df['YEAR'][53:197]  
unemp_f0 = df['UNEMP2'][53:197]
unemp_f4 = df['UNEMP6'][53:197]    
 
# Lastly, load the Excel file with growth in level and extract data for real expenditures
excel_file = pd.ExcelFile('data/raw/meanGrowth.xlsx') 
df = excel_file.parse('RCONSUM')
cons_f0 = df['drconsum2'][53:197]  
cons_f1 = df['drconsum3'][53:197]
cons_f2 = df['drconsum4'][53:197]
cons_f3 = df['drconsum5'][53:197]

# Create DataFrames for each data source and reset the index
date_df = pd.DataFrame({'DATE': date}).reset_index(drop=True)
unemp_df0 = pd.DataFrame({'SPF_UNEMPF0': unemp_f0 }).reset_index(drop=True)
unemp_df4 = pd.DataFrame({'SPF_UNEMPF4': unemp_f4}).reset_index(drop=True)

cons_df0 = pd.DataFrame({'SPF_gRPCEF0': cons_f0}).reset_index(drop=True)
cons_df1 = pd.DataFrame({'SPF_gRPCEF1': cons_f1}).reset_index(drop=True)
cons_df2 = pd.DataFrame({'SPF_gRPCEF2': cons_f2}).reset_index(drop=True)
cons_df3 = pd.DataFrame({'SPF_gRPCEF3': cons_f3}).reset_index(drop=True)

# Define the columns to be concatenated
columns = [
    'SPF_UNEMPF0',
    'SPF_UNEMPF4',
    'SPF_gRPCEF0',
    'SPF_gRPCEF1',
    'SPF_gRPCEF2',
    'SPF_gRPCEF3'
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

decimal = False  # Set to the desired number of decimal places or False to disable formatting

if decimal is not False:
    for column in results_df.columns[1:]:
        results_df[column] = results_df[column].apply(lambda x: f"{x:.{decimal}f}")

# Uncomment these final lines to get the output of your choice
results_df.to_csv('data/output/SPF.csv')
# SPF_df.to_excel('data/output/SPF_parsed.xlsx', index=False)