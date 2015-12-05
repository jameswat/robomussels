#This script is for uploading data from our template

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
    uploadJson('C:/Users/James/Desktop/RoboMusselProject/justOneFile/BMRMUSCAHS124_2010_pgsql.txt', db.temp)

#Loop through all data in the directory and make a json formatted output
#Return string of json
def uploadJson(file, collection):
    workFile = open(file)
    
    for line in workFile:
        line = line.split(' ')
        
        if (line[0] =='biomimic'):
            biomimic = line[2].rstrip()
        elif (line[0] == 'country'):
            country = line[2].rstrip()
        elif (line[0] == 'region'):
            region = line[2].rstrip()
        elif (line[0] == 'site'):
            site = line[2].rstrip()
        elif (line[0] == 'zone'):
            zone = line[2].rstrip()
        elif (line[0] == 'subzone'):
            sub_zone = line[2].rstrip()
        elif (line[0] == 'wave_exp'):
            wave_exp = line[2].rstrip()
        else:
            break
    result = collection.insert_one(
               {
                    "site": site,
                    "country": country,
                    "biomimic": biomimic,
                    "zone": zone,
                    "sub_zone": sub_zone,
                    "wave_exp": wave_exp,
                    "region": region,
                    "data": []
                }
            )
    
    for line in workFile:
        pullData(line, collection, result.inserted_id)
    
    
   

#pull data from the given file
#Returns a string
def pullData(line, collection, mongoID):
    
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
