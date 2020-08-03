
import os
import os.path
import urllib
import urllib2
import datetime as dt
import mechanize
import requests

class WebScraping:
    def __init__(self, FileDownload, MetadataScrape):
        self.FileDownload=FileDownload
        self.MetadataScrape=MetadataScrape
    
    def DoesFileExist(self, TheFile):
        try:   
            # checks to see if the file exists and returns a true or false
            FileExists=os.path.isfile(TheFile)
            if (FileExists):
                print("Already Exists: "+TheFile)        
                return(FileExists)
        except Exception, err:
            raise RuntimeError ("** Error: DoesFileExist Failed ("+str(err)+")")  
        
    def DoesURLExist (self, TheURL):
        try:
            # Checks link for a 404/200 error and takes note of it
            TestLink=requests.get(TheURL)   
            TheStatusCode=TestLink.status_code
            if (TheStatusCode!=200):
                print("HTTP Error: {}".format(TheStatusCode)+" "+TheURL)
            return(TheStatusCode)
        except Exception, err:
            raise RuntimeError ("** Error: DoesURLExist Failed ("+str(err)+")")   
        
    def YYYYMMDD_FileName (self, FrameID, TheDate):
        try:
            # for the filename we want yyyymmdd, so zeros have to be added in front of monthly or daily dates that are 1 digit
            TheLengthMonth=len(TheDate[0])
            TheLengthDay=len(TheDate[1])
            # print("TheLengthMonth: {}, TheLengthDay: {}".format(TheLengthMonth,TheLengthDay))
            
            if (TheLengthMonth==1 and TheLengthDay==1):
                TheJPGFileName=FrameID+"_"+TheDate[2]+"0"+TheDate[0]+"0"+TheDate[1]
            elif (TheLengthMonth==1 and TheLengthDay==2):
                TheJPGFileName=FrameID+"_"+TheDate[2]+"0"+TheDate[0]+TheDate[1]
            elif (TheLengthMonth==2 and TheLengthDay==1):
                TheJPGFileName=FrameID+"_"+TheDate[2]+TheDate[0]+"0"+TheDate[1]
            else:
                TheJPGFileName=FrameID+"_"+TheDate[2]+TheDate[0]+TheDate[1]
            return(TheJPGFileName)
        except Exception, err:
            raise RuntimeError ("** Error: DoesURLExist Failed ("+str(err)+")")