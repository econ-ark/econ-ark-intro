import pandas as pd
import numpy as np

GB = pd.read_csv('data/output/GB.csv')

#Remove the first two columns of GB and SPF that capture dates and indexing
GB = GB.iloc[:, 2:]
GB_unemp = GB.iloc[:, :2]
GB_cons = GB.iloc[:, -4:]

# Define date column
start_date = pd.to_datetime('1983-01-01')
end_date = pd.to_datetime('2018-10-01')
quarterly_dates = pd.date_range(start=start_date, end=end_date, freq='QS')

annual_forecast_df = pd.DataFrame({'date': quarterly_dates})
annual_forecast_df['GB_unemp'] = GB_unemp.iloc[:, 1] - GB_unemp.iloc[:, 0]
annual_forecast_df['GB_cons'] = GB_cons.mean(axis=1)

# Next for SPF
SPF = pd.read_csv('data/output/SPF.csv')
SPF = SPF.iloc[:, 2:]
SPF_unemp = SPF.iloc[:, :2]
SPF_cons = SPF.iloc[:, -4:]
annual_forecast_df['SPF_unemp'] = SPF_unemp.iloc[:, 1] - SPF_unemp.iloc[:, 0]
annual_forecast_df['SPF_cons'] = SPF_cons.mean(axis=1)

# Last for the actual FRED changes across years
FRED = pd.read_csv('data/output/FRED.csv')
FRED = FRED.iloc[1:,:]
FRED.reset_index(drop=True, inplace=True)

diff_values = FRED[FRED.columns[1]].diff(periods=4)
print(diff_values)
avg_values = FRED[FRED.columns[2]].rolling(window=4).mean()
print(avg_values.iloc[3:-1])
print(avg_values.iloc[3:-1].shape)

annual_forecast_df['FRED_unemp'] = diff_values.iloc[4:].reset_index(drop=True)
annual_forecast_df['FRED_cons'] = avg_values.iloc[3:-1].reset_index(drop=True)

print(annual_forecast_df.iloc[67:77,:])

decimal = False  # Set to the desired number of decimal places or False to disable formatting

if decimal is not False:
    for column in annual_forecast_df.columns[1:]:
        annual_forecast_df[column] = annual_forecast_df[column].apply(lambda x: f"{x:.{decimal}f}")

annual_forecast_df.to_csv('data/output/forecast.csv')
# annual_forecast_df.to_excel('data/output/forecast.xlsx', index=False)




