import quandl
import pandas as pd

api_key = open('quandlapikey.txt','r').read()

##df= quandl.get('FMAC/HPI_47380', authtoken=api_key)
##print(df.head())

fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/U.S._postal_abbreviations#States')
print(fiddy_states[0][0])  #column of the dataframe

for abbv in fiddy_states[0][0][2:]:
    print("FMAC/HPI_"+str(abbv))
