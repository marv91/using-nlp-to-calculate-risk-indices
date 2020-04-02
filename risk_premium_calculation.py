
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import statsmodels.api as SM

def insert(df, row):
    insert_loc = df.index.max()

    if np.isnan(insert_loc):
        df.loc[0] = row
    else:
        df.loc[insert_loc + 1] = row

returns_raw = pd.DataFrame()

for filename in os.listdir("stock_prices"):
    if filename.endswith(".csv"): 
        print(filename)
        stock = pd.read_csv("stock_prices/" + filename)
        stock_name = filename[0:-4]
        stock.drop(["OPEN", "HIGH", "LOW", "VOLUME", "COUNT"], axis = 1, inplace = True)
        yest = stock.shift(1)
        yest.columns = ["Date", "close_yest"]
        yest.drop(["Date"], axis = 1, inplace = True)
        stock = pd.concat([stock, yest], axis = 1)
        stock.dropna(inplace = True)
        stock[stock_name] = np.log(stock.CLOSE / stock.close_yest)
        stock.drop(["CLOSE", "close_yest"], axis = 1, inplace = True)
        stock['Date'] = stock['Date'].astype('datetime64[ns]')
        stock[stock_name] = stock[stock_name].astype('float')
        stock.set_index("Date",inplace = True)
        returns_raw = pd.concat([returns_raw,stock], axis = 1)
        continue
    else:
        continue
                
returns = returns_raw.resample('M').sum()


# In[14]:


returns.head()

risk_factors = ["manually", "ClimateChange_Risk", "International_Risk", "Economic_Risk", "Technology_Risk"]

risk_premiums = pd.DataFrame()

resid_df = pd.DataFrame()

for rf in risk_factors:
    
    print("starting: " + rf)
    
    index = pd.read_csv(rf + "_index_raw.csv", names = ["date","value"])
    index['date'] = index['date'].astype('datetime64[ns]')
    index['value'] = index['value'].astype('float')
    index.set_index("date", inplace = True)
    index.interpolate(inplace=True,axis=1)
    index = index.resample("M").mean()
    
    data_1M = pd.concat([index,returns], axis = 1)
    data_1M  = data_1M["1990-01-31":"2018-11-30"]
    
    print(data_1M.head())
    
    data_1M.interpolate(inplace=True)
    

    X = SM.add_constant(data_1M["value"].dropna().iloc[:-1].values)

    model = SM.OLS(data_1M["value"].dropna().iloc[1:],X, missing = "drop")
    model_fit = model.fit()
    
    print("**********************************************************")
    print(rf + " OLS summary:")
    print(model_fit.summary())
    print("**********************************************************")
    
    '''
    shift twice. 
    - first because regression was performed on n-1 values
    - second because we want to regress resdiual t-1 against stock return t
    '''
    
    data_1M["EI_Residuals"] = model_fit.resid.shift(2)
    data_1M.drop(["value"], axis = 1, inplace = True)
    #data_1M.drop(["EI_Residuals_raw"], axis = 1, inplace = True)
    
    resid_df[rf] = data_1M["EI_Residuals"]

    from sklearn import linear_model

    betas = pd.DataFrame(columns = ["comp", "beta"])
    print(betas.head())

    for col in data_1M.columns:

        if col == "EI_Residuals":
            continue

        try:
            X = data_1M[["EI_Residuals", col]]
            X.dropna(inplace = True)

            X = SM.add_constant(X)

            X_ = X[["const", "EI_Residuals"]]
            
            regr = SM.OLS(X[col].values.reshape(-1,1), X_, missing = "drop")
            regr_fit = regr.fit()

            insert(betas,[col,regr_fit.params["EI_Residuals"]])

        except:

            continue
            
            
    betas.set_index("comp", inplace = True)
    
    result = data_1M.drop("EI_Residuals", axis = 1).transpose()

    full = result.merge(right = betas, how = "left", left_index = True, right_index = True)
    risk_premium = pd.DataFrame(columns = ["date", "risk_premium"])
    
    print(abs(full[["beta"]]).sort_values(by = ["beta"], ascending=False).head())

    for col in full.columns:

        if col == "beta":
            continue
            
        regression_data = full[["beta", col]].dropna()

        X = SM.add_constant(regression_data[col].values)
        model = SM.OLS(regression_data["beta"].values,X, missing = "drop")
        model_fit = model.fit()
        insert(risk_premium,[col,model_fit.params[1]])
    
    risk_premiums["date"] = risk_premium["date"]
    risk_premiums[rf] = risk_premium["risk_premium"]
            
    print("finished: " + rf)

risk_premiums.set_index("date", inplace = True)

risk_premiums.to_csv("Risk_Premium.csv")

