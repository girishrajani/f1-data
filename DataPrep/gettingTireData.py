import pandas as pd
import numpy as np


year = input("Enter the year: ")
raceId = input("Enter raceID: ")

openFile = "Data/" + year + "/" + raceId + ".csv"

data = pd.read_csv(openFile)
data = data.drop("Unnamed: 0",axis=1)

# For not fiving out a warning while changing values
pd.set_option('mode.chained_assignment', None)

# Add New Cols 
data["currentTire"] = None
data["actualCompound"] = None
data["tireAge"] = float("nan")

driverDict = {}
tireDict = {}

soft = input("Enter what Soft Stands for: ")
medium = input("Enter what Medium Stands for: ")
hard = input("Enter what Hard Stands for: ")
tireDict["soft"] = soft
tireDict["medium"] = medium
tireDict["hard"] = hard


dataStruct = {
    "raceId" : [],
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
}

raceData = pd.DataFrame(dataStruct)

for i in range(20):
    driver = data["driverId"][i]
    startingTire = input("Enter starting tire for " + driver + ": ")
    tireAge = 0
    actualCompound = tireDict[startingTire]
    driverDict[driver] = {
        "currentTire" : startingTire,
        "actualCompound" : actualCompound ,
        "tireAge" : tireAge,
    }
    formationLap = {
        "raceId" : raceId,
        "raceTrack" : data["raceTrack"][i],
        "lapId" : 0,
        "primaryKey" : driver + "0",
        "totalLaps" :  data["totalLaps"][i],
        "lapsRem" : data["totalLaps"][i],
        "driverId" : driver,
        "laptime" : "0:0.0",
        "stopNo" : float("nan"),
        "stopDuration": float("nan"),
        "currentTire" : startingTire,
        "actualCompound" : actualCompound,
        "tireAge" : tireAge
    }
    raceData = raceData.append(formationLap, ignore_index=True)

size = data.shape[0]

for i in range(size):
    driver = data["driverId"][i]
    if pd.isna(data["stopNo"][i]):
        # Copy Paste the data from Dict
        # Update tireAge by 1
        # Update NaN Values None(Null)
        data["stopNo"][i] = None
        data["stopDuration"][i] = None
        data["currentTire"][i] = driverDict[driver]["currentTire"]
        data["actualCompound"][i] = driverDict[driver]["actualCompound"]
        driverDict[driver]["tireAge"] = int(driverDict[driver]["tireAge"]) + 1
        data["tireAge"][i] = driverDict[driver]["tireAge"]        
    else:
        # Driver Pits:
        # Take user input 
        # Update the Dict
        newTire = input("Enter the new Compund Fitted by "+ driver +" at lap "+ str(data["lapId"][i]) +": ")
        actualCompound = tireDict[newTire]
        tireAge = 0
        driverDict[driver]["currentTire"] = newTire
        driverDict[driver]["actualCompound"] = actualCompound
        driverDict[driver]["tireAge"] = tireAge
        data["currentTire"][i] = driverDict[driver]["currentTire"]
        data["actualCompound"][i] = driverDict[driver]["actualCompound"]
        data["tireAge"][i] = driverDict[driver]["tireAge"]


data = raceData.append(data)

filename = "Test/test.csv"

data.to_csv(filename, encoding = 'utf-8-sig',index = False) 

print("DONE")

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
