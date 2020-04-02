
# coding: utf-8

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

indices = pd.DataFrame()

indices["manually"] = manually_index_1m["value"]
indices["ClimateChange_Risk"] = climate_index_1m["value"]
indices["International_Risk"] = international_index_1m["value"]
indices["Economic_Risk"] = eco_index_1m["value"]
indices["Technology_Risk"] = tech_index_1m["value"]

print(indices.corr().round(2))

indices.corr().round(2).to_csv("csv\\corr_index.csv")

risk_premium = pd.read_csv("Risk_Premium.csv", parse_dates = ["date"])
risk_premium.set_index("date", inplace = True)

scaling = {"manually" : 0.066930,
          "ClimateChange_Risk" : 0.056938,
          "International_Risk": 0.079334,
          "Economic_Risk" :0.114494,
          "Technology_Risk" : 0.055559}

for rf in ["manually", "ClimateChange_Risk", "International_Risk", "Economic_Risk", "Technology_Risk"]:
   
    plt.plot(risk_premium[rf], color = "black")
    if rf == "manually":
        plt.title("Manually risk premium")
    if rf == "ClimateChange_Risk":
        plt.title("Climate change risk premium")
    if rf == "International_Risk":
        plt.title("International risk premium")
    if rf == "Economic_Risk":
        plt.title("Economic risk premium")
    if rf == "Technology_Risk":
        plt.title("Technology risk premium")
    plt.savefig("Graphics/" + rf + "_Risk_Premium" +".png")
    plt.show()

    
    print(risk_premium.mean()[rf]/scaling[rf])


risk_premium.rolling(window=12).mean().plot()
plt.legend(["manually","Climate change", "Economic", "International", "Digitalization"])
plt.show()

risk_premium.resample("Y").sum().rolling(window=2).mean().plot()
plt.show()

## Premiums

risk_premium.corr().round(2).head()
risk_premium.corr().round(2).to_csv("csv\\corr_premiums.csv")


from scipy import stats

for rf in  ["manually", "ClimateChange_Risk", "International_Risk", "Economic_Risk", "Technology_Risk"]:
    print(rf + ": " + str(stats.ttest_1samp((risk_premium[rf]/scaling[rf]), 0)))


risk_factors = ["ClimateChange_Risk", "International_Risk", "Economic_Risk", "Technology_Risk", "manually"]

risk_premium_std = pd.DataFrame()

for rf in risk_factors:
    risk_premium_std[rf] = risk_premium[rf] / scaling[rf]
    print(rf)
    print("MEAN " + str(risk_premium_std.mean()[rf]))
    print("SD " + str(risk_premium_std.std()[rf]))
    print("RSD " + str(risk_premium_std.std()[rf]/risk_premium_std.mean()[rf]))
    print()
    
print(risk_premium_std.std())



