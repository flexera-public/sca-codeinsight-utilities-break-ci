'''
Copyright 2023 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Wed Jan 11 2023
File : check_scan_results.py
'''

import sys, os, logging, requests

###################################################################################
# Test the version of python to make sure it's at least the version the script
# was tested on, otherwise there could be unexpected results
if sys.version_info <= (3, 7):
    raise "Script created/tested against python version 3.5"
else:
    pass

logfilePath = os.path.dirname(os.path.realpath(__file__)) 
logfileName = "_" + os.path.basename(__file__).split('.')[0] + ".log"
logfile = os.path.join(logfilePath, logfileName)

###################################################################################
#  Set up logging handler to allow for different levels of logging to be capture
logging.basicConfig(format='%(asctime)s,%(msecs)-3d  %(levelname)-8s [%(filename)-30s:%(lineno)-4d]  %(message)s', datefmt='%Y-%m-%d:%H:%M:%S', filename=logfile, filemode='w',level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)  # Disable logging for module

#--------------------------------------------
def main():

    # Simple check for script arguments
    if len(sys.argv) != 4:
        logger.error("Script called with invalid number of arguments")
        print("")
        print("Script called with invalid number of arguments")
        print("   Expected arguments")
        print("     1 - Code Insight URL")
        print("     2 - Code Insight Project Name")
        print("     3 - Code Insight Authorization Token")
        print("")
        sys.exit(0)

    else:
        # Is the first argument an URL?
        if sys.argv[1].startswith("https:") or sys.argv[1].startswith("http:"):
            baseURL = (sys.argv[1])
        else:
            logger.error("First argument expected to be Code Insight URL - http(s)://address:port")
            print("")
            print("First argument expected to be Code Insight URL - http(s)://address:port")
            print("")
            sys.exit(0)
        
        projectName = (sys.argv[2])
        authorizationToken = (sys.argv[3])

        logger.debug("Code Insight URL:  %s" %baseURL)
        logger.debug("Project Name:  %s" %projectName)
        logger.debug("Authorization Token:  XXXXXXX")

        # Get the project ID from the supplied name
        projectID = get_project_id(baseURL, projectName, authorizationToken)

        logger.debug("Project %s  - ProjectID %s" %(projectName, projectID))

        inventorySummary = get_project_inventory_summary(baseURL, projectID, authorizationToken)

        print(len(inventorySummary))
       

#---------------------------------------------------------------------
def get_project_id(baseURL, projectName, authorizationToken):
    logger.info("Entering get_project_id")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api"
    RESTAPI_URL = RESTAPI_BASEURL +  "/project/id?projectName=" + projectName
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authorizationToken} 

    #-------------------------   
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return {"error" : error}
    
    if response.status_code == 200:
        return(response.json()["Content: "])
    else:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        return {"error" : response.text}

#---------------------------------------------------------------------
def get_project_inventory_summary(baseURL, projectID, authorizationToken):
    logger.info("Entering get_project_inventory")

    APIOPTIONS = "&vulnerabilitySummary=false"
    RESTAPI_BASEURL = baseURL + "/codeinsight/api"
    ENDPOINT_URL = RESTAPI_BASEURL + "/projects/" + str(projectID) + "/inventorySummary/?offset=" 
    RESTAPI_URL = ENDPOINT_URL + "1" + APIOPTIONS
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authorizationToken} 

    #-------------------------   
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return {"error" : error}
    
    if response.status_code == 200:
        projectInventorySummary = response.json()["data"]

        # If there are no inventory items just return
        if not projectInventorySummary:
            return projectInventorySummary

        currentPage = response.headers["Current-page"]
        numPages = response.headers["Number-of-pages"]
        nextPage = int(currentPage) + 1

        while int(nextPage) <= int(numPages):
            RESTAPI_URL = ENDPOINT_URL + str(nextPage) + APIOPTIONS
            logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
            response = requests.get(RESTAPI_URL, headers=headers)

            nextPage = int(response.headers["Current-page"]) + 1
            projectInventorySummary += response.json()["data"]

        return projectInventorySummary


    else:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        return {"error" : response.text}


#---------------------------------------
if __name__ == '__main__':
    main()