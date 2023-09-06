from joblib import load
import pandas as pd
import numpy as np

model = load('lgbm_model.joblib')

def data_preprocessing(df):
    df = feature_engineering(df)
    df = drop_features(df)
    df = feature_order(df)
    return df



def main(input):
    df = pd.DataFrame([input.model_dump()])
    df = data_preprocessing(df)
    predicted = model.predict_proba(df)[:,1][0] #get cancel probability
    print(predicted)
    return predicted
    
    
    
def feature_engineering(df):
    # total persons
    df['total_persons'] = df['no_of_adults'] + df['no_of_children']

    # total nights
    df['total_nights'] = df['no_of_weekend_nights'] + df['no_of_week_nights']

    # Season
    season_code = {
        'Spring':0,
        'Summer':1,
        'Fall':2,
        'Winter':3,
    }

    def get_season(month):
        if month in [3, 4, 5]:
            return season_code['Spring']
        elif month in [6, 7, 8]:
            return season_code['Summer']
        elif month in [9, 10, 11]:
            return season_code['Fall']
        else:
            return season_code['Winter']

    df['Season'] = df['arrival_month'].apply(get_season)

    # Weekday vs. Weekend Arrival:
    df['Weekday_Arrival'] = (df['arrival_date'] % 7 < 5).astype(int)

    # Cancellation Ratio
    df['Cancellation_Ratio'] = df['no_of_previous_cancellations'] / (df['no_of_previous_cancellations'] + df['no_of_previous_bookings_not_canceled'])


    # Special Request Ratio:
    df['Special_Request_Ratio'] = df['no_of_special_requests'] / df['total_nights']
    df.Special_Request_Ratio.fillna(0, inplace=True)
    df.Special_Request_Ratio.replace([np.inf, -np.inf], 0, inplace=True)

    # Price Per Person
    df['Price_Per_Person'] = df['avg_price_per_room'] / df['total_persons']
    df.Price_Per_Person.replace([np.inf, -np.inf], 0, inplace=True)

    # Children Ratio
    df['Children_Ratio'] = df['no_of_children'] / df['total_persons']
    df.Children_Ratio.fillna(0, inplace=True)

    # Adults  Ratio:
    df['Adults_Ratio'] = df['no_of_adults'] / df['total_persons']
    df.Adults_Ratio.fillna(0, inplace=True)

    # Is_Repeated_Guest:
    df['Is_Repeated_Guest'] = df['repeated_guest'] * df['no_of_previous_bookings_not_canceled']
    
    return df

def drop_features(df):

    # drop all columns which have 0 corr relation
    df = df.drop(['Children_Ratio','Adults_Ratio','arrival_date','no_of_children'], axis=1)

    # drop low important feattures
    df = df.drop(['no_of_previous_cancellations','no_of_adults','no_of_previous_bookings_not_canceled','Cancellation_Ratio','total_persons','Is_Repeated_Guest'], axis=1)
    
    return df

def feature_order(df):
    order = ['no_of_weekend_nights', 'no_of_week_nights', 'type_of_meal_plan',
       'required_car_parking_space', 'room_type_reserved', 'lead_time',
       'arrival_year', 'arrival_month', 'market_segment_type',
       'repeated_guest', 'avg_price_per_room', 'no_of_special_requests',
       'total_nights', 'Season', 'Weekday_Arrival', 'Special_Request_Ratio',
       'Price_Per_Person']
    return df.reindex(columns=order)