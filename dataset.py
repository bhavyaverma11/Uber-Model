import pandas as pd
import numpy as np
import datetime 

traffic_df= pd.read_csv("./Dataset_Uber Traffic.csv")
events_df= pd.read_csv("./events.txt")
tempRain_df= pd.read_csv("./temp_rain.csv")

traffic_df.info()
events_df.info()
tempRain_df.info()

traffic_df['Date']= traffic_df['DateTime'].str[:6] + '20' + traffic_df['DateTime'].str[6:8] 
traffic_df['Date2']= pd.to_datetime(traffic_df['Date'], format="%d/%m/%Y")

events_df['Date2']= pd.to_datetime(events_df['Date'], format= "%Y-%m-%d")

tempRain_df['Date2']= pd.to_datetime(tempRain_df['Date'], format= "%d-%m-%Y")

traffic_event= pd.merge(traffic_df, events_df, how='left', on="Date2")

traffic_event_temp= pd.merge(traffic_event, tempRain_df, how='left', on="Date2")

traffic_event_temp = traffic_event_temp.drop(columns=['Date_x', 'Year', 'Date_y', '_id', 'Date'])

traffic_event_temp.rename(columns= {'Date2': 'Date'}, inplace= True)

traffic_event_temp['Category']= traffic_event_temp['Category'].fillna('No Category')

traffic_event_temp['Event Name']= traffic_event_temp['Event Name'].fillna('No Event')

traffic_event_temp['Venue/Location']= traffic_event_temp['Venue/Location'].fillna('No Venue/Location')

traffic_event_temp['time']= traffic_event_temp['DateTime'].str[9:]

traffic_event_temp['TimeStamp']= pd.to_datetime(traffic_event_temp['time'], format='%H:%M').dt.time

traffic_event_temp.drop(columns=('time'), inplace= True)

final_dataset= traffic_event_temp[['DateTime', 'Date', 'TimeStamp', 'Junction', 'Vehicles', 'ID', 'Category', 'Event Name',
                                   'Venue/Location', 'Rain', 'Temp Max', 'Temp Min']]


final_dataset.drop_duplicates(subset=['DateTime', 'Junction', 'ID'], inplace=True)

final_dataset.to_csv('./Integrated Dataset.csv', index= False)
