#!/usr/bin/python3
import sys
from zipfile import ZipFile
from xml.etree import ElementTree as ET

def extract_zip(input_zip):
    input_zip=ZipFile(input_zip)
    for name in input_zip.namelist():
        if(name.endswith(".iflw")):
            return input_zip.read(name)

def parseXML(input_string):
    return ET.fromstring(input_string)

if(len(sys.argv) < 2):
    print ("Please specify where your iFlow zip is located as the first parameter.")
    exit()
else:
    # get file descriptor to iflow file
    iflowFd = extract_zip(sys.argv[1]) 
    # parse XML string to object  
    iFlowObj = parseXML(iflowFd)
    propertyList = []
    print("Your properties can be found here in the iFlow:")
    print("-----------------------")
    print("Property | Content Modifier | Process")
    print("-----------------------")
    for node in iFlowObj.iter():
        if(node.tag.endswith("process")):
            for contentmodifier in node.iter():
                if("callActivity" in contentmodifier.tag):
                    for technicalProperty in contentmodifier.iter():
                        if("property" in technicalProperty.tag):
                            for propertyTable in technicalProperty.iter():
                                #print(propertyTable.text)
                                if(propertyTable.text is not None and "row" in propertyTable.text and "cell" in propertyTable.text):
                                    # Integration Process Name print(node.get("name"))
                                    # Content Modifier Name print(contentmodifier.get("name"))
                                    for row in parseXML("<fake>"+propertyTable.text+"</fake>").iter():
                                        if(row.get("id") is not None and "Name" in row.get("id")):
                                            #if(propertyMap.get(row.text) is None):
                                                # property not yet seen, add it to dict
                                                #propertyMap[row.text]
                                            propertyList.append([row.text, contentmodifier.get("name"), node.get("name")])
    propertyList.sort()
    for entry in propertyList:
        print(entry)