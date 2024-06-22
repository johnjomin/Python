import requests
import json

def getAuthors(pageSize):
    '''
    Sends GET HTTP request and returns the result!

    Returns:
        requests.models.Response: The result of GET Response
    '''
    try:
        getRequest = requests.get(f"https://jsonapiplayground.reyesoft.com/v2/authors?page[size]={pageSize}")
    except Exception as e:
        print("Exception in getAuthors method: " + str(e))
    return getRequest


def addRecordsinDictionary(data):
    '''
    Retrieves GET Response as text and returns the data into dictionary

    Args:
        data (str): HTTP Response in text format
    
    Returns:
        dict: The result populated in Dictionary
    '''
    try:
        result = {}
        jsonResult = json.loads(data)
        for eachRecord in jsonResult.get("data"):
            result[eachRecord.get("attributes").get("name")] = len(eachRecord.get("relationships").get('books').get('data'))
    except Exception as e:
        print("Exception in addRecordsinDictionary method: " + str(e))
    return result

def outputResult(data):
    '''
    Output elements from dictionary

    Args:
        data (dict): Parameter in Dictionary format
    '''
    try:
        for record in data:
            print("Authors Name: " + record + "\nTotal Books: " + str(data[record]) + "\n")
    except Exception as e:
        print("Exception in getAuthors method: " + str(e))

if __name__ == "__main__":
    '''
    Function to execute HTTP GET Response and convert result in Dictionary.
    Also to Output the results.
    '''
    getRequest = getAuthors(10)
    resultInDict = addRecordsinDictionary(getRequest.text)
    outputResult(resultInDict)
