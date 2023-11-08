# Data Preparation

Logic Behind the Ergest API Scripts:

2 API Endpoints Used: <br>
    1. Laptimes https://ergast.com/api/f1/2019/1/laps.json?limit=10000 <br> 
    2. PitStops https://ergast.com/api/f1/2019/1/pitstops.json?limit=10000 <br> 

    Input Parameters:
        => year/season
        => round/race no.
        => no. of laps
        => custom unique raceid/ csv file name

    Explanation:
    => Both the endpoints are called seprately and are then stored in DataFrames.
    => Each lap or row or data-entry is given a unique id i.e. the primary key for both the dataframes.
    => Primary Key derivation ->  driverid+lapno
    => This primary key is later used for Joining the 2 Dataframes.
    => Left Outer Join is used to merge the 2 dataframes, so that the values for laps which didn't have pitstops 
    while be set to NaN
    => df = pd.merge(a, b, on='id', how='left')
    => Once merged the Primary key can be dropped from the Dataframe
    => All the data is then exported to a CSV File 