#This script parses the data and uploads it to mongoDB
#It creates a document for each unique microsite, then it updates that document
#when it finds the correct data using collection.update
#
#This works for dates formatted MM/DD/YY or MM/DD/YYYY. It's also really slow,
#I think its due to the update operation. 

import pymongo
import os
import json
import datetime
import ast


#Loop through all data in the directory and make a json formatted output
def main():
    from pymongo import MongoClient
    client = MongoClient()
    db = client.robo_data
    uploadJson(db.temp)

#Loop through all data in the directory and make a json formatted output
#Return string of json
def uploadJson(collection):
    #The directory where the data for individual biomimics is stored
    ddir = "C:/Users/James/Desktop/RoboMusselProject/newOne"
    #The file text file containing the microsite data
    siteData = open("C:/Users/James/Desktop/RoboMusselProject/InfoMicroSite_2015_text.txt")
    
    noSiteData = []         #List of files with no corresponding site data
    for i in os.listdir(ddir):
        found = False           #has the ith file in ddir been found in siteData?
        id = i[:i.find('_')]    #The id of the ith file
        print "Found id: ", id
      
        siteData.seek(0)
        for line in siteData:
            if (id == line[:line.find('\t')]):
                found = True                    #Found the ith file
                #list the columns of 'line' separated by tabs
                line = line.split('\t')
                site = line[1]
                loc = line[4]
                country = line[6]
                biomimic = line [7]
                zone = line[10]
                sub_zone = line[11]
                wave_exp = line[13]
                region = line[5]
                
                #Insert into DB. store in result to access unique ID
                result = collection.insert_one(
                    {
                        "site": site,
                        "location": loc,
                        "country": country,
                        "biomimic": biomimic,
                        "zone": zone,
                        "sub_zone": sub_zone,
                        "wave_exp": wave_exp,
                        "region": region,
                        "data": []
                    }
                )
            
        #If microsite data was found, a document was uploaded to mongo. If that'script
        #the case, upload the data
        if (found):
            try:                    #toIsodate only works on some formats....
                pullData(ddir + '/' + i, collection, result.inserted_id)
                print("success")
            except:
                print("failure")
                continue
    
    return json

#pull data from the given file
#Returns a string
def pullData(file, collection, mongoID):
    workFile = open(file)
    workList = []
    
    for line in workFile:
        if (line[0] == 'T'):
            continue
        line = line.split('\t')
        temp = float(line[1].rstrip())
        date = toIsodate(line[0])
        collection.update(
            {"_id": mongoID},
            { "$push": {"data": 
                {"Time":  datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S"),
                "Temp": temp}
                }
            }    
        )
    
    final = str(workList)
    return final.replace("\"", "")

#Format the given string as isodate
#Returns a string
def toIsodate(string):
    datelist = string.split('/')
    
    month = int(datelist[0])
    day = int(datelist[1])
    year = int(datelist[2][:datelist[2].find(' ')])
    
    time = datelist[2][datelist[2].find(' '):]
    time = time.split(':')
    hours = int(time[0])
    minutes = int(time[1])
    
    return datetime.datetime(year, month, day, hours, minutes).isoformat()


main()
