# import necessary libraries 
import pandas as pd 
import os 
import glob 


# use glob to get all the csv files 
# in the folder 
path = os.getcwd() 
csv_files = glob.glob(os.path.join(path, "*Data/.csv")) 


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
	data = pd.read_csv(f)
	print("Race: ",a) 
	size = data.shape[0]
	for i in range(size):
		lapId = data["lapId"][i]
		if lapId == 0:
			data=data.drop(i)
	raceDataMerged = raceDataMerged.append(data, ignore_index = True)
	

fileName = "Output/allRaceWithoutFormation.csv"
raceDataMerged.to_csv(fileName, encoding = 'utf-8-sig',index = False) 

