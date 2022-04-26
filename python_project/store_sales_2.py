#Is competition distance a factor in sales for stores/storetypes?

import pandas as pd
#Set option so it shows all rows and columns despite the size
pd.set_option('display.max_rows', None, 'display.max_columns',None)


#Read in the Sales dataset using specified columns
df_sales = pd.read_csv('store_sales/sales_data.csv', usecols=['Store', 'Sales'])
#Read in the Stores dataset using specified columns
df_stores = pd.read_csv('store_sales/store_data.csv', usecols=['Store', 'StoreType', 'CompetitionDistance'])


#Merge the two datasets on the Store column
dfM = pd.merge(df_sales,df_stores, on='Store')
#Clean data so only fields are those that have actual sales AND competition locally
dfM = dfM[(dfM['Sales'] != 0) & (dfM['CompetitionDistance'].isnull()==False)]
#Get basic statistics for the Sales and CompetitionDistance columns
dfM[['Sales', 'CompetitionDistance']].describe()


#Group dataset by the Store
dfS = dfM.groupby('Store')
#Get basic statistics for Sales and CompetitionDistance
dfS['Sales'].describe().head(100)
#Get the average Sales and CompetitionDistance of each store
dfSC = dfS.agg({'Sales':'mean', 'CompetitionDistance':'mean'})
#Sort the aggregated columns by Sales from highest to lowest
dfSC_sorted=dfSC.sort_values('Sales', ascending=False)
#Check top 300 stores in sales and see if Competition Distance seems to be a factor
dfSC_sorted.head(300)
#Check correlation with correlation function
dfSC_sorted.corr()


#Group original dataset by the Store Type (either a,b,c or d)
dfT = dfM.groupby('StoreType')
#Get statistics on Sales and Competition Distance for each store type
dfT[['Sales', 'CompetitionDistance']].describe()
#Get the average Sales and Competition Distance for each store type
dfTC = dfT.agg({'Sales':'mean', 'CompetitionDistance':'mean'})
#Check data to see if Competition Distance seems to be a factor
print(dfTC)
#Create list of store types to check intuition
stypes = ['a','b','c','d']
#Iterate through types and see if correlation between Sales and Competition Distance
for type in stypes:
    #Create temporary dataframe from original merged dataframe for just iterated store type
    tempdf = dfM[dfM['StoreType']==type]
    #reduce to just Sales and Competition Distance columns
    tempdf = tempdf[['Sales','CompetitionDistance']]
    #print correlation to confirm/deny intuition
    print(tempdf.corr())
