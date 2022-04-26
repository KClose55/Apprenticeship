#Top 10 most selling and least selling stores and difference between highest and lowest sales

import pandas as pd


#Load dataset with just required columns
df_sales = pd.read_csv('store_sales/sales_data.csv', usecols=['Store', 'Sales'])
#Check to ensure correct columns
df_sales.columns


#Grouping dataset by the Store column
dfM = df_sales.groupby('Store')
#Creating a variable summing the Sales column
dfMS = dfM.agg('sum')
#Sort column from largest to smallest
dfMS = dfMS.sort_values('Sales', ascending=False)


#Show top 10
dfMS.head(10)
#Show bottom 10
dfMS.tail(10)


#Difference between highest and lowest sales
print(f'${dfMS.iloc[0,0]-dfMS.iloc[-1,0]:,}')
