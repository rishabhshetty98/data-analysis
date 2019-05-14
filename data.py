import pandas as pd

df = pd.read_csv('FMAC-HPI_49700.csv')

print(df.head())
df.set_index('Date', inplace=True)
df.to_csv('newcsv2.csv')

df = pd.read_csv('newcsv2.csv')
print(df.head())

df = pd.read_csv('newcsv2.csv', index_col=0)
print(df.head())

df.columns= ['Cabo NSA value', 'Cabo SA value']
print(df.head())

df.to_csv('newcsv3.csv')
df.to_csv('newcsv4.csv', header=False)

df=pd.read_csv('newcsv4.csv', names=['Date', 'Cabo NSA', 'Cabo SA'], index_col=0)
print(df.head())

df.to_html('example.html')
df.rename(columns={'Cabo SA':'Cabo Seasonally Adjusted'}, inplace = True)
print(df.head())


 
