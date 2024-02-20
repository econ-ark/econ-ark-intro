import pandas as pd
import numpy as np

forecast = pd.read_csv('data/output/forecast.csv')

#Remove the first column capturing indexing
forecast = forecast.iloc[:, 1:]
start_date = pd.to_datetime('1983-01-01')
end_date = pd.to_datetime('2018-10-01')
quarterly_dates = pd.date_range(start=start_date, end=end_date, freq='QS')

# Calculate squared differences
GB_sqe_unemp = (forecast[forecast.columns[1]] - forecast[forecast.columns[5]])**2
SPF_sqe_unemp = (forecast[forecast.columns[3]] - forecast[forecast.columns[5]])**2
GB_sqe_cons = (forecast[forecast.columns[2]] - forecast[forecast.columns[6]])**2
SPF_sqe_cons = (forecast[forecast.columns[4]] - forecast[forecast.columns[6]])**2

# Calculate difference between SPF and GB sq differences
diff_sqe_unemp = GB_sqe_unemp - SPF_sqe_unemp
diff_sqe_cons = GB_sqe_cons - SPF_sqe_cons

errors_df = pd.DataFrame({'date': quarterly_dates,
                        'GB_error_unemp': GB_sqe_unemp,
                       'SPF_error_unemp': SPF_sqe_unemp,
                       'GB_error_cons': GB_sqe_cons,
                       'SPF_error_cons': SPF_sqe_cons,
                       'diff_error_unemp': diff_sqe_unemp,
                       'diff_error_cons': diff_sqe_cons})

print(errors_df)
errors_df.to_csv('data/output/errors.csv')
# errors_df.to_excel('data/output/errors.xlsx', index=False)
