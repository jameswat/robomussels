import pymongo
import os
import json
import datetime
import ast


#Loop through all data in the directory and make a json formatted output
def main():
    from pymongo import MongoClient
    client = MongoClient('mongodb://robodb01.blieberman.me/')
    db = client.robo_data
    uploadJson(db.temp)

#Loop through all data in the directory and make a json formatted output
#Return string of json
def uploadJson(collections):
    ddir = "/Users/Tiffanys/Documents/NEU/05-01/Software Dev/TextFiles"
    siteData = open("/Users/Tiffanys/Documents/NEU/05-01/Software Dev/InfoMicrosite_2015.txt")
    jsonTmpl = '{\'site\' : \'%s\', \'region\' : \'%s\', \'location\' : \'%s\', \'country\' : \'%s\', \'biomimic\' : \'%s\', \'zone\' : \'%s\', \'subzone\' : \'%s\', \'waveexp\' : \'%s\', \'data\' : %s}'
    
    noSiteData = []         #List of files with no corresponding site data
    for i in os.listdir(ddir):
        found = False           #has the ith file in ddir been found in siteData?
        id = i[:i.find('_')]    #The id of the ith file
        print "Found id: ", id
        try:                    #toIsodate only works on some formats....
            data = pullData(ddir + '/' + i)
        except:
            data = "[]"
    
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
                json_string = jsonTmpl % (site, region, loc, country, biomimic, zone, sub_zone, wave_exp, data)
                post = ast.literal_eval(json_string)
                collections.insert(post)
    return json

#pull data from the given file
#Returns a string
def pullData(file):
    workFile = open(file)
    workList = []
    
    for line in workFile:
        if (line[0] == 'T'):
            continue
        line = line.split('\t')
        toIsodate(line[0])
        temp = float(line[1].rstrip())
        date = toIsodate(line[0])
        workList.append('{\'Time\' : \'%s\', \'Temperature(C)\' : %.1f}' % (date, temp))
    
    final = str(workList)
    return final.replace("\"", "")

#Format the given string as isodate
#Returns a string
#Note: Tons of goddamn formats.........
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
