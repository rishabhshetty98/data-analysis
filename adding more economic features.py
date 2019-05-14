import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

api_key = open('quandlapikey.txt','r').read()


    

def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/U.S._postal_abbreviations#States')
    return fiddy_states[0][0][2:]  #column of the dataframe

def grab_initial_state_data():
    
    states= state_list()
    main_df = pd.DataFrame()

    for abbv in states:
        query =  "FMAC/HPI_"+str(abbv)
        df = quandl.get(query, authtoken = api_key)
        df.rename(columns={'NSA Value':str(abbv) + ' NSA Value' , 'SA Value' : str(abbv) + ' SA Value'}, inplace=True)
        df [abbv +' NSA Value'] = (df [abbv +' NSA Value'] - df [abbv +' NSA Value'] [0]) / df [abbv +' NSA Value'] [0] * 100.0
        df [abbv + ' SA Value'] = (df [abbv +' SA Value'] - df [abbv +' SA Value'] [0]) / df [abbv +' SA Value'] [0] * 100.0

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    print(main_df.head())

    pickle_out = open('fiddy_states3.pickle','wb') 
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken = api_key)
    df ['NSA Value'] = (df ['NSA Value'] - df ['NSA Value'] [0]) / df ['NSA Value'] [0] * 100.0
    df ['SA Value'] = (df ['SA Value'] - df ['SA Value'] [0]) / df ['SA Value'] [0] * 100.0
    return df

def mortgage_30yr():
    df = quandl.get("FMAC/MORTG", trim_start = "1975-01-01", authtoken = api_key)
    df["Value"]=(df["Value"]-df["Value"][0])/df["Value"][0]*100
    df = df.resample('M').mean()
    df.columns = ['M30']
    return df

def sp500_data():
    df = quandl.get("MULTPL/SP500_REAL_PRICE_MONTH", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Value':'sp500'}, inplace=True)
    df = df['sp500']
    return df

def gdp_data():
    df = quandl.get("BCB/4385", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Value':'GDP'}, inplace=True)
    df = df['GDP']
    return df


    

sp500 = sp500_data()
US_GDP = gdp_data()
m30 = mortgage_30yr()
HPI_data = pd.read_pickle('fiddy_states3.pickle')
HPI_bench = HPI_Benchmark()

HPI = HPI_data.join(m30, US_GDP, sp500 )
print(HPI)
print(HPI.corr())


 
