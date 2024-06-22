import requests
import json

def getAuthors(author_id):
    '''
    Sends GET HTTP request and returns the result!

    Returns:
        requests.models.Response: The result of GET Response
    '''
    try:
        getRequest = requests.get(f"https://jsonapiplayground.reyesoft.com/v2/authors/{author_id}")
        if getRequest.status_code == 400:
            raise ValueError("\nServer cannot process request due to recieved response. \nHence Bad Request")
    except Exception as e:
        print("\nException in getAuthors method: " + str(e))
    return getRequest


def addRecordsinDictionary(data):
    '''
    Retrieves GET Response as text and returns the data into dictionary,
    As well as stops paging once 15 pages has been processed or no more authors found

    Args:
        data (str): HTTP Response in text format
    
    Returns:
        dict: The result populated in Dictionary

    Raises:
        Exception: If no records found, then populate appropriate error
    '''
    try:
        result = {}
        jsonResult = json.loads(data)
        eachRecord = jsonResult.get("data")
        result[eachRecord.get("attributes").get("name")] = len(eachRecord.get("relationships").get('books').get('data'))
    except Exception as e:
        if jsonResult.get("errors"):
            print("\nNo Records found under Request to be implemented in Dictionary")
        else:
            print("\nException in addRecordsinDictionary method: " + str(e))
    return result


def outputResult(data):
    '''
    Output elements from dictionary

    Args:
        data (dict): Parameter in Dictionary format
    '''
    try:
        print("\nTotal Record in Dictionary: " + str(len(data)) + "\n")
        for record in data:
            print("Authors Name: " + record + "\nTotal Books: " + str(data[record]) + "\n")
    except Exception as e:
        print("\nException in getAuthors method: " + str(e))


if __name__ == "__main__":
    '''
    Function to execute HTTP GET Response and convert result in Dictionary.
    Also to Output the results.
    '''
    getRequest = getAuthors(2)
    resultInDict = addRecordsinDictionary(getRequest.text)
    outputResult(resultInDict)