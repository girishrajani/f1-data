# import necessary libraries 
import pandas as pd 
import os 
import glob 


# use glob to get all the csv files 
# in the folder 
path = os.getcwd() 
csv_files = glob.glob(os.path.join(path, "*/Data/.csv")) 


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

raceDataMerged = pd.DataFrame(dataStruct)
a = 0
for f in csv_files:
	a+=1 
	df = pd.read_csv(f)
	print("Race: ",a) 
	raceDataMerged = raceDataMerged.append(df, ignore_index = True)
	

fileName = "Output/allRace.csv"
raceDataMerged.to_csv(fileName, encoding = 'utf-8-sig',index = False) 

