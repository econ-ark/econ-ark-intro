import pandas as pd
import numpy as np

forecast = pd.read_csv('data/output/forecast.csv')

#Remove the first column capturing indexing
forecast = forecast.iloc[:, 1:]
start_date = pd.to_datetime('1983-01-01')
end_date = pd.to_datetime('2018-10-01')
quarterly_dates = pd.date_range(start=start_date, end=end_date, freq='QS')

# Calculate squared differences
GB_abse_unemp = np.abs((forecast[forecast.columns[1]] - forecast[forecast.columns[5]]))
SPF_abse_unemp = np.abs((forecast[forecast.columns[3]] - forecast[forecast.columns[5]]))
GB_abse_cons = np.abs((forecast[forecast.columns[2]] - forecast[forecast.columns[6]]))
SPF_abse_cons = np.abs((forecast[forecast.columns[4]] - forecast[forecast.columns[6]]))

# Calculate difference between SPF and GB sq differences
diff_abse_unemp = GB_abse_unemp - SPF_abse_unemp
diff_abse_cons = GB_abse_cons - SPF_abse_cons

abs_errors_df = pd.DataFrame({'date': quarterly_dates,
                        'GB_error_unemp': GB_abse_unemp,
                       'SPF_error_unemp': SPF_abse_unemp,
                       'GB_error_cons': GB_abse_cons,
                       'SPF_error_cons': SPF_abse_cons,
                       'diff_error_unemp': diff_abse_unemp,
                       'diff_error_cons': diff_abse_cons})

abs_errors_df.to_csv('data/output/abs_errors.csv')
# abs_errors_df.to_excel('data/output/abs_errors.xlsx', index=False)

# Storing the mean of the absolute value of the errors for both GB and SPF
print(abs_errors_df)
df = abs_errors_df.iloc[:,1:-2]
full_mean_abse = df.mean()
print(full_mean_abse)

df2 = abs_errors_df.iloc[48:,1:-2]
res_mean_abse = df2.mean()
print(res_mean_abse)