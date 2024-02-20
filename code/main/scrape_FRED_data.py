import pandas as pd
import numpy as np
import fredpy as fp
import matplotlib.pyplot as plt

fp.api_key = "c735c085b4e162a17326871bc1d5c625"
win = ['01-01-1982','12-01-2017']
win2 = ['10-01-1981','12-01-2018']
unemp = fp.series("UNRATE").window(win2).as_frequency(freq='Q')

#pce_Q = fp.series("PCEPI").window(win2).apc().as_frequency(freq='Q')
#pce_core_Q = fp.series("PCEPILFE").window(win2).apc().as_frequency(freq='Q')

#grPCE_Q = fp.series("PCEC96").window(win).as_frequency(freq='Q').pc(annualized=True)
#grPCE_Q = fp.series("DPCERA3M086SBEA").window(win2).as_frequency(freq='Q').pc(annualized=True)
grPCE_Q = fp.series("DPCERA3Q086SBEA").window(win2).as_frequency(freq='Q').pc(annualized=True)

obs_df = pd.DataFrame({"Unemployment": unemp.data,
                   #"Inflation": pce_Q.data,
                   #"Core Inflation": pce_core_Q.data,        
                   "real Consumption Growth": grPCE_Q.data
})

print(obs_df.head)

decimal = False  # Set to the desired number of decimal places or False to disable formatting

if decimal is not False:
    for column in obs_df.columns[1:]:
        obs_df[column] = obs_df[column].apply(lambda x: f"{x:.{decimal}f}")

obs_df.to_csv('data/output/FRED.csv')

# obs_df.to_excel('data/output/FRED_scraped.xlsx', index=False)