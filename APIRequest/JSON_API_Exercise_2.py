import requests
import json

def getAuthors(pageSize, pageNumber):
    '''
    Sends GET HTTP request and goes into loop based on page numbers.
    Then finally returns the result!

    Returns:
        dict: The result of GET Response converted to Dictionary
    '''
    try:
        limit = pageNumber + 1
        result = {}
        for x in range(1, limit):
            getRequest = requests.get(f"https://jsonapiplayground.reyesoft.com/v2/authors?page[size]={pageSize}&page[number]={x}")
            jsonResult = json.loads(getRequest.text)
            if not jsonResult.get("data"):
                print("\nThere are no more authors\n\n")
                print("\nTotal Number of pages: " + str(pageNumber) + "\n")
                break
            elif jsonResult.get("meta").get("page") > 15:
                print("\n15 pages has been processed\n")
                print("\nTotal Number of pages: " + str(pageNumber) + "\n")
                break
            else:
                for eachRecord in jsonResult.get("data"):
                    result[eachRecord.get("attributes").get("name")] = len(eachRecord.get("relationships").get('books').get('data'))

    except Exception as e:
        print("Exception in getAuthors method: " + str(e))
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
    getRequest = getAuthors(10, 16)
    outputResult(getRequest)
