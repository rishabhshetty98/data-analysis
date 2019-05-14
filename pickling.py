import quandl
import pandas as pd
import pickle

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
        df ['SA Value'] = (df ['SA Value'] - df ['SA Value'] [0]) / df ['SA Value'] [0] * 100.0.

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    print(main_df.head())

    pickle_out = open('fiddy_states.pickle','wb') ##pickle using pickle library
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

##grab_initial_state_data()

pickle_in = open('fiddy_states.pickle','rb')
HPI_data = pickle.load(pickle_in)
print(HPI_data)

HPI_data.to_pickle('pickle.pickle') ##pickle using pandas library
HPI_data2 = pd.read_pickle('pickle.pickle')
print(HPI_data2)

    

    

