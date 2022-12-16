import pymongo
import pandas as pd

client = pymongo.MongoClient()

# Selecting database
db = client.NA_project

# Create Collection
# db.create_collection('CityPop_2_Restaurant')

# Import CSV
# csv_path = r'C:\Users\Dell\Documents\Datasets\FastFood_Population_City.csv'
# csv_data = pd.read_csv(csv_path)
# csv_data.head()

# Convert CSV into dictionary (aka: JSON Object)
# dict_data = csv_data.to_dict(orient='records')
# print([document for document in dict_data[:5]])

# Import data into MongoDB
# db.CityPop_2_Restaurant.insert_many(dict_data)

# Selecting collection
collection = db.CityPop_2_Restaurant
number_documents = collection.count_documents({})
collection_keys = list(collection.find_one().keys())
restaurant_names = collection.distinct('Restaurant Name')

# Population Growths
# distinct_pop_growths = collection.distinct('Population Growth')

# original_distinct_pop_growths_list = \
# [-97.0, -96.0, -95.0, -93.0, -90.0, -88.0, -82.0, -81.0, -80.0, -75.0, -72.0, -70.0, -68.0, -63.0, -62.0, -54.0, -32.0, -29.0, -26.0, -22.0, 
# -21.0, -20.0, -19.0, -18.0, -17.0, -16.0, -15.0, -14.000000000000002, -13.0, -12.0, -11.0, -10.0, -9.0, -8.0, -7.000000000000001, -6.0, -5.0, 
# -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.000000000000001, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.000000000000002, 15.0, 
# 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.000000000000004, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 
# 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 50.0, 51.0, 54.0, 55.00000000000001, 56.00000000000001, 56.99999999999999, 
# 57.99999999999999, 59.0, 63.0, 64.0, 65.0, 68.0, 69.0, 70.0, 73.0, 74.0, 75.0, 77.0, 82.0, 85.0, 87.0, 91.0, 93.0, 109.0, 119.0, 136.0, 141.0, 
# 145.0, 166.0, 177.0, 182.0, 195.0, 213.0, 238.0, 265.0, 291.0, 313.0, 396.0, 438.0, 717.0]

# Growths to change:
# growths_to_change = [ratio for ratio in original_distinct_pop_growths_list if len(str(ratio)) > 5]
# growths_to_change

# Change growths to all have maximum of 1 decimal spot
# for ratio in growths_to_change:
#     collection.update_many({'Population Growth': ratio}, {'$set': {'Population Growth': round(ratio,1)}})

# Distinct Population Growths after cleaning data
# distinct_pop_growths = collection.distinct('Population Growth')
# distinct_pop_growths

# Create a US Regions dictionary to use at a later time
regions_dict = {}
state_regions = pd.read_csv(r'C:\Users\Dell\Documents\Python\PyMongo\state_regions.csv')
regions = state_regions['Region'].unique()
for region in regions:
    regions_dict[region] = {}
divisions = state_regions['Division'].unique()
for division in divisions:
    tempdf = state_regions[state_regions['Division'] == division]
    region = tempdf['Region'].head(1).values[0]
    if division not in regions_dict[region]:
        regions_dict[region][division] = []
states = state_regions['State Code'].unique()
for state in states:
    tempdf = state_regions[state_regions['State Code'] == state]
    region, division = tempdf[['Region', 'Division']].values[0]
    regions_dict[region][division].append(state)


# Check the population growths by state
full_collection_state_avg_pop_growth = list(collection.aggregate([{'$group': {'_id':'$State', 'Population Growth':{'$avg':'$Population Growth'}}},
                                                                    {'$sort':{'Population Growth':-1}}]))
state_population_growth_dataframe = pd.DataFrame(full_collection_state_avg_pop_growth)
state_population_growth_dataframe.rename(columns={'_id':'State'}, inplace=True)
state_population_growth_dataframe

regions_dict


'''
Create seperate collections based on region
for region in regions:
    region_states = []
    for division in regions_dict[region]:
        region_states += regions_dict[region][division]
    print(region,region_states)
    pipeline = [{'$match': {'State':{'$in':region_states}}},
                {'$out':region}]
    collection.aggregate(pipeline)
'''
# Pull in each regions collection
south_collection = db.South
midwest_collection = db.Midwest
west_collection = db.West
northeast_collection = db.Northeast


# Check Kentucky's Population growths by city
ky_pipeline = [{'$match': {'State':'KY'}},
               {'$group': {'_id':'$City', 'Population Growth':{'$avg':'$Population Growth'}}},
               {'$sort':{'Population Growth':-1}}]
kentucky_list = list(south_collection.aggregate(ky_pipeline))
kentucky_dataframe = pd.DataFrame(kentucky_list)
kentucky_dataframe.rename(columns={'_id':'State'}, inplace=True)
kentucky_dataframe


# Check entire collections for Population Growth Ratios > 50 and Number of restaurants
population_growth_pipeline = [{'$match': {'Population Growth': {'$gte':50}}},
                              {'$group': {'_id': ['$City', '$State'],
                                          'Restaurants':{'$sum':1},
                                          'Population Growth':{'$first':'$Population Growth'}}},
                              {'$sort':{'Population Growth':-1}}]
population_growth_50 = list(collection.aggregate(population_growth_pipeline))
population_growth_50_dataframe = pd.DataFrame(population_growth_50)
population_growth_50_dataframe.rename(columns={'_id':'City, State'}, inplace=True)
population_growth_50_dataframe

# Check if 70% of top 10 are actually in Northeast
regions_dict['Northeast']

# Create a dataframe checking population Differences by numbers as opposed to ratios
top_list = list(population_growth_50_dataframe['City, State'].head(10))
city_state_list = []
for city_state in top_list:
    city,state = city_state
    city_state_list += list(collection.aggregate([{'$match':{'City':city, 'State':state}},
                                                  {'$project':{'_id':0, 'City':1, 'State':1, 'Population 2020':1, 'Population 2015':1, 
                                                               'Population Difference':{'$subtract':['$Population 2020', '$Population 2015']}}},
                                                  {'$limit':1}]))
city_state_df = pd.DataFrame(city_state_list)
city_state_df

# Check the population difference by number and state as opposed to ratio and city
state_group = city_state_df.groupby('State')
state_group_df = pd.DataFrame(state_group['Population Difference'].sum())
state_group_df.sort_values('Population Difference', ascending=False, inplace=True)
state_group_df

# Double check that one of the NJ cities seems to be the best choice
city_state_df.sort_values('Population Difference', ascending=False, inplace=True)
city_state_df
