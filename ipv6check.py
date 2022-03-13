#!/usr/bin/env python3
import requests
import json
import urllib3
import sys
import pandas as pd


#Create global vars for Prime
primeIP = sys.argv[1]
primeUser = sys.argv[2]
primePass = sys.argv[3]


#Disable SSL warnings
urllib3.disable_warnings()



#Query below is based off of this api https://developer.cisco.com/site/prime-infrastructure/documents/api-reference/rest-api-v3-6/v4/data/BulkSanitizedConfigArchives@_docs/

def checkV6():
    #retrieve prime configs with prime api
    base_uri = 'https://' + primeIP
    user = primeUser
    password = primePass
    rest_path = '/webacs/api/v4/data/BulkSanitizedConfigArchives.json'
    

    url = base_uri + rest_path
    response = requests.get(url, auth=(user, password), verify=False)
    response = json.loads(response.content)
    configs = response['queryResponse']['entityId']
    
    devicesWithNov6 = []
    print('These device names/IPs do not have IPv6 enabled: \n')
    for bulk in configs:
        #prime returns the url to make api calls to retrieve information about specific configs
        url = bulk['@url'] + '.json'
        
        response = requests.get(url, auth=(user, password), verify=False)
        response = json.loads(response.content)
        
        entities = response['queryResponse']['entity']

        for entity in entities:
            #Save devcice name and IP for later, along with the list of configs that are tied to that device
            deviceIP = entity['bulkSanitizedConfigArchivesDTO']['deviceIpAddress']
            deviceName = entity['bulkSanitizedConfigArchivesDTO']['deviceName']
            files = entity['bulkSanitizedConfigArchivesDTO']['files']['file']
            
            #if the file related to this device is the runningconfig, investigate further
            for file in files:
                if file['fileState'] == 'RUNNINGCONFIG':
                    configData = file['data']
                    
                    #CHECK IF V6 config is here!! 
                    if 'ipv6 enable' or 'ipv6 interface' not in configData:
                        devicesWithNov6.append({'deviceName': deviceName, 'deviceIp': deviceIP, 'config': configData})
                        print('Device: ', deviceName, ' IP: ', deviceIP, ' does not have IPv6 in its running config \n')
    
    
    #print('These devices do not have v6 configs: \n', devicesWithNov6, ' list len = ', len(devicesWithNov6))
    jsonList = json.dumps(devicesWithNov6)

    #Dump device name/ip/config into Excel sheet
    df_json = pd.read_json(jsonList)
    df_json.to_excel('deviceInfo.xlsx')
    return devicesWithNov6

checkV6()