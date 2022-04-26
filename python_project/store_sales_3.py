#Stores to close on sundays?

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Read in Sales Data dataset using specified columns
dfM = pd.read_csv('store_sales/sales_data.csv', usecols=['Store', 'DayOfWeek', 'Sales'])
#Dictionary for converting integer day variables into actual Days
daydic = {1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 7:'Sunday'}


#Create dataframe to grab only Sales that exist on Sunday
dfsundays = dfM[(dfM['DayOfWeek'] == 7)&(dfM['Sales']>0)]
#Create list of the stores in the previous dataframe
sundayStores = list(dfsundays.Store.unique())
#Create new dataframe from the original that only uses the stores that are open Sundays
dfSSt=dfM[dfM['Store'].isin(sundayStores)]


#Create a dictionary for storing the average sales for each day for each store open on Sunday
SundayStoreDict = {}
#Begin iterations using the list of stores open Sunday created above
for store in sundayStores:
    #Temporary dictionary for storing each store's daily average sales
    dayAVG = {}
    for weekday in range(1,8):
        #Create temporary dataframe for each iterated store and for specified day of the week
        dftemp = dfM[ (dfM['Store'] == store) & (dfM['DayOfWeek']==weekday) ]
        #Store the weekday average into the dictionary created above for the accompanying store
        dayAVG[daydic[weekday]]=dftemp.Sales.mean()
    #Add the dayAVG dict into the SundayStoreDict for the specified store from the list above
    SundayStoreDict[store] = dayAVG


#Create a list for stores that should remain open and another for stores that should close
openstore = []
closestore = []
#Iterate through the stores in the SundayStoreDict in order to figure out which should close/stay open
for store in SundayStoreDict:
    #Get the average for Monday through Saturday for each store
    weekdayA = round(sum(list(SundayStoreDict[store].values())[:6])/6,2)
    #Get the average for Sunday for each store
    sundayA = round(list(SundayStoreDict[store].values())[6],2)
    #Create a list to use for checking values and then adding to appropriate openstore/closestore list
    templist = [store, weekdayA, sundayA]
    #Check if Sunday average sales are at least 40% of average sales for other weekdays
    if sundayA < (weekdayA*.4):
        #If less than 40% of weekday average print to close and add templist to closestore list
        print('CLOSE STORE', store)
        closestore.append(templist)
    else:
        #If greater than or equal to 40% of weekday average print to remain open and add templist to openstore list
        print('Store', store, 'should remain open.')
        openstore.append(templist)


#Create a dataframe for the stores to remain open and index it by the store
dfos = pd.DataFrame(data=openstore, columns=['Store', '6_Day_Average', 'Sunday_Average'])
dfos.set_index('Store', inplace=True)
#Create a dataframe for the stores to close on Sundays and index it by the store
dfcs = pd.DataFrame(data=closestore, columns=['Store', '6_Day_Average', 'Sunday_Average'])
dfcs.set_index('Store', inplace=True)


#Iterate through the open store and closed store dataframe and create plots for each in order to get visual confirmation of computers business advice
for storedata in [dfcs, dfos]:
    #Creating X-Axis ticks
    closeind=np.arange(len(storedata))
    #Creating a bar for MON-SAT and a bar for SUN
    monsat = storedata['6_Day_Average']
    sunday = storedata['Sunday_Average']
    width = 0.35
    #Initialize plot
    fig, ax = plt.subplots()
    #Set bars so they are side by side as opposed to stacked or overlapped
    ax.bar(closeind-width/2, monsat, width, color='b')
    ax.bar(closeind+width/2, sunday, width, color='r')
    #Create all axis labels and plot label
    ax.set_ylabel('Sales')
    ax.set_xlabel('Store')
    ax.set_title('Average Store Sales MON-SAT Compared to SUN')
    #Set the X-Axis ticks previously established and label them
    ax.set_xticks(closeind)
    ax.set_xticklabels(list(storedata.index), rotation=(45))
    #Set the Y-Axis limits depending on whether its the open stores or close stores dataframe
    if list(storedata.index) == list(dfcs.index):
        ax.set_yticks(np.arange(0, max(storedata['6_Day_Average'])+500, 1000))
    else:
        ax.set_yticks(np.arange(0, max(max(storedata['6_Day_Average'])+2000, 
        max(storedata['Sunday_Average'])+2000), 2000))
    #Create the plot's legend
    ax.legend(labels=['MON-SAT', 'SUN'])
    #Turn on the ability for the plot to be shown in full screen by default
    fig.canvas.manager.full_screen_toggle()
    #Show the plot for either the closed or open stores dataframe
    plt.show()