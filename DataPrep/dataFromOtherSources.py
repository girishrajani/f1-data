import pandas as pd
import numpy as np


year = input("Enter the year: ")
raceId = input("Enter raceID: ")

openFile = "Data/" + year + "/" + raceId + ".csv"

data = pd.read_csv(openFile)
data = data.drop("Unnamed: 0",axis=1)

size = data.shape[0]

# For not fiving out a warning while changing values
pd.set_option('mode.chained_assignment', None)
trackId = int(input("Enter trackID: "))
data["trackId"] = trackId

# Script for ToPit or NotToPit Coloumn (Output)
# 1 => True (Pit) Box-Box
# 0 => False (Don't Pit)
data["toPit"] = 0
for i in range(size):
    if pd.isna(data["stopNo"][i]):
        data["toPit"][i] = 0
    else:
        data["toPit"][i] = 1


# Script for RaceProgress
# Divide currentlap and total laps
# Required Value between 0 and 1
data["raceProgress"] = float('nan')
for i in range(size):
    curr =  data["lapId"][i]
    tot = data["totalLaps"][i]
    data["raceProgress"][i] = round(curr/tot,2)


# Script for converting time from String to Float
data["lapTimes"] = float('nan')
for i in range(size):
    currentString = data["laptime"][i]
    # minsToSecs = int(currentString[0]) * 60
    # seconds = float(currentString[2:])
    lapTimeInSecs = (int(currentString[0]) * 60) + float(currentString[2:])
    data["lapTimes"][i] = lapTimeInSecs
data = data.drop("laptime",axis=1)



# Add New Cols for Track Cat
trackCat = int(input("Enter race track category: "))
data["trackCat"] = trackCat

# Add New Cols 
data["currentTire"] = None
data["actualCompound"] = None
data["tireAge"] = float("nan")

driverDict = {}
tireDict = {}

soft = input("Enter what Soft(1) Stands for: ")
medium = input("Enter what Medium(2) Stands for: ")
hard = input("Enter what Hard(3) Stands for: ")
tireDict["1"] = soft
tireDict["2"] = medium
tireDict["3"] = hard

# Formation Lap Data
dataStruct = {
    "raceId" : [],
    "trackId" : [],
    "trackCat" : [],
    "raceTrack" : [],
    "lapId" : [],
    "primaryKey" : [],
    "totalLaps" :  [],
    "lapsRem" : [],
    "driverId" : [],
    "laptime" : [],
    "stopNo" : [],
    "stopDuration": [],
    "currentTire" : [],
    "actualCompound" : [],
    "tireAge" : [],
    "raceProgress" :[],
    "lapTimes" : [],
    "safteyCarType" : [],
    "pitStopFulfilled" : [],
    "toPit" : [],
    "toChange" : []
}

raceData = pd.DataFrame(dataStruct)

for i in range(20):
    driver = data["driverId"][i]
    startingTire = int(input("Enter starting tire for " + driver + ": "))
    tireAge = 0
    actualCompound = tireDict[str(startingTire)]
    driverDict[driver] = {
        "currentTire" : startingTire,
        "actualCompound" : actualCompound ,
        "tireAge" : tireAge,
        "pitFulfilled" : 0,
    }
    formationLap = {
        "raceId" : raceId,
        "trackId" : trackId,
        "trackCat" : trackCat,
        "raceTrack" : data["raceTrack"][i],
        "lapId" : 0,
        "primaryKey" : driver + "0",
        "totalLaps" :  data["totalLaps"][i],
        "lapsRem" : data["totalLaps"][i],
        "driverId" : driver,
        "stopNo" : float(0.0),
        "stopDuration": float(0.0),
        "currentTire" : startingTire,
        "actualCompound" : actualCompound,
        "tireAge" : tireAge,
        "raceProgress" : 0.00,
        "lapTimes" : 0.0,
        "safteyCarType": 0,
        "pitStopFulfilled" : 0,
        "toPit" : 0,
        "toChange" : 0
    }
    raceData = raceData.append(formationLap, ignore_index=True)


data["toChange"] = 0

for i in range(size):
    driver = data["driverId"][i]
    if pd.isna(data["stopNo"][i]):
        # Copy Paste the data from Dict
        # Update tireAge by 1
        # Update NaN Values None(Null)
        data["stopNo"][i] = float('nan')
        data["stopDuration"][i] = float(0.0)
        data["currentTire"][i] = driverDict[driver]["currentTire"]
        data["actualCompound"][i] = driverDict[driver]["actualCompound"]
        driverDict[driver]["tireAge"] = int(driverDict[driver]["tireAge"]) + 1
        data["tireAge"][i] = driverDict[driver]["tireAge"]        
    else:
        # Driver Pits:
        # Take user input 
        # Update the Dict
        newTire = input("Enter the new Compund Fitted by "+ driver +" at lap "+ str(data["lapId"][i]) +": ")
        actualCompound = tireDict[str(newTire)]
        tireAge = 0
        driverDict[driver]["currentTire"] = newTire
        driverDict[driver]["actualCompound"] = actualCompound
        driverDict[driver]["tireAge"] = tireAge
        data["currentTire"][i] = driverDict[driver]["currentTire"]
        data["actualCompound"][i] = driverDict[driver]["actualCompound"]
        data["tireAge"][i] = driverDict[driver]["tireAge"]
        data["toChange"][i] = newTire




# Add New Cols for Saftey Car Status
data["safteyCarType"] = 0

print("1: Yes , 0: No")
safteyCar = int(input("Was there a saftey car in this race: "))

safteyDict = {}
counter = 0
lapsWhichHaveSC = []

while safteyCar == 1:
    type = int(input("Enter the Type: (1 for SC or 2 for VSC): "))
    startLap = int(input("Enter start lap: "))
    endLap = int(input("Enter end lap: "))
    for k in range(startLap,endLap):
        safteyDict[k] = type
    safteyDict[endLap] = type
    safteyCar = int(input("Enter 1 if more saftey cars else enter 0: "))

allSafteyCars = list(safteyDict.keys())


# print(allSafteyCars)
for i in range(size):
    lap = int(data["lapId"][i])
    if lap in allSafteyCars:
        data["safteyCarType"][i] = safteyDict[lap]


data["pitStopFulfilled"] = float('nan')

for i in range(size):
    driver = data["driverId"][i]
    if not pd.isna(data["stopNo"][i]):
        driverDict[driver]["pitFulfilled"] = 1      
    data["pitStopFulfilled"][i] = driverDict[driver]["pitFulfilled"]


print(data)


data = raceData.append(data)
filename = "Test/test.csv"

data.to_csv(filename, encoding = 'utf-8-sig',index = False) 























"""
Todo for next time:

    so get all the driver ids 1st by iterating first 20 entries
    then make a new data frame with those driver ids and their starting tires. that will be you lap 0
    then append the csv data frame behind the new dataframe.
    then run a loop with a if else statement seeing that if the pitstop time is nan then
    put the current compund as the compund in the last lap that will be stored in a temp var.
    if its not nan then the program will stop and give the primary key and ask the user/me lol to 
    enter what tire did they change to 

    Add 3 cols:
    Tire Compund: C1,C2,C3,C4,C5
    Meaning: soft,medium, hard
    TireAge: keep on adding everytime

    Assumption for the paper: ALl the tires that are put on are new

"""
