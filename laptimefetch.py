import requests
import pandas as pd


def getRaceLapTimeData(year, raceNo, raceId, totalLaps):
    dataStruct = ({
        'raceId': [],
        "raceTrack" : [],
        'lapId' : [],
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
            importData = {
                "raceId" : raceId,
                "raceTrack" : raceTrack,
                "lapId" : currentLap,
                "totalLaps" : totalLaps,
                "lapsRem" : lapsRem,
                "driverId" : driverId,
                "laptime" : laptime
            }
            raceData = raceData.append(importData, ignore_index=True)
    return raceData



def saveCSV(saveToCSV,filename):
    saveToCSV.to_csv(filename, encoding = 'utf-8-sig') 
    return 0


year = input("Enter the Year: ")
raceno = input("Enter the Race No. : ")
raceId = int(input("Enter the raceId: "))
totalLaps = int(input("Enter No. of Laps: "))

lapTimesForAllDrivers = getRaceLapTimeData(year,raceno,raceId,totalLaps)
file = str(raceId) + ".csv" 
saveCSV(lapTimesForAllDrivers, file)

