#This script formats robomussel data as json
# TODO
#   -Write to text file
#   -Try to upload to mongo
#   -Expand toIsodate
#
#
#
#
import os
import json
import datetime

#Loop through all data in the directory and make a json formatted output
def main():
    ddir = "C:/Users/James/Desktop/RoboMusselProject/raw"
    siteData = open("C:/Users/James/Desktop/RoboMusselProject/InfoMicroSite_2015_text.txt")
    jsonTmpl = '{"site" : "%s", "location" : "%s",   "country" : "%s", "biomimic" : "%s", "zone" : "%s", "sub-zone" : "%s", "wave-exp" : "%s, "data" : %s}'
    
    noSiteData = []         #List of files with no corresponding site data
    for i in os.listdir(ddir):
        found = False           #has the ith file in ddir been found in siteData?
        id = i[:i.find('_')]    #The id of the ith file
        
        try:                    #toIsodate only works on some formats....
            data = pullData(ddir + '/' + i)
        except:
            data = 'no data'
            
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
            
                json = jsonTmpl % (site, loc, country, biomimic, zone, sub_zone, wave_exp, data)
                print json
        
        #Keep track of files with no site data
        if (found == False):
            noSiteData.append(id)
    print "No site data for: ", noSiteData

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
        workList.append('{"Time" : %s, "Temperature(C)" : %.1f}' % (date, temp))
        
    final = str(workList)
    return final.replace("'", "")
 
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
