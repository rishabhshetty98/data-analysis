import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

api_key = open('quandlapikey.txt','r').read()

##df= quandl.get('FMAC/HPI_47380', authtoken=api_key)
##print(df.head())

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
                    
    

##grab_initial_state_data()

##fig = plt.figure()
##ax1 = plt.subplot2grid((1,1,),(0,0))                    

HPI_data = pd.read_pickle('fiddy_states3.pickle')
##benchmark = HPI_Benchmark()
##                    
##HPI_data.plot(ax = ax1)
##benchmark.plot(ax=ax1, color='k', linewidth=10)
##                    
##plt.legend().remove()
##plt.show()

HPI_State_Correlation = HPI_data.corr()
print(HPI_State_Correlation)

print(HPI_State_Correlation.describe())

    

