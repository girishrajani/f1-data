import requests
import pandas as pd


def getRaceLapTimeData(year, raceNo, raceId, totalLaps):
    dataStruct = ({
        'raceId': [],
        "raceTrack" : [],
        'lapId' : [],
        'primaryKey' : [],
        "totalLaps" : [],
        "lapsRem" : [],
        'driverId' : [],
        # 'position': [],
        'laptime': [],
    })
    raceData = pd.DataFrame(dataStruct)

    URL = "https://ergast.com/api/f1/"+year+"/"+raceNo+"/laps.json?limit=10000"

    apiCall = requests.get(URL)
    jsonResponse = apiCall.json()
    lapData = jsonResponse["MRData"]["RaceTable"]["Races"][0]['Laps']
    raceTrack = jsonResponse["MRData"]["RaceTable"]["Races"][0]["raceName"]
    for i in range(totalLaps):
        allDriversLapTimings = lapData[i]["Timings"]
        currentLap = lapData[i]["number"]
        print("Processing Lap: ",currentLap)
        for current in allDriversLapTimings:
            driverId = current["driverId"]
            position = current["position"]
            laptime = current["time"]
            lapsRem = totalLaps - int(currentLap)
            primKey = driverId + currentLap
            importLapData = {
                "raceId" : raceId,
                "raceTrack" : raceTrack,
                "lapId" : currentLap,
                "primaryKey" : primKey,
                "totalLaps" : totalLaps,
                "lapsRem" : lapsRem,
                "driverId" : driverId,
                "laptime" : laptime
            }
            raceData = raceData.append(importLapData, ignore_index=True)
    return raceData



def getPitStopData(year,raceNo,raceId):
# def getPitStopData():
    dataStruct = ({
        'primaryKey' : [],
        'stopNo' : [],
        'stopDuration': [],
    })
    pitData = pd.DataFrame(dataStruct)
    
    URL = "https://ergast.com/api/f1/"+year+"/"+raceNo+"/pitstops.json?limit=10000"
    # URL = "https://ergast.com/api/f1/2019/1/pitstops.json?limit=1000"
    apiCall = requests.get(URL)
    jsonResponse = apiCall.json()
    pitStops = jsonResponse["MRData"]["RaceTable"]["Races"][0]['PitStops']
    print("Processsing All the PitStops")
    for perStop in pitStops:
        primaryKey = perStop["driverId"] + perStop["lap"]
        stopNo = perStop["stop"]
        stopDuration = perStop["duration"]
        importStopData = {
            "primaryKey" : primaryKey,
            "stopNo" : stopNo,
            "stopDuration": stopDuration
        }
        pitData = pitData.append(importStopData, ignore_index=True)
    return pitData


def joinTwoDataFrames(lapTimes,pitStops):
    print("Combining all the Data")
    df = pd.merge(lapTimes, pitStops, on='primaryKey', how='left')
    print(df.head(20))


def saveLaptimeCSV(saveToCSV,filename):
    saveToCSV.to_csv(filename, encoding = 'utf-8-sig') 
    return 0


year = input("Enter the Year: ")
raceno = input("Enter the Race No. : ")
raceId = int(input("Enter the raceId: "))
totalLaps = int(input("Enter No. of Laps: "))

# print(getPitStopData())

allPitStops = getPitStopData(year,raceno,raceId)

lapTimesForAllDrivers = getRaceLapTimeData(year,raceno,raceId,totalLaps)

joinTwoDataFrames(lapTimesForAllDrivers,allPitStops)
file = "data/"+year+"/"+str(raceId) + ".csv" 
saveLaptimeCSV(lapTimesForAllDrivers, file)



"""
Logic Behind the Ergest API Scripts:

2 API Endpoints Used:
    1. Laptimes
    2. PitStops

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
"""