import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
from constants import MAX_HALF_LIFE, WINDOW

def calculate_half_life(spread):
    df_spread = pd.DataFrame(spread, columns=["spread"])
    spread_lag = df_spread.spread.shift(1)
    spread_lag.iloc[0] = spread_lag.iloc[1]
    spread_ret = df_spread.spread - spread_lag
    spread_ret.iloc[0] = spread_ret.iloc[1]
    spread_lag2 = sm.add_constant(spread_lag)
    model = sm.OLS(spread_ret, spread_lag2)
    res = model.fit()
    half_life = round(-np.log(2) / res.params[1], 0)
    return half_life

# calculate z-score
def calculate_z_score(spread):
    spread_series = pd.Series(spread)
    mean = spread_series.rolling(center=False, window=WINDOW).mean()
    std = spread_series.rolling(center=False, window=WINDOW).std()
    x = spread_series.rolling(center=False, window=1).mean()
    z_score = (x-mean)/std
    return z_score

# calculate cointegration
def calculate_cointegration(series_1, series_2):
    series_1 = np.array(series_1).astype(np.float)
    series_2 = np.array(series_2).astype(np.float)
    coint_flag = 0
    coint_res = coint(series_1, series_2)
    coint_t = coint_res[0]
    p_value = coint_res[1]
    critical_value = coint_res[2][1]
    model = sm.OLS(series_1, series_2).fit()
    hedge_ratio = model.params[0]
    spread = series_1 - (hedge_ratio*series_2)
    half_life = calculate_half_life(spread)
    t_check = coint_t < critical_value
    coint_flag = 1 if p_value < 0.05 and t_check else 0
    return coint_flag, hedge_ratio, half_life


def store_cointegration_results(df_market_prices):
    
    # initialize
    markets = df_market_prices.columns.to_list()
    critera_met_pairs = []

    # find cointegrated pairs
    for index, base_market in enumerate(markets[:-1]):
        series_1 = df_market_prices[base_market].values.astype(float).tolist()

        # get base pair
        for quote_market in markets[index+1:]:
            series_2 =  df_market_prices[quote_market].values.astype(float).tolist()

            # check cointegration
            coint_flag, hedge_ratio, half_life = calculate_cointegration(series_1=series_1, series_2=series_2)

            # log pair
            if (coint_flag == 1 and half_life <= MAX_HALF_LIFE and half_life > 0):
                critera_met_pairs.append({
                    "base_market": base_market,
                    "quote_market": quote_market,
                    "hedge_ratio": hedge_ratio,
                    "half_life": half_life
                })
    
    # create and save df
    df_criteria_met = pd.DataFrame(critera_met_pairs)
    df_criteria_met.to_csv('cointegrated_pairs.csv')
    del df_criteria_met

    # return result
    print("Cointegrated pairs saved!")
    return "saved"
