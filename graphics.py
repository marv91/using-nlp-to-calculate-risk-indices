
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

from pylab import rcParams
rcParams['figure.figsize'] = 10, 5

keys = ["date", "value"]
parse_dates = ["date"]
dtypes = {"value":np.float64}

date_index = pd.date_range('01/01/1990', periods=365*30, freq='D')

manually_index = pd.read_csv("manually_index_raw.csv", names = keys, dtype = dtypes ,parse_dates = parse_dates)
tech_index = pd.read_csv("Technology_Risk_index_raw.csv", names = keys, dtype = dtypes ,parse_dates = parse_dates)
eco_index = pd.read_csv("Economic_Risk_index_raw.csv", names = keys, dtype = dtypes, parse_dates = parse_dates)
international_index = pd.read_csv("International_Risk_index_raw.csv", names = keys, dtype = dtypes, parse_dates = parse_dates)
climate_index = pd.read_csv("ClimateChange_Risk_index_raw.csv", names = keys, dtype = dtypes, parse_dates = parse_dates)

manually_index.set_index("date", inplace = True)
tech_index.set_index("date", inplace = True)
eco_index.set_index("date", inplace = True)
international_index.set_index("date", inplace = True)
climate_index.set_index("date", inplace = True)

manually_index = manually_index.reindex(date_index)
tech_index = tech_index.reindex(date_index)
eco_index = eco_index.reindex(date_index)
international_index = international_index.reindex(date_index)
climate_index = climate_index.reindex(date_index)

manually_index.interpolate("time", inplace = True)
tech_index.interpolate("time", inplace = True)
eco_index.interpolate("time", inplace = True)
international_index.interpolate("time", inplace = True)
climate_index.interpolate("time", inplace = True)

manually_index.dropna(inplace = True)
tech_index.dropna(inplace = True)
eco_index.dropna(inplace = True)
international_index.dropna(inplace = True)
climate_index.dropna(inplace = True)

manually_index_1m = manually_index.resample("1M").mean()
tech_index_1m = tech_index.resample("1M").mean()
eco_index_1m = eco_index.resample("1M").mean()
international_index_1m = international_index.resample("1M").mean()
climate_index_1m = climate_index.resample("1M").mean()


manually_index_1m["01-01-1990":"01-01-2019"].plot(kind='line', title = "Calculated Index", color = "black", legend = False)
plt.savefig('Graphics/WSJ_Manually_Index.png')
tech_index_1m["01-01-1990":"01-01-2019"].plot(kind='line', title = "WSJ Digitalization Index", color = "black", legend = False)
plt.savefig('Graphics/WSJ_Technology_Index.png')
eco_index_1m["01-01-1990":"01-01-2019"].plot(kind='line', title = "WSJ Economic Index", color = "black", legend = False)
plt.savefig('Graphics/WSJ_Economic_Index.png')
international_index_1m["01-01-1990":"01-01-2019"].plot(kind='line', title = "WSJ Trade Index", color = "black", legend = False)
plt.savefig('Graphics/WSJ_Trade_Index.png')
climate_index_1m["01-01-1990":"01-01-2019"].plot(kind='line', title = "WSJ Climate Index", color = "black", legend = False)
plt.savefig('Graphics/WSJ_Climate_Index.png')

risk_premium = pd.read_csv("Risk_Premium.csv", parse_dates = ["date"])
risk_premium.set_index("date", inplace = True)

risk_factors = ["ClimateChange_Risk", "International_Risk", "Economic_Risk", "Technology_Risk", "manually"]


for rf in risk_factors:
    name = rf
    if (rf == "International_Risk"):
       name = "Trade_Risk" 
    if (rf == "Technology_Risk"):
       name = "Digitalization_Risk" 
    if (rf == "manually"):
       name = "Calculated" 
    risk_premium[rf].plot(title = name + " Risk Premium", color = "black")
    plt.savefig("Graphics/" + rf + "_Risk_Premium" +".png")
    plt.show()

