import os
import os.path
import urllib
import urllib2
import datetime as dt
import mechanize
import requests
import WebScrapingClass

WebScraping=WebScrapingClass.WebScraping(True,True)

InputFolder="Data/"# Sets the Input Folder path.
TheList=os.listdir(InputFolder) #Creates a list of all items within the Input Folder Path.
# get the start time    
StartTime=dt.datetime.now()

TheBrowser=mechanize.Browser()
for TheFile in TheList:
    try:
        TheFileName, TheFileExtension = os.path.splitext(TheFile) # Splits all of the items within the InputFolder 
        # based on the File Name and it's Extension and sets them to the variables TheFileName and TheFileExtension.
        # Since this is in a for loop, it will go through each file and execute the commands within the for loop
        # on each individual file based on specified parameters.
        if (TheFileExtension==".csv"): # the specified parameters are items with the file extension .img. 
            InputTXT=InputFolder+TheFileName+TheFileExtension
            
            #setup JPG output foldername to be the same as the filename
            OutputFolder=InputFolder+TheFileName+"/" # Sets the Output Folder Path.   
            if not os.path.exists(OutputFolder):
                # if the folder doesn't already exist, create it.
                os.makedirs(OutputFolder)  
            # setup metadata file and folder            
            MetaDataOutputFileName=TheFileName+"_Metadata"   
            MetaDataOutputFolder=OutputFolder+"Metadata/"               
            if not os.path.exists(MetaDataOutputFolder):
                # if the folder doesn't already exist, create it.
                os.makedirs(MetaDataOutputFolder)              
                
            OutputPath=MetaDataOutputFolder+MetaDataOutputFileName+"_{}.csv".format(dt.datetime.now().strftime('%Y%m%d%H%M%S'))  
            # "if" the file extension is .img, then the following functions will be executed. 
            print(InputTXT)
            with open(InputTXT,"r") as TheFileR:
                with open(OutputPath,"w") as TheFileW: #opens 2 files simultaneously for both reading and writing at the designated directory and creates two new variables;
                    TheFileW.write("FrameID, FlightlineID, RollNum, SpotNum, TheDate, Latitude, Longitude, HeightASL, Azimuth, NominalScale, UpperRightLat, UpperRightLon, HTTPJPGStatusCode, HTTPMetadataStatusCode\n") # Writes in TheFileW the chosen TheContents based on their numerical index and formats each TheContent by 
                    
                    # "TheFileR," and "TheFileW".
                    TheContent=TheFileR.readlines() # Sets new variable "TheContent" to the .readlines function which reads each line in sequence.
                    for TheLine in TheContent[1:]: #                   
                        TheField=TheLine.split(",")                    
                        
                        # grab the JPG link from the CSV
                        TheJPGLink=TheField[8]
                        
                        # split the date field
                        TheDateTime=TheField[7].split(" ")
                        # split it again to get yyyy mm dd
                        TheDate=TheDateTime[0].split("/")
                        FrameID=TheField[1]
                        TheJPGFileName=WebScraping.YYYYMMDD_FileName(FrameID,TheDate)
                        
                        TheJPGFile=OutputFolder+TheJPGFileName+".JPG"
                    
                        # Checks if file already exists and if the link returns 200
                        print(TheJPGFile)
                        FileExists=WebScraping.DoesFileExist(TheJPGFile)
                        HTTPJPGStatusCode=WebScraping.DoesURLExist(TheJPGLink)
                        
                        if (FileExists or HTTPJPGStatusCode!=200):
                            print("FileExists: {}, HTTPJPGStatusCode: {}".format(FileExists, HTTPJPGStatusCode))
                        else:
                            # save the data from the link as a JPG, doing this last because this is what will call the exception and break/cont the loop.
                            TheBrowser.retrieve(TheJPGLink,TheJPGFile)[0]
                            print("Downloaded: "+TheJPGFileName+".JPG")
                            TheMetadataLink=TheField[9]
                            
                            # Checks link for a 404/200 error and takes note of it                               
                            HTTPMetadataStatusCode=WebScraping.DoesURLExist(TheJPGLink)
                            
                            # Open the URL and get the response object
                            TheResponse=urllib2.urlopen(TheMetadataLink)
                            # Get the XML data from the response
                            TheMetadata=TheResponse.read() 
                            StartIndex=TheMetadata.find("<span id=\"lblFID\">")
                            while (StartIndex!=-1):
                                EndIndex=TheMetadata.find("</span>",StartIndex+10) # this will assign EndIndex to the first value that "<"/lat> appears.  where the StatIndex BEGINS +5 (so the fist number of latitude)
                                FrameID=TheMetadata[StartIndex+18:EndIndex]
                                
                                StartIndex=TheMetadata.find("<span id=\"lblFlight\">",EndIndex+10) # You put "EndIndex+5" because it will refer to where EndIndex was originally defined and go 5 places beyond it to search for <lng>                            
                                EndIndex=TheMetadata.find("</span>",StartIndex+7) # this will assign EndIndex to the first value that "<"/lat> appears.  where the StatIndex BEGINS +5 (so the fist number of latitude)
                                FlightlineID=TheMetadata[StartIndex+21:EndIndex]
                                
                                StartIndex=TheMetadata.find("<span id=\"lblRoll\">",EndIndex+10) # You put "EndIndex+5" because it will refer to where EndIndex was originally defined and go 5 places beyond it to search for <lng>                            
                                EndIndex=TheMetadata.find("</span>",StartIndex+5) # this will assign EndIndex to the first value that "<"/lat> appears.  where the StatIndex BEGINS +5 (so the fist number of latitude)
                                RollNum=TheMetadata[StartIndex+19:EndIndex]
                                
                                StartIndex=TheMetadata.find("<span id=\"lblSpot\">",EndIndex+10) # You put "EndIndex+5" because it will refer to where EndIndex was originally defined and go 5 places beyond it to search for <lng>
                                EndIndex=TheMetadata.find("</span>",StartIndex+18)
                                SpotNum=TheMetadata[StartIndex+19:EndIndex]
                                
                                StartIndex=TheMetadata.find("<span id=\"lblDate\">",EndIndex+10) # You put "EndIndex+5" because it will refer to where EndIndex was originally defined and go 5 places beyond it to search for <lng>
                                EndIndex=TheMetadata.find("</span>",StartIndex+18)
                                TheDate=TheMetadata[StartIndex+19:EndIndex]                            
                                
                                StartIndex=TheMetadata.find("<span id=\"lblLat\">",EndIndex+10) # You put "EndIndex+5" because it will refer to where EndIndex was originally defined and go 5 places beyond it to search for <lng>
                                EndIndex=TheMetadata.find("</span>",StartIndex+18)
                                Latitude=TheMetadata[StartIndex+18:EndIndex]  
                                
                                StartIndex=TheMetadata.find("<span id=\"lblLong\">",EndIndex+10) # You put "EndIndex+5" because it will refer to where EndIndex was originally defined and go 5 places beyond it to search for <lng>
                                EndIndex=TheMetadata.find("</span>",StartIndex+18)
                                Longitude=TheMetadata[StartIndex+19:EndIndex]   
                                
                                StartIndex=TheMetadata.find("<span id=\"lblHeight\">",EndIndex+10) # You put "EndIndex+5" because it will refer to where EndIndex was originally defined and go 5 places beyond it to search for <lng>
                                EndIndex=TheMetadata.find("</span>",StartIndex+18)
                                HeightASL=TheMetadata[StartIndex+21:EndIndex]  
                                   
                                StartIndex=TheMetadata.find("<span id=\"lblAzimuth\">",EndIndex+10) # You put "EndIndex+5" because it will refer to where EndIndex was originally defined and go 5 places beyond it to search for <lng>
                                EndIndex=TheMetadata.find("</span>",StartIndex+18)
                                Azimuth=TheMetadata[StartIndex+22:EndIndex]                               
                                    
                                StartIndex=TheMetadata.find("<span id=\"lblScale\">",EndIndex+10) # You put "EndIndex+5" because it will refer to where EndIndex was originally defined and go 5 places beyond it to search for <lng>
                                EndIndex=TheMetadata.find("</span>",StartIndex+18)
                                NominalScale=TheMetadata[StartIndex+20:EndIndex]                               
                                   
                                StartIndex=TheMetadata.find("<span id=\"lblULat\">",EndIndex+10) # You put "EndIndex+5" because it will refer to where EndIndex was originally defined and go 5 places beyond it to search for <lng>
                                EndIndex=TheMetadata.find("</span>",StartIndex+18)
                                UpperRightLat=TheMetadata[StartIndex+19:EndIndex]                               
                                    
                                StartIndex=TheMetadata.find("<span id=\"lblULong\">",EndIndex+10) # You put "EndIndex+5" because it will refer to where EndIndex was originally defined and go 5 places beyond it to search for <lng>
                                EndIndex=TheMetadata.find("</span>",StartIndex+18)
                                UpperRightLon=TheMetadata[StartIndex+20:EndIndex]  
                                    
    
                                print("FrameID: "+FrameID+", FlightlineID: "+FlightlineID+", RollNum: "+RollNum+", SpotNum: "+SpotNum+", TheDate: "+TheDate)
                                print("Latitude: "+Latitude+", Longitude: "+Longitude+", HeightASL: "+HeightASL+", Azimuth: "+Azimuth+", NominalScale: "+NominalScale)
                                print("UpperRightLat: "+UpperRightLat+", UpperRightLon: "+UpperRightLon+", HTTPJPGStatusCode: {}, HTTPMetadataStatusCode: {}".format(HTTPJPGStatusCode, HTTPMetadataStatusCode))
        
                                    
                                TheFileW.write(FrameID+","+FlightlineID+","+RollNum+","+SpotNum+","+TheDate+","+Latitude+","+Longitude+","+HeightASL+","+Azimuth+","+NominalScale+","+UpperRightLat+","+UpperRightLon+", {}, {}".format(HTTPJPGStatusCode, HTTPMetadataStatusCode)+"\n") # Writes in TheFileW the chosen TheContents based on their numerical index and formats each TheContent by 
                                    
                                #this needs to be here to go further in TheMetadata,  otherwise the while loop will loop endlessly.                         
                                StartIndex=TheMetadata.find("<span id=\"lblFID\">",EndIndex+6) 
                                #print("StartIndex: {}".format(StartIndex))

                            
    except Exception, err:
        print (str(err)+" ("+TheJPGLink+")")

TheFileR.close
TheFileW.close

EndTime=dt.datetime.now()

TimeDiff=EndTime-StartTime
print ("Completed Script, Time Elapsed: {}".format(TimeDiff))
